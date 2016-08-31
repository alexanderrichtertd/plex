

"""
renderthreads
==========================================

GUI to start threaded nuke rendering.

To use it execute the following script in your Nuke
Script Editor.

.. code::

    from renderthreads import renderthreads
    reload(renderthreads)

    #run
    renderthreads.run(dev = True, dock_it = True)

-----------------------
Current Status: beta
-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""


# Add tool root path
# ------------------------------------------------------------------
# import
import sys
import os

# tool_root_path
tool_root_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(tool_root_path)


# Import
# ------------------------------------------------------------------
# python
import functools
import logging
# PySide
from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools


# Import variable
do_reload = True


# renderthreads

# lib

# renderthreads_globals
from lib import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)

# renderthreads_logging
from lib import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)

# renderthreads_gui_setup
from lib import renderthreads_gui_setup
if(do_reload):
    reload(renderthreads_gui_setup)

# renderthreads_mvc_setup
from lib import renderthreads_mvc_setup
if(do_reload):
    reload(renderthreads_mvc_setup)

# renderthreads_services_setup
from lib import renderthreads_services_setup
if(do_reload):
    reload(renderthreads_services_setup)

# renderthreads_threads
from lib import renderthreads_threads
if(do_reload):
    reload(renderthreads_threads)

# lib.gui

# renderthreads_gui_helper
from lib.gui import renderthreads_gui_helper
if(do_reload):
    reload(renderthreads_gui_helper)

# renderthreads_dock_widget
from lib.gui import renderthreads_dock_widget
if(do_reload):
    reload(renderthreads_dock_widget)

# lib.mvc

# renderthreads_model_context_menu
from lib.mvc import renderthreads_model_context_menu
if(do_reload):
    reload(renderthreads_model_context_menu)


# Globals
# ------------------------------------------------------------------
TITLE = renderthreads_globals.TITLE
# Pathes
UI_PATH = renderthreads_globals.UI_PATH

INITIAL_LOGGING_LEVEL = renderthreads_globals.INITIAL_LOGGING_LEVEL

INITIAL_THREAD_INTERVAL = renderthreads_globals.INITIAL_THREAD_INTERVAL


# form_class, base_class
# ------------------------------------------------------------------
# ui_file
ui_file_name = 'renderthreads.ui'
ui_file = os.path.join(UI_PATH, ui_file_name)

# form_class, base_class
form_class, base_class = renderthreads_gui_helper.load_ui_type(ui_file)


# RenderThreads class
# ------------------------------------------------------------------
class RenderThreads(form_class, base_class):
    """
    RenderThreads class.
    """

    # Signals
    # ------------------------------------------------------------------

    # command object signals to connect with RenderCommand instances
    # in the queue. The signals are defined here in the main wdgt
    # since a new context menu instance is created at each right
    # click in the nodes view. The instance signals here remain
    # the same self
    sgnl_command_set_enabled = QtCore.Signal(bool)
    sgnl_command_set_enabled_for_identifier = QtCore.Signal(str, bool)
    sgnl_command_set_timeout = QtCore.Signal(int)
    sgnl_command_set_display_shell = QtCore.Signal(int)
    sgnl_command_set_log_exitcode_errors_only = QtCore.Signal(int)
    sgnl_command_terminate_process = QtCore.Signal()
    sgnl_command_terminate_process_for_identifier = QtCore.Signal(str)

    # Create and initialize
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        RenderThreads instance factory.
        """

        # delete and cleanup old instances
        renderthreads_gui_helper.check_and_delete_wdgt_instances_with_class_name(cls.__name__)
        renderthreads_gui_helper.check_and_delete_wdgt_instances_with_class_name(renderthreads_dock_widget.RenderThreadsDockWidget.__name__)

        # renderthreads_instance
        renderthreads_instance = super(RenderThreads, cls).__new__(cls, args, kwargs)

        return renderthreads_instance

    def __init__(self,
                    dev=False,
                    dock_it=True,
                    parent=renderthreads_gui_helper.get_nuke_main_window()):
        """
        Customize instance.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # super
        self.parent_class = super(RenderThreads, self)
        self.parent_class.__init__(parent)

        # setObjectName
        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        # dock_it
        self.dock_it = dock_it

        # dev
        self.dev = dev

        # thread_manager
        self.thread_manager = renderthreads_threads.ThreadManager()

        # Init procedure
        # ------------------------------------------------------------------
        # setup_threads
        self.thread_manager.setup_threads(thread_interval=INITIAL_THREAD_INTERVAL)

        # setupUi
        self.setupUi(self)

        # setup_additional_ui
        renderthreads_gui_setup.setup_additional_ui(self)

        # setup_mvc
        renderthreads_mvc_setup.setup_mvc(self)

        # setup_services
        renderthreads_services_setup.setup_services(self)

        # connect_context_menus
        self.connect_context_menus()

        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)
        # te_log_handler
        self.te_log_handler = renderthreads_logging.get_handler(self.te_log)
        self.logger.addHandler(self.te_log_handler)

        # run_tests
        self.run_tests()

        # dock_it
        if (self.dock_it):
            renderthreads_gui_helper.make_dockable(self)

    # Context Menus
    # ------------------------------------------------------------------
    def connect_context_menus(self):
        """
        Connect context menus. This didnt fit in the
        renderthreads_mvc_setup module because of implicit
        first argument of pyside context menu signal.
        """

        # nodes_view
        self.nodes_view.customContextMenuRequested.connect(self.display_nodes_context_menu)

    def display_nodes_context_menu(self, pos):
        """
        Create and display nodes model context menu.
        """

        # context_menu
        context_menu = renderthreads_model_context_menu.NodesContextMenu(dev=self.is_dev(),
                                                                            parent=self)
        context_menu.set_view_and_model(self.nodes_view)
        context_menu.set_main_widget(self)
        context_menu.popup(self.nodes_view.mapToGlobal(pos))

    # Getter & Setter
    # ------------------------------------------------------------------
    def is_dev(self):
        """
        Return developer status of app.
        """

        return self.dev

    # Slots
    # ------------------------------------------------------------------
    @QtCore.Slot(str, int)
    def log(self, msg, logging_level):
        """
        Log msg with self.logger. This is
        usefull because uncoupled classes
        can log on the main logger without
        being closely coupled using signals
        and slots.
        """

        # log
        self.logger.log(logging_level, msg)

    @QtCore.Slot(list, int)
    def readd_job(self, command_object_list, exitcode):
        """
        Check if job should be readded to the
        queue and if yes, do so.
        """

        # command_object
        # Only wrapped in type list to avaoid sgnl error.
        # Always contains one RenderCommand item.
        command_object = command_object_list[0]

        # check exitcode
        if (exitcode != 0):

            # command_object enabled?
            if (command_object.get_enabled()):

                # do_readd
                do_readd = self.sldr_readd_broken_job.get_value()

                # check do_readd
                if (do_readd):

                    # max_readd_count
                    max_readd_count = self.sldr_readd_broken_job_count.get_value()

                    # check readd_count
                    if (command_object.get_readd_count() < max_readd_count):

                        try:

                            # increment_readd_count
                            command_object.increment_readd_count()

                            # increment progressbar range
                            self.pbar_render.increment_range()
                            command_object.renderthreads_node.progressbar.increment_range()

                            # add
                            self.thread_manager.add_to_queue(command_object)

                            # log
                            self.logger.critical('Readded {0} ({1})'.format(command_object.logger_name,
                                                                                    exitcode))
                        except:

                            # log
                            self.logger.critical('Error readding command object to queue')

    # Misc
    # ------------------------------------------------------------------
    def dummy_method(self, msg='dummy'):
        """
        Dummy method.
        """

        # log
        self.logger.debug('{0}'.format(msg))

    def dummy_method_silent(self):
        """
        Dummy method without output.
        """

        pass

    # Test
    # ------------------------------------------------------------------
    def run_tests(self):
        """
        Suite of test methods.
        """

        # log
        self.logger.debug('\n\nExecute test methods:\n-----------------------------')

        # test methods start here
        # ------------------------------------------------------------------
        # ------------------------------------------------------------------

        # dummy_method
        self.dummy_method()

        # ------------------------------------------------------------------
        # ------------------------------------------------------------------
        # test methods end here

        # log
        self.logger.debug('\n\n-----------------------------\nFinished test methods.')

    # Events
    # ------------------------------------------------------------------
    def stop_all_threads_and_timer(self):
        """
        Try to stop all threads and timers that RenderThreads started.
        This method is ment to be used in a closeEvent.
        """

        try:
            # thread_manager threads
            self.thread_manager.stop_threads()

            # stop_services
            renderthreads_services_setup.stop_services(self)

        except:
            # log
            self.logger.debug('Error stopping threads for queue.')

    def closeEvent(self, event):
        """
        Customized closeEvent.
        """

        # log
        self.logger.debug('Close Event')

        # stop_all_threads_and_timer
        self.stop_all_threads_and_timer()

        # parent close event
        self.parent_class.closeEvent(event)


# Run
# ------------------------------------------------------------------
def run(dev=False, dock_it=True):
    """
    Standardized run() method.
    """

    # renderthreads_instance
    renderthreads_instance = RenderThreads(dev=dev, dock_it=dock_it)
    renderthreads_instance.show()
