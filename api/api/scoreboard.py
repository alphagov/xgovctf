__author__ = 'Collin Petty'

from api.common import cache
import api.common
import api.problem
from datetime import datetime

end = datetime(2020, 5, 7, 3, 59, 59)

def get_team_score(tid):
    """
    Get the score for a team.  Looks for a cached team score, if not found we query all correct submissions by the team and add up their basescores if they exist. Cache the result.

    Args:
        tid: The team id
    Returns:
        The team's score
    """

    db = common.get_conn()

    score = cache.get('teamscore_' + tid)
    if score is not None:
        return score

    pids = [d['pid'] for d in api.problem.get_correct_submissions(tid=tid)]  # ,#"timestamp": {"$lt": end}}))}
    score = sum([api.problem.get_problem(pid)['basescore'] for pid in pids])

    cache.set('teamscore_' + tid, score, 60 * 60)
    return score
