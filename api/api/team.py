"""
API functions relating to team management.
"""

import api.common
import api.user
import api.auth
import api.scoreboard

from api.common import APIException, safe_fail

max_team_users = 5

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

    match = {}
    if tid is not None:
        match.update({'tid': tid})
    elif name is not None:
        match.update({'team_name': name})
    elif api.auth.is_logged_in():
        match.update({"tid": api.user.get_user()["tid"]})
    else:
        raise APIException(0, None, "Must supply tid or team name!")

    team = db.teams.find_one(match, {"_id": 0})

    if team is None:
        raise APIException(0, None, "Team does not exist!")

    return team

def get_groups(tid=None):
    """
    Get the group membership for a team.

    Args:
        tid: The team id
    Returns:
        List of group objects the team is a member of.
    """

    tid = get_team(tid=tid)["tid"]

    db = api.common.get_conn()

    groups = []
    for group in list(db.groups.find({'members': tid}, {'name': 1, 'gid': 1, 'owners': 1})):
        groups.append({'name': group['name'],
                       'gid': group['gid'],
                       'owner': tid in group['owners'],
                       'score': api.scoreboard.get_group_score(gid=group['gid'])})
    return groups

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
    if safe_fail(get_team, name=params['team_name']) is not None:
        raise APIException(0, None, "Team {} already exists!".format(params['team_name']))

    # JB: Currently, group passwords are plaintext. We should think
    # whether we should hash them or if we need to display them
    db.teams.insert(params)

    return params['tid']

def get_team_uids(tid=None, name=None):
    """
    Retrieves the uids for all members on a team.

    Args:
        tid: the team id to query
        name: the team name to query
    Returns:
        A list of the uids of the team's members.
    """

    db = api.common.get_conn()

    tid = get_team(name=name, tid=tid)["tid"]

    return [user["uid"] for user in db.users.find({"tid": tid})]

def get_team_information(tid=None):
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

    #TODO: Consider what information we give. Right now this includes tid and the password.
    team_info = get_team()
    team_info["score"] = api.scoreboard.get_score()
    team_info["members"] = [api.user.get_user(uid=uid)["username"] for uid in get_team_uids(tid)]

    return team_info

def get_all_teams():
    """
    Retrieves all teams.

    Returns:
        A list of all of the teams.
    """

    db = api.common.get_conn()
    return list(db.teams.find({}, {"_id": 0}))
