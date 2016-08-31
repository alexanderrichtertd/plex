
"""
renderthreads_globals
==========================================

Module that has renderthreads tool globals
"""


# Import
# ------------------------------------------------------------------
# import
import os
import logging
# PySide
from PySide import QtGui
from PySide import QtCore


# Version and Title
# ------------------------------------------------------------------
TITLE = 'renderthreads'
VERSION = 0.1


# Logging
# ------------------------------------------------------------------
INITIAL_LOGGING_LEVEL = logging.INFO


# Pathes
# ------------------------------------------------------------------
TOOL_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
LIB_PATH = os.path.join(TOOL_ROOT_PATH, 'lib')
GUI_PATH = os.path.join(LIB_PATH, 'gui')
MVC_PATH = os.path.join(LIB_PATH, 'mvc')
THIRD_PARTY_PATH = os.path.join(LIB_PATH, 'third_party')

MEDIA_PATH = os.path.join(TOOL_ROOT_PATH, 'media')
ICONS_PATH = os.path.join(MEDIA_PATH, 'icons')
FONTS_PATH = os.path.join(MEDIA_PATH, 'fonts')
UI_PATH = os.path.join(MEDIA_PATH, 'ui')


# Fonts
# ------------------------------------------------------------------
# Sizes
FONT_SIZE_DEFAULT = 10
FONT_SIZE_LARGE = 14
FONT_SIZE_SMALL = 8
# Fonts
FUTURA_LT_LIGHT = ('Futura LT Light', 'futura-lt-light.ttf')

# FONTS_LIST [(Font Name, Font File Name), (Font Name, Font File Name)...]
FONTS_LIST = [FUTURA_LT_LIGHT]

# iterate and install if not installed
for font_name, font_file_name in FONTS_LIST:
    # font not installed
    if not (font_name in QtGui.QFontDatabase().families()):
        # current_font_path
        current_font_path = os.path.join(FONTS_PATH, font_file_name).replace('\\', '/')
        # add font
        QtGui.QFontDatabase.addApplicationFont(current_font_path)


# Colors
# ------------------------------------------------------------------
# darkening_factor
DARKENING_FACTOR = 120
# brightening_factor
BRIGHTENING_FACTOR = 150
# transparency
TRANSPARENCY = 100

BLACK = QtGui.QColor('#000000')
WHITE = QtGui.QColor('#f5f5f5')
WHITE_DARK = WHITE.darker(DARKENING_FACTOR)
WHITE_BRIGHT = WHITE.lighter(DARKENING_FACTOR)
GREY = QtGui.QColor('#484f57')
GREY_DARK = GREY.darker(DARKENING_FACTOR)
GREY_BRIGHT = GREY.lighter(DARKENING_FACTOR)
RED = QtGui.QColor('#fb3e2a')
RED_DARK = RED.darker(DARKENING_FACTOR)
RED_BRIGHT = RED.lighter(DARKENING_FACTOR)
BLUE = QtGui.QColor('#07faff')
BLUE_DARK = BLUE.darker(DARKENING_FACTOR)
BLUE_BRIGHT = BLUE.lighter(DARKENING_FACTOR)


# Images
# ------------------------------------------------------------------
HEADER_IMAGE = os.path.join(ICONS_PATH, 'renderthreads_header.png').replace('\\', '/')
ICON_RENDERTHREADS = os.path.join(ICONS_PATH, 'icn_renderthreads.png').replace('\\', '/')


# Text
# ------------------------------------------------------------------
WRITE_NODE_REPLACEMENT_TEMPLATE = 'write_node_template'
TEXT_DIVIDER = '---------------------------'


# Misc.
# ------------------------------------------------------------------
COMMAND_LINE_FLAG_SPACING = 4


