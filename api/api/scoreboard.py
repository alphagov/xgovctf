""" Module for getting scoreboard information """

import api

from api.common import cache, APIException
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

def get_all_team_scores():
    """
    Gets the score for every team in the database.

    Returns:
        A dictionary of tid:score mappings
    """

    tids = [team['tid'] for team in api.team.get_all_teams()]
    
    result = {}
    for tid in tids:
        result[tid] = get_score(tid=tid)

    return result

def get_all_user_scores():
    """
    Gets the score for every user in the database.

    Returns:
        A dictionary of uid:score mappings
    """

    uids = [user['uid'] for user in api.user.get_all_users()]
    
    result = {}
    for uid in uids:
        result[uid] = get_score(uid=uid)

    return result
