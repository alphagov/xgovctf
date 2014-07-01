__author__ = 'Collin Petty'
import imp

from api.common import cache, validate, ValidationException
from api import team, user, common
from pymongo.errors import DuplicateKeyError
from datetime import datetime

root_web_path = ""
relative_auto_prob_path = ""

auto_generators = dict()


def acquire_problem_instance(pid, uid):
    return None


def get_solved_pids_for_cat(uid=None, tid=None, gid=None):
    """Gets all solved PIDs for the given category
    """
    db = common.get_conn()
    if gid is not None:
        pids = set()
        for t in db.teams.find({'gid': gid}):
            pids |= get_solved_pids_for_cat(tid=t['tid'])
        return pids
    if tid is not None:
        pids = set()
        for u in db.users.find({'tid': tid}):
            pids |= get_solved_pids_for_cat(uid=u['uid'])
        return pids
    if uid is not None:
        return {p['pid'] for p in db.submissions.find({'uid': uid, 'correct': True})}
    return None


def get_viewable_pids_for_cat(uid=None, tid=None, gid=None):
    solved_pids = get_solved_pids_for_cat(**locals())
    db = common.get_conn()
    return {p['pid'] for p in db.problems.find() if 'weightmap' not in p or
                                                    'threshold' not in p or
                                                    sum(p['weightmap'].get(pid, 0) for pid in solved_pids) >= p['threshold']}


def get_viewable_pids_for_solved(pids):
    if pids is None:
        return None
    db = common.get_conn()
    return {p['pid'] for p in db.problems.find() if 'weightmap' not in p or
                                                    'threshold' not in p or
                                                    sum(p['weightmap'].get(pid, 0) for pid in pids) >= p['threshold']}


def load_viewable_problems(tid):
    """Gets the list of all viewable problems for a team.

    First check for 'unlocked_<tid>' in the cache, if it exists return it otherwise rebuild the unlocked list.
    Query all problems from the database as well as all submissions from the current team.
    Cycle over all problems while looking at their weightmap, check to see if problems in the weightmap are solved.
    Increment the threshold counter for solved weightmap problems.
    If the threshold counter is higher than the problem threshold then add the problem to the return list (ret).
    """
    solved_pids = get_solved_pids_for_cat(tid=tid)
    viewable_pids = get_viewable_pids_for_solved(solved_pids)
    db = common.get_conn()
    probs = []
    for p in db.problems.find({'pid': {"$in": list(viewable_pids)}}):
        probs.append({'pid':         p['pid'],
                      'displayname': p.get('displayname'),
                      'hint':        p.get('hint'),
                      'basescore':   p.get('basescore'),
                      'category':    p.get('category'),
                      'correct':     True if p['pid'] in solved_pids else False,
                      'desc':        p.get('desc')})

    return probs


def get_solved_problems():
    """Returns a list of all problems the team has solved.

    Checks for 'solved_<tid>' in the cache, if the list does not exists it rebuilds/inserts it.
    Queries the database for all submissions by the logged in team where correct == True.
    Finds all problems with a PID in the list of correct submissions.
    All solved problems are returned as a pid and display name.
    """
    useracct = user.get_user()
    if 'tid' in useracct:
        solved_pids = get_solved_pids_for_cat(tid=useracct['tid'])
    else:
        solved_pids = get_solved_pids_for_cat(uid=useracct['uid'])

    db = common.get_conn()
    probs = [{'pid':         p['pid'],
              'displayname': p.get('displayname'),
              'basescore':   p.get('basescore'),
              'category': p.get('category')} for p in db.problems.find({'pid': {"$in": list(solved_pids)}})]
    probs.sort(key=lambda k: k.get('basescore', 99999), reverse=True)

    return probs


def get_single_problem(pid, tid):
    """Retrieve a single problem.

    Grab all problems from load_unlocked_problems (most likely cached). Iterate over the problems looking for the
    desired pid. Return the problem if found. If not found return status:0 with an error message.
    """
    for prob in load_viewable_problems(tid):
        if prob['pid'] == pid:
            return prob
    return {'status': 0, 'message': 'Internal error, problem not found.'}


#TODO: Decide where to strip pid, key
def submit_problem(tid, pid, key):
    """Handle problem submission.

    Gets the key and pid from the submitted problem, calls the respective grading function if the values aren't empty.
    If correct all relevant cache values are cleared. The submission is the inserted into the database
    (an attempt is made). A relevant message is returned if the problem has already been solved or the answer
    has been tried.
    """
    db = common.get_conn()
    try:
        pid = validate(pid.strip(), "Problem ID", min_length=1)
        key = validate(key.strip(), "Answer", min_length=1)
    except ValidationException as validation_failure:
        return 0, None, validation_failure.value

    correct = False
    if pid not in [p['pid'] for p in load_viewable_problems(tid)]:
        print("unavailable")
        print(pid)
        print(load_viewable_problems(uid))
        return 0, {'points': 0}, "You cannot submit problems you have not unlocked."

    prob = db.problems.find_one({"pid": pid})
    if prob is None:
        print("broken")
        return 0, {'points': 0}, "Problem ID not found in the database."

    if key == "pico":  # JB: Backdoor! Need to remove!!!
        correct = True
        message = "Cheater! :)"
    elif not prob.get('autogen', False):  # This is a standard problem, not auto-generated
        try:
            (correct, message) = imp.load_source(prob['grader'][:-3], "./graders/" + prob['grader']).grade(uid, key)
        except FileNotFoundError:
            return 0, {'points': 0}, "Grader script not found"
    else:
        return 0, {'points': 0}, "Autogenerated problems are currently broken"
    # else:  # This is an auto-generated problem, grading is different.
    #     team = db.teams.find_one({'uid': uid})
    #     grader_type = prob.get('grader', 'script')
    #     if grader_type == 'script':
    #         (correct, message) = imp.load_source(team['probinstance'][pid]['grader'][:-3],
    #                                              team['probinstance'][pid]['grader']).grade(uid, key)
    #     elif grader_type == 'key':
    #         correct = team['probinstance'][pid]['key'] == key
    #         message = prob.get('correct_msg', 'Correct!') if correct else prob.get('wrong_msg', 'Nope!')


    submission = {'uid': uid,
                  'tid': tid,
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
            return 0, {"points": 0}, "You or one of your teammates has already solved this challenge."
    else:
        try:
            db.submissions.insert(submission)
        except DuplicateKeyError:
            return 0, {"points": 0}, "You or one of your teammates has already tried this solution."

    return (1 if correct else 0), {"points": prob.get('basescore', 0)}, message


# JB: This needs updating
def get_all_problems():
    db = common.get_conn()
    return [{'pid': p['pid'],
             'displayname': p['displayname'],
             'basescore': p['basescore'],
             'hardlock': p.get('hardlock', False),
             'ignorethresh': p.get('ignorethresh', False),
             'autogen': p.get('autogen', False)} for p in db.problems.find({})]


def _full_auto_prob_path():
    return root_web_path + relative_auto_prob_path
