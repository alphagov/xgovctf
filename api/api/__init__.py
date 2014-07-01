from flask import Flask, url_for, request, session

app = Flask(__name__)

from api import setup, user, auth, team, problem, scoreboard
from api.annotations import return_json, require_login, require_admin, log_request

# Initialize/Sanity check envionment
setup.load_config(app)
setup.check_database_indexes()

@app.after_request
def after_request(response):
    if (request.headers.get('Origin', '') in
            ['http://picoctf.com',
             'http://www.picoctf.com']):
        response.headers.add('Access-Control-Allow-Origin',
                             request.headers['Origin'])
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, *')
    response.headers.add('Cache-Control', 'no-cache')
    response.headers.add('Cache-Control', 'no-store')
    response.mimetype = 'application/json'
    return response


@app.route("/api/sitemap", methods=["GET"])
@return_json
def site_map_hook():
    print("Building sitemap")
    links = []
    for rule in app.url_map._rules:
        if "GET" in rule.methods or "POST" in rule.methods:
            try:
                url = url_for(rule.endpoint)
                links.append(url)
            except:
                pass
    return 1, links, "This is a message."


@app.route('/api/user/create', methods=['POST'])
@return_json
def create_user_hook():
    #TB: Do not directly return these!
    return user.register_user(request.values)


@app.route('/api/updatepass', methods=['POST'])
@return_json
@require_login
def update_password_hook():
    return user.update_password(user.get_user.uid, request.form.get('pass'), request.form.get('confirm'))


@app.route('/api/getsshacct', methods=['GET'])
@return_json
@require_login
def get_ssh_account_hook():
    return user.get_ssh_account(user.get_user().uid)


@app.route('/api/login', methods=['POST'])
@return_json
def login_hook():
    return auth.login(request.form.get('username'), 
                      request.form.get('password'), session)


@app.route('/api/logout', methods=['GET'])
@return_json
@log_request
def logout_hook():
    if auth.is_logged_in():
        auth.logout(session)
        return 1, None, "Successfully logged out."
    else:
        return 0, None, "You do not appear to be logged in."


@app.route('/api/isloggedin', methods=['GET'])
@return_json
def is_logged_in_hook():
    if auth.is_logged_in(session):
        return 1, None, "You are logged in."
    else:
        return 0, None, "You are not logged in."


@app.route('/api/isadmin', methods=['GET'])
@return_json
def is_admin_hook():
    if auth.is_admin():
        return 1, None, "You have admin permissions."
    else:
        return 0, None, "You do not have admin permissions."


@app.route('/api/team', methods=['GET'])
@return_json
@require_login
def team_hook():
    user_account = user.get_user()
    tid = useracct['tid']
    uid = useracct['uid']
    return 1, auth.get_team_information(tid, uid)


@app.route('/api/admin/getallproblems', methods=['GET'])
@return_json
@require_admin
def get_all_problems_hook():
    probs = problem.get_all_problems()
    if probs is None:
        return 0, None, "There was an error querying problems from the database."
    return 1, probs


@app.route('/api/admin/getallusers', methods=['GET'])
@return_json
@require_admin
def get_all_users_hook():
    users = user.get_all_users()
    if users is None:
        return 0, None, "There was an error query users from the database."
    return 1, users


@app.route('/api/problems', methods=['GET'])
@require_login
@return_json
def load_viewable_problems_hook():
    return 1, problem.load_viewable_problems(get_user().tid)


@app.route('/api/problems/solved', methods=['GET'])
@require_login
@return_json
def get_solved_problems_hook():
    return 1, problem.get_solved_problems()


@app.route('/api/submit', methods=['POST'])
@return_json
@require_login
def submit_problem_hook():
    user_account = user.get_user()
    tid = user_account.tid

    return problem.submit_problem(tid, request.form.get('pid',''), read.form.get('key',''))

@app.route('/api/problems/<path:pid>', methods=['GET'])
@require_login
@return_json
@log_request
def get_single_problem_hook(pid):
    problem_info = problem.get_single_problem(pid, user.get_user().tid)
    if 'status' not in problem_info:
        problem_info.update({"status": 1})
    return 1, problem_info


@app.route('/api/score', methods=['GET'])
@require_login
@return_json
def get_team_score_hook():
    score = scoreboard.get_team_score(session['uid'])
    if score is not None:
        return 1, {'score': score}
    return 0, None, "There was an error retrieving your score."
