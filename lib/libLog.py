#*************************************************************
# CONTENT       write logs in data/log or local
#
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
import sys
import logging
import logging.config

import libFileFolder

# TEMP***************************
sys.path.append(r"..\settings")
import setEnv
setEnv.SetEnv()
#********************************
#os.environ["SOFTWARE"] = "default"
import getProject
DATA = getProject.GetProject()

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
def initLog(software="default", script="default", level=logging.INFO, path="", *args, **kwargs):
    logger = logging.getLogger(script)

    # CHECK path param
    if not path:
        # CHECK software param
        if software == "default":
            try:
                software = os.environ["SOFTWARE"]
            except KeyError:
                print ("WARNING : os.environ['SOFTWARE'] is not existing")

        path = ("/").join([os.environ["DATA_PATH"], "log", software, script + ".log"])
        print path
    # CREATE path folder
    libFileFolder.createFolder(path)

    info_path  = path # ("/").join([path, script + "_info.log"])
    error_path = path # ("/").join([path, script + "_error.log"])
    debug_path = DATA.PATH["data_local"]

    logging_config = dict(
        version= 1,
        disable_existing_loggers= False,
        formatters= {
            "simple": {
                "format": "%(asctime)s | %(user)-10s | %(module)-10s | %(levelname)-8s - %(lineno)-5d | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleInfo": {
                "format": "%(asctime)s | %(user)-10s | %(module)-10s - %(funcName)-18s | %(lineno)-5d | %(levelname)-8s | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleDebug": {
                "format": "%(asctime)s | %(module)-10s - %(funcName)-18s | %(lineno)-5d | %(levelname)-8s | %(message)s",
                "datefmt":"%d.%m.%Y %H:%M:%S"
            },
            "simpleConsole": {
                "format": "%(module)-10s - %(funcName)-18s | %(lineno)-5d | %(levelname)-8s | %(message)s"
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

    # logging.config.dictConfig(logging_config)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    formatter       = logging.Formatter(logging_config["formatters"]["simpleConsole"]["format"])
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    if level == logging.DEBUG:
        print("PATH to DEBUG is %s"% debug_path)
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
    # logger.handlers[1].addFilter(MyFilter([logging.INFO]))
    # logger.handlers[2].addFilter(MyFilter([logging.DEBUG, logging.CRITICAL,logging.ERROR]))

    return logger


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
