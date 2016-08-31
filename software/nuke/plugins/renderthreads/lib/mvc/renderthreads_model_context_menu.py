

"""
renderthreads_model_context_menu
==========================================

Menu created on right-click at renderthreads
model instance.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""


# Import
# ------------------------------------------------------------------
# python
import sys
import os
import functools
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

#  renderthreads_logging
from .. import renderthreads_logging
if(do_reload):
    reload(renderthreads_logging)

#  renderthreads_nuke
from .. import renderthreads_nuke
if(do_reload):
    reload(renderthreads_nuke)

#  renderthreads_command_line_engine
from .. import renderthreads_command_line_engine
if(do_reload):
    reload(renderthreads_command_line_engine)

#  renderthreads_render
from .. import renderthreads_render
if(do_reload):
    reload(renderthreads_render)

#  renderthreads_gui_setup
from .. import renderthreads_gui_setup
if(do_reload):
    reload(renderthreads_gui_setup)

# lib.gui

# renderthreads_gui_helper
from ..gui import renderthreads_gui_helper
if(do_reload):
    reload(renderthreads_gui_helper)


# NodesContextMenu
# ------------------------------------------------------------------
class NodesContextMenu(QtGui.QMenu):
    """
    Customized context menu for the model
    that manages the renderthread nodes.
    """

    def __new__(cls, *args, **kwargs):
        """
        NodesContextMenu instance factory.
        """

        # nodes_context_menu_instance
        nodes_context_menu_instance = super(NodesContextMenu, cls).__new__(cls, args, kwargs)

        return nodes_context_menu_instance

    def __init__(self,
                dev=True,
                parent=None):
        """
        Customize instance.
        """

        # super and objectName
        # ------------------------------------------------------------------
        # parent_class
        self.parent_class = super(NodesContextMenu, self)
        self.parent_class.__init__(parent=parent)

        # setObjectName
        self.setObjectName(self.__class__.__name__)

        # instance variables
        # ------------------------------------------------------------------
        # dev
        self.dev = dev

        # logger
        self.logger = renderthreads_logging.get_logger(self.__class__.__name__)

        # view
        self.view = None

        # wdgt_main
        self.wdgt_main = None

        # Init procedure
        # ------------------------------------------------------------------
        # setup_ui
        self.setup_ui()

        # connect_ui
        self.connect_ui()

        # style_ui
        self.style_ui()

        # run_tests
        self.run_tests()

    # Setup
    # ------------------------------------------------------------------
    def setup_ui(self):
        """
        Setup menu ui.
        """

        # acn_add_selected
        self.acn_add_selected = QtGui.QAction('Add selected write nodes', self)
        self.acn_add_selected.setObjectName(self.__class__.__name__ + '_' + 'acn_add_selected')
        self.addAction(self.acn_add_selected)

        # acn_add_all
        self.acn_add_all = QtGui.QAction('Add all write nodes', self)
        self.acn_add_all.setObjectName(self.__class__.__name__ + '_' + 'acn_add_all')
        self.addAction(self.acn_add_all)

        # Separator
        self.addSeparator()

        # mnu_render
        self.mnu_render = QtGui.QMenu('Render', parent=self)
        self.mnu_render.setObjectName(self.__class__.__name__ + '_' + 'mnu_render')
        self.addMenu(self.mnu_render)

        # acn_render_selected
        self.acn_render_selected = QtGui.QAction('Render selected nodes', self)
        self.acn_render_selected.setObjectName(self.__class__.__name__ + '_' + 'acn_render_selected')
        self.mnu_render.addAction(self.acn_render_selected)

        # acn_render_all
        self.acn_render_all = QtGui.QAction('Render all nodes', self)
        self.acn_render_all.setObjectName(self.__class__.__name__ + '_' + 'acn_render_all')
        self.mnu_render.addAction(self.acn_render_all)

        # Separator
        self.mnu_render.addSeparator()

        # acn_disable_render_selected
        self.acn_disable_render_selected = QtGui.QAction('Disable selected', self)
        self.acn_disable_render_selected.setObjectName(self.__class__.__name__ + '_' + 'acn_disable_render_selected')
        self.mnu_render.addAction(self.acn_disable_render_selected)

        # acn_disable_render_all
        self.acn_disable_render_all = QtGui.QAction('Disable all', self)
        self.acn_disable_render_all.setObjectName(self.__class__.__name__ + '_' + 'acn_disable_render_all')
        self.mnu_render.addAction(self.acn_disable_render_all)

        # Separator
        self.addSeparator()

        # mnu_remove
        self.mnu_remove = QtGui.QMenu('Remove', parent=self)
        self.mnu_remove.setObjectName(self.__class__.__name__ + '_' + 'mnu_remove')
        self.addMenu(self.mnu_remove)

        # acn_remove_selected
        self.acn_remove_selected = QtGui.QAction('Remove selected nodes', self)
        self.acn_remove_selected.setObjectName(self.__class__.__name__ + '_' + 'acn_remove_selected')
        self.mnu_remove.addAction(self.acn_remove_selected)

        # acn_remove_all
        self.acn_remove_all = QtGui.QAction('Remove all nodes', self)
        self.acn_remove_all.setObjectName(self.__class__.__name__ + '_' + 'acn_remove_all')
        self.mnu_remove.addAction(self.acn_remove_all)

        # Separator
        self.addSeparator()

        # mnu_select
        self.mnu_select = QtGui.QMenu('Select', parent=self)
        self.mnu_select.setObjectName(self.__class__.__name__ + '_' + 'mnu_select')
        self.addMenu(self.mnu_select)

        # acn_select_selected
        self.acn_select_selected = QtGui.QAction('Select selected nodes', self)
        self.acn_select_selected.setObjectName(self.__class__.__name__ + '_' + 'acn_select_selected')
        self.mnu_select.addAction(self.acn_select_selected)

        # acn_select_all
        self.acn_select_all = QtGui.QAction('Select all nodes', self)
        self.acn_select_all.setObjectName(self.__class__.__name__ + '_' + 'acn_select_all')
        self.mnu_select.addAction(self.acn_select_all)

        # Separator
        self.mnu_select.addSeparator()

        # acn_deselect_all
        self.acn_deselect_all = QtGui.QAction('Deselect all DAG nodes', self)
        self.acn_deselect_all.setObjectName(self.__class__.__name__ + '_' + 'acn_deselect_all')
        self.mnu_select.addAction(self.acn_deselect_all)

        # dev
        if (self.is_dev()):

            # Separator
            self.addSeparator()

            # mnu_dev
            self.mnu_dev = QtGui.QMenu('Dev', parent=self)
            self.mnu_dev.setObjectName(self.__class__.__name__ + '_' + 'mnu_dev')
            self.addMenu(self.mnu_dev)

    # Connect
    # ------------------------------------------------------------------

    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        # acn_add_selected
        self.acn_add_selected.triggered.connect(functools.partial(self.add_selected))
        # acn_add_all
        self.acn_add_all.triggered.connect(functools.partial(self.add_all))

        # acn_remove_selected
        self.acn_remove_selected.triggered.connect(functools.partial(self.remove_selected))
        # acn_remove_all
        self.acn_remove_all.triggered.connect(functools.partial(self.remove_all))

        # acn_select_selected
        self.acn_select_selected.triggered.connect(functools.partial(self.select_selected))
        # acn_select_all
        self.acn_select_all.triggered.connect(functools.partial(self.select_all))
        # acn_deselect_all
        self.acn_deselect_all.triggered.connect(functools.partial(self.deselect_all))

        # acn_render_selected
        self.acn_render_selected.triggered.connect(functools.partial(self.render_selected))
        # acn_render_all
        self.acn_render_all.triggered.connect(functools.partial(self.render_all))

        # acn_disable_render_selected
        self.acn_disable_render_selected.triggered.connect(functools.partial(self.disable_render_selected))
        # acn_disable_render_all
        self.acn_disable_render_all.triggered.connect(functools.partial(self.disable_render_all))

        # dev
        if (self.is_dev()):

            pass

    # Style
    # ------------------------------------------------------------------

    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        # styled_background
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        # correct_styled_background_attribute
        renderthreads_gui_helper.correct_styled_background_attribute(self)

        # set_margins_and_spacing_for_child_layouts
        renderthreads_gui_helper.set_margins_and_spacing_for_child_layouts(self)

    # Getter & Setter
    # ------------------------------------------------------------------

    def set_view_and_model(self, view):
        """
        Set self.view and self.model
        """

        self.view = view
        self.model = view.model()

    def set_main_widget(self, wdgt):
        """
        Set self.wdgt_main
        """

        self.wdgt_main = wdgt

    def is_dev(self):
        """
        Return developer status of app.
        """

        return self.dev

    # Methods
    # ------------------------------------------------------------------

    def get_selected_indices(self):
        """
        Return list of selected indices from view.
        """

        # if view
        if (self.view):
            # selected_indices_list
            selected_indices_list = self.view.selectedIndexes()
        # else
        else:
            # selected_indices_list
            selected_indices_list = []

        return selected_indices_list

    def indices_list_to_data_list(self, model_index_list):
        """
        Convert a list of modelindices to the list of
        data they contain. This does NOT give the renderthreads
        nodes from the models data list, but the content of
        the view fields.
        """

        try:
            # data_list
            data_list = [model_index.data() for model_index in model_index_list]

        except:
            # data_list
            data_list = []

        return data_list

    def indices_list_to_node_list(self, model_index_list):
        """
        Convert a list of modelindices to the list of
        renderthread nodes from the model.
        """

        # node_list
        node_list = []

        try:
            # iterate
            for index in model_index_list:

                # index invalid
                if not(index.isValid()):

                    # log
                    self.logger.debug('Index {0} not valid. Continuing.'.format(index))
                    continue

                # row
                row = index.row()

                # model
                model = index.model()

                # current_node
                current_node = model.data_list[row][0]

                # check duplicates
                if (id(current_node) in [id(node) for node in node_list]):
                    continue

                # append
                node_list.append(current_node)  # column is always zero

        except:
            pass

        return node_list

    def get_renderthreads_node_to_command_object_list_from_nodes(self, renderthreads_node_list):
        """
        Return list of RenderThreadNode and RenderCommand objects for
        given list of renderthread nodes. The format is:
        [[renderthreads_node, command_object], [renderthreads_node, command_object], ...].
        There is a pair for each frame that needs to be rendered.
        """

        # renderthreads_node_to_command_object_list
        renderthreads_node_to_command_object_list = []

        # timeout
        timeout = self.wdgt_main.sldr_thread_timeout.get_value()
        # display_shell
        display_shell = self.wdgt_main.sldr_display_shell.get_value()
        # log_exitcode_errors_only
        log_exitcode_errors_only = self.wdgt_main.sldr_log_exitcode_errors_only.get_value()

        # iterate and add job
        for renderthreads_node in renderthreads_node_list:

            # frame_list
            frame_list = renderthreads_node.get_frame_list()

            # iterate frame list
            for frame in frame_list:

                # command
                command = renderthreads_command_line_engine.get_command_line_string(self.wdgt_main,
                                                                                    renderthreads_node,
                                                                                    frame)

                # identifier
                identifier = renderthreads_node.get_nuke_node_full_name()
                # priority
                priority = renderthreads_node.get_priority()
                # negated_priority (PriorityQueue needs negated values)
                negated_priority = 101 - priority

                # command_object
                command_object = renderthreads_render.RenderCommand(command,
                                                                    timeout,
                                                                    display_shell,
                                                                    identifier,
                                                                    negated_priority,
                                                                    frame,
                                                                    log_exitcode_errors_only,
                                                                    renderthreads_node)

                # append
                renderthreads_node_to_command_object_list.append([renderthreads_node, command_object])

        # return
        return renderthreads_node_to_command_object_list

    def connect_command_object_list(self, renderthreads_node_to_command_object_list):
        """
        Connect the given RenderCommand objects
        in command_object_list to signals and slots.
        """

        # iterate
        for renderthreads_node, command_object in renderthreads_node_to_command_object_list:

            # Command States
            # sgnl_command_set_enabled
            self.wdgt_main.sgnl_command_set_enabled.connect(command_object.set_enabled)
            # sgnl_command_set_enabled_for_identifier
            self.wdgt_main.sgnl_command_set_enabled_for_identifier.connect(command_object.set_enabled_for_identifier)
            # sgnl_command_terminate_process
            self.wdgt_main.sgnl_command_terminate_process.connect(command_object.terminate_process)
            # sgnl_command_terminate_process_for_identifier
            self.wdgt_main.sgnl_command_terminate_process_for_identifier.connect(command_object.terminate_process_for_identifier)

            # sgnl_command_set_timeout
            self.wdgt_main.sgnl_command_set_timeout.connect(command_object.set_timeout)
            # sgnl_command_set_display_shell
            self.wdgt_main.sgnl_command_set_display_shell.connect(command_object.set_display_shell)
            # sgnl_command_set_log_exitcode_errors_only
            self.wdgt_main.sgnl_command_set_log_exitcode_errors_only.connect(command_object.set_log_exitcode_errors_only)
            # sgnl_command_set_priority_for_identifier
            renderthreads_node.sgnl_command_set_priority_for_identifier.connect(command_object.set_priority_for_identifier)

            # Command Object
            # sgnl_task_done
            command_object.sgnl_task_done.connect(self.wdgt_main.pbar_render.increment_value)
            command_object.sgnl_task_done.connect(renderthreads_node.progressbar.increment_value)
            command_object.sgnl_task_done.connect(self.wdgt_main.nodes_view.update)
            # sgnl_log
            command_object.sgnl_log.connect(self.wdgt_main.log)
            # sgnl_readd_job
            command_object.sgnl_readd_job.connect(self.wdgt_main.readd_job)

    def add_command_object_list_to_queue(self, renderthreads_node_to_command_object_list):
        """
        Add the given RenderCommand objects
        in command_object_list to the queue.
        """

        # iterate
        for renderthreads_node, command_object in renderthreads_node_to_command_object_list:

            # increment progressbar range
            self.wdgt_main.pbar_render.increment_range()
            renderthreads_node.progressbar.increment_range()

            # add
            self.wdgt_main.thread_manager.add_to_queue(command_object)

    # Slots
    # ------------------------------------------------------------------
    @QtCore.Slot()
    def add_selected(self):
        """
        Add selected DAG graph write nodes as
        renderthread nodes to model.
        """

        # nuke_node_list
        nuke_node_list = renderthreads_nuke.get_nodes('Write', True)
        # renderthread_node_list
        renderthread_node_list = renderthreads_nuke.convert_nodes(nuke_node_list)

        try:
            # update
            self.model.add_flat(renderthread_node_list)
        except:
            # log
            self.logger.debug('Error adding renderthread node list from selected DAG nodes to model. Maybe model is not set.')

    @QtCore.Slot()
    def add_all(self):
        """
        Add all DAG graph write nodes as
        renderthread nodes to model.
        """

        # nuke_node_list
        nuke_node_list = renderthreads_nuke.get_nodes('Write')
        # renderthread_node_list
        renderthread_node_list = renderthreads_nuke.convert_nodes(nuke_node_list)

        try:
            # update
            self.model.add_flat(renderthread_node_list)
        except:
            # log
            self.logger.debug('Error adding renderthread node list from all DAG nodes to model. Maybe model is not set.')

    @QtCore.Slot()
    def remove_selected(self):
        """
        Remove selected nodes from model.
        """

        # selected_indices_list
        selected_indices_list = self.get_selected_indices()

        # renderthread_node_list
        renderthread_node_list = self.indices_list_to_node_list(selected_indices_list)

        try:
            # clear
            self.model.remove_data_from_list(renderthread_node_list)
        except:
            # log
            self.logger.debug('Error removing selected nodes from model. Maybe model is not set.')

    @QtCore.Slot()
    def remove_all(self):
        """
        Clear model.
        """

        try:
            # clear
            self.model.clear()
        except:
            # log
            self.logger.debug('Error clearing model. Maybe model is not set.')

    @QtCore.Slot()
    def select_selected(self):
        """
        Select write nodes which are currently
        selected in model.
        """

        try:
            # deselect_all
            renderthreads_nuke.deselect_all()

            # selected_indices_list
            selected_indices_list = self.get_selected_indices()

            # renderthread_node_list
            renderthread_node_list = self.indices_list_to_node_list(selected_indices_list)

            # nuke_node_list
            nuke_node_list = [node.nuke_node for node in renderthread_node_list]

            # select
            renderthreads_nuke.select_nodes(nuke_node_list)
        except:
            # log
            self.logger.debug('Error selecting selected nodes.')

    @QtCore.Slot()
    def select_all(self):
        """
        Select all write nodes in model.
        """

        try:
            # deselect_all
            renderthreads_nuke.deselect_all()

            # renderthread_node_list
            renderthread_node_list = self.model.get_data_list_flat()

            # nuke_node_list
            nuke_node_list = [node.nuke_node for node in renderthread_node_list]

            # select
            renderthreads_nuke.select_nodes(nuke_node_list)
        except:
            # log
            self.logger.debug('Error selecting all nodes.')

    @QtCore.Slot()
    def deselect_all(self):
        """
        Deselect all nodes in scene. Recurse groups.
        """

        try:
            # deselect_all
            renderthreads_nuke.deselect_all()
        except:
            # log
            self.logger.debug('Error deselecting all nodes.')

    @QtCore.Slot()
    def render_selected(self):
        """
        Render renderthread nodes which are currently
        selected in the model.
        """

        # save
        if (self.wdgt_main.sldr_save_script.get_value()):

            # save_successful
            save_successful = renderthreads_nuke.save_script()

            # not successful
            if not (save_successful):

                # log
                self.logger.debug('Script saving failed. Not rendering.')
                return

            # set (new) script path in ui
            renderthreads_gui_setup.update_script_path(self.wdgt_main)
            # log
            self.logger.debug('Script saved: {0}'.format(renderthreads_nuke.get_script_path()))

        # selected_indices_list
        selected_indices_list = self.get_selected_indices()

        # renderthread_node_list
        renderthread_node_list = self.indices_list_to_node_list(selected_indices_list)

        # renderthreads_node_to_command_object_list
        renderthreads_node_to_command_object_list = self.get_renderthreads_node_to_command_object_list_from_nodes(renderthread_node_list)

        # connect_command_object_list
        self.connect_command_object_list(renderthreads_node_to_command_object_list)

        # add_command_object_list_to_queue
        self.add_command_object_list_to_queue(renderthreads_node_to_command_object_list)

    @QtCore.Slot()
    def render_all(self):
        """
        Render renderthread nodes which are currently
        in the model.
        """

        # save
        if (self.wdgt_main.sldr_save_script.get_value()):

            # save_successful
            save_successful = renderthreads_nuke.save_script()

            # not successful
            if not (save_successful):

                # log
                self.logger.debug('Script saving failed. Not rendering.')
                return

            # set (new) script path in ui
            renderthreads_gui_setup.update_script_path(self.wdgt_main)
            # log
            self.logger.debug('Script saved: {0}'.format(renderthreads_nuke.get_script_path()))

        # renderthread_node_list
        renderthread_node_list = self.model.get_data_list_flat()

        # renderthreads_node_to_command_object_list
        renderthreads_node_to_command_object_list = self.get_renderthreads_node_to_command_object_list_from_nodes(renderthread_node_list)

        # connect_command_object_list
        self.connect_command_object_list(renderthreads_node_to_command_object_list)

        # add_command_object_list_to_queue
        self.add_command_object_list_to_queue(renderthreads_node_to_command_object_list)

    @QtCore.Slot()
    def disable_render_selected(self):
        """
        Emit sgnl_command_set_enabled_for_identifier(identifier, False)
        and sgnl_command_terminate_process_for_identifier(identifier).
        The identifier is the full node name. The signals first cause
        all RenderCommand objects with a matching identifier to have
        the enabled member set to false and then the process, if not
        None, will be killed.The RenderCommand objects still
        follow the get/task_done procedure of the queue
        though, which means that total finishing of
        all objects might take a while.
        """

        # selected_indices_list
        selected_indices_list = self.get_selected_indices()

        # renderthreads_node_list
        renderthreads_node_list = self.indices_list_to_node_list(selected_indices_list)

        # iterate
        for renderthreads_node in renderthreads_node_list:

            # identifier
            identifier = renderthreads_node.get_nuke_node_full_name()

            # emit
            self.wdgt_main.sgnl_command_set_enabled_for_identifier.emit(identifier, False)
            self.wdgt_main.sgnl_command_terminate_process_for_identifier.emit(identifier)

    @QtCore.Slot()
    def disable_render_all(self):
        """
        Emit sgnl_command_set_enabled(False) and
        sgnl_command_terminate_process. Those two
        signals cause an immediate stop for all
        RenderCommand objects. The currently rendering objects
        are aborted and the ones that wait in the queue
        are not executed anymore since they have been
        set disabled. The RenderCommand objects still
        follow the get/task_done procedure of the queue
        though, which means that total finishing of
        all objects might take a while.
        """

        # emit
        self.wdgt_main.sgnl_command_set_enabled.emit(False)
        self.wdgt_main.sgnl_command_terminate_process.emit()

    # Misc
    # ------------------------------------------------------------------
    def dummy_method(self, msg='dummy'):
        """
        Dummy method.
        """

        # log
        self.logger.debug('{0}'.format(msg))

    def dummy_method_silent(self):
        """
        Dummy method without output.
        """

        pass

    # Test
    # ------------------------------------------------------------------
    def run_tests(self):
        """
        Suite of test methods.
        """

        # log
        self.logger.debug('\n\nExecute test methods:\n-----------------------------')

        # test methods start here
        # ------------------------------------------------------------------
        # ------------------------------------------------------------------

        # dummy_method
        self.dummy_method()

        # ------------------------------------------------------------------
        # ------------------------------------------------------------------
        # test methods end here

        # log
        self.logger.debug('\n\n-----------------------------\nFinished test methods.')
