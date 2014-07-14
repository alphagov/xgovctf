""" Module for handling groups of teams """


from voluptuous import Required, Length, Schema
from api.common import check, APIException, validate

import api.common
import api.user
import api.team

register_group_schema = Schema({
    Required("group-name"): check(
        (0, "Group name must be between 3 and 50 characters.", [str, Length(min=3, max=100)]),
        (0, "A group with that name already exists! Try joining it instead." [
            lambda name: get_group(name=name) is None])
    )
})

join_group_schema = Schema({
    Required("group-name"): check(
        (0, "Group name must be between 3 and 50 characters.", [str, Length(min=3, max=100)]),
        (0, "No group exists with that name! Try creating it instead.", [
            lambda name: get_group(name=name) is not None]),
        (0, "Your team is already a member of that group.", [
            lambda name: get_group(name=name) not in [group["gid"] for group in api.team.get_groups()]
        ])
    )
})

def get_group(name=None, gid=None):
    """
    Retrieve a group based on its name or gid.

    Args:
        name: the name of the group
        gid: the gid of the group
    Returns:
        The group object.
    """

    db = api.common.get_conn()

    match = {}
    if name is not None:
        match.update({"name": name})
    elif gid is not None:
        match.update({"gid": gid})
    else:
        raise APIException(0, None, "Group name or gid must be specified to look it up.")

    return db.groups.find_one(match, {"_id": 0})

def create_group(tid, group_name):
    """
    Inserts group into the db. Assumes everything is validated.

    Args:
        tid: The id of the team creating the group.
        group_name: The name of the group.
    Returns:
        The new group's gid.
    """

    db = api.common.get_conn()

    gid = api.common.token()

    db.groups.insert({
        "name": group_name,
        "owners": [tid],
        "members": [tid],
        "gid": gid
    })

    return gid


def create_group_request(params, tid=None):
    """
    Creates a new group. Validates forms.
    All required arguments are assumed to be keys in params.

    Args:
        group-name: The name of the group

        Optional:
            tid: The team id creating the group. If oxmmitted,
            the tid will be grabbed from the logged in user.
    Returns:
        The new gid
    """

    validate(register_group_schema, params)

    if tid is None:
        tid = api.user.get_team()["tid"]

    return create_group(tid, params["group-name"])


def join_group(tid, gid):
    """
    Adds a team to a group. Assumes everything is valid.

    Args:
        tid: the team id
        gid: the group id to join
    """

    db = api.common.get_conn()

    db.groups.update({'gid': gid}, {'$push': {'members': tid}})

def join_group_request(params, tid=None):
    """
    Tries to place a team into a group. Validates forms.
    All required arguments are assumed to be keys in params.

    Args:
        group-name: The name of the group to join.

        Optional:
            tid: If omitted,the tid will be grabbed from the logged in user.
    """

    validate(join_group_schema, params)

    tid = api.user.get_team()["tid"]

    gid = get_group(name=params["group-name"])

    join_group(tid, gid)


#TODO: Refactor into request/naive form
def leave_group(tid, gid=None, name=None):
    """
    Removes a team from a group

    Args:
        tid: the team id
        gid: the group id to leave
        name: the group name to leave
    """

    db = api.common.get_conn()

    if gid:
        match = {'gid': gid}
    elif name:
        match = {'group_name': name}
    else:
        raise APIException(0, None, "No group information passed.")

    if db.groups.find_one(match) is None:
        raise APIException(0, None, "Group not found.")

    db.groups.update(match, {'$pull': {'owners': tid}})
    db.groups.update(match, {'$pull': {'members': tid}})
