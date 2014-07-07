__author__ = 'Collin Petty'
import imp

from api.common import APIException
import api.common
import api.user
import api.team
from datetime import datetime

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

def submit_problem(pid, tid, key):
    """
    Checks the given key with the grader for the problem. Adds the submission to the database.

    Args:
        pid: The problem id
        tid: The team id
        key: The key to check against the grader
    """
    pass
