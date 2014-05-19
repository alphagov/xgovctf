__author__ = 'collinpetty'

from api.annotations import *
from api import app, common, user


def get_team(tid=None, teamname=None):
    db = common.get_conn()
    if tid is not None:
        return db.teams.find_one({'tid': tid})
    elif teamname is not None:
        return db.teams.find_one({'teamname': teamname})
    return None


@app.route('/api/team/create', methods=['POST'])
@return_json
def create_team():
    pass