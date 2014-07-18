"""
Caching Library for picoCTF API
"""

from functools import wraps
from bson import json_util

import api
from pymemcache.client import Client

from api.common import InternalException

log = api.logger.use(__name__)

memcache_host = "127.0.0.1"
memcache_port = 11211

def json_serializer(_, value):
    """
    Memcache json serializer
    """

    return (value, 1) if type(value) == str else (json_util.dumps(value), 2)

def json_deserializer(_, value, flag):
    """
    Memcache json deserializer
    """
    return value if flag == 1 else json_util.loads(value.decode("utf-8"))

cache = Client(
    (memcache_host, memcache_port),
    serializer=json_serializer,
    deserializer=json_deserializer
)


def get_key(f, *args, **kwargs):
    """
    Returns a unique key for a memoized function.

    Args:
        f: the function
        args: positional arguments
        kwargs: keyword arguments
    Returns:
        The key.
    """

    key = "{}.{}${}${}".format(f.__module__, f.__name__, str(args), str(kwargs)).replace(" ", "~")

    return key

def memoize(timeout=0):
    """
    Cache a function based on its arguments.

    Args:
        timout: Time the result stays valid in the cache.
    Returns:
        The functions result.
    """

    def decorator(f):
        """
        Inner decorator
        """

        @wraps(f)
        def wrapper(*args, **kwargs):
            """
            Function cache
            """

            key = get_key(f, *args, **kwargs)

            cached_result = cache.get(key)

            if cached_result is None:
                function_result = f(*args, **kwargs)

                cache.set(key, function_result, timeout)
                return function_result

            return cached_result

        return wrapper

    return decorator

def invalidate_memoization(f, *args, **kwargs):
    """
    Invalidate a memoized function.

    Args:
        f: the function
        You must pass all arguments given to the function to accurately invalidate it.
    """

    key = get_key(f, *args, **kwargs)
    cache.delete(key)

