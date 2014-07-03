"""
Testing Module
"""

import pytest

@pytest.mark.usefixtures("db")
class TestUsers(object):
    """
    API Tests for User.py
    """

    def test_what(self, db):
        pass
