"""
picoCTF API Startup script
"""

import logging
from colorama import init, Fore, Style
from argparse import ArgumentParser

from flask import request, has_request_context
from sys import stdout

from api.app import app

def main():
    """
    Runtime management of the picoCTF API
    """

    init(autoreset=True)

    parser = ArgumentParser(description="picoCTF API configuration")

    parser.add_argument("-v", "--verbose", action="count", help="increase verbosity", default=0)
    parser.add_argument("-s", "--flask-debug-off", action="store_true", help="show flask context with debug errors.", default=False)
    parser.add_argument("-l", "--log-file", help="log output to a file", default=None)

    args = parser.parse_args()
    setup_loggers(args)

    app.run(host="0.0.0.0", port=8000, debug=True)

def setup_loggers(args):
    """
    Manage loggers for the api.
    """

    #Get log level
    level = [logging.WARNING, logging.INFO, logging.DEBUG]\
        [2 if args.verbose > 2 else args.verbose]

    class ColorFormatter(logging.Formatter):
        """
        Visual logging!
        """
        colors = {
            logging.INFO: (Fore.GREEN, Fore.WHITE),
            logging.DEBUG: (Fore.MAGENTA, Fore.WHITE),
            logging.WARNING: (Fore.YELLOW, Fore.YELLOW),
            logging.ERROR: (Fore.RED, Fore.YELLOW),
            logging.CRITICAL: (Fore.RED, Fore.RED)
        }


        def __init__(self, fmt="%(levelno)s: %(msg)s"):
            logging.Formatter.__init__(self, fmt, "%H:%M", style="%")

        def format(self, record):
            color, text = self.colors.get(record.levelno, self.colors[logging.INFO])

            log_text = '{3}%(asctime)s{2} %(name)-8s {4}{3}%(levelname)-8s{1}{5} {6}%(message)s{1}'.format(
                Fore.WHITE, Fore.RESET, Fore.WHITE, color, Style.NORMAL, Style.RESET_ALL, text)

            if has_request_context():
                flask_log_base = "="*80 + \
                """\nRequest: {method} {path}\nIP: {ip} Agent: {agent_platform} | {agent_browser} {agent_browser_version}\n""".format(
                    method=request.method,
                    path=request.path,
                    ip=request.remote_addr,
                    agent_platform=request.user_agent.platform,
                    agent_browser=request.user_agent.browser,
                    agent_browser_version=request.user_agent.version,
                    agent=request.user_agent.string) + "{0}\n" + "="*80
                log_text = flask_log_base.format(log_text)

            self._style = logging._STYLES["%"][0](log_text)

            return logging.Formatter.format(self, record)

    del app.logger.handlers[:]

    stdout_log = logging.StreamHandler(stdout)
    stdout_log.setFormatter(ColorFormatter())

    app.logger.addHandler(stdout_log)
    app.logger.root.setLevel(level)

    if args.log_file:
        file_log = logging.FileHandler(args.log_file)
        file_log.setLevel(level)
        file_log.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        app.logger.addHandler(file_log)

main()
