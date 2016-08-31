

"""
renderthreads_render
==========================================

Module that handles the actual command
line rendering in Nuke.
"""


# Import
# ------------------------------------------------------------------
# python
import sys
import os
import multiprocessing
import subprocess
import logging
import threading
# PySide
from PySide import QtGui
from PySide import QtCore


# Import variable
do_reload = True

# renderthreads

# lib

# renderthreads_logging
import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)


# Globals
# ------------------------------------------------------------------


# RenderCommand
# ------------------------------------------------------------------
class RenderCommand(QtCore.QObject):
    """
    RenderCommand class that handles the commandline process.
    """

    # Signals
    # ------------------------------------------------------------------
    sgnl_task_done = QtCore.Signal()
    sgnl_log = QtCore.Signal(str, int)
    sgnl_readd_job = QtCore.Signal(list, int)

    # Creation and Initialization
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        RenderCommand instance factory.
        """

        # render_command_instance
        render_command_instance = super(RenderCommand, cls).__new__(cls, args, kwargs)

        return render_command_instance

    def __init__(self,
                    command,
                    timeout,
                    display_shell,
                    identifier,
                    priority,
                    frame,
                    log_exitcode_errors_only,
                    renderthreads_node):
        """
        Customize RenderCommand instance.
        Parameter timeout is in seconds NOT in ms.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # parent_class
        self.parent_class = super(RenderCommand, self)
        self.parent_class.__init__()

        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------

        # command
        self.command = command
        # timeout
        self.timeout = timeout
        # display_shell
        self.display_shell = display_shell
        # identifier
        self.identifier = identifier  # nuke node full name
        # priority
        self.priority = priority
        # frame
        self.frame = frame
        # log_exitcode_errors_only
        self.log_exitcode_errors_only = log_exitcode_errors_only
        # renderthreads_node
        self.renderthreads_node = renderthreads_node  # only used for readd_job in main wdgt

        # process
        self.process = None
        # enabled
        self.enabled = True
        # readd_count
        self.readd_count = 0

        # logger_name
        self.logger_name = '{0}-{1}-{2}'.format(self.__class__.__name__, identifier, frame)
        # logger
        self.logger = renderthreads_logging.get_logger(self.logger_name)

    # Operator overrides
    # ------------------------------------------------------------------
    def __call__(self):
        """()"""

        # run
        self.run()

    def __cmp__(self, other):
        """Implement all comparison methods"""

        # priority equal
        if (self.priority == other.priority):
            return cmp(self.identifier, other.identifier)

        # else
        else:
            return cmp(self.priority, other.priority)

    # Methods
    # ------------------------------------------------------------------

    def run(self):
        """
        Method to start timed process.
        """

        # not enabled
        if not (self.enabled):

            # notify gui
            self.sgnl_task_done.emit()
            # log_exitcode
            self.log_exitcode('disabled')

            # return 0 (0 being the code for "executed properly")
            return 0

        # import
        import os
        import subprocess
        import logging
        import threading

        def target():
            """
            Target method to do the actual work.
            Wrapped by thread that terminates on timeout.
            """

            # env_dict
            env_dict = os.environ.copy()

            # creation_flags
            creation_flags = 0

            # display_shell
            if (self.display_shell):
                creation_flags = subprocess.CREATE_NEW_CONSOLE

            # process
            self.process = subprocess.Popen('{0}'.format(self.command),
                                            env=env_dict,
                                            creationflags=creation_flags)

            # communicate
            self.process.communicate()

        # thread
        thread = threading.Thread(target=target)
        # start
        thread.start()
        # wait for timeout
        timeout_in_seconds = self.timeout * 60
        thread.join(timeout_in_seconds)

        # on timeout
        if(thread.is_alive()):

            # log
            self.logger.debug('Terminating process')

            # terminate process
            self.process.terminate()

            # finish thread
            thread.join()

        # exitcode
        exitcode = self.process.returncode

        # notify gui
        self.sgnl_task_done.emit()
        # log_exitcode
        self.log_exitcode(exitcode)
        # readd_job
        # Wrap RenderCommand in list to circumvent error
        # https://github.com/timmwagener/renderthreads/issues/4
        self.sgnl_readd_job.emit([self], exitcode)

        # return
        return exitcode

    def log_exitcode(self, exitcode):
        """
        Log exitcode in a formated way.
        """

        # log_message
        log_message = self.get_log_message(exitcode)

        # errors only
        if (self.get_log_exitcode_errors_only()):

            # if error
            if (self.is_error(exitcode)):

                # emit
                self.sgnl_log.emit(log_message, logging.CRITICAL)

        # else
        else:

            # emit
            self.sgnl_log.emit(log_message, logging.DEBUG)

    def get_log_message(self, exitcode):
        """
        Return log message according
        to given exitcode.
        """

        # log_message_prefix
        log_message_prefix = '{0}-{1}:'.format(self.identifier, self.frame)

        # exitcode 'disabled'
        if (exitcode == 'disabled'):
            # log_message_suffix
            log_message_suffix = 'Disabled.'

        # exitcode None
        elif (exitcode is None):
            # log_message_suffix
            log_message_suffix = 'Exitcode is None.'

        # exitcode 0
        elif (exitcode == 0):
            # log_message_suffix
            log_message_suffix = 'Frame rendered successfull.({0})'.format(exitcode)

        # exitcode 1
        elif (exitcode == 1):
            # log_message_suffix
            log_message_suffix = 'Process terminated, maybe because of too rigid timeout setting.({0})'.format(exitcode)

        # exitcode 100
        elif (exitcode == 100):
            # log_message_suffix
            log_message_suffix = 'Process terminated because of missing license.\
Maybe pick -i (interactive) license flag.\
The default uses a render license.({0})'.format(exitcode)

        # unknown exitcode
        else:
            # log_message_suffix
            log_message_suffix = 'Unknown exitcode.({0})'.format(exitcode)

        # log_message
        log_message = log_message_prefix + ' ' + log_message_suffix

        # return
        return log_message

    def is_error(self, exitcode):
        """
        Return True or False wether or
        not the exitcode is recognized as
        error.
        """

        # no error
        if (exitcode == 0):
            return False

        return True

    # Slots
    # ------------------------------------------------------------------
    @QtCore.Slot()
    def terminate_process(self):
        """
        Terminate process if it exists.
        """

        # if exists
        if (self.process):

            try:
                # terminate
                self.process.terminate()
            except:
                pass

    @QtCore.Slot(str)
    def terminate_process_for_identifier(self, identifier):
        """
        Terminate process if it exists.
        """

        # check identifier
        if (self.identifier == identifier):

            # terminate_process
            self.terminate_process()

    # Getter & Setter
    # ------------------------------------------------------------------

    def get_enabled(self):
        """
        Return self.enabled.
        """

        return self.enabled

    @QtCore.Slot(bool)
    def set_enabled(self, value):
        """
        Set self.enabled.
        """

        self.enabled = value

    @QtCore.Slot(str, bool)
    def set_enabled_for_identifier(self, identifier, value):
        """
        Set self.enabled if identifier check
        is successfull.
        """

        # check identifier
        if (self.identifier == identifier):

            # set enabled
            self.enabled = value

    def get_priority(self):
        """
        Return self.priority.
        """

        return self.priority

    @QtCore.Slot(int)
    def set_priority(self, value):
        """
        Set self.priority.
        """

        self.priority = value

    @QtCore.Slot(str, int)
    def set_priority_for_identifier(self, identifier, value):
        """
        Set self.priority if identifier check
        is successfull.
        """

        # check identifier
        if (self.identifier == identifier):

            # set priority
            self.priority = value

    def get_timeout(self):
        """
        Return self.timeout.
        """

        return self.timeout

    @QtCore.Slot(int)
    def set_timeout(self, value):
        """
        Set self.timeout.
        """

        # set
        self.timeout = value

    def get_display_shell(self):
        """
        Return self.display_shell.
        """

        return self.display_shell

    @QtCore.Slot(bool)
    def set_display_shell(self, value):
        """
        Set self.display_shell.
        """

        self.display_shell = value

    def get_identifier(self):
        """
        Return self.identifier.
        """

        return self.identifier

    def set_identifier(self, value):
        """
        Set self.identifier.
        """

        self.identifier = value

    def get_frame(self):
        """
        Return self.frame.
        """

        return self.frame

    def set_frame(self, value):
        """
        Set self.frame.
        """

        self.frame = value

    def get_log_exitcode_errors_only(self):
        """
        Return self.log_exitcode_errors_only.
        """

        return self.log_exitcode_errors_only

    @QtCore.Slot(bool)
    def set_log_exitcode_errors_only(self, value):
        """
        Set self.log_exitcode_errors_only.
        """

        self.log_exitcode_errors_only = value

    def get_readd_count(self):
        """
        Return self.readd_count.
        """

        return self.readd_count

    @QtCore.Slot(int)
    def set_readd_count(self, value):
        """
        Set self.readd_count.
        """

        self.readd_count = value

    @QtCore.Slot()
    def increment_readd_count(self):
        """
        Increment self.readd_count.
        """

        self.readd_count += 1
