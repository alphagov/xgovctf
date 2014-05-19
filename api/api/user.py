__author__ = 'collinpetty'

from api import app, common, team

from api.annotations import *
import bcrypt


def get_user(username=None):
    db = common.get_conn()
    if username is not None:
        return db.users.find_one({'username': username})
    if 'uid' in session:
        return db.users.find_one({'uid': session['uid']})
    return None


def create_user(username, email, pwhash):
    db = common.get_conn()
    uid = common.token()
    try:
        db.users.insert({'uid': uid,
                         'username': username,
                         'email': email,
                         'pwhash': pwhash})
    except Exception as e:
        print("Error creating the user account.")
        return None
    return uid


def get_all_users():
    db = common.get_conn()
    return [{'uid': u['uid'],
             'username': u['username'],
             'email': u['email']} for u in db.users.find({})]


@app.route('/api/user/create', methods=['POST'])
@return_json
def register_user():
    """Register a new team.

    Checks that an email address, team name, adviser name, affiliation, and password were sent from the browser.
    If any of these are missing a status:0 is returned with a message saying that all fields must be provided.
    """
    email = request.form.get('email')
    username = request.form.get('username')
    pwd = request.form.get('pass')
    teamname = request.form.get('teamname')
    confirm = request.form.get('confirm', False)

    db = common.get_conn()
    if None in {email, username, pwd, teamname}:
        return 0, None, "Please fill out all required fields."
    if get_user(username) is not None:
        return 0, None, "A user with that name has already registered."
    teamacct = team.get_team(teamname=teamname)
    if confirm and teamacct is not None:
        useracct = create_user(username, email, bcrypt.hashpw(str(pwd), bcrypt.gensalt(8)))
        if useracct is None:
            return 0, None, "There was an error during registration."
        db.users.update({'uid': useracct['uid']}, {'$set': {'tid': teamacct['tid']}})
        return 1, None, "User '%s' registered successfully!" % username
    elif not confirm and teamacct is not None:
        return 2, None, "The team name you have entered exists, would like to join it?"
    elif teamacct is None:
        return 3, None, "The specified team does not exist, would you like to create it?"


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