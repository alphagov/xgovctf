__author__ = ['Peter Chapman', 'Collin Petty']

from api.common import WebSuccess, WebError, WebException, InternalException, SevereInternalException
import api.common
import api.auth
import api.logger

import json
from datetime import datetime
from functools import wraps
from flask import session, request, abort

write_logs_to_db = False # Default value, can be overwritten by api.py

log = api.logger.use("api.wrapper")

def api_wrapper(f):
    """
    Wraps api routing and handles potential exceptions
    """

    get_message = lambda exception: exception.args[0]
    @wraps(f)
    def wrapper(*args, **kwds):
        web_result = {}
        try:
            web_result = f(*args, **kwds)
        except WebException as error:
            web_result = WebError(get_message(error))
        except InternalException as error:
            message = get_message(error)
            if type(error) == SevereInternalException:
                log.critical(message)
            else:
                log.error(message)
            web_result = WebError(message)
        except Exception as error:
            log.error(get_message(error))

        return json.dumps(web_result)

    return wrapper


def require_login(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if not api.auth.is_logged_in():
            abort(403)

        #if not auth.csrf_check(request.headers):
        #   abort(403)
        return f(*args, **kwds)
    return wrapper


def check_csrf(f):
    @wraps(f)
    @require_login
    def wrapper(*args, **kwds):
        if 'token' not in session:
            abort(403)
        if 'token' not in request.form:
            abort(403)
        if session['token'] != request.form['token']:
            abort(403)
        return f(*args, **kwds)
    return wrapper


def deny_blacklisted(f):
    @wraps(f)
    @require_login
    def wrapper(*args, **kwds):
        #if auth.is_blacklisted(session['tid']):
         #   abort(403)
        return f(*args, **kwds)
    return wrapper


def require_admin(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if not session.get('admin', False):
            abort(403)
        return f(*args, **kwds)
    return wrapper
