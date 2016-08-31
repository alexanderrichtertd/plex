
"""
renderthreads_model
==========================================

Subclass of QAbstractTableModel to display
and edit renderthreads nodes.
"""


# Import
# ------------------------------------------------------------------
# python
import os
import logging
import re
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

# renderthreads_nuke
from .. import renderthreads_nuke
if(do_reload):
    reload(renderthreads_nuke)

# lib.mvc

# renderthreads_node
import renderthreads_node
if(do_reload):
    reload(renderthreads_node)


# Globals
# ------------------------------------------------------------------
TEXT_DIVIDER = renderthreads_globals.TEXT_DIVIDER


# RenderThreadsModel
# ------------------------------------------------------------------
class RenderThreadsModel(QtCore.QAbstractTableModel):
    """
    Class customized to display
    renderthreads nodes.
    ------------------------------------------

    **Expects the following format:**
    .. info::

        data_list = [[renderthreads_node], [renderthreads_node],
                        [renderthreads_node], [renderthreads_node],
                        ......]
    """

    # Creation and Initialization
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        RenderThreadsModel instance factory.
        """

        # renderthreads_model_instance
        renderthreads_model_instance = super(RenderThreadsModel, cls).__new__(cls, args, kwargs)

        return renderthreads_model_instance

    def __init__(self, parent=None):
        """
        Customize instance.
        """

        # super and objectName
        # ------------------------------------------------------------------
        self.parent_class = super(RenderThreadsModel, self)
        self.parent_class.__init__(parent=parent)

        # setObjectName
        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        # header_name_list
        self.header_name_list = ['nuke_node', 'start_frame', 'end_frame', 'progress', 'priority']

        # data_list
        self.data_list = [[]]

        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)

    # Methods
    # ------------------------------------------------------------------
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """
        Return header description for section.
        """

        # horizontal
        if(orientation == QtCore.Qt.Horizontal):

            # DisplayRole
            if (role == QtCore.Qt.DisplayRole):
                return self.format_string(self.header_name_list[section])

        # vertical
        elif(orientation == QtCore.Qt.Vertical):

            # DisplayRole
            if (role == QtCore.Qt.DisplayRole):
                return section

        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, parent):
        """
        Return row count.
        """

        # if any item in list return len
        if (any(self.data_list)):
            return len(self.data_list)

        # else 0
        return 0

    def columnCount(self, parent):
        """
        Return column count.
        """

        return len(self.header_name_list)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        Return data for current index. The returned data is
        rendered by QItemDelegate.
        """

        # index invalid
        if not(index.isValid()):
            # log
            self.logger.debug('Index {0} not valid.'.format(index))
            # evaluate in superclass
            return None

        # row & col
        row = index.row()
        col = index.column()

        # current_header
        current_header = self.header_name_list[col]

        # renderthreads_node
        renderthreads_node = self.data_list[row][0]

        # nuke_node exists
        if not(renderthreads_node.nuke_node_exists()):
            # return
            return None

        # DisplayRole and EditRole (return identical in most cases,
        # if not then do recheck later)
        if (role == QtCore.Qt.DisplayRole or
                role == QtCore.Qt.EditRole):

            # column nuke_node
            if (current_header == self.header_name_list[0]):

                # nuke_node
                nuke_node = renderthreads_node.nuke_node
                return nuke_node

            # column start_frame
            elif (current_header == self.header_name_list[1]):

                # start_frame
                start_frame = renderthreads_node.start_frame
                return start_frame

            # column end_frame
            elif (current_header == self.header_name_list[2]):

                # end_frame
                end_frame = renderthreads_node.end_frame
                return end_frame

            # column progress
            elif (current_header == self.header_name_list[3]):

                # progress
                progress = renderthreads_node.get_progressbar()
                return progress

            # column priority
            elif (current_header == self.header_name_list[4]):

                # priority
                priority = renderthreads_node.get_priority()
                return priority

            else:
                # evaluate in superclass
                return None

        # TextAlignmentRole
        elif (role == QtCore.Qt.TextAlignmentRole):

            # column start_frame
            if (current_header == self.header_name_list[1]):

                return QtCore.Qt.AlignCenter

            # column end_frame
            elif (current_header == self.header_name_list[2]):

                return QtCore.Qt.AlignCenter

            # column priority
            elif (current_header == self.header_name_list[4]):

                return QtCore.Qt.AlignCenter

            else:

                # left
                return QtCore.Qt.AlignLeft

        # ToolTipRole
        elif (role == QtCore.Qt.ToolTipRole):

            # column nuke_node
            if (current_header == self.header_name_list[0]):

                # nuke_node_full_name
                nuke_node_full_name = renderthreads_node.fullName()
                return nuke_node_full_name

            # column start_frame
            elif (current_header == self.header_name_list[1]):

                # start_frame
                start_frame = renderthreads_node.start_frame
                return start_frame

            # column end_frame
            elif (current_header == self.header_name_list[2]):

                # end_frame
                end_frame = renderthreads_node.end_frame
                return end_frame

            # column progress
            elif (current_header == self.header_name_list[3]):

                # progress_value
                progress_value = renderthreads_node.get_progressbar().text()
                return progress_value

            # column priority
            elif (current_header == self.header_name_list[4]):

                # priority
                priority = renderthreads_node.get_priority()

                # priority_tooltip
                priority_tooltip = 'Priority: {0}\n\
{1}\n\
Priority cannot be adjusted after job has been added.'.format(priority, TEXT_DIVIDER)

                # return
                return priority_tooltip

            else:
                # evaluate in superclass
                return None

        else:

            # evaluate in superclass
            return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Set data method for model.
        """

        # index invalid
        if not(index.isValid()):
            # log
            self.logger.debug('Index {0} not valid.'.format(index))
            # evaluate in superclass
            return self.parent_class.setData(index, value, role)

        # row & col
        row = index.row()
        col = index.column()

        # current_header
        current_header = self.header_name_list[col]

        # renderthreads_node
        renderthreads_node = self.data_list[row][0]

        # nuke_node exists
        if not(renderthreads_node.nuke_node_exists()):
            return False

        # EditRole
        if (role == QtCore.Qt.EditRole):

            # column nuke_node
            if (current_header == self.header_name_list[0]):

                # validate
                if(self.validate_value_for_nuke_node(value)):

                    # set value
                    renderthreads_node.setName(value)
                    # data changed signal
                    self.dataChanged.emit(index, index)

                    return True

                return False

            # column start_frame
            elif (current_header == self.header_name_list[1]):

                # validate
                if(self.validate_value_for_start_frame(value)):

                    # set value
                    renderthreads_node.start_frame = value
                    # data changed signal
                    self.dataChanged.emit(index, index)

                    return True

                return False

            # column end_frame
            elif (current_header == self.header_name_list[2]):

                # validate
                if(self.validate_value_for_end_frame(value)):

                    # set value
                    renderthreads_node.end_frame = value
                    # data changed signal
                    self.dataChanged.emit(index, index)

                    return True

                return False

            # column priority
            elif (current_header == self.header_name_list[4]):

                # validate
                if(self.validate_value_for_priority(value)):

                    # set value
                    renderthreads_node.set_priority(value)
                    # data changed signal
                    self.dataChanged.emit(index, index)

                    # Setting the priority via signal on the
                    # command objects works. However it has
                    # no influence of the PriorityQueue since
                    # priority queues cannot be updated.
                    # nuke_node_full_name
                    nuke_node_full_name = renderthreads_node.fullName()
                    # negated_value
                    negated_value = 101 - value
                    # emit sgnl_command_set_priority_for_identifier
                    renderthreads_node.sgnl_command_set_priority_for_identifier.emit(nuke_node_full_name,
                                                                                        negated_value)

                    return True

                return False

            else:
                # evaluate in superclass
                return self.parent_class.setData(index, value, role)

        else:
            # evaluate in superclass
            return self.parent_class.setData(index, value, role)

    def flags(self, index):
        """
        Return flags for indices.
        """

        # index invalid
        if not(index.isValid()):

            # log
            self.logger.debug('Index {0} not valid.'.format(index))
            # evaluate in superclass
            return self.parent_class.flags(index)

        # row & col
        row = index.row()
        col = index.column()

        # current_header
        current_header = self.header_name_list[col]

        # progress
        if (current_header == self.header_name_list[3]):

            # enabled
            return QtCore.Qt.ItemIsEnabled

        # else
        else:

            # enabled, editable, selectable
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable

    def update(self, data_list):
        """
        Set data_list and reset display.
        """

        # sorted_data_list
        sorted_data_list = self.sort_data_list(data_list)
        # set sorted_data_list
        self.data_list = sorted_data_list
        # reset
        self.reset()

    def update_flat(self, data_list_flat):
        """
        Set data_list from flat list and reset display.
        """

        # data_list
        data_list = self.convert_flat_to_nested_list(data_list_flat)

        # update
        self.update(data_list)

    @QtCore.Slot()
    def update_invalid(self):
        """
        Update data_list to remove all
        invalid entries. (Renderthread nodes
        whose get_nuke_node() returns None)
        """

        # data_list_flat
        data_list_flat = self.get_data_list_flat()

        # check if needed
        if not (all([node.nuke_node_exists() for node in data_list_flat])):

            # clean_data_list_flat
            clean_data_list_flat = [node for node in data_list_flat if (node.nuke_node_exists())]

            # update_flat
            self.update_flat(clean_data_list_flat)

    def add_flat(self, additional_data_list_flat):
        """
        Add additional_data_list to self.data_list.
        Perform check to dismiss duplicates.
        """

        # data_list_flat
        data_list_flat = self.get_data_list_flat()

        # clean_data_list_flat
        clean_data_list_flat = list(set(data_list_flat + additional_data_list_flat))

        # update_flat
        self.update_flat(clean_data_list_flat)

    def clear(self):
        """
        Set empty data_list to model.
        """

        # update
        self.update([[]])

    def sort_data_list(self, data_list):
        """
        Sort data list by full name attribute
        of nuke_node of renderthreads node.
        """

        # data_list_flat
        data_list_flat = self.convert_nested_to_flat_list(data_list)
        # sorted_data_list_flat
        sorted_data_list_flat = sorted(data_list_flat,
                                        key=lambda renderthreads_node: renderthreads_node.fullName().lower())
        # sorted_data_list
        sorted_data_list = self.convert_flat_to_nested_list(sorted_data_list_flat)

        # return
        return sorted_data_list

    def get_data_list(self):
        """
        Return self.data_list
        """

        return self.data_list

    def get_data_list_flat(self):
        """
        Return self.data_list entries as flat list.
        """

        return self.convert_nested_to_flat_list(self.data_list)

    def convert_nested_to_flat_list(self, nested_list):
        """
        Return nested_list entries as flat list.
        [[data], [data]] >> [data, data, data].
        """

        # flat_list
        flat_list = []

        # iterate
        for inner_list in nested_list:

            # check if index exists
            try:
                data = inner_list[0]
            except:
                continue

            # append
            flat_list.append(data)

        # return
        return flat_list

    def convert_flat_to_nested_list(self, flat_list):
        """
        Return flat_list entries as nested list.
        [data, data, data] >> [[data], [data]].
        """

        # flat list empty or filled with empty entries
        if not (any(flat_list)):
            return [[]]

        # nested_list
        nested_list = []

        # iterate and add
        for data in flat_list:

            # check type
            if (isinstance(data, renderthreads_node.RenderThreadsNode)):

                # append
                nested_list.append([data])

        # nested_list empty
        if not (nested_list):
            return [[]]

        # return
        return nested_list

    def remove_data_from_list(self, data_to_remove):
        """
        Cleanup data list.
        """

        # renderthreads_node
        if (isinstance(data_to_remove, renderthreads_node.RenderThreadsNode)):

            # remove_node_from_data_list
            self.remove_node_from_data_list(data_to_remove)

        # [renderthreads_node, renderthreads_node]
        elif (isinstance(data_to_remove, list)):

            # remove_nodes_from_data_list
            self.remove_nodes_from_data_list(data_to_remove)

    def remove_node_from_data_list(self, node_to_remove):
        """
        Remove single renderthreads node
        from data list.
        """

        try:
            # data_list_flat
            data_list_flat = self.get_data_list_flat()
            # remove
            clean_data_list_flat = [data for
                                    data in
                                    data_list_flat if not
                                    (id(data) == id(node_to_remove))]
            # update
            self.update_flat(clean_data_list_flat)
        except:
            # log
            self.logger.debug('Error removing node from data_list')

    def remove_nodes_from_data_list(self, node_remove_list):
        """
        Remove list of renderthreads nodes
        from data list.
        """

        try:
            # node_remove_id_list
            node_remove_id_list = [id(node) for node in node_remove_list]

            # data_list_flat
            data_list_flat = self.get_data_list_flat()

            # clean_data_list_flat
            clean_data_list_flat = [node for
                                    node in
                                    data_list_flat if not
                                    (id(node) in node_remove_id_list)]

            # update
            self.update_flat(clean_data_list_flat)
        except:
            # log
            self.logger.debug('Error removing node list from data_list')

    # Validation
    # ------------------------------------------------------------------
    def validate_value_for_nuke_node(self, value):
        """
        Validate the value that should be set on the attr. of the data object.
        Return True or False.
        """

        return True

    def validate_value_for_start_frame(self, value):
        """
        Validate the value that should be set on the attr. of the data object.
        Return True or False.
        """

        return True

    def validate_value_for_end_frame(self, value):
        """
        Validate the value that should be set on the attr. of the data object.
        Return True or False.
        """

        return True

    def validate_value_for_priority(self, value):
        """
        Validate the value that should be set on the attr. of the data object.
        Return True or False. The range for priority is between 1-100
        including 1 and 100.
        """

        # value larger than 100
        if (value > 100 or value < 1):
            return False

        return True

    # Misc
    # ------------------------------------------------------------------
    def format_string(self, string_value):
        """
        Return a pretty version of string. This method is
        catered towards my naming habits.
        """

        try:
            # First letter uppercase
            formatted_string_value = string_value[0].upper() + string_value[1:]

            # replace _
            formatted_string_value = formatted_string_value.replace('_', ' ')

        except:
            # log
            self.logger.debug('Error formatting {0}. Returning empty string'.format(string_value))
            return ''

        return formatted_string_value
