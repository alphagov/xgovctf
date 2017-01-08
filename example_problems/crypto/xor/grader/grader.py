from hashlib import sha1


def xor(key, src):
    return "".join([chr(key ^ ord(b)) for b in src])


def gen_code(n, key):
    secret_key = "secret_key"
    flag = "flag_"+str(sha1(secret_key.encode('utf-8')).hexdigest())
    return xor(key, flag)


def grade(autogen, key):
    n = autogen.instance
    if xor(10, gen_code(n, 10)) == key.lower().strip():
        return True, "Correct!"
    else:
        return False, "Try Again."
