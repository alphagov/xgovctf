__author__ = ['Peter Chapman', 'Collin Petty']

from api.common import APIException
import api.common
import api.auth
import api.logger

import json
from datetime import datetime
from functools import wraps
from flask import session, request, abort

write_logs_to_db = False # Default value, can be overwritten by api.py

log = api.logger.use("api.wrapper")

def return_json(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        try:
            ret = f(*args, **kwds)

            #TODO: clean this up
            status = ret[0]
            data = ret[1]
            msg = ret[2] if len(ret) > 2 else ""

            data_dict = {'status': status, 'data': data, 'message': msg}
            return json.dumps(data_dict)
        except APIException as error:

            error_dict = dict(zip(['status', 'data', 'message'], error.args))
            log.warning("EXCEPTION %s: %s", error_dict["status"], error_dict["message"])

            return json.dumps(error_dict)
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


def log_request(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        name = f.__name__
        path = request.path
        request_form = json.dumps(request.form)
        request_args = json.dumps(request.args)
        tid = session.get('tid', '')
        session_id = session.get('session_id', '')
        ip = request.headers.get('X-Real-IP', '')
        time = str(datetime.now())
        ret = f(*args, **kwds)
        db = api.common.get_conn()
        if write_logs_to_db:
            db.logs.insert({'name': name,
                            'path': path,
                            'request_form': request_form,
                            'request_args': request_args,
                            'tid': tid,
                            'session_id': session_id,
                            'ip': ip,
                            'time': time})  # ,
                            # 'ret': str(ret)})
        return ret
    return wrapper
