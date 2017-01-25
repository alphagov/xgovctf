def grade(arg, key):
    if "flag_why_have_1_db_when_you_can_have_2" in key:
        return True, "Correct"
    else:
        return False, "Incorrect"
