__author__ = 'Jonathan Burket'

from api.annotations import *
import api.problem
import api.user
import api.common
from api.app import app


def get_category_statistics():
    db = api.common.get_conn()
    category_scores = {}
    for p in db.problems.find():
        if p['category'] in category_scores:
            category_scores[p['category']]['total'] += 1
        else:
            category_scores[p['category']] = {'solved': 0, 'total': 1}

    for p in api.problem.get_solved_problems():
        category_scores[p['category']]['solved'] += 1

    return 1, category_scores


pid_map = {}

# Level 1
pid_map["512a8622b393a33f2cf9b37f"] = 1  # Failure to Boot
pid_map["5161be6f2f0686520c000002"] = 2  # Try Them All!
pid_map["5161c04a2f0686520c000003"] = 3  # Read the Manual
pid_map["5161cca02f0686520c000004"] = 4  # Grep is Your Friend
pid_map["5161d2a92f0686520c000005"] = 5  # Spaceport Map
pid_map["5161d7582f0686520c000006"] = 6  # Bitwise
pid_map["5161de472f0686520c000008"] = 7  # Byte Code

# Level 2
pid_map["5161e2402f0686520c000009"] = 8  # Pilot Logic
pid_map["5161e3b62f0686520c00000a"] = 9  # CFG to C
pid_map["5161e8102f0686520c00000b"] = 10  # XMLOL
pid_map["5161eae22f0686520c00000d"] = 11  # GETKey
pid_map["516ad9162f0686520c000014"] = 12  # Robomunication
pid_map["5161fa8a2f0686520c00000e"] = 13  # First Contact
pid_map["5161fea72f0686520c00000f"] = 14  # Technician Challenge
pid_map["516a186c2f0686520c000010"] = 15  # Yummy

# Level 3a
pid_map["516ad71b2f0686520c000012"] = 16  # In Hex, No One Can Hear You Complain
pid_map["516adba52f0686520c000015"] = 17  # Spamcarver
pid_map["516ae36c2f0686520c000017"] = 18  # Core Decryption

# Level 3b
pid_map["516ae8982f0686520c000019"] = 19  # Chromatophoria
pid_map["516af3b22f0686520c00001a"] = 20  # Second Contact
pid_map["516b1e8f2f0686520c00001d"] = 21  # NAVSAT
pid_map["516b2dc22f0686520c00001e"] = 22  # Dark Star
pid_map["51741fb4054c91c14b000001"] = 23  # Trivial
pid_map["5174230c054c91c14b000002"] = 24  # Classic
pid_map["5174275e054c91c14b000003"] = 25  # Harder Serial
pid_map["517429d9054c91c14b000004"] = 26  # Python Eval 1

# Level 4
pid_map["51743245054c91c14b000005"] = 27  # Python Eval 2
pid_map["51743313054c91c14b000006"] = 28  # Python Eval 3
pid_map["5174332a054c91c14b000007"] = 29  # Python Eval 4
pid_map["51743341054c91c14b000008"] = 30  # Python Eval 5
pid_map["51744070054c91c14b00000a"] = 31  # avaJ
pid_map["51744969054c91c14b00000c"] = 32  # Pretty Hard Programming
pid_map["51744c0e054c91c14b00000d"] = 33  # Evergreen
pid_map["51745431054c91c14b00000f"] = 34  # RSA
pid_map["517464b7054c91c14b000010"] = 35  # Format 1
pid_map["51759fef56dce84c7d000001"] = 36  # Format 2
pid_map["5175a37e56dce84c7d000002"] = 37  # ROP 1
pid_map["5175a39356dce84c7d000003"] = 38  # ROP 2
pid_map["5175a3b056dce84c7d000004"] = 39  # ROP 3
pid_map["5175a3d156dce84c7d000005"] = 40  # ROP 4
pid_map["5175a89b56dce84c7d000006"] = 41  # Overflow 1
pid_map["5175a8b256dce84c7d000007"] = 42  # Overflow 2
pid_map["5175a8c856dce84c7d000008"] = 43  # Overflow 3
pid_map["5175a8de56dce84c7d000009"] = 44  # Overflow 4
pid_map["5175a8f356dce84c7d00000a"] = 45  # Overflow 5
pid_map["5176cb706c342fba03000001"] = 46  # Black Hole
pid_map["517712636c342fba03000002"] = 47  # Broken CBC
pid_map["51784b1e6c342fba03000004"] = 48  # Injection
pid_map["5177398c6c342fba03000003"] = 49  # Mildly Evil
pid_map["51788a1b6c342fba03000005"] = 50  # Client-Side is the Best Side
pid_map["51788c396c342fba03000006"] = 51  # DDoS Detection
pid_map["5179a797657debeb14000001"] = 52  # PHP2
pid_map["5179dcc0657debeb14000002"] = 53  # PHP3
pid_map["5179e4f1657debeb14000003"] = 54  # PHP4
pid_map["5179eb80657debeb14000004"] = 55  # moreevil
pid_map["5179ee76657debeb14000005"] = 56  # hotcoffee
pid_map["517b49f917f5e16305000001"] = 57  # Broken RSA

etcid_map = {v: k for k, v in pid_map.items()}

def get_solved_indices():
    solved_problems = api.problem.get_solved_problems()
    return 1, sorted([pid_map[p['pid']] for p in solved_problems])


def get_game_problem(etcid):
    useracct = api.user.get_user()
    try:
        pid = etcid_map[int(etcid)]
    except (IndexError, ValueError):
        return 0, None, "Invalid Problem"
    p = api.problem.get_single_problem(pid, useracct['tid'])
    if 'status' in p and p['status'] == 0:  # JB: This interface sucks. Needs a rewrite
        return 0, None, "Problem Not Unlocked"
    p['type'] = p['category']
    p['name'] = p['displayname']
    p['points'] = p['basescore']
    p['ans'] = 'batman'
    return 1, p


def etcid_to_pid(etcid):
    try:
        pid = etcid_map[int(etcid)]
        return 1, pid
    except (IndexError, ValueError):
        return 0, None, "Invalid Problem"


def get_state():
    useracct = api.user.get_user()
    return 1, {'level': useracct['level'],
               'avatar': useracct['avatar'],
               'eventid': useracct['eventid']}


def update_state(avatar, eventid, level):
    db = api.common.get_conn()
    useracct = api.user.get_user()
    try:
        avatar = int(validate(avatar, "Avatar Value", is_int=True))
        eventid = int(validate(eventid, "Event Id", is_int=True))
    except ValidationException as validation_failure:
        return 0, None, validation_failure.value
    db.users.update({'uid': useracct['uid']},
                    {'$set': {'avatar': avatar, 'eventid': eventid, 'level': level}})
    return 1, None, "Update Successful"

