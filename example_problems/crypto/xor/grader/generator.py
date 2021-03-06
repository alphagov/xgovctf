from os import path
import base64


def xor(key, src):
    return "".join([chr(key ^ ord(b)) for b in src])


def gen_code(n, key):
    flag = "flag_{}_start_with_user_needs".format(n)
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
            "description": "<p>The GDS security engineering team has been asked to ensure that dangerous adversaries cannot read the passwords.</p><p>We all know that the best engineers invent their own tools, so we created our own encryption scheme.  We read that <a href='https://en.wikipedia.org/XOR'>XOR is an unbreakable cipher</a> but we're not sure what this keystream stuff is about</p><p>The team have stored the password in %s.</p>" % code_link
        }
    }
