

"""
renderthreads_nuke
==========================================

This module encapsulates renderthreads nuke
functionality.
"""


# Import
# ------------------------------------------------------------------
# Python
import logging
import functools
import collections
# nuke
import nuke


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

# renderthreads_node
from mvc import renderthreads_node
if(do_reload):
    reload(renderthreads_node)


# Globals
# ------------------------------------------------------------------


# logger (Module Level)
# ------------------------------------------------------------------
logger = renderthreads_logging.get_logger(__name__)


# MemoryInfo
# ------------------------------------------------------------------
MemoryInfo = collections.namedtuple('MemoryInfo', 'info ram_total ram_in_use total_virtual_memory')


# Scene Interaction
# ------------------------------------------------------------------
def get_nodes(filter_type=None, selected=False):
    """
    Return list of all write nodes in DAG.
    """

    # selected
    if (selected):
        # all nodes (also group content)
        node_list = nuke.allNodes(recurseGroups=True)
        # selected_nodes
        node_list = [node for node in node_list if (node.isSelected())]
    # all
    else:
        node_list = nuke.allNodes(recurseGroups=True)

    # filter_type
    if (filter_type):
        node_list = [node for node in node_list if (node.Class() == filter_type)]

    # check
    if not (node_list):
        # log
        logger.debug('node_list empty or None. Returning empty list.')
        return []

    return node_list


def print_nodes(filter_type=None, selected=False, convert=False):
    """
    Return list of all write nodes in DAG.
    """

    # node_list
    node_list = get_nodes(filter_type, selected)

    # convert
    if (convert):
        node_list = convert_nodes(node_list)

    # iterate and print
    for node in node_list:
        print('{0} - {1}'.format(node.fullName(), node.Class()))


def convert_nodes(nuke_node_list):
    """
    Return list of renderthread_nodes
    from given list of nuke nodes.
    """

    # renderthread_node_list
    renderthread_node_list = []

    # convert
    for nuke_node in nuke_node_list:
        try:
            # renderthread_node
            renderthread_node = convert_nuke_to_renderthread_node(nuke_node)
            # append
            renderthread_node_list.append(renderthread_node)
        except:
            # log
            logger.debug('Error converting nuke_node {0} to renderthread_node. Not converting.'.format(nuke_node))

    # return
    return renderthread_node_list


def convert_nuke_to_renderthread_node(nuke_node):
    """
    Convert a nuke to a renderthread node.
    """

    start_frame = int(nuke.Root().firstFrame())
    end_frame = int(nuke.Root().lastFrame())

    # write
    if (nuke_node.Class() == 'Write'):
        return renderthreads_node.RenderThreadsNodeWrite(nuke_node, start_frame, end_frame)
    # generic
    else:
        return renderthreads_node.RenderThreadsNode(nuke_node, start_frame, end_frame)


def node_exists(node):
    """
    Check whether or not node exists.
    """

    try:
        result = nuke.exists(node.name())
        return result
    except:
        return False


def deselect_all():
    """
    Deselect all nuke nodes.
    """

    # all nodes (also group content)
    node_list = nuke.allNodes(recurseGroups=True)

    # deselect
    for node in node_list:
        try:
            node.setSelected(False)
        except:
            continue


def select_nodes(nuke_node_list):
    """
    Select nodes from given nuke_node_list.
    """

    # iterate and select
    for nuke_node in nuke_node_list:

        # select
        try:
            select_node(nuke_node)
        except:
            logger.debug('Error selecting nuke node {0}. Continuing'.format(nuke_node))
            continue


def select_node(nuke_node, exclusive=False):
    """
    Select nuke_node from given nuke_node.
    """

    # exclusive
    if (exclusive):
        nuke_node.selectOnly()
    # else
    else:
        nuke_node.setSelected(True)


def get_memory_info(display=False):
    """
    Return list of memory info.
    """

    # values
    info = str(nuke.memory('info'))
    ram_total = byte_to_megabyte(nuke.memory('total_ram'))
    ram_in_use = byte_to_megabyte(nuke.memory('usage'))
    total_virtual_memory = byte_to_megabyte(nuke.memory('total_vm'))

    # memory_info
    memory_info = MemoryInfo(info, ram_total, ram_in_use, total_virtual_memory)

    # display
    if (display):

        # log
        logger.debug('{0}'.format(memory_info))


def byte_to_megabyte(byte_number):
    """
    Convert bytes to megabytes.
    For example a byte_number of
    17135431680 returns 16341 megabyte.
    1048576 byte are 1 mbyte.
    """

    try:
        return int(byte_number / 1048576)
    except:
        return None


def get_nuke_path():
    """
    Return path to currently used Nuke.exe.
    """

    return nuke.EXE_PATH


def get_script_path():
    """
    Return script path.
    """

    return nuke.root().name()


def save_script():
    """
    Save the current script under the
    same name. Return True or False depending on
    wether or not the operation was successful.
    """

    try:
        
        result = nuke.scriptSave()
        return result
    
    except:

        # log
        logger.info('Error saving file.')
        
        return False
