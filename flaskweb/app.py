"""
Flask routing
"""

import os
from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__, static_path="/static")
app.wsgi_app = ProxyFix(app.wsgi_app)

# log = app.logger.use(__name__)

session_cookie_domain = "127.0.0.1"
session_cookie_path = "/"
session_cookie_name = "flask"

secret_key = ""


def config_app(*args, **kwargs):
    """
    Return the app object configured correctly.
    This needed to be done for gunicorn.
    """

    app.secret_key = secret_key
    app.config["SESSION_COOKIE_DOMAIN"] = session_cookie_domain
    app.config["SESSION_COOKIE_PATH"] = session_cookie_path
    app.config["SESSION_COOKIE_NAME"] = session_cookie_name


    # app.logger.setup_logs({"verbose": 2})
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


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")
