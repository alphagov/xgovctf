"""
API functions relating to team management.
"""

import api.common
import api.user

from api.common import APIException

max_team_users = 4

def get_team(tid=None, name=None):
    """
    Retrieve a team based on a property (tid, name, etc.).

    Args:
        tid: team id
        name: team name
    Returns:
        Returns the corresponding team object or None if it could not be found
    """
    db = api.api.common.get_conn()
    if tid is not None:
        return db.teams.find_one({'tid': tid})
    elif name is not None:
        return db.teams.find_one({'team_name': name})
    return None

def create_team(params):
    """
    Directly inserts team into the database. Assumes all fields have been validated.

    Args:
        team_name: Name of the team
        adviser_name: Full name of the team's adviser
        adviser_email: Adviser's email address
        school: Name of the school
        password: Team's password
    Returns:
        The newly created team id.
    """
    db = api.common.get_conn()
    params['tid'] = api.common.token()
    if api.team.get_team(name=params['team_name']) is not None:
        raise APIException(0, None, "Team {} already exists!".format(params['team_name']))

    # JB: Currently, group passwords are plaintext. We should think
    # whether we should hash them or if we need to display them
    db.teams.insert(params)

    return params['tid']


def get_team_uids(tid):
    """
    Retrieves the uids for all members on a team.

    Args:
        tid: the team id to query
    Returns:
        A list of the uids of the team's members.
    """
    db = api.common.get_conn()
    return [user["uid"] for user in db.users.find({'tid': tid})]

def get_team_information(tid):
    """
    Retrieves the information of a team.

    Args:
        tid: the team id
    Returns:
        A dict of team information.
        team_name:
        password:
        adviser_name:
        adviser_email:
        school:
        members: A list of the member uids
    """

    db = api.common.get_conn()
    team_info = db.teams.find_one({'tid': tid}, {"_id": 0})
    team_info["members"] = get_team_uids(tid)

    return team_info

def get_all_teams():
    """
    Retrieves all teams.

    Returns:
        A list of all of the teams.
    """
    db = api.common.get_conn()
    return list(db.teams.find({}, {"_id": 0}))
