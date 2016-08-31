

"""
renderthreads_signal_remapper
==========================================

This module encapsulates a handy signal remapper
widget specific to the renderthreads tool.
SignalRemapper remaps signals with from input
ranges or values to the needed signals or values.
"""


# Import
# ------------------------------------------------------------------
# Python
import os
import logging
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


# Globals
# ------------------------------------------------------------------


# SignalRemapper
# ------------------------------------------------------------------
class SignalRemapper(QtCore.QObject):
    """
    Simple class that remaps signals from
    input widgets whose values dont match
    the needed format.
    For example it remaps the logging
    slider signal from a range of 1-5
    to the real logging constant values.
    (DEBUG, INFO etc.)
    """

    # Signals
    # ------------------------------------------------------------------
    sgnl_set_logging = QtCore.Signal(int)

    # Creation and Initialization
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        SignalRemapper instance factory.
        """

        # signal_remapper_instance
        signal_remapper_instance = super(SignalRemapper, cls).__new__(cls, args, kwargs)

        return signal_remapper_instance

    def __init__(self):
        """
        Customize instance.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # parent_class
        self.parent_class = super(SignalRemapper, self)
        self.parent_class.__init__()

        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)

    # Slots
    # ------------------------------------------------------------------

    @QtCore.Slot(int)
    def remap_logging(self, value):
        """
        Remap for logging.
        """

        # emit
        self.sgnl_set_logging.emit(value * 10)
