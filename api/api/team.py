__author__ = 'collinpetty'

from api.annotations import *
from api import app, common


def get_team(tid=None, team_name=None):
    db = common.get_conn()
    if tid is not None:
        return db.teams.find_one({'tid': tid})
    elif team_name is not None:
        return db.teams.find_one({'team_name': team_name})
    return None

def create_team(team_name, adviser_name, adviser_email, school, password):
    db = common.get_conn()
    tid = common.token()
    try:
        db.teams.insert({'tid': tid,
                         'team_name': team_name,
                         'adviser_name': adviser_name,
                         'adviser_email': adviser_email,
                         'school': school,
                         'password': password})  # JB: Currently, group passwords are plaintext. We should think
                                                 # whether we should hash them or if we need to display them
    except Exception as e:
        print("Error creating the team account.")
        return None
    return tid