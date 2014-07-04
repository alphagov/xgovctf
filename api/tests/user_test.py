"""
Testing Module
"""

import pytest
import api.user
import api.common
import bcrypt

from api.common import APIException
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
                name, name + "@gmail.com", name
            ))

        assert len(set(uids)) == len(uids), "UIDs are not unique."

        assert len(api.user.get_all_users()) == users and \
            users == len(uids), "Not all users were created."

        for i, uid in enumerate(uids):
            name = "fred" + str(i)

            user_from_uid = api.user.get_user(uid=uid)
            user_from_name = api.user.get_user(name=name)

            assert user_from_uid == user_from_name, "User lookup from uid and name are not the same."

    #TODO: Team should be tested first
    @clear_collections("user", "team")
    def test_register_user(self, db):
        """
        Tests the registration and form validation functionality.
        """
        pass

    @clear_collections("user")
    def test_change_pw_user(self):
        """
        Tests password change functionality.

        Covers:
            user.update_password
            user.hash_password
        Depends:
            user.get_user
        """
        uid = api.user.create_user("fred", "fred@gmail.com", "HASH")

        old_hash = api.user.get_user(uid=uid)["pwhash"]
        assert old_hash == "HASH", "Was unable to confirm password was stored correctly."

        api.user.update_password(uid, "HACK")

        new_hash = api.user.get_user(uid=uid)["pwhash"]

        assert bcrypt.hashpw("HACK", new_hash) == new_hash, \
            "Password does not match hashed plaintext after changing it."

        with pytest.raises(APIException):
            api.user.update_password(uid, "")
            assert False, "Should not be able to update password to nothing."



