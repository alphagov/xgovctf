__author__ = ["Collin Petty", "Peter Chapman"]
__copyright__ = "Carnegie Mellon University"
__license__ = "MIT"
__maintainer__ = ["Collin Petty", "Peter Chapman"]
__credits__ = ["David Brumley", "Collin Petty", "Peter Chapman", "Tyler Nighswander", "Garrett Barboza"]
__email__ = ["collin@cmu.edu", "peter@cmu.edu"]
__status__ = "Production"

from api.common import validate
import api.user
import bcrypt

debug_disable_general_login = False

def login(username, password, session):
    """Authenticates a user.

    Verify that the user is not already logged in. Verify that the username/password are not empty.
    Query for the user from the user interface matching on username. Check if passwords match, if so add the
    corresponding 'uid' to the session, if not inform the user of incorrect credentials.
    """

    # Read in submitted username and password
    try:
        username = validate(username, 'Username',
                            min_length=api.user.MIN_USERNAME_LENGTH, max_length=api.user.MAX_USERNAME_LENGTH)
        password = validate(password, 'Password',
                            min_length=api.user.MIN_PASSWORD_LENGTH, max_length=api.user.MAX_PASSWORD_LENGTH)
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


def logout(session):
    """Logout

    If the user has a uid in the session it is removed.
    """
    session.clear()


def is_logged_in(session):
    """Check if the user is currently logged in.

    If the user has a uid in their session, they are logged in
    """
    return 'uid' in session


def is_admin(session):
    """Check if the user is an admin.

    If the user as the 'admin' flag set in their session, they are an admin.
    """
    return session.get('admin', False)
