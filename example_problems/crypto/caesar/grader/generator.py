from os import path
import base64


def rot_x(src, key):
    from string import ascii_lowercase as lc, ascii_uppercase as uc
    lookup = str.maketrans(lc + uc, lc[key:] + lc[:key] + uc[key:] + uc[:key])
    return src.translate(lookup)


def gen_code(n):
    flag = "flag_iterate_then_iterate_again."
    return base64.b64encode(rot_x(flag, n).encode("UTF-8")).decode()


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
        {"flag": gen_code(n)},
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
            "description": "<p>GDS Security engineering have the best cryptographers, so we looked back on one of the greatest of all time, and implemented his algorithm</p><p>The team have stored the password in %s. Bet you can't get into it</p>" % code_link
        }
    }
