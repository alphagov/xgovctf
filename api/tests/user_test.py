"""
User Testing Module
"""

import pytest
import bcrypt

import api.user
import api.common
import api.team

from api.common import APIException
from common import clear_collections

@pytest.mark.usefixtures("db")
class TestUsers(object):
    """
    API Tests for user.py
    """

    new_team_user = {
        "username": "valid",
        "pass": "valid",
        "email": "valid@hs.edu",
        "create-new-team": "true",

        "team-name-new": "Valid Hacks",
        "team-adv-name-new": "Dr. Hacks",
        "team-adv-email-new": "hacks@hs.edu",
        "team-school-new": "Hacks HS",
        "team-pass-new": "leet_hax"
    }

    existing_team_user = {
        "username": "valid",
        "pass": "valid",
        "email": "valid@hs.edu",
        "create-new-team": "false",

        "team-pass-existing": "leet_hax",
        "team-name-existing": "massive_hacks"
    }

    #TB: This is sort of also testing team.py. Is there a better way to seperate these?
    base_team = {
        "team_name" : "massive_hacks",
        "adviser_name": "Dr. Hacks",
        "adviser_email": "hacks@hs.edu",
        "school": "Hacks HS",
        "password": "leet_hax"
    }

    @clear_collections("users", "teams")
    def test_create_batch_users(self, users=10):
        """
        Tests user creation.

        Covers:
            user.create_user
            user.get_all_users
            user.get_user
        """

        tid = api.team.create_team(self.base_team.copy())

        uids = []
        for i in range(users):
            name = "fred" + str(i)
            uids.append(api.user.create_user(
                name, name + "@gmail.com", name, tid
            ))

        assert len(set(uids)) == len(uids), "UIDs are not unique."

        assert len(api.user.get_all_users()) == users and \
            users == len(uids), "Not all users were created."

        for i, uid in enumerate(uids):
            name = "fred" + str(i)

            user_from_uid = api.user.get_user(uid=uid)
            user_from_name = api.user.get_user(name=name)

            assert user_from_uid == user_from_name, "User lookup from uid and name are not the same."

    @clear_collections("users", "teams")
    def test_register_user_email_validation(self):
        """
        Tests the email validation during user registration.
        
        Covers:
            partially: user.register_user
        """

        team = self.base_team.copy()    
        api.team.create_team(team)

        invalid_email_user = self.existing_team_user.copy()
        invalid_email_user["email"] = "not_an_email"

        with pytest.raises(APIException):
            api.user.register_user(invalid_email_user)
            assert False, "Was able to register a user with something that doesn't look like an email."

        invalid_email_user["email"] = "hax$@test.c"

        with pytest.raises(APIException):
            api.user.register_user(invalid_email_user)
            assert False, "Was able to register a user with invalid characters"

        valid_email_user = self.existing_team_user.copy()
        assert api.user.register_user(valid_email_user), "Was not able to register a valid email."

    @clear_collections("users", "teams")
    def test_get_tid_from_uid(self):
        """
        Tests retrieving the tid from a given uid.
        """

        team = self.base_team.copy()
        tid = api.team.create_team(team)

        uid = api.user.register_user(self.existing_team_user.copy())
        assert tid == api.user.get_tid_from_uid(uid), "Unable to pair uid and tid."

    @clear_collections("users", "teams")
    def test_register_user_general_validation(self):
        """
        Tests the registration form validation functionality.

        Covers:
            partially: user.register_user
        """

        #Generally invalidate every length requirement
        for bad_length_mod in [0, 200]:
            for user_blueprint in [self.new_team_user, self.existing_team_user]:
                for key in user_blueprint.keys():
                    sheep_user = user_blueprint.copy()

                    #Make sure to keep the basic properties

                    if key == "create-new-team":
                        continue
                    elif key == "email":
                        sheep_user[key] = "x@x." + "x" * bad_length_mod
                    else:
                        sheep_user[key] = "A" * bad_length_mod

                    if sheep_user["create-new-team"] != "true" and \
                    api.team.get_team(name=sheep_user["team-name-existing"]) is None:
                        team = self.base_team.copy()
                        team['team_name'] , team['password'] = \
                                sheep_user["team-name-existing"], sheep_user["team-pass-existing"]
                        api.team.create_team(team)

                    with pytest.raises(APIException):
                        api.user.register_user(sheep_user)
                        assert False, "Validation failed to catch {} length {}".format(bad_length_mod, key)

    @clear_collections("users", "teams")
    def test_register_user_new_team(self):
        """
        Tests the registration of users creating new teams.

        Covers:
            partially: user.register_user
            team.get_team_uids
        """

        uid = api.user.register_user(self.new_team_user)
        assert uid == api.user.get_user(name="valid")["uid"], "Good user created unsuccessfully."

        team = api.team.get_team(name=self.new_team_user["team-name-new"])
        assert team, "Team was not created."

        team_uids = api.team.get_team_uids(team["tid"])
        assert uid in team_uids, "User was not successfully placed into the new team."

        sheep_user = self.new_team_user.copy()
        sheep_user["username"] = "something_different"

        with pytest.raises(APIException):
            api.user.register_user(sheep_user)
            assert False, "Was able to create a new team... twice"

        sheep_user = self.new_team_user.copy()
        sheep_user["team-name-new"] = "noneixstent_team"

        with pytest.raises(APIException):
            api.user.register_user(sheep_user)
            assert False, "Was able to create two users with the same username."

    @clear_collections("users", "teams")
    def test_register_user_existing_team(self):
        """
        Tests the registration of users on existing teams.

        Covers:
            partially: user.register_user
            team.get_team_uids
            team.create_team
        """

        tid = api.team.create_team(self.base_team.copy())
        assert tid, "Team was not created."

        uid = api.user.register_user(self.existing_team_user.copy())
        assert uid == api.user.get_user(name="valid")["uid"], "Good user created unsuccessfully."

        with pytest.raises(APIException):
            api.user.register_user(self.existing_team_user.copy())
            assert False, "Was able to register and join the team twice."

        with pytest.raises(APIException):
            invalid_team_user = self.existing_team_user.copy()
            invalid_team_user["team-name-existing"] = "Totally Invalid"
            api.user.register_user(invalid_team_user)
            assert False, "Was able to join a team that doesn't exist."

        with pytest.raises(APIException):
            invalid_team_user = self.existing_team_user.copy()
            invalid_team_user["team-pass-existing"] = "Not correct"
            api.user.register_user(invalid_team_user)
            assert False, "Was able to join a team with an invalid password."

        team_uids = api.team.get_team_uids(tid)

        assert uid in team_uids, "User was not successfully placed into the existing team."
        assert len(team_uids) == 1, "Invalid teams were created though the tests passed."

    @clear_collections("users", "teams")
    def test_change_pw_user(self):
        """
        Tests password change functionality.

        Covers:
            user.update_password
            user.hash_password
        """

        tid = api.team.create_team(self.base_team.copy())
        uid = api.user.create_user("fred", "fred@gmail.com", "HASH", tid)

        old_hash = api.user.get_user(uid=uid)["pwhash"]
        assert old_hash == "HASH", "Was unable to confirm password was stored correctly."

        api.user.update_password(uid, "HACK")

        new_hash = api.user.get_user(uid=uid)["pwhash"]

        assert bcrypt.hashpw("HACK", new_hash) == new_hash, \
            "Password does not match hashed plaintext after changing it."

        with pytest.raises(APIException):
            api.user.update_password(uid, "")
            assert False, "Should not be able to update password to nothing."

