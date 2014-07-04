"""
API functions relating to team management.
"""

from api import app, common, user

def get_team(tid=None, name=None):
    """
    Retrieve a team based on a property (tid, name, etc.).

    Args:
        tid: team id
        name: team name
    Returns:
        Returns the corresponding team object or None if it could not be found
    """

    db = common.get_conn()
    if tid is not None:
        return db.teams.find_one({'tid': tid})
    elif name is not None:
        return db.teams.find_one({'team_name': name})
    return None

#TODO: Considering everything is a key value pair, we could consider passing these all
#      in their own dictionary. There quite a few lines of code just turning dicts into
#      singletons to become dicts again.
def create_team(team_name, adviser_name, adviser_email, school, password):
    """
    Directly inserts team into the database. Assumes all fields have been validated.
    """
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


def get_teammate_uids(tid):
    db = common.get_conn()
    return [t['uid'] for t in db.users.find({'tid': tid})]


def get_team_information(tid, uid):
    db = common.get_conn()
    team_cur = db.teams.find_one({'tid': tid})

    teammates = []
    for u in get_teammate_uids(tid):
        teammate = db.users.find_one({'uid': u})
        teammates.append({'teammate': teammate['username'], 'is_you': teammate['uid'] == uid})

    team_data = {'team_name': team_cur['team_name'], 'password': team_cur['password'],
                 'adviser_name': team_cur['adviser_name'], 'adviser_email': team_cur['adviser_email'],
                 'school': team_cur['school'],
                 'teammates': teammates}
    return team_data
