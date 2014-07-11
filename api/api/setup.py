import logging
import configparser

import api.annotations
import api.common
import api.utilities
import api.problem

def load_config(app):
    app.logger.setLevel(logging.INFO)
    app.logger.info("Parsing the configuration file")

    config = configparser.ConfigParser()
    config.read('mister.config')

    if config.get('debug', 'admin_emails') is not None:
        api.common.admin_emails = list()
        
    for email in config.get('debug', 'admin_emails').split(','):
        app.logger.info(" Adding '%s' to admin_emails" % email)
        api.common.admin_emails.append(email.strip())

    app.config['DEBUG'] = False

    secret_key = config.get('flask', 'secret_key')
    if secret_key == '':
        app.logger.error('The Flask secret key specified in the config file is empty.')
        exit()
    app.secret_key = secret_key

    app.config['SESSION_COOKIE_HTTPONLY'] = False
    app.config['SESSION_COOKIE_DOMAIN'] = config.get('flask', 'SESSION_COOKIE_DOMAIN')
    app.config['SESSION_COOKIE_PATH'] = config.get('flask', 'SESSION_COOKIE_PATH')
    app.config['SESSION_COOKIE_NAME'] = config.get('flask', 'SESSION_COOKIE_NAME')

    api.common.session_cookie_domain = config.get('flask', 'SESSION_COOKIE_DOMAIN')

    mongo_addr = config.get("mongodb", "addr")
    if mongo_addr is not None:
        print("Setting mongo address to '%s'" % mongo_addr)
        api.common.mongo_addr = mongo_addr

    mongo_port = config.getint("mongodb", "port")
    if mongo_port is not None:
        print("Setting mongo port to '%d'" % mongo_port)
        api.common.mongo_port = mongo_port

    mongo_db_name = config.get("mongodb", "db_name")
    if mongo_db_name is not None:
        print("Setting mongo db_name to '%s'" %mongo_db_name)
        api.common.mongo_db_name = mongo_db_name

    for protocol in config.get('security','allowed_protocols').split(','):
        api.common.allowed_protocols.append(protocol.strip())

    for port in config.get('security','allowed_ports').split(','):
        api.common.allowed_ports.append(port.strip())

    api.team.max_team_users = int(config.get('teams', 'max_team_users'))

    enable_email = config.getboolean('email', 'enable_email')
    if enable_email:
        api.utilities.enable_email = enable_email

    smtp_url = config.get('email', 'smtp_url')
    api.utilities.smtp_url = smtp_url

    email_username = config.get('email', 'username')
    api.utilities.email_username = email_username

    email_password = config.get('email', 'password')
    api.utilities.email_password = email_password

    from_addr = config.get('email', 'from_addr')
    api.utilities.from_addr = from_addr

    from_name = config.get('email', 'from_name')
    api.utilities.from_name = from_name

    api.problem.root_web_path = config.get('autogen', 'root_web_path')
    api.problem.relative_auto_prob_path = config.get('autogen', 'relative_auto_prob_path')

    write_logs_to_db = config.getboolean('logging', 'write_logs_to_db')
    if write_logs_to_db:
        print("Enabling 'write logs to database'")
        api.annotations.write_logs_to_db = write_logs_to_db


def check_database_indexes():
    db = api.common.get_conn()

    print("##### Ensuring indexes ######")

    print(" 'users' collection...")
    print("  'uid' unique")
    db.users.ensure_index("uid", unique=True, name="unique uid")
    print("  'username' unique")
    db.users.ensure_index("username", unique=True, name="unique username")

    print(" 'problems' collection...")
    print("  'pid' unique")
    db.problems.ensure_index("pid", unique=True, name="unique pid")
