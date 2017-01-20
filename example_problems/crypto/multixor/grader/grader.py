def grade(autogen, key):
    n = autogen.instance
    if "flag_{}_make_things_open:_it_makes_things_better".format(n) == key.lower().strip():
        return True, "Correct!"
    else:
        return False, "Try Again."
