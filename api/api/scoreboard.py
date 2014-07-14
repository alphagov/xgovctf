""" Module for getting scoreboard information """

from api.common import cache, APIException
import api.common
import api.problem
from datetime import datetime

end = datetime(2020, 5, 7, 3, 59, 59)

def get_score(tid=None, uid=None):
    """
    Get the score for a user or team.
    Looks for a cached score, if not found we query all correct submissions by the team and add up their scores if they exist. Cache the result.

    Args:
        tid: The team id
        uid: The user id
    Returns:
        The users's or team's score
    """

    pids = [s['pid'] for s in api.problem.get_correct_submissions(tid=tid, uid=uid)]
    score = sum([api.problem.get_problem(pid)['score'] for pid in pids])

    return score
