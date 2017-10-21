#*********************************************************************
# content   = write loggings into console and files
# version   = 0.1.0
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys
import logging
import logging.config

USER = os.getenv('username')

#*********************************************************************
# CLASS
class ContextFilter(logging.Filter):
    USERS = USER

    def filter(self, record):
        record.user = ContextFilter.USERS
        return True


#*********************************************************************
# LOGGING
def init(software="default", script="default", level=logging.DEBUG, path="", *args, **kwargs):

    if not path: path = ("/").join([os.getenv('DATA_USER_PATH'), USER + ".log"])
    create_folder(path)

    info_path, error_path, debug_path = path, path, path

    logging_config = dict(
        version= 1,
        disable_existing_loggers= False,
        formatters= {
            "simple": {
                "format": "%(asctime)s | %(user)-10s | %(module)-10s | %(levelname)-7s - %(lineno)-4d | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleInfo": {
                "format": "%(asctime)s | %(levelname)-7s | %(user)-10s | %(module)-10s - %(funcName)-18s | %(lineno)-4d | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleDebug": {
                "format": "%(asctime)s | %(levelname)-7s | %(module)-10s - %(funcName)-18s | %(lineno)-4d | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleConsole": {
                "format": "%(asctime)s | %(levelname)-7s | %(module)-10s - %(funcName)-16s | %(lineno)-4d | %(message)s",
                "datefmt":"%H:%M:%S" }
        }
    )

    logger = logging.getLogger(script)

    # CONSOLE
    console_handler = logging.StreamHandler(stream=sys.stdout)
    formatter       = logging.Formatter(logging_config["formatters"]["simpleConsole"]["format"], logging_config["formatters"]["simpleConsole"]["datefmt"])
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    # DEBUG
    if level == logging.DEBUG:
        debug_handler = logging.handlers.RotatingFileHandler(debug_path, mode='a', maxBytes=10485760, backupCount=20, encoding="utf8")
        formatter     = logging.Formatter(logging_config["formatters"]["simpleDebug"]["format"], logging_config["formatters"]["simpleDebug"]["datefmt"])
        debug_handler.setFormatter(formatter)
        debug_handler.setLevel(level)
        logger.addHandler(debug_handler)

    # INFO, WARNING, ERROR
    else: #level == logging.INFO:
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
    if len(path.split('.')) > 1: path = os.path.dirname(path)
    if not os.path.exists(path):
        try:    os.makedirs(path)
        except: print('CANT create folder: {}'.format(path))
