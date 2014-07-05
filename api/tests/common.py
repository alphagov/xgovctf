import pytest
import api.common

from functools import wraps

def clear_collections(*collections):
    """
    Clears collections listed after function has completed.
    """
    def clear(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
            except Exception:
                raise
            finally:
                db = api.common.get_conn()
                for collection in collections:
                    db[collection].remove()
                    assert len(list(db[collection].find())) == 0, "Unable to clear collection: " + collection

            return result
        return wrapper
    return clear
