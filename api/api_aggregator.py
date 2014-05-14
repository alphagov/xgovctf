#!/usr/bin/env python
from datetime import datetime
import time
import logging

import scoreboard
from api import common


end = datetime(2020, 5, 7, 3, 59, 59)


def load_group_scoreboards():
    db = common.get_conn()
    for group in list(db.groups.find()):
        scoreboard.load_group_scoreboard(group)

LOG_FILENAME = 'agg_output.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.debug("\nAGGREGATOR START")
while True:
    load_group_scoreboards()
    time.sleep(30)
