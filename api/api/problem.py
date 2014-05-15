__author__ = 'Collin Petty'
import imp

from api.common import cache
from api.annotations import *
from api import app, team
from pymongo.errors import DuplicateKeyError
from datetime import datetime

root_web_path = ""
relative_auto_prob_path = ""

auto_generators = dict()


def acquire_problem_instance(pid, uid):
    return None


def _get_solved_pids(uid=None):
    if uid is None:
        uid = session['uid']
    db = common.get_conn()
    return {p['pid'] for p in db.submissions.find({'uid': uid, 'correct': True})}


@app.route('/api/problems', methods=['GET'])
@require_login
@return_json
def load_viewable_problems():
    """Gets the list of all viewable problems for a team.

    First check for 'unlocked_<tid>' in the cache, if it exists return it otherwise rebuild the unlocked list.
    Query all problems from the database as well as all submissions from the current team.
    Cycle over all problems while looking at their weightmap, check to see if problems in the weightmap are solved.
    Increment the threshold counter for solved weightmap problems.
    If the threshold counter is higher than the problem threshold then add the problem to the return list (ret).
    """
    uid = session['uid']
    db = common.get_conn()
    #unlocked = cache.get('unlocked_' + uid)  # Get the teams list of unlocked problems from the cache
    #if unlocked is not None:  # Return this if it is not empty in the cache
    #    return json.loads(unlocked)
    user = db.users.find_one({'uid': uid})
    if 'probinstance' not in user:
        db.teams.update({'uid': uid}, {'$set': {'probinstance': {}}})
        user['probinstance'] = dict()
    solved_pids = _get_solved_pids()
    if 'tid' in user:
        for teammate in db.users.find({'tid': user['tid']}):
            solved_pids |= _get_solved_pids(teammate['uid'])
    unlocked = [{'pid':         p['pid'],
                 'displayname': p.get('displayname'),
                 'hint':        p.get('hint'),
                 'basescore':   p.get('basescore'),
                 'correct':     True if p['pid'] in solved_pids else False,
                 'desc':        p.get('desc') if not p.get('autogen', False) else
                 user['probinstance'][p['pid']].get('desc', None) if p['pid'] in user['probinstance'] else
                 acquire_problem_instance(p['pid'], uid).get('desc')}
                for p in db.problems.find() if 'weightmap' not in p or
                                               'threshold' not in p or
                                               sum(p['weightmap'].get(pid, 0) for pid in solved_pids) >= p.get('threshold', 0)]

    unlocked.sort(key=lambda k: k['basescore'] if 'basescore' in k else 99999)
    #cache.set('unlocked_' + uid, json.dumps(unlocked), 60 * 60)
    return 1, unlocked


def get_solved_problems():
    """Returns a list of all problems the team has solved.

    Checks for 'solved_<tid>' in the cache, if the list does not exists it rebuilds/inserts it.
    Queries the database for all submissions by the logged in team where correct == True.
    Finds all problems with a PID in the list of correct submissions.
    All solved problems are returned as a pid and display name.
    """
    uid = session['uid']
    db = common.get_conn()
    #solved = cache.get('solved_' + uid)
    #if solved is not None:
    #    return json.loads(solved)
    solved_pids = _get_solved_pids()
    probs = list(db.problems.find({"pid": {"$in": list(solved_pids)}}, {'pid': 1, 'displayname': 1, 'basescore': 1}))
    solved = sorted([{'pid': p['pid'],
                      'displayname': p.get('displayname', None),
                      'basescore': p.get('basescore', None)} for p in probs],
                    key=lambda k: k['basescore'] if 'basescore' in k else 99999,
                    reverse=True)
    cache.set('solved_' + uid, json.dumps(solved), 60 * 60)
    return solved


def get_single_problem(pid, uid):
    """Retrieve a single problem.

    Grab all problems from load_unlocked_problems (most likely cached). Iterate over the problems looking for the
    desired pid. Return the problem if found. If not found return status:0 with an error message.
    """
    for prob in load_unlocked_problems(uid):
        if prob['pid'] == pid:
            return prob
    return {'status': 0, 'message': 'Internal error, problem not found.'}


@app.route('/api/submit', methods=['POST'])
@return_json
@require_login
def submit_problem():
    """Handle problem submission.

    Gets the key and pid from the submitted problem, calls the respective grading function if the values aren't empty.
    If correct all relevant cache values are cleared. The submission is the inserted into the database
    (an attempt is made). A relevant message is returned if the problem has already been solved or the answer
    has been tried.
    """
    uid = session['uid']
    db = common.get_conn()
    pid = request.form.get('pid', '').strip()
    key = request.form.get('key', '').strip()
    correct = False
    if pid == '':
        return {"status": 0, "points": 0, "message": "Problem ID cannot be empty."}
    if key == '':
        return {"status": 0, "points": 0, "message": "Answer cannot be empty."}
    if pid not in [p['pid'] for p in load_unlocked_problems(uid)]:
        return {"status": 0, "points": 0, "message": "You cannot submit problems you have not unlocked."}
    prob = db.problems.find_one({"pid": pid})
    if prob is None:
        return {"status": 0, "points": 0, "message": "Problem ID not found in the database."}

    if not prob.get('autogen', False):  # This is a standard problem, not auto-generated
        (correct, message) = imp.load_source(prob['grader'][:-3], "./graders/" + prob['grader']).grade(uid, key)
    else:  # This is an auto-generated problem, grading is different.
        team = db.teams.find_one({'uid': uid})
        grader_type = prob.get('grader', 'script')
        if grader_type == 'script':
            (correct, message) = imp.load_source(team['probinstance'][pid]['grader'][:-3],
                                                 team['probinstance'][pid]['grader']).grade(uid, key)
        elif grader_type == 'key':
            correct = team['probinstance'][pid]['key'] == key
            message = prob.get('correct_msg', 'Correct!') if correct else prob.get('wrong_msg', 'Nope!')
    submission = {'uid': uid,
                  'timestamp': datetime.now(),
                  'pid': pid,
                  'ip': request.headers.get('X-Real-IP', None),
                  'key': key,
                  'correct': correct}
    if correct:
        cache.delete('unlocked_' + uid)  # Clear the unlocked problem cache as it needs updating
        cache.delete('solved_' + uid)  # Clear the list of solved problems
        cache.delete('teamscore_' + uid)  # Clear the team's cached score
        cache.delete('lastsubdate_' + uid)
        try:
            db.submissions.insert(submission)
        except DuplicateKeyError:
            return {"status": 0, "points": 0, "message": "You have already solved this problem!"}
    else:
        try:
            db.submissions.insert(submission)
        except DuplicateKeyError:
            return {"status": 0, "points": 0, "message": "You already tried that!"}
    return {"status": 1 if correct else 0, "points": prob.get('basescore', 0), "message": message}


def get_all_problems():
    db = common.get_conn()
    return [{'pid': p['pid'],
             'displayname': p['displayname'],
             'basescore': p['basescore'],
             'hardlock': p.get('hardlock', False),
             'ignorethresh': p.get('ignorethresh', False)} for p in db.problems.find({})]


def _full_auto_prob_path():
    return root_web_path + relative_auto_prob_path


@app.route('/api/problems/solved', methods=['GET'])
@require_login
@return_json
@log_request
def get_solved_problems_hook():
    return get_solved_problems(session['uid'])


@app.route('/api/problems/<path:pid>', methods=['GET'])
@require_login
@return_json
@log_request
def get_single_problem_hook(pid):
    problem_info = get_single_problem(pid, session['uid'])
    if 'status' not in problem_info:
        problem_info.update({"status": 1})
    return problem_info