# Threads
# ------------------------------------------------------------------
INITIAL_THREAD_INTERVAL = 200  # msec
INITIAL_THREAD_TIMEOUT = 10  # min
INITIAL_DISPLAY_SHELL = 1  # Can be 0 or 1
INITIAL_LOG_EXITCODE_ERRORS_ONLY = 1  # Can be 0 or 1
INITIAL_READD_BROKEN_JOB = 1  # Can be 0 or 1
INITIAL_READD_BROKEN_JOB_COUNT = 2
INITIAL_SAVE_SCRIPT_BEFORE_RENDER = 1  # msec

INITIAL_PRIORITY = 50  # Range is from 1 - 100. PriorityQueue values are negated so 1 is highest, 100 lowest


# Websites
# ------------------------------------------------------------------
WEBSITE_DOCS = r'http://renderthreads.readthedocs.org/'
WEBSITE_DOCS_QUICK = r'http://renderthreads.readthedocs.org/quickstart.html'
WEBSITE_PYPI = r'https://pypi.python.org/pypi/renderthreads/'
WEBSITE_GITHUB = r'https://github.com/timmwagener/renderthreads'
WEBSITE_GITHUB_ISSUES = r'https://github.com/timmwagener/renderthreads/issues'
WEBSITE_AUTHOR = r'http://www.timmwagener.com/'
WEBSITE_VIMEO = r'https://vimeo.com/timmwagener/renderthreads'
WEBSITE_LINKEDIN = r'https://www.linkedin.com/pub/timm-wagener/54/5a2/b55'


# Tooltips
# ------------------------------------------------------------------
TT_THREADCOUNT = 'Threadcount\n\
{0}\n\
Number of threads to use for command-line rendering.\n\
Minimum is 1 and maximum is the number of available\n\
cores in the system. The default is half of all available\n\
cores.\n\
{0}\n\
Be carefull with the thread count in case of low system memory.'.format(TEXT_DIVIDER)

TT_THREAD_INTERVAL = 'Thread interval (msec.)\n\
{0}\n\
Interval in milliseconds in which the threads repeatedly\n\
ask their queue for new work. The default is 200 msec.'.format(TEXT_DIVIDER)

TT_THREAD_TIMEOUT = 'Thread Timeout (min.)\n\
{0}\n\
Time in minutes till the current render process is forcibly\n\
terminated. The exit code of a terminated process is 1. A terminated\n\
process will be logged as an error.'.format(TEXT_DIVIDER)

TT_DISPLAY_SHELL = 'Display shell\n\
{0}\n\
Wether or not to open a new shell for each rendered frame.'.format(TEXT_DIVIDER)

TT_LOG_EXITCODE_ERRORS_ONLY = 'Log exitcode errors only\n\
{0}\n\
Each frame is rendered in a new instance of Nuke in a separate\n\
process. Each of these processes gives a return code when closed\n\
which can happen when it has finished or has been terminated etc.\n\
The return code indicates whether or not the process was successfull.\n\
This flag determines if all return codes or just the ones that were\n\
not sucessfull should be logged. The default is logging only errors.'.format(TEXT_DIVIDER)

TT_INITIAL_READD_BROKEN_JOB = 'Re-add broken job\n\
{0}\n\
When a process has returned an exit code that indicates\n\
an error, wether or not to add this job to the queue again.'.format(TEXT_DIVIDER)

TT_INITIAL_READD_BROKEN_JOB_COUNT = 'Re-add broken job count\n\
{0}\n\
How many times a broken job will be added to the queue again.'.format(TEXT_DIVIDER)

TT_LOGGING_LEVEL = 'Logging level\n\
{0}\n\
Verbosity of the tool. Values from 1-5 correspond to the logging\n\
constants from DEBUG to CRITICAL (10-50).\n\
The default is 2.'.format(TEXT_DIVIDER)

TT_SAVE_SCRIPT = 'Save script before render\n\
{0}\n\
Save the current script before command-line rendering starts.\n\
If this is off the latest changes to your comp might not be rendered\n\
because they are not in the version of the comp that is opened\n\
by the command-line Nuke.'.format(TEXT_DIVIDER)
