
"""
renderthreads_view
==========================================

Subclass of QTableView to display renderthread
nodes.
"""


# Import
# ------------------------------------------------------------------
# python
import logging
# PySide
from PySide import QtGui
from PySide import QtCore


#  Import variable
do_reload = True


#  renderthreads

#  lib

#  renderthreads_globals
from .. import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)

#  renderthreads_logging
from .. import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)


# RenderThreadsView
# ------------------------------------------------------------------
class RenderThreadsView(QtGui.QTableView):
    """
    Subclass of QTableView.
    """

    def __new__(cls, *args, **kwargs):
        """
        RenderThreadsView instance factory.
        """

        # renderthreads_view_instance
        renderthreads_view_instance = super(RenderThreadsView, cls).__new__(cls, args, kwargs)

        return renderthreads_view_instance

    def __init__(self,
                parent=None):
        """
        Customize instance.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # parent_class
        self.parent_class = super(RenderThreadsView, self)
        self.parent_class.__init__(parent=parent)

        # setObjectName
        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)
