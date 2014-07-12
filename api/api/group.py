""" Module for handling groups of teams """
import api.common

def get_group_membership(tid):
    """
    Get the group membership for a team.

    Args:
        tid: The team id
    Returns:
        List of groups that tid is a member of
    """

    db = api.common.get_conn()

    groups = list()
    for g in list(db.groups.find({'members': tid}, {'name': 1, 'gid': 1, 'owners': 1})):
        groups.append({'name': str(g['name']),
                       'gid': g['gid'],
                       'owner': tid in g['owners']})

    return groups


def create_group(tid, group_name):
    """
    Create a new group.

    Args:
        tid: The team id creating the group
        group_name: The name of the group
    Returns:
        The new gid
    """

    db = api.common.get_conn()

    if group_name == '':
        raise APIException(0, None, "The group name cannot be empty!")
    group_name = group_name.strip().replace(' ', '_')

    try:
        group_name.decode('ascii')
    except UnicodeEncodeError:
        raise APIException(0, None, "The group name can only contain ASCII characters.")
    if db.groups.find_one({'name': group_name}) is not None:
        raise APIException(0, None, "This group exists, would you like to join it?")

    gid = api.common.token()
    db.groups.insert({"name": group_name, "owners": [tid], "members": [tid], "gid": gid})

    return gid


def join_group(tid, gid=None, name=None):
    """
    Adds a team to a group.

    Args:
        tid: the team id
        gid: the group id to join
        name: the group name to join
    """

    db = api.common.get_conn()

    if name:
        if name == '':
            raise APIException(0, None, "The group name cannot be empty!")
        name = name.strip().replace(' ', '_')
        group = db.groups.find_one({'name': name})
    elif gid:
        group = db.groups.find_one({'gid': gid})
    else:
        raise APIException(0, None, "No group information passed")

    if group is None:
        raise APIException(3, None, "Cannot find group '%s', create it?" % name)
    if db.groups.find({'gid': group['gid'], '$or': [{'owners': tid},
                                                    {'members': tid}]}).count() != 0:
        raise APIException(2, None, "You are already in '%s'." % name)

    db.groups.update({'gid': group['gid']}, {'$push': {'members': tid}})


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
