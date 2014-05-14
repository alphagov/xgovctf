__author__ = ["Collin Petty", "Peter Chapman"]

from api.annotations import *
from api import app, problem, user


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