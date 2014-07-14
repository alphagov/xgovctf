"""
Group Testing Module
"""

import pytest
import api.user
import api.team
import api.common
import bcrypt

from api.common import APIException
from common import clear_collections, ensure_empty_collections
from conftest import setup_db, teardown_db

class TestGroups(object):
    """
    API Tests for group.py
    """

    base_teams = [
        {
            "team_name": "team" + str(i),
            "adviser_name": "Dr. Test",
            "adviser_email": "test@hs.edu",
            "school": "Test HS",
            "password": "much_protected"
        }
        for i in range(5)
    ]

    base_group = {
        "group-name": "group",
    }

    def setup_class(self):
        setup_db()

        # create teams
        self.owner_tid = api.team.create_team(self.base_teams[0])
        for team in self.base_teams[1:]:
            api.team.create_team(team)

    def teardown_class(self):
        teardown_db()

    @ensure_empty_collections("groups")
    @clear_collections("groups")
    def test_create_batch_groups(self, groups=10):
        gids = []
        for i in range(groups):
            group = self.base_group.copy()
            group["group-name"] += str(i)
            gids.append(api.group.create_group_request(group, tid=self.owner_tid))

        assert len(set(gids)) == len(gids), "gids are not unique."

        assert len(api.team.get_groups(tid=self.owner_tid)) == len(gids), "Not all groups were created."

        for i, gid in enumerate(gids):
            name = self.base_group['group-name'] + str(i)

            group_from_gid = api.group.get_group(gid=gid)
            group_from_name = api.group.get_group(name=name)

            assert group_from_gid == group_from_name, "Group lookup from gid and name are not the same."
