
"""
renderthreads_slider_widget
==========================================

Widget that offers a label used as header and a slider
with signals and slots.
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

# lib.gui

# renderthreads_gui_helper
import renderthreads_gui_helper
if(do_reload):
    reload(renderthreads_gui_helper)


# Globals
# ------------------------------------------------------------------


# Slider
# ------------------------------------------------------------------
class Slider(QtGui.QWidget):
    """
    Widget that offers a label used as header and a slider
    with signals and slots.
    """

    # Signals
    # ------------------------------------------------------------------
    value_changed = QtCore.Signal(int)

    # Create and initialize
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        Slider instance factory.
        """

        # slider_instance
        slider_instance = super(Slider, cls).__new__(cls, args, kwargs)

        return slider_instance

    def __init__(self,
                    header='Slider',
                    minimum=0,
                    maximum=99,
                    initial_value=50,
                    tracking=True,
                    parent=None):
        """
        Slider instance customization.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # parent_class
        self.parent_class = super(Slider, self)
        # super class constructor
        self.parent_class.__init__(parent)

        # objectName
        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        # initial_value
        self.initial_value = initial_value
        # minimum
        self.minimum = minimum
        # maximum
        self.maximum = maximum
        # header
        self.header = header
        # tracking
        self.tracking = tracking

        # wdgt_spinbox_complete
        self.wdgt_spinbox_complete = None

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
        Setup additional UI.
        """

        # lyt_slider
        self.lyt_slider = QtGui.QVBoxLayout(self)

        # lbl_slider
        self.lbl_slider = QtGui.QLabel(text=self.header)
        self.lbl_slider.setObjectName(self.__class__.__name__ + type(self.lbl_slider).__name__)
        self.lyt_slider.addWidget(self.lbl_slider)

        # wdgt_slider_and_display
        self.wdgt_slider_and_display = QtGui.QWidget()
        self.lyt_slider.addWidget(self.wdgt_slider_and_display)

        # lyt_wdgt_slider_and_display
        self.lyt_wdgt_slider_and_display = QtGui.QHBoxLayout(self.wdgt_slider_and_display)

        # slider
        self.slider = QtGui.QSlider()
        self.slider.setObjectName(self.__class__.__name__ +
                                    type(self.slider).__name__)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setRange(self.minimum, self.maximum)
        self.slider.setValue(self.initial_value)
        self.slider.setTracking(self.tracking)
        self.lyt_wdgt_slider_and_display.addWidget(self.slider)

        # lcd_slider_value
        self.lcd_slider_value = QtGui.QLCDNumber()
        self.lcd_slider_value.display(self.initial_value)
        self.lyt_wdgt_slider_and_display.addWidget(self.lcd_slider_value)

    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        # slider
        self.slider.valueChanged.connect(self.on_value_changed)

    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        # correct_styled_background_attribute
        renderthreads_gui_helper.correct_styled_background_attribute(self)

        # set_margins_and_spacing_for_child_layouts
        renderthreads_gui_helper.set_margins_and_spacing_for_child_layouts(self)

    # Getter and Setter
    # ------------------------------------------------------------------
    def set_tick_position(self, position):
        """
        Set Tick position and appearance on slider.
        Tick visibility is off by default.
        """

        self.slider.setTickPosition(position)

    def set_tick_interval(self, value):
        """
        Set Tick interval value. This has no implications
        on the slider steps.
        """

        self.slider.setTickInterval(value)

    def get_value(self):
        """
        Return self.slider.value().
        """

        return self.slider.value()

    # Slots
    # ------------------------------------------------------------------
    @QtCore.Slot(int)
    def on_value_changed(self, value):
        """
        Value of spinbox changed.
        """

        # change display
        self.lcd_slider_value.display(value)

        # emit value_changed
        self.value_changed.emit(value)
