"""
Problem Testing Module
"""

import pytest

import api.user
import api.team
import api.common
import api.problem

from api.common import APIException
from common import clear_collections, ensure_empty_collections

class TestProblems(object):
    """
    API Tests for problem.py
    """
    
    test_user = {
        "username": "valid",
        "password": "valid",
        "email": "test@hs.edu",
        "create-new-team": "on",

        "team-name-new": "test",
        "team-adv-name-new": "test",
        "team-adv-email-new": "hacks@hs.edu",
        "team-school-new": "Hacks HS",
        "team-password-new": "leet_hax"
    }

    problems = [
        {
            "disabled": False,
            "autogen" : False,
            "basescore" : 20,
            "desc" : "a",
            "displayname" : "Failure to Boot",
            "grader" : "test.py",
            "hint" : "It might be helpful to Google™ the error.",
            "relatedproblems" : ["a"],
            "tags" : ["a"],
            "threshold" : 0,
            "weightmap" : {"a":"a"},
            "category": ""
        }
    ]

    # backdoor key
    backdoor = "test"

    @ensure_empty_collections("problems", "teams", "users")
    def setup_class(self):
        """
        Class setup code
        """

        # initialization code
        self.uid = api.user.register_user(self.test_user)
        self.tid = api.user.get_team(uid=self.uid)['tid']

        # insert all problems
        self.pids = []
        for problem in self.problems:
            pid = api.problem.insert_problem(problem)
            self.pids.append(pid)

    @clear_collections("problems", "teams", "users")
    def teardown_class(self):
        """
        Class teardown code
        """
        pass

    def test_insert_problems(self):
        """
        Tests problem insertion.

        Covers:
            problem.insert_problem
            problem.get_problem
            problem.get_all_problems
        """

        # try to insert the problems again
        for problem in self.problems:
            with pytest.raises(APIException):
                api.problem.insert_problem(problem)
                assert False, "Was able to insert problem twice."


        # verify pids are correct
        db_problems = api.problem.get_all_problems()
        p = self.pids
        assert len(self.problems) == len(db_problems), "Not all problems were inserted"
        assert all([p['pid'] in self.pids for p in db_problems]), "pids do not match"

    def test_submissions(self):
        """
        Tests key submissions.

        Covers:
            problem.submit_key
            problem.get_submissions
            problem.get_team_submissions
        """

        pass

    def test_solve_problems(self):
        """
        Tests key submissions.

        Covers:
            problem.submit_key
            problem.get_solved_problems
        """

        for pid in self.pids:
            api.problem.submit_key(self.tid, pid, self.backdoor, uid=self.uid)

            solved = api.problem.get_solved_problems(self.tid)
            assert api.problem.get_problem(pid=pid) in solved
