__author__ = 'collinpetty'

from api import app, common

from api.annotations import *
import bcrypt


def get_user(name=None):
    db = common.get_conn()
    if 'uid' in session:
        return db.users.find_one({'uid': session['uid']})
    users = db.users.find({'name': name})
    if users.count() == 0:
        return None
    user = users[0]  # Pull the top entry off the cursor
    return user


def create_user(name, email, pwhash):
    db = common.get_conn()
    uid = common.token()
    try:
        db.users.insert({'uid': uid,
                         'name': name,
                         'email': email,
                         'pwhash': pwhash})
    except Exception as e:
        print("Error creating the user account.")
        return None
    return uid


def get_all_users():
    db = common.get_conn()
    return [{'uid': u['uid'],
             'name': u['name'],
             'email': u['email']} for u in db.users.find({})]


@app.route('/api/register', methods=['POST'])
@return_json
def register_user():
    """Register a new team.

    Checks that an email address, team name, adviser name, affiliation, and password were sent from the browser.
    If any of these are missing a status:0 is returned with a message saying that all fields must be provided.
    """
    email = request.form.get('email', '')
    name = request.form.get('username', '')
    pwd = request.form.get('pass', '')

    if '' in {email, name, pwd}:
        return 0, None, "Please fill out all required fields."
    if get_user(name) is not None:
        return 0, None, "A user with that name has already registered."
    uid = create_user(name, email, bcrypt.hashpw(str(pwd), bcrypt.gensalt(8)))
    if uid is None:
        return 0, None, "There was an error creating your account."
    return 1, None, "User '%s' created successfully!" % name


@app.route('/api/updatepass', methods=['POST'])
@return_json
@require_login
def update_password(uid, request):
    """Update account password.

    Gets the new password and the password entered into the 'confirm password' box and verifies that 1) The new pw is
    not empty and 2) the new pw and the conf pw are the same. We salt/hash the password and update the team object
    in mongo then return a status:1 with a success message.
    """

    db = common.get_conn()
    pwd = request.form.get('pwd', '')
    conf = request.form.get('conf', '')
    if pwd == '':
        return 0, None, "Your password cannot be empty."
    if pwd != conf:
        return 0, None, "Your passwords do not match."
    db.users.update({'uid': uid}, {'$set': {'pwhash': bcrypt.hashpw(pwd, bcrypt.gensalt(8))}})
    return 1, None, "Your password has been successfully updated!"


@app.route('/api/getsshacct', methods=['GET'])
@return_json
@require_login
def get_ssh_account():
    """Get a webshell account.

    Searches the sshaccts collection for a document that has the current team's tid, if one is found the creds are
    returned. If no ssh account is associated with the user an account with no tid is selected and assigned to the
    current team. The credentials are then returned. If no unused accounts are found an error email is sent to the
    admin_emails list and an error is returned.
    """
    uid = session['uid']
    db = common.get_conn()
    sshacct = db.sshaccts.find_one({'uid': uid})
    if sshacct is not None:
        return 1, {'username': sshacct['user'], 'password': sshacct['password']}
    sshacct = db.sshaccts.find_one({'$or': [{'uid': ''}, {'uid': {'$exists': False}}]})
    if sshacct is not None:
        db.sshaccts.update({'_id': sshacct['_id']}, {'$set': {'uid': uid}})
        return 1, {'username': sshacct['user'], 'password': sshacct['password']}
    return 0, None, "No free SSH accounts were found, please notify and administrator."