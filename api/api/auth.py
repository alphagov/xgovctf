__author__ = ["Collin Petty", "Peter Chapman"]
__copyright__ = "Carnegie Mellon University"
__license__ = "MIT"
__maintainer__ = ["Collin Petty", "Peter Chapman"]
__credits__ = ["David Brumley", "Collin Petty", "Peter Chapman", "Tyler Nighswander", "Garrett Barboza"]
__email__ = ["collin@cmu.edu", "peter@cmu.edu"]
__status__ = "Production"

from flask import session
from voluptuous import Schema, Required, Length

import api.user
from api.user import check
from api.common import APIException
import bcrypt

debug_disable_general_login = False

user_login_schema = Schema({
    Required('username'): check(
        (0, "Usernames must be between 3 and 50 characters.", [str, Length(min=3, max=50)]),
    ),
    Required('password'): check(
        (0, "Passwords must be between 3 and 50 characters.", [str, Length(min=3, max=50)])
    )
})

def login(username, password):
    """Authenticates a user.

    Verify that the user is not already logged in. Verify that the username/password are not empty.
    Query for the user from the user interface matching on username. Check if passwords match, if so add the
    corresponding 'uid' to the session, if not inform the user of incorrect credentials.
    """

    # Read in submitted username and password
    user_login_schema({
        "username": username,
        "password": password
    })
    user = api.user.get_user(username)
    if user is None:
        raise APIException(0, None, "Incorrect username.")

    password_hash = user['password_hash']
    if bcrypt.hashpw(password, password_hash) == password_hash:
        if user.get('debugaccount', False):
            session['debugaccount'] = True
        if debug_disable_general_login:
            if session.get('debugaccount', False):
                raise APIException(2, None, "Correct credentials! But the game has not started yet...")
        if user['uid'] is not None:
            session['uid'] = user['uid']
            raise APIException(1, None, "Successfully logged in as " + username)
        else:
            raise APIException(0, None, "Login Error")
    raise APIException(0, None, "Incorrect Password")


def logout():
    """Logout

    If the user has a uid in the session it is removed.
    """
    session.clear()


def is_logged_in():
    """Check if the user is currently logged in.

    If the user has a uid in their session, they are logged in
    """
    return 'uid' in session


def is_admin():
    """Check if the user is an admin.

    If the user as the 'admin' flag set in their session, they are an admin.
    """
    return session.get('admin', False)
