def grade(autogen, key):
    n = autogen.instance
    if "flag_iterate_then_iterate_again" == key.lower().strip():
        return True, "Correct!"
    else:
        return False, "Try Again."
