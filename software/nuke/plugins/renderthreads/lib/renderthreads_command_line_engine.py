

"""
renderthreads_command_line_engine
==========================================

This module handles the creation of the
command line string used for rendering.
"""


# Import
# ------------------------------------------------------------------
# Python
import logging
import functools
import re


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


# Globals
# ------------------------------------------------------------------
WRITE_NODE_REPLACEMENT_TEMPLATE = renderthreads_globals.WRITE_NODE_REPLACEMENT_TEMPLATE


# logger (Module Level)
# ------------------------------------------------------------------
logger = renderthreads_logging.get_logger(__name__)


# Command line engine
# ------------------------------------------------------------------
def get_command_line_string(wdgt,
                            renderthreads_node=None,
                            frame=None):
    """
    Convert given list of CommandLineFlag objects into
    a command line string that can be used for
    rendering.
    """

    # script_path
    script_path = wdgt.le_script_path.text()
    # nuke_path
    nuke_path = wdgt.le_nuke_path.text()
    # flag_list
    flag_list = wdgt.command_line_flag_list

    # command_line_string
    command_line_string = r'"{0}"'.format(nuke_path)
    command_line_string += ' '

    # flag_string
    flag_string = get_flag_string(flag_list, renderthreads_node, frame)

    # add
    command_line_string += flag_string
    command_line_string += ' '

    # script_path
    command_line_string += r'"{0}"'.format(script_path)

    # return
    return command_line_string


def get_flag_string(flag_list,
                    renderthreads_node=None,
                    frame=None):
    """
    Return flag string ready to be used in
    command line string from list of
    RenderThreadsCommandLineFlag objects.
    Replace frame and write_node_name
    if not None with regexprs.
    """

    # flag_string
    flag_string = r''

    # iterate flag list
    for index, flag in enumerate(sorted(flag_list)):

        # check state
        if (flag.get_state()):

            # append flag
            flag_string += flag.get_flag()

            # last entry
            if not (index == len(flag_list) - 1):

                # add space
                flag_string += ' '

    # renderthreads_node
    if not(renderthreads_node is None):

        # write_node_name
        write_node_name = renderthreads_node.fullName()

        # pattern
        pattern = re.compile('-X\s[\w]+')

        # replace template
        flag_string = pattern.sub('-X {0}'.format(write_node_name), flag_string)

    # frame
    if not(frame is None):

        # pattern
        pattern = re.compile('-F\s-?\d+')

        # replace frame
        flag_string = pattern.sub('-F {0}'.format(frame), flag_string)

    # return
    return flag_string
