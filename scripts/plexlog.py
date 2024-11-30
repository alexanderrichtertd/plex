#*********************************************************************
# content   = write loggings into console and files
# date      = 2024-11-16
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys
import getpass
import logging
import logging.config

USER = getpass.getuser()
config_user_path = eval(os.environ['PLEX_PATHS'])['config_user']


#*********************************************************************
# CLASS
class ContextFilter(logging.Filter):
    USERS = USER

    def filter(self, record):
        record.user = ContextFilter.USERS
        return True


#*********************************************************************
# LOGGING
def init(software="default", script="default", level=logging.DEBUG, path="", 
         debug_console=False, multi_threads=False, *args, **kwargs):

    if not path: 
        path = "/".join([config_user_path or os.path.expanduser('~'), USER + ".log"])

    create_folder(path)

    # OPTIONAL: separate levels into different files
    info_path, error_path, debug_path = path, path, path

    logging_config = dict(
        version= 1,
        disable_existing_loggers= False,
        formatters= {
            "simple": {
                "format": "%(asctime)s | %(user)-10s | %(module)-12s | %(levelname)-7s - %(lineno)-4d | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleInfo": {
                "format": "%(asctime)s | %(levelname)-7s | %(user)-10s | %(module)-12s - %(funcName)-20s | %(lineno)-4d | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleDebug": {
                "format": "%(asctime)s | %(levelname)-7s | %(module)-12s - %(funcName)-20s | %(lineno)-4d | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "threadsDebug": {
                "format": "%(asctime)s | %(levelname)-7s | %(threadName)-10s | %(module)-12s - %(funcName)-20s | %(lineno)-4d | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleConsole": {
                "format": "%(asctime)s | %(levelname)-7s | %(message)s",
                "datefmt":"%H:%M:%S" }
        }
    )

    logger = logging.getLogger(script)
    logger.propagate = False

    if not logger.handlers:
        # CONSOLE
        console_handler = logging.StreamHandler(stream=sys.stdout)
        formatter       = logging.Formatter(logging_config["formatters"]["simpleConsole"]["format"], logging_config["formatters"]["simpleConsole"]["datefmt"])
        console_handler.setFormatter(formatter)
        if debug_console: console_handler.setLevel(level)
        else:             console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

        # DEBUG
        if level == logging.DEBUG:
            debug_handler = logging.handlers.RotatingFileHandler(debug_path, mode='a', maxBytes=10485760, backupCount=20, encoding="utf8")
            if multi_threads: formatter = logging.Formatter(logging_config["formatters"]["threadsDebug"]["format"], logging_config["formatters"]["simpleDebug"]["datefmt"])
            else:             formatter = logging.Formatter(logging_config["formatters"]["simpleDebug"]["format"], logging_config["formatters"]["threadsDebug"]["datefmt"])
            debug_handler.setFormatter(formatter)
            debug_handler.setLevel(level)
            logger.addHandler(debug_handler)

        # INFO, WARNING, ERROR
        else: # level == logging.INFO:
            info_handler = logging.handlers.RotatingFileHandler(info_path, mode='a', maxBytes=10485760, backupCount=20, encoding="utf8")
            formatter    = logging.Formatter(logging_config["formatters"]["simpleInfo"]["format"], logging_config["formatters"]["simple"]["datefmt"])
            info_handler.setFormatter(formatter)
            info_handler.setLevel(level)
            logger.addHandler(info_handler)

        logger.setLevel(level)
        logger.addFilter(ContextFilter())

    return logger


#*********************************************************************
def create_folder(path):
    if len(path.split('.')) > 1: 
        path = os.path.dirname(path)

    if not os.path.exists(path):
        try:    os.makedirs(path)
        except: print(f"CAN'T create folder: {path}")
