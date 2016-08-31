
"""
renderthreads_item_delegate
==========================================

Subclass of QStyledItemDelegate to format view
"""


# Import
# ------------------------------------------------------------------
# python
import logging
# PySide
from PySide import QtGui
from PySide import QtCore
# nuke
import nuke

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

# renderthreads_progressbar
from ..gui import renderthreads_progressbar
if(do_reload):
    reload(renderthreads_progressbar)


# Globals
# ------------------------------------------------------------------
# Colors
BLACK = renderthreads_globals.BLACK
RED = renderthreads_globals.RED
BLUE = renderthreads_globals.BLUE


# RenderThreadsItemDelegate
# ------------------------------------------------------------------
class RenderThreadsItemDelegate(QtGui.QStyledItemDelegate):
    """
    Subclass of QStyledItemDelegate.
    """

    # Creation and Initialization
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        RenderThreadsItemDelegate instance factory.
        """

        # renderthreads_item_delegate_instance
        renderthreads_item_delegate_instance = super(RenderThreadsItemDelegate, cls).__new__(cls, args, kwargs)

        return renderthreads_item_delegate_instance

    def __init__(self,
                    parent=None):
        """
        Customize instance.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # parent_class
        self.parent_class = super(RenderThreadsItemDelegate, self)
        self.parent_class.__init__(parent=parent)

        # setObjectName
        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)

    # Size Hint
    # ------------------------------------------------------------------
    def sizeHint(self, option, index):
        """
        Returns the size for a type a certain index represents.
        -----------------------

        Types handled:
        #. Lists
        #. nuke.Node
        """

        # index invalid
        if not(index.isValid()):

            # parent_class sizeHint
            return self.parent_class.sizeHint(option, index)

        # data
        data = index.data(QtCore.Qt.DisplayRole)

        # row & col
        row = index.row()
        col = index.column()

        # check types

        # list
        if(type(data) is list):

            # value_string
            value_string = ''
            for index, value in enumerate(data):

                # last value
                if(index == len(data) - 1):
                    value_string += str(value)
                    continue

                # append
                value_string += str(value + ';\n')

            # text_size
            q_font_metrics = QtGui.QFontMetrics(QtGui.QApplication.font())
            text_size = q_font_metrics.size(0, value_string)
            return text_size

        # nuke.Node
        elif(type(data) is nuke.Node):

            # value_string
            value_string = data.fullName()

            # text_size
            q_font_metrics = QtGui.QFontMetrics(QtGui.QApplication.font())
            text_size = q_font_metrics.size(0, value_string)
            return text_size

        # other type
        else:

            # parent_class sizeHint
            return self.parent_class.sizeHint(option, index)

    # Paint
    # ------------------------------------------------------------------
    def paint(self, painter, option, index):
        """
        Define the look of the current item based on its type.
        -----------------------

        Types handled:
        #. Lists
        #. nuke.Node
        """

        # index invalid
        if not(index.isValid()):

            # parent_class paint
            self.parent_class.paint(painter, option, index)
            return

        # data
        data = index.data(QtCore.Qt.DisplayRole)

        # row & col
        row = index.row()
        col = index.column()

        # list
        if(type(data) is list):

            # paint_list_as_string_with_lines
            self.paint_list_as_string_with_lines(painter, option, data)

        # nuke.Node
        elif(type(data) is nuke.Node):

            # paint_nuke_node
            self.paint_nuke_node(painter, option, data)

        # renderthreads_progressbar.RenderThreadsProgressBar
        elif(type(data) is renderthreads_progressbar.RenderThreadsProgressBar):

            # paint_renderthreads_progressbar
            self.paint_renderthreads_progressbar(painter, option, data)

        # other type
        else:

            # parent_class paint
            self.parent_class.paint(painter, option, index)

    def paint_list_as_string_with_lines(self, painter, option, data):
        """
        Paint list as string with a seperate
        line for each list entry.
        """

        # save painter
        painter.save()

        # value_string
        value_string = ''
        for index, value in enumerate(data):

            # last value
            if(index == len(data) - 1):
                value_string += str(value)
                continue

            # append
            value_string += str(value + ';\n')

        # draw
        painter.drawText(option.rect, QtCore.Qt.AlignLeft, value_string)

        # restore painter
        painter.restore()

    def paint_nuke_node(self, painter, option, data):
        """
        Paint nuke.Node as string
        consisting of nuke_node full name.
        """

        # save painter
        painter.save()

        # value_string
        value_string = str(data.fullName())

        # draw
        painter.drawText(option.rect, QtCore.Qt.AlignLeft, value_string)

        # restore painter
        painter.restore()

    def paint_renderthreads_progressbar(self, painter, option, data, custom=True):
        """
        Paint renderthreads_progressbar.RenderThreadsProgressBar
        as QStyleOptionProgressBar in ui.
        """

        # custom
        if (custom):

            # custom
            self.paint_renderthreads_progressbar_custom(painter, option, data)

        # else (style option):
        else:

            # style option
            self.paint_renderthreads_progressbar_style_option(painter, option, data)

    def paint_renderthreads_progressbar_custom(self, painter, option, data):
        """
        Paint renderthreads_progressbar.RenderThreadsProgressBar
        as QStyleOptionProgressBar in ui.
        """

        # save painter
        painter.save()

        # no pen
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        # draw background
        painter.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.transparent)))
        painter.drawRect(option.rect)

        # maximum
        maximum = float(data.maximum())
        # minimum
        minimum = float(data.minimum())
        # value
        value = float(data.value())

        # percent
        percent = float(0)
        if (value):
            percent = value / maximum

        # x, y, width, height
        x = option.rect.x()
        y = option.rect.y()
        width = float(option.rect.width())
        height = option.rect.height()

        # rect_progress
        rect_progress = QtCore.QRectF(x, y, width * percent, height)

        # draw progress
        painter.setBrush(QtGui.QBrush(QtGui.QColor(RED)))
        painter.drawRect(rect_progress)

        # pen text progress
        painter.setPen(QtGui.QPen(QtGui.QColor(BLACK)))
        painter.drawText(option.rect, QtCore.Qt.AlignCenter, data.text())

        # job_count
        job_count = '{0}'.format(data.maximum() - 1)

        # pen text job_count
        painter.setPen(QtGui.QPen(QtGui.QColor(BLUE)))
        painter.drawText(option.rect, QtCore.Qt.AlignRight, job_count)

        # restore painter
        painter.restore()

    def paint_renderthreads_progressbar_style_option(self, painter, option, data):
        """
        Paint renderthreads_progressbar.RenderThreadsProgressBar
        as QStyleOptionProgressBar in ui.
        """

        # maximum
        maximum = data.maximum()
        # minimum
        minimum = data.minimum()
        # value
        value = data.value()

        # progressbar_option
        progressbar_option = QtGui.QStyleOptionProgressBarV2()
        progressbar_option.rect = option.rect
        progressbar_option.minimum = 0
        progressbar_option.maximum = maximum
        progressbar_option.progress = value
        progressbar_option.text = '{0} %'.format(value)
        progressbar_option.textVisible = True

        # draw
        QtGui.QApplication.instance().style().drawControl(QtGui.QStyle.CE_ProgressBar, progressbar_option, painter)

    # Custom Editors
    # ------------------------------------------------------------------
    def createEditor(self, parent, option, index):
        """
        Virtual method of itemDelegate that creates an editor widget and returns
        it when EditRole requests it.
        """

        # index invalid
        if not(index.isValid()):

            # parent_class setEditorData
            return self.parent_class.createEditor(parent, option, index)

        # row & col
        row = index.row()
        col = index.column()

        # nuke_node
        if(col == 0):

            # editor
            editor = QtGui.QLineEdit(parent=parent)
            return editor

        # other columns
        else:

            # parent_class setEditorData
            return self.parent_class.createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        """
        Virtual method of itemDelegate that sets the editor data after
        the editor is initialized.
        """

        # index invalid
        if not(index.isValid()):

            # parent_class setEditorData
            return self.parent_class.setEditorData(editor, index)

        # data
        data = index.data(QtCore.Qt.DisplayRole)

        # row & col
        row = index.row()
        col = index.column()

        # nuke_node
        if(col == 0):

            # set
            editor.setText(str(data.name()))

        # other columns
        else:

            # evaluate in superclass
            self.parent_class.setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        """
        Set data into model.
        """

        # index invalid
        if not(index.isValid()):

            # parent_class setModelData
            return self.parent_class.setModelData(editor, model, index)

        # row & col
        row = index.row()
        col = index.column()

        # nuke_node
        if(col == 0):

            # set
            model.setData(index, editor.text())

        # other columns
        else:

            # parent_class setModelData
            self.parent_class.setModelData(editor, model, index)
