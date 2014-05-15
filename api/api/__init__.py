from api.annotations import *

from flask import Flask
app = Flask(__name__)

from api import admin, utilities, annotations, scoreboard, problem, user
import configparser
import logging
import zmq
from zmq.log.handlers import *


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


def initialize():
    context = zmq.Context()
    pub = context.socket(zmq.PUB)
    pub.bind('tcp://127.0.0.1:7979')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = PUBHandler(pub)
    handler.root_topic = 'pico'
    logger.addHandler(handler)
    logger.info("Loading the configuration file")


    config = configparser.ConfigParser()
    config.read('mister.config')
    if config.get('debug', 'admin_emails') is not None:
        common.admin_emails = list()
    for email in config.get('debug', 'admin_emails').split(','):
        common.admin_emails.append(email.strip())

    app.config['DEBUG'] = False
    secret_key = config.get('flask', 'secret_key')
    if secret_key == '':
        common.log('The Flask secret key specified in the config file is empty.')
        exit()
    app.secret_key = secret_key
    app.config['SESSION_COOKIE_HTTPONLY'] = False
    app.config['SESSION_COOKIE_DOMAIN'] = config.get('flask', 'SESSION_COOKIE_DOMAIN')
    app.config['SESSION_COOKIE_PATH'] = config.get('flask', 'SESSION_COOKIE_PATH')
    app.config['SESSION_COOKIE_NAME'] = config.get('flask', 'SESSION_COOKIE_NAME')

    common.session_cookie_domain = config.get('flask', 'SESSION_COOKIE_DOMAIN')

    mongo_addr = config.get("mongodb", "addr")
    if mongo_addr is not None:
        print("Setting mongo address to '%s'" % mongo_addr)
        common.mongo_addr = mongo_addr
    mongo_port = config.getint("mongodb", "port")
    if mongo_port is not None:
        print("Setting mongo port to '%d'" % mongo_port)
        common.mongo_port = mongo_port
    mongo_db_name = config.get("mongodb", "db_name")
    if mongo_db_name is not None:
        print("Setting mongo db_name to '%s'" %mongo_db_name)
        common.mongo_db_name = mongo_db_name

    for protocol in config.get('security','allowed_protocols').split(','):
        common.allowed_protocols.append(protocol.strip())

    for port in config.get('security','allowed_ports').split(','):
        common.allowed_ports.append(port.strip())

    enable_email = config.getboolean('email', 'enable_email')
    if enable_email:
        utilities.enable_email = enable_email
    smtp_url = config.get('email', 'smtp_url')
    utilities.smtp_url = smtp_url

    email_username = config.get('email', 'username')
    utilities.email_username = email_username

    email_password = config.get('email', 'password')
    utilities.email_password = email_password

    from_addr = config.get('email', 'from_addr')
    utilities.from_addr = from_addr

    from_name = config.get('email', 'from_name')
    utilities.from_name = from_name

    problem.root_web_path = config.get('autogen', 'root_web_path')
    problem.relative_auto_prob_path = config.get('autogen', 'relative_auto_prob_path')

    write_logs_to_db = config.getboolean('logging', 'write_logs_to_db')
    if write_logs_to_db:
        print("Enabling 'write logs to database'")
        annotations.write_logs_to_db = write_logs_to_db