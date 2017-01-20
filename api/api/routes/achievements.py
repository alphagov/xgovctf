from flask import Blueprint
import api

from api.common import WebSuccess, WebError
from api.annotations import api_wrapper, require_login
from api.annotations import block_before_competition, block_after_competition
from api.annotations import log_action

blueprint = Blueprint("achievements_api", __name__)

@blueprint.route('', methods=['GET'])
@require_login
@api_wrapper
def get_achievements_hook():
    tid = api.user.get_team()["tid"]
    achievements = api.achievement.get_earned_achievements_display(tid=tid)

    for achievement in achievements:
        achievement["timestamp"] = None  # JB : Hack to temporarily fix achievements timestamp problem

    return WebSuccess(data=achievements)

@blueprint.route('/all', methods=['GET'])
@api_wrapper
def get_all_achievements_hook():
    achievements = api.achievement.get_all_achievements()

    for achievement in achievements:
        achievement["timestamp"] = None  # JB : Hack to temporarily fix achievements timestamp problem

    return WebSuccess(data=achievements)

@blueprint.route('/earned', methods=['GET'])
@api_wrapper
def get_all_players_achievements_hook():
    achievements = api.achievement.get_earned_achievement_instances()

    for instance_achievement in achievements:
        achievement = api.achievement.get_achievement(aid=instance_achievement["aid"])
        team = api.team.get_team(tid=instance_achievement["tid"])

        #Make sure not to override name or description.
        achievement.pop("name")
        achievement.pop("description")
        instance_achievement["team"] = team["team_name"]

        instance_achievement.update(achievement)
        instance_achievement.pop("data", None)


    return WebSuccess(data=achievements)
