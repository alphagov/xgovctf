"""
Flask routing
"""

from flask import Flask, request, render_template, flash, redirect, session
from werkzeug.contrib.fixers import ProxyFix
import requests

app = Flask(__name__, static_path="/static")
app.wsgi_app = ProxyFix(app.wsgi_app)

# log = app.logger.use(__name__)

session_cookie_domain = "127.0.0.1"
session_cookie_path = "/"
session_cookie_name = "flask"

secret_key = "not_a_real_secret"


def config_app(*args, **kwargs):
    """
    Return the app object configured correctly.
    This needed to be done for gunicorn.
    """

    app.secret_key = secret_key
    app.config["SESSION_COOKIE_DOMAIN"] = session_cookie_domain
    app.config["SESSION_COOKIE_PATH"] = session_cookie_path
    app.config["SESSION_COOKIE_NAME"] = session_cookie_name
    return app


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, *')
    response.headers.add('Cache-Control', 'no-cache')
    response.headers.add('Cache-Control', 'no-store')
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form["create-team"] == "Yes":
            post_data = {
                "email": request.form["email"],
                "firstname": "No",
                "lastname": "Name",
                "country": "uk",
                "username": request.form["username"],
                "password": request.form["password"],
                "background": "Government",
                "create-new-teacher": "false",
                "create-new-team": "true",
                "team-name-new": request.form["create-team-name"],
                "team-school-new": "None",
                "team-password-new": request.form["create-team-password"],
                "ctf-emails": "false"
            }
            r = requests.post("http://localhost:8000/api/user/create", data=post_data)
            resp = r.json()
            if resp["status"] == 1:
                app.logger.info("User created "+r.text)
                session["token"] = r.cookies["token"]
                return redirect("/problems")
            else:
                flash(resp["message"])
                app.logger.error(r.text)
        else:
            post_data = {
                "email": request.form["email"],
                "firstname": "No",
                "lastname": "Name",
                "country": "uk",
                "username": request.form["username"],
                "password": request.form["password"],
                "background": "Government",
                "create-new-teacher": "false",
                "create-new-team": "false",
                "team-name-existing": request.form["team-name"],
                "team-password-existing": request.form["team-select-password"],
                "ctf-emails": "false"
            }
            r = requests.post("http://localhost:8000/api/user/create", data=post_data)
            resp = r.json()
            if resp["status"] == 1:
                app.logger.info("User created "+r.text)
                session["token"] = r.cookies["token"]
                return redirect("/problems")
            else:
                flash(resp["message"])
                app.logger.error(r.text)
            pass

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        post_data = {
            "username": request.form["username"],
            "password": request.form["password"],
        }
        r = requests.post("http://127.0.0.1:8000/api/user/login", data=post_data)
        resp = r.json()
        if resp["status"] == 1:
            app.logger.info(r.cookies)
            app.logger.info(r.cookies.get("flask"))
            session["token"] = r.cookies["token"]
            session["api-session"] = r.cookies["flask"]
            return redirect("/problems")
        else:
            flash(resp["message"])
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/problems")
def problems():
    if "token" in session:
        token = session["token"]
        team_info = requests.get("http://localhost:8000/api/team", cookies={"token": token, "flask": session["api-session"]})
        status = requests.get("http://localhost:8000/api/user/status", cookies={"token": token, "flask": session["api-session"]})
        problems = requests.get("http://localhost:8000/api/problems", cookies={"token": token, "flask": session["api-session"]})
        return render_template("problems.html", team_info=team_info.json()["data"], status=status.json()["data"], problems=problems.json()["data"])
    else:
        return redirect("/")
