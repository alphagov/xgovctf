__author__ = 'Collin Petty'

from api.common import cache
from api import common
from datetime import datetime

end = datetime(2020, 5, 7, 3, 59, 59)


def get_team_score(uid):
    """Get the score for a team.

    Looks for a cached team score, if not found we query all correct submissions by the team and add up their
    basescores if they exist. Cache the result.
    """
    db = common.get_conn()
    score = cache.get('teamscore_' + uid)
    if score is not None:
        return score
    s = {d['pid'] for d in list(db.submissions.find({"uid": uid, "correct": True}))}  # ,#"timestamp": {"$lt": end}}))}
    score = sum([d['basescore'] if 'basescore' in d else 0 for d in list(db.problems.find({
        'pid': {"$in": list(s)}}))])
    cache.set('teamscore_' + uid, score, 60 * 60)
    return score
