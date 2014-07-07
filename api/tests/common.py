import pytest
import api.common

from functools import wraps

def clear_collections(*collections):
    """
    Clears collections listed after function has completed.
    Will throw an assertion if any collection is not empty when called.
    """
    def clear(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            db = api.common.get_conn()
            collection_size = lambda name: len(list(db[name].find()))
            for collection in collections:
                assert collection_size(collection) == 0, "Collection was not empty: " + collection
            try:
                result = f(*args, **kwargs)
            except Exception:
                raise
            finally:
                #Clear the collections.
                for collection in collections:
                    db[collection].remove()
            return result
        return wrapper
    return clear
