
"""
Team Testing Module
"""

import pytest
import api.user
import api.common
import bcrypt

from api.common import APIException
from common import clear_collections

@pytest.mark.usefixtures("db")
class TestTeams(object):
    """
    API Tests for team.py
    """

    base_team = {
        "team_name": "team",
        "adviser_name": "Dr. Test",
        "adviser_email": "test@hs.edu",
        "school": "Test HS",
        "password": "much_protected"
    }
    
    @clear_collections("teams")
    def test_create_batch_teams(self, teams=10):
        """
        Tests team creation.
        
        Covers:
            team.create_team
            team.get_team
            team.get_all_teams
        """
        tids = []
        for i in range(teams):
            team = self.base_team.copy()
            team["team_name"] += str(i)
            tids.append(api.team.create_team(team))

        assert len(set(tids)) == len(tids), "tids are not unique."

        assert len(api.team.get_all_teams()) == len(tids), "Not all teams were created."

        for i, tid in enumerate(tids):
            name = "team" + str(i)

            team_from_tid = api.team.get_team(tid=tid)
            team_from_name = api.team.get_team(name=name)

            assert team_from_tid == team_from_name, "team lookup from tid and name are not the same."


