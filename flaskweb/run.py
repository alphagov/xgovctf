#!/usr/bin/python3
"""
picoCTF FlaskWeb Startup script
"""

import app

from argparse import ArgumentParser


def main():
    """
    Runtime management of the picoCTF WebFrontend
    """

    parser = ArgumentParser(description="picoCTF API configuration")

    parser.add_argument("-v", "--verbose", action="count", help="increase verbosity", default=0)

    parser.add_argument("-p", "--port", action="store", help="port the server should listen on.", type=int, default=8001)
    parser.add_argument("-l", "--listen", action="store", help="host the server should listen on.", default="0.0.0.0")
    parser.add_argument("-d", "--debug", action="store_true", help="run the server in debug mode.", default=False)

    args = parser.parse_args()

    keyword_args, _ = object_from_args(args)

    app.config_app() \
        .run(host=args.listen, port=args.port, debug=args.debug)


def object_from_args(args):
    """
    Turns argparser's namespace into something manageable by an external library.

    Args:
        args: The result from parse.parse_args
    Returns:
        A tuple of a dict representing the kwargs and a list of the positional arguments.
    """

    return dict(args._get_kwargs()), args._get_args()  # pylint: disable=protected-access


main()
