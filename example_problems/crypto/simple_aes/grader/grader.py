def grade(autogen, key):
    n = autogen.instance
    if "flag_{}_do_the_hard_work_to_make_it_simple".format(n) == key.lower().strip():
        return True, "Correct!"
    else:
        return False, "Try Again."
