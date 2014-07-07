__author__ = 'Collin Petty'
from common import db
import common


def get_group_membership(tid):
    """Get the group membership for a team.

    Find all groups to which a tid is an owner then add all groups to which a user is just a member.
    """
    groups = list()
    owners = set()
    for g in list(db.groups.find({'owners': tid}, {'name': 1, 'gid': 1})):
        groups.append({'name': str(g['name']),
                       'gid': g['gid'],
                       'owner': True})
        owners.add(g['gid'])
    groups += filter(lambda g: g['gid'] not in owners,
                     ({'name': str(g['name']),
                       'gid': g['gid'],
                       'owner': False} for g in list(db.groups.find({'members': tid}, {'name': 1, 'gid': 1}))))
    return groups


def create_group(tid, gname):
    """Create a new group.

    Get a groupname posted from a logged in user. Check to see if the group exists, if it does notify the user.
    If the group does not exist create it and add the user as a member/owner.
    """
    if gname == '':
        return {'status': 0, 'message': "The group name cannot be empty!"}
    gname = gname.strip().replace(' ', '_')
    try:
        gname.decode('ascii')
    except UnicodeEncodeError:
        return {'status': 0, 'message': "The group name can only contain ASCII characters."}
    if db.groups.find_one({'name': gname}) is not None:
        return {'status': 2, 'message': "This group exists, would you like to join it?"}
    db.groups.insert({"name": gname, "owners": [tid], "members": [tid], "gid": common.token()})
    return {'status': 1, 'message': "Successfully created the group"}


def join_group(tid, gname):
    """Join a group.

    Get a groupname posted from a logged in user.  Errors if the name is empty.  Search db for the non-empty group
    name, if no group with that name exists and error is returned.  If a group is found, we query db to see if the
    user is already a member/owner, if either, error.  If we haven't error so far add the user as a member to the group
    and return a status=1 for success.
    """
    if gname == '':
        return {'status': 0, 'message': "The group name cannot be empty!"}
    gname = gname.strip().replace(' ', '_')
    group = db.groups.find_one({'name': gname})
    if group is None:
        return {'status': 3, 'message': "Cannot find group '%s', create it?" % gname}
    if db.groups.find({'gid': group['gid'], '$or': [{'owners': tid},
                                                    {'members': tid}]}).count() != 0:
        return {'status': 2, 'message': "You are already in '%s'." % gname}

    db.groups.update({'gid': group['gid']}, {'$push': {'members': tid}})
    return {'status': 1, 'message': "Success! You have been added to '%s'." % gname}


def leave_group(tid, gid):
    """Removes the current team from a group"""
    if gid is None:
        return {'status': 0, 'message': "No group id passed."}
    if db.groups.find_one({'gid': gid}) is None:
        return {'status': 0, 'message': "Internal error, group not found."}
    db.groups.update({'gid': gid}, {'$pull': {'owners': tid}})
    db.groups.update({'gid': gid}, {'$pull': {'members': tid}})
    return {'status': 1, 'message': "You have successfully been removed from the group."}
