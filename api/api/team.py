__author__ = 'collinpetty'

from api.annotations import *
from api import common, user


def get_team(tid):
    db = common.get_conn()
    return db.teams.find_one({'tid': tid})