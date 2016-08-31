
"""
renderthreads_progressbar
==========================================

Subclass of QProgressBar to provide ability for custom type checks
and events.
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
# Colors
BLUE = renderthreads_globals.BLUE


# RenderThreadsProgressBar class
# ------------------------------------------------------------------
class RenderThreadsProgressBar(QtGui.QProgressBar):
    """
    Subclass of QProgressBar to provide ability for
    custom type checks and events.
    """

    # Signals
    # ------------------------------------------------------------------

    # Create and initialize
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        RenderThreadsProgressBar instance factory.
        """

        # renderthreads_progressbar_instance
        renderthreads_progressbar_instance = super(RenderThreadsProgressBar, cls).__new__(cls, args, kwargs)

        return renderthreads_progressbar_instance

    def __init__(self,
                parent=None):
        """
        RenderThreadsProgressBar instance customization.
        """

        # parent_class
        self.parent_class = super(RenderThreadsProgressBar, self)
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

        pass

    # Slots
    # ------------------------------------------------------------------
    @QtCore.Slot(int)
    def increment_range(self, step=1):
        """
        Increment range by step.
        """

        # set
        self.setMaximum(self.maximum() + step)

    @QtCore.Slot(int)
    def increment_value(self, step=1):
        """
        Increment value by step.
        """

        # new_value
        new_value = self.value() + step

        # if new value == maximum - 1
        if (new_value >= (self.maximum() - 1)):

            # set
            self.setValue(0)
            # reset
            self.setRange(0, 1)

        # else increment
        else:

            # set
            self.setValue(new_value)

    # Events
    # ------------------------------------------------------------------
    def closeEvent(self, event):
        """
        Customized closeEvent
        """

        # parent close event
        self.parent_class.closeEvent(event)

    def paintEvent(self, event):
        """
        Customized paintEvent to display complete
        job count.
        """

        # parent class paint event
        self.parent_class.paintEvent(event)

        # painter
        painter = QtGui.QPainter(self)

        # painter
        painter.setPen(QtGui.QColor(BLUE))

        # font
        font = QtGui.QFont()
        font.setBold(True)
        painter.setFont(font)

        # job_count
        job_count = 'jobs: {0}'.format(self.maximum() - 1)

        # drawText
        painter.drawText(self.rect(), QtCore.Qt.AlignRight, job_count)
