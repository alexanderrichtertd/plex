

"""
renderthreads_logging
==========================================

Module to handle all things related to logging in
the renderthreads package.

------------------------------------------

Members:

#. UniversalPrintObject
    Implements the print_message interface
    used in UniversalStreamHandler.

#. UniversalStreamHandler
    Stream handler subclass that is initialized with
    a UniversalPrintObject that delivers the correct
    print behaviour under the same interface.

...
"""


#  Import
#  ------------------------------------------------------------------
#  python
import sys
import logging
import functools
#  PySide
from PySide import QtGui
from PySide import QtCore


#  Import variable
do_reload = True

#  renderthreads

#  lib

#  renderthreads_globals
import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)


#  Globals
#  ------------------------------------------------------------------
INITIAL_LOGGING_LEVEL = renderthreads_globals.INITIAL_LOGGING_LEVEL


#  Decorators
#  ------------------------------------------------------------------

def execute_with_logger(logger_class):
    """
    Closure logger with argument.
    """

    def execute_with_logger_func_decorator(func):
        """
        Use enclosed logger_class and
        return func object to use.
        """

        def wrapped_func(*args, **kwargs):

            # current_logger_class
            current_logger_class = logging.getLoggerClass()

            # set default logger
            logging.setLoggerClass(logger_class)

            # execute func
            result = func(*args, **kwargs)

            # reset logger
            logging.setLoggerClass(current_logger_class)

            # return
            return result

        return wrapped_func

    return execute_with_logger_func_decorator


#  UniversalPrintObject
#  ------------------------------------------------------------------
class UniversalPrintObject(object):
    """
    UniversalPrintObject implements the print_message interface
    used in UniversalStreamHandler.
    UniversalStreamHandler gets initialized with an instance var.
    of type UniversalPrintObject which in turn is initialized
    with a display member. Based on the type of display,
    UniversalPrintObject delivers the correct print behaviour
    to UniversalStreamHandler.
    """

    def __init__(self,
                    display=sys.stdout,
                    logging_level=INITIAL_LOGGING_LEVEL):
        """
        Initialize UniversalPrintObject
        """

        #  super
        #  ------------------------------------------------------------------
        self.parent_class = super(UniversalPrintObject, self)
        self.parent_class.__init__()

        #  logger
        #  ------------------------------------------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        #  instance vars
        #  ------------------------------------------------------------------
        #  display
        self.display = display

    #  Methods
    #  ------------------------------------------------------------------
    def get_print_message(self):
        """
        Return correct print method based on
        type of self.display.
        """

        #  stdout
        if (self.display == sys.stdout):
            return self.print_message_stdout

        #  QtGui.QTextEdit
        elif (type(self.display) == QtGui.QTextEdit):
            return self.print_message_qtextedit

        #  unknown
        else:
            return None

    print_message = property(fget=get_print_message)
    """descriptor object"""

    def print_message_stdout(*args):
        """
        Print message on self.display object.
        """

        # self
        self = args[0]
        # message
        message = args[1]
        # print
        print(message)

    def print_message_qtextedit(*args):
        """
        Print message on self.display object.
        """

        # self
        self = args[0]
        # message
        message = args[1]
        # append
        self.display.append(message)


#  UniversalStreamHandler
#  ------------------------------------------------------------------
class UniversalStreamHandler(logging.StreamHandler):
    """
    Stream handler subclass that is initialized with
    a UniversalPrintObject that delivers the correct
    print behaviour under the same interface.
    """

    def __init__(self,
                    universal_print_object=UniversalPrintObject(),
                    logging_level=INITIAL_LOGGING_LEVEL):
        """
        Initialize UniversalStreamHandler
        """

        #  super class init
        super(UniversalStreamHandler, self).__init__()

        #  logger
        #  ------------------------------------------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        #  instance vars
        #  ------------------------------------------------------------------
        #  universal_print_object
        self.universal_print_object = universal_print_object

    #  Methods
    #  ------------------------------------------------------------------
    def emit(self, record):
        """
        Custom emit for UniversalStreamHandler.
        """

        try:
            #  message
            message = self.format(record)
            #  print (just a wrapper around sys.stdout.write())
            self.universal_print_object.print_message(message)
            #  flush
            self.flush()

        except (KeyboardInterrupt, SystemExit):
            raise

        except:
            self.handleError(record)


#  RenderThreadsLogger
#  ------------------------------------------------------------------
class RenderThreadsLogger(logging.getLoggerClass()):
    """
    Custom logging class RenderThreadsLogger to
    be able to test against type.
    """


#  Functions
#  ------------------------------------------------------------------
def get_formatter(verbose_level=logging.WARNING):
    """
    Return correctly formatted handler for display.
    For ease of use, verbose_level corresponds to
    known logging constants.
    """

    # debug
    if (verbose_level == logging.DEBUG):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # info
    elif (verbose_level == logging.INFO):
        return logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # warning
    elif (verbose_level == logging.WARNING):
        return logging.Formatter('%(name)s - %(message)s')

    # error
    elif (verbose_level >= logging.ERROR):
        return logging.Formatter('%(message)s')


def get_handler(display=sys.stdout):
    """
    Return correctly formatted handler for display.
    """

    # formatter
    formatter = get_formatter()
    # universal_print_object
    universal_print_object = UniversalPrintObject(display)
    # handler
    handler = UniversalStreamHandler(universal_print_object)
    # add formatter
    handler.setFormatter(formatter)

    # return
    return handler


@execute_with_logger(RenderThreadsLogger)
def get_logger(name,
                display=sys.stdout,
                logging_level=INITIAL_LOGGING_LEVEL):
    """
    Return correctly formatted logger from single source.
    """

    # handler
    handler = get_handler(display)

    # logger
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)
    logger.handlers = []
    logger.addHandler(handler)

    # return
    return logger


def set_logging_level(logging_level):
    """
    Set logging level for all instances of
    RenderThreads loggers. (That is all loggers in
    global dict of type RenderThreadsLogger)
    """

    # iterate
    for logger_name, logger in logging.Logger.manager.loggerDict.iteritems():

        # check type (a direct type check fails here, for whatever reason)
        # Instead check against __name__ of type which succeeds
        if (type(logger).__name__ == RenderThreadsLogger.__name__):

            # set level
            logger.setLevel(logging_level)

            # print
            print('Set logger {0} to {1}'.format(logger_name, logging_level))
