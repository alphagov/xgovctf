def grade(autogen, key):
    n = autogen.instance
    if "flag_{}_start_with_user_needs".format(n) == key.lower().strip():
        return True, "Correct!"
    else:
        return False, "Try Again."
