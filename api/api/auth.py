__author__ = ["Collin Petty", "Peter Chapman"]
__copyright__ = "Carnegie Mellon University"
__license__ = "MIT"
__maintainer__ = ["Collin Petty", "Peter Chapman"]
__credits__ = ["David Brumley", "Collin Petty", "Peter Chapman", "Tyler Nighswander", "Garrett Barboza"]
__email__ = ["collin@cmu.edu", "peter@cmu.edu"]
__status__ = "Production"

import bcrypt
from api.annotations import *
from api import app
from api.common import validate
import api
import api.user
debug_disable_general_login = False


@app.route('/api/login', methods=['POST'])
@return_json
def login():
    """Authenticates a user.

    Verify that the user is not already logged in. Verify that the username/password are not empty.
    Query for the user from the user interface matching on username. Check if passwords match, if so add the
    corresponding 'uid' to the session, if not inform the user of incorrect credentials.
    """
    if 'uid' in session:  # we assume that if there is a uid in the session then the user is authenticated
        return 1, None, "You are already logged in."

    # Read in submitted username and password
    try:
        username = validate(request.form.get('username'), 'Username',
                            min_length=user.MIN_USERNAME_LENGTH, max_length=user.MAX_USERNAME_LENGTH)
        password = validate(request.form.get('password'), 'Password',
                            min_length=user.MIN_PASSWORD_LENGTH, max_length=user.MAX_PASSWORD_LENGTH)
    except common.ValidationException as validation_failure:
        return 0, None, validation_failure.value

    user = api.user.get_user(username)
    if user is None:
        return 0, None, "Incorrect username."

    pwhash = user['pwhash']  # The pw hash from the db
    if bcrypt.hashpw(password, pwhash) == pwhash:
        if user.get('debugaccount', False):
            session['debugaccount'] = True
        if debug_disable_general_login:
            if session.get('debugaccount', False):
                return 2, None, "Correct credentials! But the game has not started yet..."
        if user['uid'] is not None:
            session['uid'] = user['uid']
            return 1, None, "Successfully logged in as '%s'." % username
        else:
            return 0, None, "Login Error"
    return 0, None, "Incorrect Password"


@app.route('/api/logout', methods=['GET'])
@return_json
@log_request
def logout():
    """Logout

    If the user has a uid in the session it is removed and status:1 is returned.
    If uid is not in session status:0 is returned.
    """
    if 'uid' in session:
        session.clear()
        return 1, None, "Successfully logged out."
    else:
        return 0, None, "You do not appear to be logged in."


@app.route('/api/isloggedin', methods=['GET'])
@return_json
def is_logged_in():
    """Check if the user is currently logged in.

    If the user has a uid in their session return status:1 and a message
    If they are not logged in return a message saying so and status:0
    """
    if 'uid' in session:
        return 1, None, "You are logged in."
    else:
        return 0, None, "You are not logged in."


@app.route('/api/isadmin')
@return_json
def is_admin():
    """Check if the user is an admin.

    If the user as the 'admin' flag set in their session. If so return status:1,
    if not return status:0.
    """
    if session.get('admin', False):
        return 1, None, "You have admin permissions."
    return 0, None, "You do not have admin permissions."