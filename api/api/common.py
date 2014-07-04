""" The common module contains general-purpose functions potentially used by multiple modules in the system."""
__author__ = ["Collin Petty", "Peter Chapman", "Jonathan Burket"]
__copyright__ = "Carnegie Mellon University"
__license__ = "MIT"
__maintainer__ = ["Collin Petty", "Peter Chapman", "Jonathan Burket"]
__email__ = ["collin@cmu.edu", "peter@cmu.edu", "jburket@cmu.edu"]
__status__ = "Production"

from pymongo import MongoClient
from werkzeug.contrib.cache import SimpleCache
from voluptuous import Invalid
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


class APIException(Exception):
    """
    Exception thrown by the API.
    It should always be raised with a three tuple
    """
    #TODO: Find correct way to validate tuple property.
    pass

def flat_multi(multidict):
    """
    Flattens any single element lists in a multidict.
    
    Args:
        multidict: multidict to be flattened.
    Returns:
        Partially flattened database.
    """
    flat = {}
    for key, values in multidict.items():
        flat[key] = values[0] if type(values) == list and len(values) == 1 \
                    else values
    return flat

def check(*callback_tuples):
    """
    Voluptuous wrapper function to raise our APIException

    Args:
        callback_tuples: a callback_tuple should contain (status, msg, callbacks)
    Returns:
        Returns a function callback for the Schema
    """
    def validate(value):
        """
        Trys to validate the value with the given callbacks.

        Args:
            value: the item to validate
        Raises:
            APIException with the given error code and msg.
        Returns:
            The value if the validation callbacks are satisfied.
        """
        for status, msg, callbacks in callback_tuples:
            for callback in callbacks:
                try:
                    if not callback(value):
                        raise Invalid()
                except Exception:
                    raise APIException(status, None, msg)
        return value
    return validate

