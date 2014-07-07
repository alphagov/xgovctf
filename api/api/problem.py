""" Module for interacting with the problems """
import imp

import api.common
import api.user
import api.team
from datetime import datetime
from api.common import validate, APIException, check
from voluptuous import Schema, Length, Required

submission_schema = Schema({
    Required("tid"): check(
        (0, "This does not look like a valid tid.", [str, Length(max=100)])),
    Required("pid"): check(
        (0, "This does not look like a valid pid.", [str, Length(max=100)])),
    Required("key"): check(
        (0, "This does not look like a valid key.", [str, Length(max=100)]))
})

def grade_problem(uid, pid, key):
    """
    Grades the problem with its associated grader script.

    Args:
        uid: user's uid
        pid: problem's pid
        key: user's submission
    Returns:
        A dict.
        correct: boolean
        points: number of points the problem is worth.
        message: message returned from the grader.
    """

    problem = api.problem.get_problem(pid)

    try:
        (correct, message) = imp.load_source(
            problem["grader"][:-3], "./graders/" + problem["grader"]
        ).grade(uid, key)
    except FileNotFoundError:
       raise APIException(0, None, "Problem {} grader is offline.".format(problem["pid"]))

    return {
        "correct": correct,
        "points": problem["basescore"],
        "message": message
    }

def submit_problem(tid, pid, key, uid=None, ip=None):
    """
    User problem submission. Problem submission is inserted into the database.

    Args:
        tid: user's team id
        pid: problem's pid
        key: answer text
        uid: user's uid
    Returns:
        A dict.
        correct: boolean
        points: number of points the problem is worth.
        message: message returned from the grader.
    """

    db = api.common.get_conn()
    validate(submission_schema, {"tid": tid, "pid": pid, "key": key})

    if pid not in get_unlocked_pids(tid):
        raise APIException(0, None, "You can submit flags to problems you haven't unlocked.")

    if pid in get_solved_pids(tid):
        raise APIException(0, None, "You have already solved this problem.")

    user = api.user.get_user(uid=uid)
    if user is None:
        raise APIException(0, None, "User submitting flag does not exist.")
    uid = user["uid"]

    result = grade_problem(uid, pid, key)

    submission = {
        'uid': uid,
        'tid': tid,
        'timestamp': datetime.now(),
        'pid': pid,
        'ip': ip,
        'key': key,
        'correct': result["correct"]
    }

    try:
        db.submissions.insert(submission)
    except DuplicateKeyError:
        raise APIException(0, None, "You or one of your teammates has already tried this solution.")

    return result


def get_submissions(uid):
    """
    Gets the submissions from a given user.

    Args:
        uid: the user id

    Returns:
        A list of submissions from the given user
    """

    db = api.common.get_conn()
    return db.submissions.find({'uid': uid})

def get_team_submissions(tid):
    """
    Gets the submissions from the entire team

    Args:
        tid: the team id

    Returns:
        A list of submissions from the entire team
    """

    db = api.common.get_conn()
    return db.submissions.find({'tid': tid})

def get_problem(pid):
    """
    Gets a single problem.

    Args:
        pid: The problem id

    Returns:
        The problem dictionary from the database
    """

    db = api.common.get_conn()
    return db.problems.find_one({'pid': pid})


def get_all_problems(category=None):
    """
    Gets all of the problems in the database.

    Args:
        category: Optional parameter to restrict which problems are returned
    """

    db = api.common.get_conn()

    if category:
        return db.problems.find({'category': category})
    return db.problems.find()

def get_solved_pids(tid, category=None):
    """
    Gets the solved pids for a given team.

    Args:
        tid: The team id
        category: Optional parameter to restrict which problems are returned

    Returns:
        List of solved problem ids
    """

    correct_pids = [sub['pid'] for sub in get_team_submission(tid) if sub['correct'] == True]

    solved = []
    for pid in correct_pids:
        solved += pid

    return solved

def get_solved_problems(tid, category=None):
    """
    Gets the solved problems for a given team.

    Args:
        tid: The team id
        category: Optional parameter to restrict which problems are returned

    Returns:
        List of solved problem dictionaries
    """

    return [get_problem(pid) for pid in get_solved_pids(tid, category)]

def get_unlocked_pids(tid, category=None):
    """
    Gets the unlocked pids for a given team.

    Args:
        tid: The team id
        category: Optional parameter to restrict which problems are returned

    Returns:
        List of unlocked problem ids
    """

    solved = get_solved_problems(tid, category)

    unlocked = []
    for problem in get_all_problems():
        if 'weightmap' not in problem or 'threshold' not in problem:
            unlocked.append(problem['pid'])
        else:
            weightsum = sum(problem['weightmap'].get(pid, 0) for pid in get_solved_pids())
            if weightsum >= problem['threshold']:
                unlocked.append(problem['pid'])

    return unlocked

def get_unlocked_problems(tid, category=None):
    """
    Gets the unlocked problems for a given team.

    Args:
        tid: The team id
        category: Optional parameter to restrict which problems are returned

    Returns:
        List of unlocked problems dictionaries
    """

    return [get_problem(pid) for pid in get_unlocked_pids(tid, category)]
