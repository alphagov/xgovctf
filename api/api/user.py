"""
API functions relating to user management and registration.
"""

from flask import session
from voluptuous import Schema, Required, Length
from api.common import check, APIException

import api.team
import api.common
import api.auth

import bcrypt

user_schema = Schema({
    Required('email'):
        check((0, "Email must be between 5 and 100 characters.", [str, Length(min=5, max=100)])),
    Required('username'): check(
        (0, "Usernames must be between 3 and 50 characters.", [str, Length(min=3, max=50)]),
        (-1, "This username already exists.", [
            lambda name: get_user(name) == None])
    ),
    Required('pass'):
        check((0, "Passwords must be between 3 and 50 characters.", [str, Length(min=3, max=50)]))
}, extra=True)

new_team_schema = Schema({
    Required('team-name-new'): check(
        (0, "The team name must be between 3 and 50 characters.", [str, Length(min=3, max=50)]),
        (-1, "A team with that name already exists.", [
            lambda name: api.team.get_team(name=name) == None])
    ),
    Required('team-pass-new'):
        check((0, "Team passwords must be between 3 and 50 characters.", [str, Length(min=3, max=50)])),
    Required('team-adv-name-new'):
        check((0, "Adviser names should be between 3 and 50 characters.", [str, Length(min=3, max=50)])),
    Required('team-adv-email-new'):
        check((0, "Adviser emails must be between 5 and 100 characters.", [str, Length(min=5, max=100)])),
    Required('team-school-new'):
        check((0, "School names must be between 3 and 150 characters.", [str, Length(min=3, max=150)]))

}, extra=True)

existing_team_schema = Schema({
    Required('team-name-existing'): check(
        (0, "Existing team names must be between 3 and 50 characters.", [str, Length(min=3, max=50)]),
        (-1, "There is no existing team named that.", [
            lambda name: api.team.get_team(name=name) != None])
    ),
    Required('team-pass-existing'):
        check((0, "Team passwords must be between 3 and 50 characters.", [str, Length(min=3, max=50)]))
})

def get_tid_from_uid(uid):
    """
    Retrieve the the corresponding tid to the user's uid.

    Args:
        uid: user's userid
    Returns:
        The user's teamid.
    """
    db = api.common.get_conn()
    return db.users.find_one({'uid': uid})['tid']


def get_user(name=None, uid=None):
    """
    Retrieve a user based on a property. If the user is logged in,
    it will return that user object.

    Args:
        name: the user's username
        uid: the user's uid
    Returns:
        Returns the corresponding user object or None if it could not be found
    """
    db = api.common.get_conn()

    if name is not None:
        return db.users.find_one({'username': name})

    if uid is not None:
        return db.users.find_one({'uid': uid})

    if api.auth.is_logged_in():
        return db.users.find_one({'uid': session['uid']})

    return None


def create_user(username, email, pwhash):
    """
    This inserts a user directly into the database. It assumes all data is valid.

    Args:
        username: user's username
        email: user's email
        pwhash: a hash of the user's password
    Returns:
        Returns the uid of the newly created user
    """
    db = api.common.get_conn()
    uid = api.common.token()
    try:
        db.users.insert({'uid': uid,
                         'username': username,
                         'email': email,
                         'pwhash': pwhash,
                         'avatar': 3,
                         'eventid': 0,
                         'level': 'Not Started'})
    except Exception:
        raise APIException(0, None, "Unable to create user.")

    return uid


def get_all_users():
    """
    Returns:
        Returns the uid, username, and email of all users.
    """
    db = api.common.get_conn()
    return [{'uid': u['uid'],
             'username': u['username'],
             'email': u['email']} for u in db.users.find({})]


def register_user(params):
    """
    Registers a new user and creates/joins a team. Validates all fields.
    Assume arguments to be specified in a dict.

    Args:
        username: user's username
        pass: user's password
        email: user's email
        create-new-team:
            boolean indicating whether or not the user is creating a new team or
            joining an already existing team.

        team-name-existing: Name of existing team to join.
        team-pass-existing: Password of existing team to join.

        team-name-new: Name of new team.
        team-adviser-name-new: Name of adviser.
        team-adviser-email-new: Adviser's email address.
        team-school-new: Name of the team's school.
        team-password-new: Password to join team.

    """
    user_schema(params)

    if params.get("create-new-team", None) == "true":
        new_team_schema(params)

        join_team = api.team.create_team(
            params["team-name-new"],
            params["team-adv-name-new"],
            params["team-adv-email-new"],
            params["team-school-new"],
            params["team-pass-new"]
        )

        if join_team is None:
            raise APIException(-10, None, "Failed to create new team")
    else:
        existing_team_schema(params)

        team_account = api.team.get_team(name=params["team-name-new"])

        if team_account['password'] != params['team-password-existing']:
            raise APIException(0, None, "Your team password is incorrect.")

        join_team = team_account['tid']

    db = api.common.get_conn()

    # Create new user
    user_account = create_user(
        params["username"],
        params["email"],
        bcrypt.hashpw(params["pass"], bcrypt.gensalt(8))
    )

    if user_account is None:
        raise APIException(0, None, "There was an error during registration.")

    # Have the new user join the correct team
    db.users.update({'uid': user_account}, {'$set': {'tid': join_team}})

def update_password(uid, password):
    """
    Update account password.

    Args:
        uid: the user id
        password: the new password
    """
    db = api.common.get_conn()

    #CG: Where should schema's fit in here? We've already defined a password validator
    #in the user_schema but this doesn't have the other fields... :(
    if len(password) == 0:
        raise APIException(0, None, "Your password cannot be empty.")

    db.users.update({'uid': uid}, {'$set': {'pwhash': bcrypt.hashpw(password, bcrypt.gensalt(8))}})

def get_ssh_account(uid):
    """
    Gets a webshell account for the user.

    Args:
        uid: the user's user id
    Returns:
        A dict with the username and password of the account.
    """
    db = api.common.get_conn()
    sshacct = db.sshaccts.find_one({'uid': uid})
    if sshacct is not None:
        return {'username': sshacct['user'], 'password': sshacct['password']}
    sshacct = db.sshaccts.find_one({'$or': [{'uid': ''}, {'uid': {'$exists': False}}]})
    if sshacct is not None:
        db.sshaccts.update({'_id': sshacct['_id']}, {'$set': {'uid': uid}})
        return {'username': sshacct['user'], 'password': sshacct['password']}
    raise APIException(0, None, "No free SSH accounts were found, please notify and administrator.")
