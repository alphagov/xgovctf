__author__ = ["Collin Petty", "Peter Chapman"]
__copyright__ = "Carnegie Mellon University"
__license__ = "MIT"
__maintainer__ = ["Collin Petty", "Peter Chapman"]
__credits__ = ["David Brumely", "Collin Petty", "Peter Chapman", "Tyler Nighswander", "Garrett Barboza"]
__email__ = ["collin@cmu.edu", "peter@cmu.edu"]
__status__ = "Production"

import bcrypt
from api.annotations import *
from api import app
import api
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
    username = request.form.get('username', None)  # get the teamname and password from the POSTed form
    password = request.form.get('password', None)
    if username is None or username == '':
        return 0, None, "Username cannot be empty."
    if password is None or password == '':  # No password submitted
        return 0, None, "Password cannot be empty."
    if len(username) > 250:
        return 0, None, "STAHP!"
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
    return 0, None, "Incorrect Password"


@app.route('/api/logout', methods=['GET'])
@return_json
@log_request
def logout():
    """Logout

    If the user has a teamID in the session it is removed and success:1 is returned.
    If teamID is not in session success:0 is returned.
    """

    if 'tid' in session:
        session.clear()
        return 1, None, "Successfully logged out."
    else:
        return 0, None, "You do not appear to be logged in."


@app.route('/api/isloggedin', methods=['GET'])
@return_json
def is_logged_in():
    """Check if the user is currently logged in.

    If the user has a teamID in their session return success:1 and a message
    If they are not logged in return a message saying so and success:0
    """
    if 'tid' in session:
        return 1, None, "You are logged in."
    else:
        return 0, None, "You are not logged in."


@app.route('/api/isadmin')
@return_json
def is_admin():
    if session.get('admin'):
        return 1, None, "You have admin permissions."
    return 0, None, "You do not have admin permissions."