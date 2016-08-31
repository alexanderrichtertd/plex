

"""
renderthreads_gui_helper
==========================================

This module encapsulates global ui related
helper functions.
"""


# Import
# ------------------------------------------------------------------
# Python
import os
import logging
import webbrowser
# PySide
from PySide import QtGui
from PySide import QtCore


# Import variable
do_reload = True

# renderthreads

# lib

# renderthreads_globals
from .. import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)

# renderthreads_logging
from .. import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)

# lib.gui

# renderthreads_dock_widget
from ..gui import renderthreads_dock_widget
if(do_reload):
    reload(renderthreads_dock_widget)


# Globals
# ------------------------------------------------------------------
# Pathes
THIRD_PARTY_PATH = renderthreads_globals.THIRD_PARTY_PATH


# logger (Module Level)
# ------------------------------------------------------------------
logger = renderthreads_logging.get_logger(__name__)


# Cleanup
# ------------------------------------------------------------------
def get_widget_by_class_name_closure(wdgt_class_name):
    """
    Practicing closures. Doesnt really make sense here, or could at least
    be done much simpler/better.
    Want to try it with filter in order to get more into the builtins.
    """

    def get_widget_by_class_name(wdgt):
        """
        Function that is closed in. Accepts and checks all
        widgets against wdgt_class_name from enclosing function.
        All this mess to be able to use it with filter.
        """
        try:
            if (type(wdgt).__name__ == wdgt_class_name):
                return True
        except:
            pass
        return False

    return get_widget_by_class_name


def get_widget_by_name_closure(wdgt_name):
    """
    Practicing closures. Doesnt really make sense here, or could at least
    be done much simpler/better.
    Want to try it with filter in order to get more into the builtins.
    """

    def get_widget_by_name(wdgt):
        """
        Function that is closed in. Accepts and checks all
        widgets against wdgt_name from enclosing function.
        ALl this mess to be able to use it with filter.
        """
        try:
            if (wdgt.objectName() == wdgt_name):
                return True
        except:
            pass
        return False

    return get_widget_by_name


def check_and_delete_wdgt_instances_with_class_name(wdgt_class_name):
    """
    Search for all occurences with wdgt_class_name and delete them.
    """

    # get_wdgt_closure
    get_wdgt_closure = get_widget_by_class_name_closure(wdgt_class_name)

    # wdgt_list
    wdgt_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    # iterate and delete
    for index, wdgt in enumerate(wdgt_list):

        # Enable when threads are in.
        # try to stop threads
        try:
            wdgt.stop_all_threads_and_timer()
            logger.debug('Stopped threads for wdgt {0}'.format(wdgt.objectName()))
        except:
            pass

        # schedule widget for deletion
        try:
            # log
            logger.debug('Scheduled widget {0} for deletion'.format(wdgt.objectName()))
            # delete
            wdgt.deleteLater()
        except:
            pass

    return wdgt_list


def check_and_delete_wdgt_instances_with_name(wdgt_name):
    """
    Search for all occurences with wdgt_name and delete them.
    """

    # get_wdgt_closure
    get_wdgt_closure = get_widget_by_name_closure(wdgt_name)

    # wdgt_list
    wdgt_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    # iterate and delete
    for index, wdgt in enumerate(wdgt_list):

        # schedule widget for deletion
        try:
            # log
            logger.debug('Scheduled widget {0} for deletion'.format(wdgt.objectName()))
            # delete
            wdgt.deleteLater()
        except:
            pass

    return wdgt_list


# Organize and Compile
# ------------------------------------------------------------------
def load_ui_type(ui_file):
    """
    Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
    and then execute it in a special frame to retrieve the form_class.
    This function return the form and base classes for the given qtdesigner ui file.
    """

    # add path for pysideuic
    import sys
    sys.path.append(THIRD_PARTY_PATH)

    # lazy import

    try:
        # python
        import os
        import logging
        import re
        import shutil
        from cStringIO import StringIO
        import xml.etree.ElementTree as xml
        import types
        # PySide
        from PySide import QtGui
        from PySide import QtCore
        from PySide import QtUiTools
        import pysideuic

    except Exception as exception_instance:
        # log
        logger.debug('Import failed: {0}'.format(exception_instance))
        # return None
        return None

    # compile ui

    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(ui_file, 'r') as f:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = eval('QtGui.%s' % widget_class)

    return form_class, base_class


def get_nuke_main_window():
    """
    Return the Maya main window.
    """

    try:
        # PySide
        from PySide import QtGui
        from PySide import QtCore

    except Exception as exception_instance:

        # log
        logger.debug('Import failed: {0}'.format(exception_instance))
        # return None
        return None

    # ptr_main_window
    ptr_main_window = QtGui.QApplication.activeWindow()

    # if True
    if (ptr_main_window):
        return ptr_main_window

    return None


