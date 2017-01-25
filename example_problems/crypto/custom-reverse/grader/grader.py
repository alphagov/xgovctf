def grade(autogen, key):
    n = autogen.instance
    if "aefgbcdh" == key.lower().strip():
        return True, "Correct!"
    else:
        return False, "Try Again."
