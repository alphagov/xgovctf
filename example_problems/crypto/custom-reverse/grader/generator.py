from os import path
import Crypto.Cipher.AES
import base64


def generate(random, pid, autogen_tools, n):
    """
    Generate an instance of the problem
    Needs to return a list of files to copy to particular instance.
    """

    return {
        "resource_files": {
            "public": [
            ],
        },
        "static_files": {
        },
        "problem_updates": {
            "description": "<p>Having tried all of the algorithms that we can think of, we set our best engineer on creating a custom algorithm</p><p>They came up with a <a href=/problem-static/crypto/custom/algorithm.txt>custom algorithm</a> based on doing a <a href=/problem-static/crypto/custom/description.txt>number of substitutions and permutations</a> on the input</p><p>Can you implement the algorithm in order to encrypt the password 'abcdefghi'</p>"
        }
    }
