from os import path
import base64


def key_extend(key, l):
    while len(key) < l:
        key += key
    return key


def xor(key, src):
    return "".join([chr(ord(k) ^ ord(b)) for k, b in zip(key_extend(key, len(src)), src)])


def gen_code(n, key):
    flag = "flag_{}_Make_things_open:_it_makes_things_better".format(n)
    return base64.b64encode(xor(key, flag).encode("ascii")).decode()


def generate(random, pid, autogen_tools, n):
    """
    Generate an instance of the problem
    Needs to return a list of files to copy to particular instance.
    """

    generator_path = autogen_tools.get_directory(__file__)

    template_path = path.join(generator_path, "code.txt.template")
    rendered_template_path = path.join(generator_path, "code.txt")

    autogen_tools.replace_source_tokens(
        template_path,
        {"flag": gen_code(n, "GDS")},
        rendered_template_path
    )

    code_link = autogen_tools.generate_resource_link(pid, "code.txt", title="Encrypted file")

    return {
        "resource_files": {
            "public": [
                (rendered_template_path, "code.txt"),
            ],
        },
        "static_files": {
        },
        "problem_updates": {
            "description": "<p>Apparently using XOR with a single character is not sufficient prevent the most advanced attackers</p><p>The team wanted to ensure the key was at least 8 characters and included symbols, uppercase, lowercase and digits, but some NCSC guidance said we didn't need those rules, so we picked a memorable password instead</p><p>The team have stored the password in %s. Bet you can't get into it</p>" % code_link
        }
    }
