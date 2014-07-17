"""
Caching Library for picoCTF API
"""

from functools import wraps
from bson import json_util

import api
import memcache

memcache_host = "127.0.0.1"
memcache_port = 11211

cache = memcache.Client(["{}:{}".format(memcache_host, memcache_port)])

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

    return "{}.{}${}${}".format(f.__module__, f.__name__, str(args), str(kwargs))

def memoize(f, timeout=0):
    """
    Cache a function based on its arguments.

    Args:
        timout: Time the result stays valid in the cache.
    Returns:
        The functions result.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        """
        Function cache
        """

        key = get_key(f, *args, **kwargs)

        cached_result = cache.get(key)
        function_result = None

        if cached_result is None:
            function_result = f(*args, **kwargs)

            serialized_result = json_util.dumps(function_result)
            cache.set(key, serialized_result, timeout)
        else:
            function_result = json_util.loads(cached_result)

        return function_result

    return wrapper
