

"""
renderthreads_services_setup
==========================================

This module encapsulates the creation of services
for the renderthreads tool that run in the background.
This might include timers that trigger something
every once in a while or real daemon threads.
"""


# Import
# ------------------------------------------------------------------
# Python
import logging
import functools
# PySide
from PySide import QtGui
from PySide import QtCore


# Import variable
do_reload = True

# renderthreads

# lib

# renderthreads_globals
import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)

# renderthreads_logging
import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)

# renderthreads_nuke
import renderthreads_nuke
if(do_reload):
    reload(renderthreads_nuke)

# renderthreads_gui_setup
import renderthreads_gui_setup
if(do_reload):
    reload(renderthreads_gui_setup)


# Globals
# ------------------------------------------------------------------


# logger (Module Level)
# ------------------------------------------------------------------
logger = renderthreads_logging.get_logger(__name__)


# Setup
# ------------------------------------------------------------------
def setup_services(wdgt):
    """
    Main method that sets up the entire additional ui.
    """

    # log
    logger.debug('create_services')
    # create_services
    create_services(wdgt)

    # log
    logger.debug('connect_services')
    # connect_services
    connect_services(wdgt)


# Create
# ------------------------------------------------------------------
def create_services(wdgt):
    """
    Create services for RenderThreads instance.
    """

    # create_mvc_validity_check
    create_mvc_validity_check(wdgt)

    # create_memory_check
    create_memory_check(wdgt)

    # create_script_check
    create_script_check(wdgt)


def create_mvc_validity_check(wdgt, interval=1000):
    """
    Setup check to remove invalid entries from
    model. invalid entries are renderthread nodes
    within the model whose nuke node in the
    scene DAG have been deleted. (renderthread nodes
    whose get_nuke_node delivers None)
    """

    # tmr_validity_check
    wdgt.tmr_validity_check = QtCore.QTimer(wdgt)
    wdgt.tmr_validity_check.start(interval)


def create_memory_check(wdgt, interval=2000):
    """
    Create a timer that delivers info about memory
    constantly.
    """

    # tmr_memory_check
    wdgt.tmr_memory_check = QtCore.QTimer(wdgt)
    wdgt.tmr_memory_check.start(interval)


def create_script_check(wdgt, interval=1000):
    """
    Create a timer that delivers the name of
    the current nuke script.
    """

    # tmr_script_check
    wdgt.tmr_script_check = QtCore.QTimer(wdgt)
    wdgt.tmr_script_check.start(interval)


# Connect
# ------------------------------------------------------------------
def connect_services(wdgt):
    """
    Connect services.
    """

    # connect_mvc_validity_check
    connect_mvc_validity_check(wdgt)

    # connect_memory_check
    connect_memory_check(wdgt)

    # connect_script_check
    connect_script_check(wdgt)


def connect_mvc_validity_check(wdgt):
    """
    Connect mvc validity check service.
    """

    # tmr_validity_check
    wdgt.tmr_validity_check.timeout.connect(functools.partial(wdgt.nodes_model.update_invalid))


def connect_memory_check(wdgt):
    """
    Connect memory check service.
    """

    # tmr_memory_check
    wdgt.tmr_memory_check.timeout.connect(functools.partial(renderthreads_nuke.get_memory_info))


def connect_script_check(wdgt):
    """
    Connect script check service.
    """

    # tmr_script_check
    wdgt.tmr_script_check.timeout.connect(functools.partial(renderthreads_gui_setup.update_script_path, wdgt))


# Close
# ------------------------------------------------------------------
def stop_services(wdgt):
    """
    Stop all services created in this module.
    """

    # tmr_validity_check
    wdgt.tmr_validity_check.stop()

    # tmr_memory_check
    wdgt.tmr_memory_check.stop()

    # tmr_script_check
    wdgt.tmr_script_check.stop()
