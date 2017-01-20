from os import path
import Crypto.Cipher.AES
import base64


def stretch(key):
    while len(key) % 16 != 0:
        key += " "
    return key


def gen_code(n, key):
    flag = stretch("flag_{}_Do_the_hard_work_to_make_it_simple".format(n))
    nkey = stretch(key)
    ciphertext = Crypto.Cipher.AES.new(nkey).encrypt(flag)
    return base64.b64encode(ciphertext+b":"+key.encode("ascii")).decode()


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
        {"flag": gen_code(n, "Aviation House")},
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
            "description": "<p>We've updated the system to AES.  We heard that this is military grade encryption so that should fix everything</p><p>The team have stored the password in %s. Bet you can't get into it</p>" % code_link
        }
    }
