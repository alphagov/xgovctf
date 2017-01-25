def grade(autogen, key):
    n = autogen.instance
    if "flag_{}_iterate_then_iterate_again".format(n) == key.lower().strip():
        return True, "Correct!"
    else:
        return False, "Try Again."
