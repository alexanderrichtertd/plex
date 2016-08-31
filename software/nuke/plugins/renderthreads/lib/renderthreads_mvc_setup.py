

"""
renderthreads_mvc_setup
==========================================

This module encapsulates the creation of the
renderthreads MVC.
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

# lib.mvc

# renderthreads_model
from mvc import renderthreads_model
if(do_reload):
    reload(renderthreads_model)

# renderthreads_view
from mvc import renderthreads_view
if(do_reload):
    reload(renderthreads_view)

# renderthreads_item_delegate
from mvc import renderthreads_item_delegate
if(do_reload):
    reload(renderthreads_item_delegate)


# Globals
# ------------------------------------------------------------------


# logger (Module Level)
# ------------------------------------------------------------------
logger = renderthreads_logging.get_logger(__name__)


# Setup
# ------------------------------------------------------------------
def setup_mvc(wdgt):
    """
    Main method that sets up the entire additional ui.
    """

    # log
    logger.debug('create_mvc')
    # create_mvc
    create_mvc(wdgt)

    # log
    logger.debug('connect_mvc')
    # connect_mvc
    connect_mvc(wdgt)


# Create
# ------------------------------------------------------------------
def create_mvc(wdgt):
    """
    Create MVC for RenderThreads instance.
    """

    # nodes_view
    wdgt.nodes_view = renderthreads_view.RenderThreadsView(parent=wdgt)
    wdgt.nodes_view.setWordWrap(True)
    wdgt.nodes_view.setShowGrid(False)
    # set resize mode for horizontal header
    wdgt.nodes_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
    wdgt.nodes_view.horizontalHeader().setStretchLastSection(False)
    wdgt.nodes_view.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
    wdgt.nodes_view.setAlternatingRowColors(True)
    # objectNames
    wdgt.nodes_view.setObjectName('nodes_view')
    wdgt.nodes_view.horizontalHeader().setObjectName('nodes_view_horizontal_header')
    wdgt.nodes_view.verticalHeader().setObjectName('nodes_view_vertical_header')
    # hide vertical header
    wdgt.nodes_view.verticalHeader().hide()
    # context menu
    wdgt.nodes_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    # add to ui
    wdgt.frm_nodes.layout().addWidget(wdgt.nodes_view)

    # nodes_item_delegate
    wdgt.nodes_item_delegate = renderthreads_item_delegate.RenderThreadsItemDelegate(parent=wdgt)
    wdgt.nodes_item_delegate.setObjectName('nodes_item_delegate')
    # set in view
    wdgt.nodes_view.setItemDelegate(wdgt.nodes_item_delegate)

    # nodes_model
    wdgt.nodes_model = renderthreads_model.RenderThreadsModel(parent=wdgt)
    # set model in view
    wdgt.nodes_view.setModel(wdgt.nodes_model)

    # nodes_selection_model
    wdgt.nodes_selection_model = QtGui.QItemSelectionModel(wdgt.nodes_model)
    wdgt.nodes_view.setSelectionModel(wdgt.nodes_selection_model)


# Connect
# ------------------------------------------------------------------

def connect_mvc(wdgt):
    """
    Connect MVC components.
    """

    pass
