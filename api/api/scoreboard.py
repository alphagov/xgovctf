""" Module for getting scoreboard information """

from api.common import cache, APIException
import api.common
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

    db = api.common.get_conn()

    if tid is not None:
        cache_name = "teamscore_" + tid
    elif uid is not None:
        cache_name = "userscore_" + uid
    else:
        raise APIException(0, None, "Must supply uid or tid")

    score = cache.get(cache_name)
    if score is not None:
        return score

    pids = [s['pid'] for s in api.problem.get_correct_submissions(tid=tid, uid=uid)]
    score = sum([api.problem.get_problem(pid)['score'] for pid in pids])

    cache.set(cache_name, score, 60 * 60)
    return score

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
