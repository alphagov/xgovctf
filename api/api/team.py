__author__ = 'collinpetty'

from api.annotations import *
from api import app, common, user


def get_team(tid=None, team_name=None):
    db = common.get_conn()
    if tid is not None:
        return db.teams.find_one({'tid': tid})
    elif team_name is not None:
        return db.teams.find_one({'teamname': team_name})
    return None


def create_team(team_name, adviser_name, adviser_email):
    db = common.get_conn()
    tid = common.token()
    try:
        db.teams.insert({'tid': tid,
                         'team_name': team_name,
                         'adviser_name': adviser_name,
                         'adviser_email': adviser_email})
    except Exception as e:
        print("Error creating the team account.")
        return None
    return tid

@app.route('/api/team/create', methods=['POST'])
@return_json
def create_team_hook():
    team_name = request.form.get('teamname')
    adviser_name = request.form.get('adviser_name')
    adviser_email = request.form.get('adviser_email')

    if None in {team_name, adviser_email, adviser_name}:
        return 0, None, "Please fill out all of the required fields."
    team_acct = get_team(team_name=team_name)
    if team_acct is None:
        tid = create_team(team_name, adviser_name, adviser_email)
        if tid is None:
            return 0, None, "There was an error creating the team"
        return 1, None, "Successfully created the team '%s'!" % team_name
    return 2, None, "The specified team exists."