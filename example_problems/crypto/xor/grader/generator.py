from os import path
from hashlib import sha1


def xor(key, src):
    return "".join([chr(key ^ ord(b)) for b in src])


def gen_code(n, key):
    flag = "flag_{}_574rbuck5_c0ffee".format(n)
    return xor(key, flag)



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
        {"flag": gen_code(n, 10)},
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
            "description": "Here is an encrypted file %s? Decrypt it to get the code" % code_link
        }
    }
