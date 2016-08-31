
"""
renderthreads_dock_widget
==========================================

Subclass of QDockWidget to provide ability for custom type checks.
"""


# Import
# ------------------------------------------------------------------
# python
import logging
# PySide
from PySide import QtGui
from PySide import QtCore


# Import variable
do_reload = True


# renderthreads

# lib

# renderthreads_logging
from .. import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)

# lib.gui

# renderthreads_stylesheets
import renderthreads_stylesheets
if(do_reload):
    reload(renderthreads_stylesheets)


# Globals
# ------------------------------------------------------------------


# RenderThreadsDockWidget class
# ------------------------------------------------------------------
class RenderThreadsDockWidget(QtGui.QDockWidget):
    """
    Subclass of QWidget to allow for custom styling and
    type checking.
    """

    # Signals
    # ------------------------------------------------------------------

    # Create and initialize
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        RenderThreadsDockWidget instance factory.
        """

        # renderthreads_dock_widget_instance
        renderthreads_dock_widget_instance = super(RenderThreadsDockWidget, cls).__new__(cls, args, kwargs)

        return renderthreads_dock_widget_instance

    def __init__(self,
                parent=None):
        """
        RenderThreadsDockWidget instance customization.
        """

        # parent_class
        self.parent_class = super(RenderThreadsDockWidget, self)
        self.parent_class.__init__(parent)

        # objectName
        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------

        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)

        # Init procedure
        # ------------------------------------------------------------------

        # setup_ui
        self.setup_ui()

        # connect_ui
        self.connect_ui()

        # style_ui
        self.style_ui()

    # UI setup methods
    # ------------------------------------------------------------------

    def setup_ui(self):
        """
        Setup UI.
        """

        pass

    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        pass

    def style_ui(self):
        """
        Style UI widgets.
        """

        # set_stylesheet
        self.setStyleSheet(renderthreads_stylesheets.get_stylesheet())

    # Events
    # ------------------------------------------------------------------

    def closeEvent(self, event):
        """
        Customized closeEvent
        """

        # log
        self.logger.debug('Close Event')

        try:

            # stop_all_threads_and_timer
            self.widget().stop_all_threads_and_timer()

        except:

            # log
            self.logger.debug('Error stopping threads and timers for widget().')

        # parent close event
        self.parent_class.closeEvent(event)
