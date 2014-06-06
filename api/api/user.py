__author__ = 'collinpetty'

from api import app, common, team

from api.common import validate, ValidationException
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

    try:
        email = validate(request.form.get('email'), 'Email', min_length=1, max_length=100)
        user_name = validate(request.form.get('username'), 'Username', max_length=50, min_length=3)
        pwd = request.form.get('pass')   # JB: Consider adding password validation

        create_new = request.form.get('create-new-team') == 'true'

        # Creating a new team / password
        if create_new:
            team_name_new = validate(request.form.get('team-name-new'), 'Team Name', max_length=50, min_length=3)
            team_password_new = validate(request.form.get('team-pass-new'), 'Team Password',
                                         max_length=50, min_length=3)  # JB: Consider adding password validation
            team_adviser_name_new = validate(request.form.get('team-adv-name-new'), 'Adviser Name',
                                             max_length=50, min_length=3)
            team_adviser_email_new = validate(request.form.get('team-adv-email-new'), 'Adviser Email',
                                              max_length=50, min_length=3)
            team_school_new = validate(request.form.get('school-new'), 'School Name', max_length=50, min_length=3)

        else:
            # Joining an existing team
            team_name_existing = request.form.get('team-name-existing')
            team_password_existing = request.form.get('team-pass-existing')

    except common.ValidationException as validation_failure:
        return 0, None, validation_failure.value

    db = common.get_conn()

    # Check for duplicate usernames
    if get_user(user_name) is not None:
        return 0, None, "A user with that name has already registered."

    if create_new:
        teamacct = team.get_team(team_name=team_name_new)
        if teamacct is not None:
            return 0, None, "A team with that name already exists"
        join_team = team.create_team(team_name_new, team_adviser_name_new, team_adviser_email_new,
                                     team_school_new, team_password_new)
        if join_team is None:
            return 0, None, "Failed to create new team"
    else:
        teamacct = team.get_team(team_name=team_name_existing)
        print(teamacct)
        if teamacct is None:
            return 0, None, "There is no existing team called '%s'" % team_name_existing
        if teamacct['password'] != team_password_existing:
            return 0, None, "Your team password is incorrect"
        join_team = teamacct['tid']

    # Create new user
    useracct = create_user(user_name, email, bcrypt.hashpw(str(pwd), bcrypt.gensalt(8)))
    if useracct is None:
        return 0, None, "There was an error during registration."

    # Have the new user join the correct team
    db.users.update({'uid': useracct}, {'$set': {'tid': join_team}})

    return 1, None, "User '%s' registered successfully!" % user_name



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