# Style
# ------------------------------------------------------------------
def correct_styled_background_attribute(wdgt):
    """
    Set QtCore.Qt.WA_StyledBackground True for all widgets.
    Without this attr. set, the background-color stylesheet
    will have no effect on QWidgets. This should replace the
    need for palette settings.
    ToDo:
    Maybe add exclude list when needed.
    """

    # wdgt_list
    wdgt_list = wdgt.findChildren(QtGui.QWidget)  # Return several types ?!?!

    # iterate and set
    for wdgt in wdgt_list:

        # check type
        if(type(wdgt) is QtGui.QWidget):

            # styled_background
            wdgt.setAttribute(QtCore.Qt.WA_StyledBackground, True)


def set_margins_and_spacing_for_child_layouts(wdgt, margin_list=[0, 0, 0, 0]):
    """
    Eliminate margin and spacing for all layout widgets.
    """

    # lyt_classes_list
    lyt_classes_list = [QtGui.QStackedLayout, QtGui.QGridLayout, QtGui.QFormLayout,
                        QtGui.QBoxLayout, QtGui.QVBoxLayout, QtGui.QHBoxLayout, QtGui.QBoxLayout]

    # lyt_list
    lyt_list = []
    for lyt_class in lyt_classes_list:
        lyt_list += [child_wdgt for child_wdgt in wdgt.findChildren(lyt_class)]

    # set margin and spacing
    for lyt in lyt_list:

        # check type
        if(type(lyt) in lyt_classes_list):

            # set
            lyt.setContentsMargins(*margin_list)
            lyt.setSpacing(0)


def insert_spacer_widget(wdgt_or_lyt, minimum_width=0, minimum_height=0, parent=None):
    """
    Insert spacer widget into layout with given min width
    and min height.
    """

    # lyt
    lyt = wdgt_or_lyt

    # not instance of layout
    if not (isinstance(lyt, QtGui.QLayout)):

        # lyt
        lyt = wdgt_or_lyt.layout()

    # wdgt_spacer
    wdgt_spacer = QtGui.QWidget(parent=parent)
    wdgt_spacer.setMinimumWidth(minimum_width)
    wdgt_spacer.setMinimumHeight(minimum_height)

    # add to lyt
    lyt.addWidget(wdgt_spacer)


def prepare_string_for_word_wrap(string_to_prepare, steps=20):
    """
    Insert spaces into string at steps
    to make sure word wrap has an effect.
    This aids the display of long, continous
    strings in widgets with word-wrap enabled.
    """

    # string_to_prepare_broken
    string_to_prepare_broken = ''

    # step_count
    step_count = 0

    # iterate
    for char in string_to_prepare:

        # char is whitespace
        if (char == ' '):

            # reset step_count
            step_count = 0

        # else
        else:

            # check step_count
            if (step_count > steps):

                # insert space
                char = ' {0}'.format(char)

                # reset step_count
                step_count = 0

            # else
            else:

                # increment step_count
                step_count += 1

        # append
        string_to_prepare_broken += char

    # return
    return string_to_prepare_broken


# Docking
# ------------------------------------------------------------------
def make_dockable(wdgt):
    """
    Make this wdgt dockable.
    """

    # nuke_main_window
    nuke_main_window = get_nuke_main_window()

    # q_main_window_list
    q_main_window_list = nuke_main_window.findChildren(QtGui.QMainWindow)
    # check
    if not (q_main_window_list):
        # log
        logger.debug('Current Nuke configuration has no QMainWindow instance which is needed for docking\
Not performing dock behaviour.')
        return

    # q_main_window
    q_main_window = q_main_window_list[0]

    # wdgt_dock
    wdgt_dock = renderthreads_dock_widget.RenderThreadsDockWidget(parent=q_main_window)
    wdgt_dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)

    # set wdgt
    wdgt_dock.setWidget(wdgt)

    # add to maya main window
    q_main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, wdgt_dock)


# File/Directory picking
# ------------------------------------------------------------------

def pick_file(wdgt_display=None, filter_string=None):
    """
    Pick a file and display it on wdgt_display
    if set.
    """

    # file_path
    file_path, selected_filter = QtGui.QFileDialog.getOpenFileName(filter=filter_string)
    file_path = str(file_path)

    # check
    if not (file_path):
        # log
        logger.debug('File path invalid. Returning None.')
        return None

    # absolute path
    file_path = os.path.abspath(file_path).replace('\\', '/')

    # wdgt_display
    if (wdgt_display):

        # setText()
        if (type(wdgt_display) is QtGui.QLineEdit or
                type(wdgt_display) is QtGui.QLabel):

            # set
            wdgt_display.setText(file_path)

        # unknown
        else:

            # log
            logger.debug('wdgt_display type {0} is unknown. File path cannot be set.'.format(type(wdgt_display)))

    # log
    logger.debug('{0}'.format(file_path))

    # return
    return file_path


# Web
# ------------------------------------------------------------------
def open_website(url, new=2):
    """
    Wrapper around webbrowser.open().
    """

    try:
        # open
        webbrowser.open(url, new)
    except:
        # log
        logger.error('Error opening {0}'.format(url))
