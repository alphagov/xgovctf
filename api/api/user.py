"""
API functions relating to user management and registration.
"""

from flask import session
from voluptuous import Required, Length, Schema
from api.common import check, APIException, validate

import api.team
import api.common
import api.auth

import bcrypt

from re import match

user_schema = Schema({
    Required('email'): check(
        (0, "Email must be between 5 and 100 characters.", [str, Length(min=5, max=100)]),
        (0, "This does not look like an email address.", [
            lambda email: match(r"[A-Za-z0-9\._%+-]+@[A-Za-z0-9\.-]+\.[A-Za-z]{2,4}", email) is not None])
    ),
    Required('username'): check(
        (0, "Usernames must be between 3 and 50 characters.", [str, Length(min=3, max=50)]),
        (0, "This username already exists.", [
            lambda name: get_user(name) == None])
    ),
    Required('password'):
        check((0, "Passwords must be between 3 and 50 characters.", [str, Length(min=3, max=50)]))
}, extra=True)

new_team_schema = Schema({
    Required('team-name-new'): check(
        (0, "The team name must be between 3 and 50 characters.", [str, Length(min=3, max=50)]),
        (0, "A team with that name already exists.", [
            lambda name: api.team.get_team(name=name) == None])
    ),
    Required('team-password-new'):
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
        (0, "There is no existing team named that.", [
            lambda name: api.team.get_team(name=name) != None]),
        (0, "There are too many members on that team for you to join.", [
            lambda name: len(api.team.get_team_uids(name=name)) < api.team.max_team_users
        ])
    ),
    Required('team-password-existing'):
        check((0, "Team passwords must be between 3 and 50 characters.", [str, Length(min=3, max=50)]))
}, extra=True)

def hash_password(password):
    """
    Hash plaintext password.

    Args:
        password: plaintext password
    Returns:
        Secure hash of password.
    """

    return bcrypt.hashpw(password, bcrypt.gensalt(8))

def get_team(uid=None):
    """
    Retrieve the the corresponding team to the user's uid.

    Args:
        uid: user's userid
    Returns:
        The user's team.
    """

    user = get_user(uid=uid)
    return api.team.get_team(tid=user["tid"])

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


def create_user(username, email, password_hash, tid):
    """
    This inserts a user directly into the database. It assumes all data is valid.

    Args:
        username: user's username
        email: user's email
        password_hash: a hash of the user's password
        tid: the team id to join
    Returns:
        Returns the uid of the newly created user
    """

    db = api.common.get_conn()
    uid = api.common.token()

    if get_user(name=username) is not None:
        raise APIException(0, None, "User {0} already exists!".format(username))

    db.users.insert({
        'uid': uid,
        'username': username,
        'email': email,
        'password_hash': password_hash,
        'tid': tid,
        'avatar': 3,
        'eventid': 0,
        'level': 'Not Started'
    })

    return uid

def get_all_users():
    """
    Returns:
        Returns the uid, username, and email of all users.
    """

    db = api.common.get_conn()
    return list(db.users.find({}, {"uid": 1, "username": 1, "email": 1}))


def register_user(params):
    """
    Registers a new user and creates/joins a team. Validates all fields.
    Assume arguments to be specified in a dict.

    Args:
        username: user's username
        password: user's password
        email: user's email
        create-new-team:
            boolean "true" indicating whether or not the user is creating a new team or
            joining an already existing team.

        team-name-existing: Name of existing team to join.
        team-password-existing: Password of existing team to join.

        team-name-new: Name of new team.
        team-adv-name-new: Name of adviser.
        team-adv-email-new: Adviser's email address.
        team-school-new: Name of the team's school.
        team-password-new: Password to join team.

    """
    validate(user_schema, params)

    if params.get("create-new-team", None) == "on":
        validate(new_team_schema, params)

        team_params = {
            "team_name": params["team-name-new"],
            "adviser_name": params["team-adv-name-new"],
            "adviser_email": params["team-adv-email-new"],
            "school": params["team-school-new"],
            "password" : params["team-password-new"]
        }

        tid = api.team.create_team(team_params)

        if tid is None:
            raise APIException(-10, None, "Failed to create new team")
        team = api.team.get_team(tid=tid)
    else:
        validate(existing_team_schema, params)

        team = api.team.get_team(name=params["team-name-existing"])

        if team['password'] != params['team-password-existing']:
            raise APIException(0, None, "Your team password is incorrect.")


    # Create new user
    uid = create_user(
        params["username"],
        params["email"],
        hash_password(params["password"]),
        team["tid"]
    )

    if uid is None:
        raise APIException(0, None, "There was an error during registration.")

    return uid

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

    db.users.update({'uid': uid}, {'$set': {'password_hash': hash_password(password)}})

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
