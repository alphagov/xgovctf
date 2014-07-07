__author__ = 'Collin Petty'
import imp

from api.common import APIException
import api.common
import api.user
import api.team
from datetime import datetime

def get_problem(pid):
    """
    Gets a single problem.

    Args:
        pid: The problem id

    Returns:
        The problem dictionary from the database
    """
    pass


def get_all_problems(category=None):
    """
    Gets all of the problems in the database.

    Args:
        category: Optional parameter to restrict which problems are returned
    """
    pass

def get_solved_problems(tid, category=None):
    """
    Gets the solved problems for a given team.

    Args:
        tid: The team id
        category: Optional parameter to restrict which problems are returned
    """
    pass

def get_unlocked_problems(tid, category=None):
    """
    Gets the unlocked problems for a given team.

    Args:
        tid: The team id
        category: Optional parameter to restrict which problems are returned
    """
    pass

def submit_problem(pid, tid, key):
    """
    Checks the given key with the grader for the problem. Adds the submission to the database.

    Args:
        pid: The problem id
        tid: The team id
        key: The key to check against the grader
    """
    pass
