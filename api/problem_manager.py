"""
Problem management script.
"""

import argparse
import sys
import json

import api.problem
from api.common import APIException

from os.path import isfile
from bson import json_util

def insert_problems(files):
    for _, contents in files.items():
        for line in contents:
            try:
                api.problem.insert_problem_from_json(line.strip())
            except APIException as error:
                raise
                exit(1)

def migrate_problems(files, output_file, debug):

    migration_key = {
        "displayname": "display_name",
        "basescore": "score",
        "desc": "description",
        "relatedproblems": "related_problems"
    }

    migration_overwrites = {
        "grader": "test.py"
    }

    deletion_key = ["_id", "pid", "generator", "submissiontype", "devnotes"]

    output = ""
    for _, contents in files.items():
        for line in contents:
            problem = json_util.loads(line.strip())

            if "desc" not in problem:
                problem["desc"] = "I'm bad."

            for key in list(problem.keys()):

                if key in migration_key:
                    problem[migration_key[key]] = problem[key]

                if key in migration_overwrites:
                    problem[key] = migration_overwrites[key]

                if key in migration_key or key in deletion_key:
                    problem.pop(key, None)
            output += json_util.dumps(problem) + "\n"
    output_file.write(output)

def get_output_file(output):
    if output == sys.stdout:
        return output
    else:
        try:
            return open(output, "w")
        except IOError as error:
            print(error.msg)
            exit(1)

def main():
    parser = argparse.ArgumentParser(description='picoCTF problem manager')

    #TODO: Implement these?
    #parser.add_argument("-l", action="store_true", dest="show_list", help="View problem list")
    #parser.add_argument("-f", action="append", default=[], dest="filters", help="Key:value pairs that are used to search the database for problems. Used in conjuction with -l.")

    parser.add_argument("-m", action="store_true", dest="migrate", help="Migrate old 2013 problems to new format.", default=False)
    parser.add_argument("-d", action="store_true", dest="debug", help="Debug mode", default=False)
    parser.add_argument("-o", action="store", dest="output_file", help="Output file.", default=sys.stdout)
    parser.add_argument("--no-confirm", action="store_true", dest="no_confirm", help="Remove confirmation and assume default action.")

    parser.add_argument("files", nargs="*", help="Files containing problems to insert.")

    args = parser.parse_args()

    files = {}

    #Check that all listed files exist.
    for file_path in args.files:
        if not isfile(file_path):
            print("{}: File does not exist!".format(file_path))
            exit(1)
        with open(file_path, "r") as f:
            files[file_path] = f.readlines()

    output_file = get_output_file(args.output_file)

    if args.migrate:
        migrate_problems(files, output_file, args.debug)
    else:
        insert_problems(files)
main()
