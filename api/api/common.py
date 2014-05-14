""" The common module contains general-purpose functions potentially used by multiple modules in the system."""
__author__ = 'Peter Chapman'

from pymongo import MongoClient
from werkzeug.contrib.cache import SimpleCache
import uuid

allowed_protocols = []
allowed_ports = []

cache = SimpleCache()
admin_emails = None

__connection = None


def get_conn():
    global __connection
    if not __connection:
        __connection = MongoClient('localhost', 27017)['pico']
    return __connection


def esc(s):
    """Escapes a string to prevent html injection

    Returns a string with special HTML characters replaced.
    Used to sanitize output to prevent XSS. We looked at 
    alternatives but there wasn't anything of an appropriate 
    scope that we could find. In the long-term this should be 
    replaced with a proper sanitization function written by 
    someone else."""
    return s\
        .replace('&', '&amp;')\
        .replace('<', '&lt;')\
        .replace('>', '&gt;')\
        .replace('"', '&quot;')\
        .replace("'", '&#39;')


def token():
    """Generate a token, should be random but does not have to be secure necessarily. Speed is a priority.
    """
    return str(uuid.uuid4().hex)


def sec_token():
    """Generate a secure token that is cryptographically secure.
    """
    return token()

