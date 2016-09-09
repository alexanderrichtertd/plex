#*************************************************************
# CONTENT       write logs in data/log
#
# AUTHOR        Alexander Richter 
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
import sys

import logging
import logging.config

import settings as s


#************************
# CLASS
#************************
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
# LOG
#************************
def initLog(script="default", level=logging.INFO, logger=logging.getLogger()):
    
    if not logger.handlers == []:
        return logger

    path = os.path.join(s.PATH["data_log"], os.environ("SOFTWARE"))

    if level == logging.DEBUG:
        path = os.path.join(path, "DEBUG")
        
    if not os.path.exists(path):
        os.mkdir(path)

    path = os.path.join(path, script + ".log")

    info_path  = path # os.path.join(path, script + "_info.log")
    debug_path = path # os.path.join(path, script + "_debug.log")
    error_path = path # os.path.join(path, script + "_error.log")

    logging_config = dict(
        version= 1,
        disable_existing_loggers= False,
        formatters= {
            "simple": {
                "format": "%(asctime)s | %(module)-16s | %(levelname)-8s | %(user)-12s | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleDebug": {
                "format": "%(asctime)s | %(module)-16s - %(funcName)-22s | %(levelname)-8s | %(user)-12s | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleConsole": {
                "format": "%(module)-16s - %(funcName)-20s | %(levelname)-8s | %(message)s"
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
                "formatter": "simpleDebug",
                "filename": info_path,
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            },

            "debug_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simpleDebug",
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

    # logging.config.dictConfig(logging_config)
    # help(logging.StreamHandler)
    if level == logging.DEBUG:
        console_handler = logging.StreamHandler(stream=sys.stdout)
        formatter       = logging.Formatter(logging_config["formatters"]["simpleConsole"]["format"])
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

    # info_handler = logging.handlers.RotatingFileHandler(info_path, mode='a', maxBytes=10485760, backupCount=20, encoding="utf8")
    # formatter    = logging.Formatter(logging_config["formatters"]["simpleDebug"]["format"], logging_config["formatters"]["simple"]["datefmt"])
    # info_handler.setFormatter(formatter)
    # info_handler.setLevel(logging.INFO)
    # logger.addHandler(info_handler)

    debug_handler = logging.handlers.RotatingFileHandler(debug_path, mode='a', maxBytes=10485760, backupCount=20, encoding="utf8")
    formatter     = logging.Formatter(logging_config["formatters"]["simpleDebug"]["format"], logging_config["formatters"]["simpleDebug"]["datefmt"])
    debug_handler.setFormatter(formatter)
    debug_handler.setLevel(logging.DEBUG)
    logger.addHandler(debug_handler)

    # error_handler = logging.handlers.RotatingFileHandler(error_path, mode='a', maxBytes=10485760, backupCount=20, encoding="utf8")
    # formatter     = logging.Formatter(logging_config["formatters"]["simpleDebug"]["format"], logging_config["formatters"]["simpleDebug"]["datefmt"])
    # error_handler.setFormatter(formatter)
    # error_handler.setLevel(logging.ERROR)
    # logger.addHandler(error_handler)

    logger.setLevel(level)
    logger.addFilter(ContextFilter())
    # logger.handlers[1].addFilter(MyFilter([logging.INFO]))
    # logger.handlers[2].addFilter(MyFilter([logging.DEBUG, logging.CRITICAL,logging.ERROR]))
    return logger


#************************
# TEST
#************************
def test():
    title = "default"
    LOG1 = initLog(script=title, level=logging.INFO, logger=logging.getLogger(title))
    LOG1.info("START1")
    LOG1.debug('Failed')
    LOG1.error('Failed to open file', exc_info=True)

    title = "default_new"
    LOG2 = initLog(script=title, level=logging.DEBUG, logger=logging.getLogger(title))
    LOG2.info("START2")
    LOG2.debug('Failed')
    LOG2.error('Failed to open file', exc_info=True)

    LOG1.info('START1_2')
    LOG1.debug('Failed2')
    LOG2.info("START2_SECONDFUCKINGTIME")

    try:
        1/0
    except:
        print ""

# test()