"""
Testing Module
"""

import pytest
import api.user
import api.common

from common import clear_collections

@pytest.mark.usefixtures("db")
class TestUsers(object):
    """
    API Tests for User.py
    """
    @clear_collections("user")
    def test_create_batch_normal_users(self, users=100):
        """
        Tests user creation.

        Covers:
            user.create_user
            user.get_all_users
            user.get_user
        """

        uids = []
        for i in range(users):
            name = "fred" + str(i)
            uids.append(api.user.create_user(
                name, name + "@gmail.com", "HASH"
            ))

        assert len(set(uids)) == len(uids), "UIDs are not unique."

        assert len(api.user.get_all_users()) == users and \
            users == len(uids), "Not all users were created."

        for i, uid in enumerate(uids):
            name = "fred" + str(i)

            user_from_uid = api.user.get_user(uid=uid)
            user_from_name = api.user.get_user(name=name)

            assert user_from_uid == user_from_name, "User lookup from uid and name are not the same."

    def test_register_user(self, db):
        """
        Tests the registration and form validation functionality.
        """

        pass

