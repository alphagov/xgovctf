""" The common module contains general-purpose functions potentially used by multiple modules in the system."""
__author__ = ["Collin Petty", "Peter Chapman", "Jonathan Burket"]
__copyright__ = "Carnegie Mellon University"
__license__ = "MIT"
__maintainer__ = ["Collin Petty", "Peter Chapman", "Jonathan Burket"]
__email__ = ["collin@cmu.edu", "peter@cmu.edu", "jburket@cmu.edu"]
__status__ = "Production"

from pymongo import MongoClient
from werkzeug.contrib.cache import SimpleCache
import uuid

allowed_protocols = []
allowed_ports = []

cache = SimpleCache()
admin_emails = None

__connection = None

mongo_addr = "127.0.0.1"
mongo_port = 27017
mongo_db_name = ""


def get_conn():
    """Get a database connection

    Ensures that only one global database connection exists per thread.
    If the connection does not exist a new one is created and returned.
    """
    global __connection
    if not __connection:
        __connection = MongoClient(mongo_addr, mongo_port)[mongo_db_name]
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


class ValidationException(Exception):
    def __init__(self, value):
        self.value = value


def validate(string_input, field_name, min_length=None, max_length=None, is_int=None):
    if string_input is None and min_length > 0:
        raise ValidationException("{0} cannot be blank".format(field_name))
    if min_length is not None:
        if len(string_input) < min_length:
            if len(string_input) == 0:
                raise ValidationException("{0} cannot be blank".format(field_name))
            else:
                raise ValidationException("{0} must me at lease {1} characters".format(field_name, min_length))
    if max_length is not None:
        if len(string_input) > max_length:
            raise ValidationException("{0} cannot exceed {1} characters".format(field_name, max_length))
    if is_int is not None:
        try:
            int(string_input)
        except ValueError:
            raise ValidationException("{0} must be an integer".format(field_name))

    return string_input