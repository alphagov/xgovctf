""" Module for getting scoreboard information """

from api.common import cache, APIException
import api.common
import api.group
import api.problem
import api.team
import api.user
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

def get_group_scores(gid=None, name=None):
    """
    Get the group scores.

    Args:
        gid: The group id
        name: The group name
    Returns:
        A dictionary of tid:score mappings
    """

    members = api.group.get_group(gid, name)['members']

    result = {}
    for tid in members:
        result[tid] = get_score(tid=tid)

    return result

def get_group_score(gid=None, name=None):
    """
    Get the group score.

    Args:
        gid: The group id
        name: The group name
    Returns:
        The total score of the group
    """

    return sum(get_group_scores(gid, name).values())
