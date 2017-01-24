#*********************************************************************
# content   = write loggings into console and files
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <contact@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys
import logging
import logging.config

THIS_DIR = ("/").join([os.path.dirname(__file__)])

#************************
# CLASS
class ContextFilter(logging.Filter):
    USERS = os.getenv('username')

    def filter(self, record):
        record.user = ContextFilter.USERS
        return True

class MyFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        for level in self.__level:
            if logRecord.levelno == level:
                return True
        return False


#************************
# LOGGING
def initLog(software="default", script="default", level=logging.DEBUG, path="", *args, **kwargs):
    logger = logging.getLogger(script)

    # CHECK path param
    if not path:
        path = ("/").join([getEnv('DATA_PATH'), 'user', os.getenv('username'), os.getenv('username') + ".log"])

    createFolder(path)

    info_path, error_path, debug_path = path, path, path

    logging_config = dict(
        version= 1,
        disable_existing_loggers= False,
        formatters= {
            "simple": {
                "format": "%(asctime)s | %(user)-10s | %(module)-10s | %(levelname)-8s - %(lineno)-4d | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleInfo": {
                "format": "%(asctime)s | %(user)-10s | %(module)-10s - %(funcName)-18s | %(lineno)-4d | %(levelname)-8s | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleDebug": {
                "format": "%(asctime)s | %(module)-10s - %(funcName)-18s | %(lineno)-4d | %(levelname)-8s | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleConsole": {
                "format": "%(asctime)s | %(module)-10s - %(funcName)-16s | %(lineno)-4d | %(levelname)-8s | %(message)s",
                "datefmt":"%H:%M:%S"
            }
        },

        handlers= {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simpleConsole",
                "stream": "ext://sys.stdout"
            },

            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simpleInfo",
                "filename": info_path,
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            },

            "debug_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simpleInfo",
                "filename": debug_path,
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            },

            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simpleDebug",
                "filename": error_path,
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
             }
        },

        logger= {
            "my_module": {
                "level": level,
                "handlers": ["console"],
                "propagate": "no"
            }
        },

        root= {
            "level": level,
            #"handlers": ["console", "info_file_handler", "debug_file_handler", "error_file_handler"]
        }
    )

    console_handler = logging.StreamHandler(stream=sys.stdout)
    formatter       = logging.Formatter(logging_config["formatters"]["simpleConsole"]["format"])
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    if level == logging.DEBUG:
        debug_handler = logging.handlers.RotatingFileHandler(debug_path, mode='a', maxBytes=10485760, backupCount=20, encoding="utf8")
        formatter     = logging.Formatter(logging_config["formatters"]["simpleDebug"]["format"], logging_config["formatters"]["simpleDebug"]["datefmt"])
        debug_handler.setFormatter(formatter)
        debug_handler.setLevel(level)
        logger.addHandler(debug_handler)

    else: #level == logging.INFO:
        info_handler = logging.handlers.RotatingFileHandler(info_path, mode='a', maxBytes=10485760, backupCount=20, encoding="utf8")
        formatter    = logging.Formatter(logging_config["formatters"]["simpleInfo"]["format"], logging_config["formatters"]["simple"]["datefmt"])
        info_handler.setFormatter(formatter)
        info_handler.setLevel(level)
        logger.addHandler(info_handler)

    logger.setLevel(level)
    logger.addFilter(ContextFilter())

    return logger

#************************
# FUNC
def createFolder(path):
    if len(path.split(".")) > 1:
        path = os.path.dirname(path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            print("WARNING : Can not create folder : %s"% path)


def getEnv(var):
    if os.environ.__contains__(var):
        return os.environ[var].split(';')[0]
    LOG.warning('ENV doesnt exist: {}'.format(var))
    return ""

#************************
# TEST
def test():
    title = "default"
    LOG1  = initLog(script=title, logger=logging.getLogger(title))
    LOG1.info("START1")
    print LOG1
    LOG1.debug('Failed')
    LOG1.error('Failed to open file', exc_info=True)

    title = "default_new"
    LOG2  = initLog(script=title, level=logging.DEBUG, logger=logging.getLogger(title))
    LOG2.info("START2")
    LOG2.debug('Failed')

    try: a()
    except: LOG2.error('Failed to open file', exc_info=True)

    LOG1.info('START1_2')
    LOG2.debug(os.getenv('username'))
    print LOG2.warning("START2_SECONDFUCKINGTIME")

    try:
        1/0
    except:
        print ""

# test()
