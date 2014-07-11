"""
Manage loggers for the api.
"""

import logging

from flask import request, has_request_context

from sys import stdout
from colorama import init, Fore, Style

init(autoreset=True)

log = None

def use(name):
    """
    Alias for logging.getLogger(name)

    Args:
        name: The name of the logger.
    Returns:
        The logging object.
    """

    return logging.getLogger(name)

def _flask_request_format(msg):
    """
    Wraps a message with the flask request context if available.

    Args:
        msg: The message to wrap
    Returns:
        The wrapped message
    """

    if has_request_context():
        flask_log_base = "="*80 + \
        """\nRequest: {method} {path}\nIP: {ip} Agent: {agent_platform} | {agent_browser} {agent_browser_version}\n""" \
        .format(
            method=request.method,
            path=request.path,
            ip=request.remote_addr,
            agent_platform=request.user_agent.platform,
            agent_browser=request.user_agent.browser,
            agent_browser_version=request.user_agent.version,
            agent=request.user_agent.string
        ) + "{0}\n" + "="*80

        return flask_log_base.format(msg)

    return msg

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

    style = logging._STYLES["%"][0] # pylint: disable=protected-access

    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        logging.Formatter.__init__(self, fmt, "%H:%M", style="%")

    def format(self, record):
        color, text = self.colors.get(record.levelno, self.colors[logging.INFO])

        log_text = '{3}%(asctime)s{2} %(name)-8s {4}{3}%(levelname)-8s{1}{5} {6}%(message)s{1}'.format(
            Fore.WHITE, Fore.RESET, Fore.WHITE, color, Style.NORMAL, Style.RESET_ALL, text)

        self._style = _flask_request_format(self.style(log_text))


        return logging.Formatter.format(self, record)

def setup_logs(args):
    """
    Initialize the api loggers.

    Args:
        args: dict containing the configuration options.
    """


    log = use(__name__)

    level = [logging.WARNING, logging.INFO, logging.DEBUG][
        max(args.get("verbose", 1), 2)]

    stdout_log = logging.StreamHandler(stdout)
    stdout_log.setFormatter(ColorFormatter())

    log.root.addHandler(stdout_log)
    log.root.setLevel(level)

