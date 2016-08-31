
"""
renderthreads_command_line_flag_widget
==========================================

Widget that offers a checkbox to enable/disable the flag.
A label that represents the flag and a tooltip that explains
it plus an input widget in case the flag needs some parameters.
The input widget can be set as long as it supports a certain
interface.
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
TEXT_DIVIDER = renderthreads_globals.TEXT_DIVIDER


# CommandLineFlag
# ------------------------------------------------------------------
class CommandLineFlag(QtGui.QFrame):
    """
    Widget that offers a checkbox to enable/disable the flag.
    A label that represents the flag and a tooltip that explains
    it plus an input widget in case the flag needs some parameters.
    The input widget can be set as long as it supports a certain
    interface.
    """

    # Signals
    # ------------------------------------------------------------------
    state_changed = QtCore.Signal()
    parameter_changed = QtCore.Signal()

    # Create and initialize
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        CommandLineFlag instance factory.
        """

        # command_line_flag_instance
        command_line_flag_instance = super(CommandLineFlag, cls).__new__(cls, args, kwargs)

        return command_line_flag_instance

    def __init__(self,
                    flag='',
                    tooltip='',
                    state=True,
                    checkable=True,
                    wdgt_parameter=None,
                    parent=None):
        """
        CommandLineFlag instance customization.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # parent_class
        self.parent_class = super(CommandLineFlag, self)
        # super class constructor
        self.parent_class.__init__(parent)

        # objectName
        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        # flag
        self.set_flag(flag)
        # tooltip
        self.tooltip = tooltip
        # state
        self.set_state(state)
        # checkable
        self.checkable = checkable
        # wdgt_parameter
        self.wdgt_parameter = wdgt_parameter

        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)

        # container_protocol_index_size
        self.container_protocol_index_size = 5

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

        # lyt_command_line_flag
        self.lyt_command_line_flag = QtGui.QHBoxLayout(self)

        # chkbx_state
        self.chkbx_state = QtGui.QCheckBox(text='')
        self.chkbx_state.setObjectName(self.__class__.__name__ + type(self.chkbx_state).__name__)
        self.chkbx_state.setChecked(self.get_state())
        self.chkbx_state.setEnabled(self.checkable)
        self.lyt_command_line_flag.addWidget(self.chkbx_state)

        # wdgt_spacer_chkbx_and_flag
        self.wdgt_spacer_chkbx_and_flag = QtGui.QWidget()
        self.wdgt_spacer_chkbx_and_flag.setMinimumWidth(10)
        self.wdgt_spacer_chkbx_and_flag.setMaximumWidth(10)
        self.lyt_command_line_flag.addWidget(self.wdgt_spacer_chkbx_and_flag)

        # lbl_flag
        self.lbl_flag = QtGui.QLabel(text=self._flag)
        self.lbl_flag.setObjectName(self.__class__.__name__ + type(self.lbl_flag).__name__)
        self.lbl_flag.setEnabled(self.get_state())
        self.lyt_command_line_flag.addWidget(self.lbl_flag)

        # wdgt_parameter
        if (self.wdgt_parameter):

            # add stretch
            self.lyt_command_line_flag.addStretch()

            # setEnabled
            self.wdgt_parameter.setEnabled(self.get_state())

            # addWidget
            self.lyt_command_line_flag.addWidget(self.wdgt_parameter)

        # else
        else:

            # addStretch
            self.lyt_command_line_flag.addStretch()

    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        # chkbx_state
        self.chkbx_state.toggled.connect(self.set_state)

        # self.state_changed.
        self.state_changed.connect(self.update_ui)

        # wdgt_parameter
        if (self.wdgt_parameter):

            # connect_parameter
            self.connect_parameter()

    def connect_parameter(self):
        """
        Connect parameter_changed signal to specific
        parameter change signal of wdgt_parameter.
        """

        # not existing
        if not (self.wdgt_parameter):
            # log
            self.logger.debug('wdgt_parameter not set on {0}. Not connecting signal parameter_changed'.format(self))
            return None

        # textChanged
        if (type(self.wdgt_parameter) is QtGui.QLineEdit):

            # connect
            self.wdgt_parameter.textChanged.connect(self.parameter_changed)

        # currentIndexChanged
        if (type(self.wdgt_parameter) is QtGui.QComboBox):

            # connect
            self.wdgt_parameter.currentIndexChanged.connect(self.parameter_changed)

        # valueChanged
        if (type(self.wdgt_parameter) is QtGui.QSpinBox or
                type(self.wdgt_parameter) is QtGui.QDoubleSpinBox or
                type(self.wdgt_parameter) is QtGui.QDial or
                type(self.wdgt_parameter) is QtGui.QSlider):

            # connect
            self.wdgt_parameter.valueChanged.connect(self.parameter_changed)

    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        # correct_styled_background_attribute
        renderthreads_gui_helper.correct_styled_background_attribute(self)

        # set_margins_and_spacing_for_child_layouts
        renderthreads_gui_helper.set_margins_and_spacing_for_child_layouts(self)

    # Properties
    # ------------------------------------------------------------------
    def get_state(self):
        """
        Return self_state.
        """

        return self._state

    def set_state(self, value):
        """
        Set self._state and emit
        state changed signal.
        """

        # set state
        self._state = value

        # emit
        self.state_changed.emit()

    state = property(get_state, set_state, None, "State of the flag. Either True or False.\
An update of this Descriptor (set) causes an update of the ui.")
    """
    State of the flag. Either True or False.
    An update of this Descriptor (set) causes an
    update of the ui.
    """

    def get_flag_without_parameter(self):
        """
        Return self._flag. This is not the function
        from the property, which adds a possible
        parameter value from wdgt_parameter.
        This method is usefull for string comparison
        for example.
        """

        return self._flag

    def get_flag(self):
        """
        Return self._flag and format it together.
        This method always delivers the entire
        flag as it could be used on the command line.
        """

        # flag_string
        flag_string = self._flag

        # wdgt_parameter
        if (self.wdgt_parameter):

            # parameter_value
            parameter_value = self.get_parameter_as_string()

            # string not empty
            if (parameter_value):

                # append
                flag_string = flag_string + ' ' + parameter_value

        return flag_string

    def set_flag(self, value):
        """
        Set self._flag.
        """

        # set flag
        self._flag = value

    flag = property(get_flag, set_flag, None, "Descriptor that cascades access to self._flag.\
The getter of the property will always return the flag readily formatted for command line use.\
The setter just sets self._flag.")
    """
    Descriptor that cascades access to self._flag.
    The getter of the property will always return the
    flag readily formatted for command line use.
    The setter just sets self._flag.
    """

    # Getter and Setter
    # ------------------------------------------------------------------
    def get_parameter(self):
        """
        Return parameter value from wdgt_parameter,
        if it exists. If it doesnt exist, rturn None.
        """

        # not existing
        if not (self.wdgt_parameter):
            # log
            self.logger.debug('wdgt_parameter not set on {0}. Returning None'.format(self))
            return None

        # text()
        if (type(self.wdgt_parameter) is QtGui.QLineEdit):

            # get_parameter_with_text
            return self.get_parameter_with_text()

        # currentText()
        if (type(self.wdgt_parameter) is QtGui.QComboBox):

            # get_parameter_with_currentText
            return self.get_parameter_with_currentText()

        # value()
        if (type(self.wdgt_parameter) is QtGui.QSpinBox or
                type(self.wdgt_parameter) is QtGui.QDoubleSpinBox or
                type(self.wdgt_parameter) is QtGui.QDial or
                type(self.wdgt_parameter) is QtGui.QSlider):

            # get_parameter_with_value
            return self.get_parameter_with_value()

    def get_parameter_as_string(self):
        """
        Return parameter as string.
        Return empty string if parameter value
        is None.
        """

        # parameter_value
        parameter_value = self.get_parameter()
        # check
        if (parameter_value is None):
            return ''

        # return
        return str(parameter_value)

    def get_parameter_with_text(self):
        """
        Return value for wdgt_parameter if
        wdgt_parameter is QtGui.QLineEdit.
        """

        return self.wdgt_parameter.text()

    def get_parameter_with_currentText(self):
        """
        Return value for wdgt_parameter if
        wdgt_parameter is QtGui.QComboBox.
        """

        return self.wdgt_parameter.currentText()

    def get_parameter_with_value(self):
        """
        Return value for wdgt_parameter if
        wdgt_parameter is QtGui.QSpinBox.
        """

        return self.wdgt_parameter.value()

    def set_tooltip(self):
        """
        Set tooltip as combination of current flag
        and user entered tooltip string.
        """

        # tooltip
        tooltip = '{0}\n{1}\n{2}'.format(self.get_flag(), TEXT_DIVIDER, self.tooltip)

        # set tooltip
        self.setToolTip(tooltip)

    # Operator overrides
    # ------------------------------------------------------------------
    def __eq__(self, other):
        """=="""
        return self.get_flag_without_parameter() == other.get_flag_without_parameter()

    def __ne__(self, other):
        """!="""
        return self.get_flag_without_parameter() != other.get_flag_without_parameter()

    def __gt__(self, other):
        """>"""
        return self.get_flag_without_parameter() > other.get_flag_without_parameter()

    def __lt__(self, other):
        """<"""
        return self.get_flag_without_parameter() < other.get_flag_without_parameter()

    def __ge__(self, other):
        """>="""
        return self.get_flag_without_parameter() >= other.get_flag_without_parameter()

    def __le__(self, other):
        """<="""
        return self.get_flag_without_parameter() <= other.get_flag_without_parameter()

    def __hash__(self):
        return hash(self.get_flag_without_parameter())

    def __len__(self):
        """
        Return number of properties.
        [0]flag
        [1]_flag (without possible parameter)
        [2]state
        [3]wdgt_parameter
        [4]parameter
        """
        return self.container_protocol_index_size

    def __getitem__(self, key):
        """
        Return values when accessed by index operator.
        See __len__ for a list.
        """

        # TypeError
        if not (type(key) == int):
            raise TypeError

        # KeyError
        if (key < 0 and
                key > self.container_protocol_index_size - 1):
            raise KeyError

        # 0
        if (key == 0):
            return self.get_flag()
        # 1
        elif (key == 1):
            return self.get_flag_without_parameter()
        # 2
        elif (key == 2):
            return self.get_state()

        # 3
        elif (key == 3):
            return self.wdgt_parameter

        # 4
        elif (key == 4):
            return self.get_parameter()

    # Slots
    # ------------------------------------------------------------------
    def update_ui(self):
        """
        Set enabled/disabled on widgets depending
        on state
        """

        # state
        state = self.get_state()
        # log
        self.logger.debug('state {0}'.format(state))

        # lbl_flag
        self.lbl_flag.setEnabled(state)
        # log
        self.logger.debug('lbl_flag {0}'.format(self.lbl_flag.isEnabled()))

        # wdgt_parameter
        if (self.wdgt_parameter):
            self.wdgt_parameter.setEnabled(state)
            # log
            self.logger.debug('wdgt_parameter {0}'.format(self.wdgt_parameter.isEnabled()))

    def force_parameter_enabled(self, status):
        """
        This method is for the rare cases where you want
        the lbl_flag and wdgt_parameter stati (enabled or
        disabled) to be different from the flag state.
        This is only useful if you want a locked input
        for wdgt_parameter on an activated flag. An example
        would be the flg_X or flg_F.
        """

        # lbl_flag
        self.lbl_flag.setEnabled(status)

        # wdgt_parameter
        if (self.wdgt_parameter):
            self.wdgt_parameter.setEnabled(status)

    # Events
    # ------------------------------------------------------------------
    def event(self, event):
        """
        Override event to catch ToolTip event.
        """

        # check event type
        if (event.type() == QtCore.QEvent.ToolTip):

            # set_tooltip
            self.set_tooltip()

            # return
            return self.parent_class.event(event)

        # return
        return self.parent_class.event(event)
