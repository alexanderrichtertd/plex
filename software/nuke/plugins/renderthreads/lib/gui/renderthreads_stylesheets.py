
"""
renderthreads_stylesheets
==========================================

Module that has only one method.

#. get_stylesheet
"""


# Import
# ------------------------------------------------------------------
# Import variable
do_reload = True


# renderthreads

# renderthreads_globals
from .. import renderthreads_globals
if(do_reload):
    reload(renderthreads_globals)


# Globals
# ------------------------------------------------------------------
# Pathes
TOOL_ROOT_PATH = renderthreads_globals.TOOL_ROOT_PATH
MEDIA_PATH = renderthreads_globals.MEDIA_PATH
ICONS_PATH = renderthreads_globals.ICONS_PATH
UI_PATH = renderthreads_globals.UI_PATH

# Fonts
FONT_SIZE_DEFAULT = renderthreads_globals.FONT_SIZE_DEFAULT
FONT_SIZE_LARGE = renderthreads_globals.FONT_SIZE_LARGE
FONT_SIZE_SMALL = renderthreads_globals.FONT_SIZE_SMALL

FUTURA_LT_LIGHT = renderthreads_globals.FUTURA_LT_LIGHT

# Header
HEADER_IMAGE = renderthreads_globals.HEADER_IMAGE

TRANSPARENCY = renderthreads_globals.TRANSPARENCY

# Colors
BLACK = renderthreads_globals.BLACK
WHITE = renderthreads_globals.WHITE
WHITE_DARK = renderthreads_globals.WHITE_DARK

GREY = renderthreads_globals.GREY
GREY_DARK = renderthreads_globals.GREY_DARK
GREY_BRIGHT = renderthreads_globals.GREY_BRIGHT

RED = renderthreads_globals.RED
RED_DARK = renderthreads_globals.RED_DARK
RED_BRIGHT = renderthreads_globals.RED_BRIGHT

BLUE = renderthreads_globals.BLUE
BLUE_DARK = renderthreads_globals.BLUE_DARK
BLUE_BRIGHT = renderthreads_globals.BLUE_BRIGHT


# get_stylesheet
# ------------------------------------------------------------------
# ss_dict
ss_dict = {'header_image': HEADER_IMAGE,
            'font_size_default': FONT_SIZE_DEFAULT,
            'font_size_large': FONT_SIZE_LARGE,
            'font_size_small': FONT_SIZE_SMALL,
            'futura_lt_light': FUTURA_LT_LIGHT[0],
            'black': BLACK.name(),
            'white': WHITE.name(),
            'white_dark': WHITE_DARK.name(),
            'grey': GREY.name(),
            'grey_dark': GREY_DARK.name(),
            'grey_bright': GREY_BRIGHT.name(),
            'red': RED.name(),
            'red_dark': RED_DARK.name(),
            'red_bright': RED_BRIGHT.name(),
            'blue': BLUE.name(),
            'blue_dark': BLUE_DARK.name(),
            'blue_bright': BLUE_BRIGHT.name()}


def get_stylesheet():
    """
    Return stylesheet string, defining all stylesheets for RenderThreads.
    """

    # str_stylesheet
    str_stylesheet = " \
\
\
/* QWidget */\
QWidget { background-color: %(white)s; \
          font-family: \"%(futura_lt_light)s\"; \
          font-size: %(font_size_default)spt; \
          color: %(grey)s; \
          selection-background-color: %(white)s; \
}\
\
\
/* QWidget - wdgt_header_icon */\
QWidget#wdgt_header_icon { background-color: %(black)s; \
                            border-image: url(%(header_image)s); } \
\
\
/* QWidget - wdgt_header_spacer_left */\
QWidget#wdgt_header_spacer_left { background-color: %(black)s; } \
\
\
/* QWidget - wdgt_header_spacer_right */\
QWidget#wdgt_header_spacer_right { background-color: %(black)s; } \
\
\
/* QWidget - wdgt_stkwdgt_menu */\
QWidget#wdgt_stkwdgt_menu { background-color: %(black)s; \
                            border: none; \
} \
\
\
/* QWidget - stkwdgt_content */\
QWidget#stkwdgt_content { background-color: %(white)s; \
                            border: none; \
} \
\
\
/* QWidget - wdgt_header_spacer_bottom */\
QWidget#wdgt_header_spacer_bottom { background-color: %(black)s; \
                                    border: none; \
} \
\
\
/* QWidget - wdgt_header_spacer_top */\
QWidget#wdgt_header_spacer_top { background-color: %(black)s; \
                                    border: none; \
} \
\
\
\
\
\
\
/* QFrame - frm_nodes_header */\
QFrame#frm_nodes_header { padding: 10px; \
                            border: 1px solid %(grey)s; \
} \
\
\
/* QFrame - frm_nodes */\
QFrame#frm_nodes { padding: 0px; \
                    border-left: 1px solid %(grey)s; \
                    border-right: 1px solid %(grey)s; \
                    border-bottom: none; \
                    border-top: none; \
} \
\
\
/* QFrame - frm_pbar_render */\
QFrame#frm_pbar_render { padding: 0px; \
                            border-left: none; \
                            border-right: none; \
                            border-bottom: none; \
                            border-top: none; \
} \
\
\
/* QFrame - frm_log_header */\
QFrame#frm_log_header { padding: 10px; \
                            border: 1px solid %(grey)s; \
} \
\
\
/* QFrame - frm_log_text_edit */\
QFrame#frm_log_text_edit { padding: 0px; \
                            border-left: 1px solid %(grey)s; \
                            border-right: 1px solid %(grey)s; \
                            border-bottom: 1px solid %(grey)s; \
                            border-top: none; \
} \
\
\
/* QFrame - frm_threads_options */\
QFrame#frm_threads_options { padding: 0px; \
                                border: none; \
} \
\
\
/* QFrame - frm_threads_header */\
QFrame#frm_threads_header { padding: 10px; \
                            border: 1px solid %(grey)s; \
} \
\
\
/* QFrame - frm_threads */\
QFrame#frm_threads { padding: 10px; \
                        border-left: 1px solid %(grey)s; \
                        border-right: 1px solid %(grey)s; \
                        border-bottom: 1px solid %(grey)s; \
                        border-top: none; \
} \
\
\
/* QFrame - frm_queue_header */\
QFrame#frm_queue_header { padding: 10px; \
                            border: 1px solid %(grey)s; \
} \
\
\
/* QFrame - frm_queue */\
QFrame#frm_queue { padding: 10px; \
                    border-left: 1px solid %(grey)s; \
                    border-right: 1px solid %(grey)s; \
                    border-bottom: 1px solid %(grey)s; \
                    border-top: none; \
} \
\
\
/* QFrame - frm_command_line_complete */\
QFrame#frm_command_line_complete { padding: 0px; \
                                    border: none; \
} \
\
\
/* QFrame - frm_command_line_header */\
QFrame#frm_command_line_header { padding: 10px; \
                                    border-left: 1px solid %(black)s; \
                                    border-right: 1px solid %(black)s; \
                                    border-bottom: none; \
                                    border-top: 1px solid %(black)s; \
} \
\
\
/* QFrame - frm_command_line */\
QFrame#frm_command_line { background-color: %(black)s; \
                            padding: 10px; \
                            border-left: 1px solid %(grey)s; \
                            border-right: 1px solid %(grey)s; \
                            border-bottom: 1px solid %(red)s; \
                            border-top: 1px solid %(red)s; \
} \
\
\
/* QFrame - frm_command_line_options */\
QFrame#frm_command_line_options { padding: 10px; \
                                    border-left: 1px solid %(grey)s; \
                                    border-right: 1px solid %(grey)s; \
                                    border-bottom: 1px solid %(grey)s; \
                                    border-top: none; \
} \
\
\
/* QFrame - frm_constants_header */\
QFrame#frm_constants_header { padding: 10px; \
                                border: 1px solid %(grey)s; \
} \
\
\
/* QFrame - frm_constants */\
QFrame#frm_constants { padding: 10px; \
                        border-left: 1px solid %(grey)s; \
                        border-right: 1px solid %(grey)s; \
                        border-bottom: 1px solid %(grey)s; \
                        border-top: none; \
} \
\
\
/* QFrame - frm_options */\
QFrame#frm_options { padding: 0px; \
                        border: none; \
} \
\
\
/* QFrame - frm_general_options_header */\
QFrame#frm_general_options_header { padding: 10px; \
                                    border: 1px solid %(grey)s; \
} \
\
\
/* QFrame - frm_general_options */\
QFrame#frm_general_options { padding: 10px; \
                                border-left: 1px solid %(grey)s; \
                                border-right: 1px solid %(grey)s; \
                                border-bottom: 1px solid %(grey)s; \
                                border-top: none; \
} \
\
\
/* QFrame - frm_header_icon */\
QFrame#frm_header_icon { background-color: %(black)s; \
                            border: 1px solid %(white)s; \
} \
\
\
\
\
\
\
/* QStackedWidget - stkwdgt_content */\
QStackedWidget#stkwdgt_content { padding: 10px; } \
\
\
\
\
\
\
/* QToolTip */\
QToolTip { background-color: %(black)s; \
            color: %(white)s; \
            border-left: none; \
            border-top: 1px solid %(red)s; \
            border-bottom: none; \
            border-right: none; \
} \
\
\
\
\
\
\
/* QMenuBar - mnubar_stkwdgt */\
QMenuBar#mnubar_stkwdgt { background-color: transparent;\
                        font-size: %(font_size_large)spt; \
                        color: %(white)s; \
                        border-left: none; \
                        border-right: none; \
                        border-bottom: none; \
                        border-top: none; \
} \
\
\
/* QMenuBar - mnubar_stkwdgt - item */\
QMenuBar#mnubar_stkwdgt::item { background-color: transparent;\
                                font-size: %(font_size_large)spt; \
                                color: %(white)s; \
                                margin-left: 8; \
                                margin-right: 8; \
                                border-left: none; \
                                border-right: none; \
                                border-bottom: none; \
                                border-top: none; \
} \
\
\
/* QMenuBar - mnubar_stkwdgt - item - selected */\
QMenuBar#mnubar_stkwdgt::item:selected { background-color: transparent;\
                                            font-size: %(font_size_large)spt; \
                                            color: %(red)s; \
                                            border-left: none; \
                                            border-right: none; \
                                            border-bottom: none; \
                                            border-top: none; \
} \
\
\
/* QMenuBar - mnubar_stkwdgt - item - pressed */\
QMenuBar#mnubar_stkwdgt::item:pressed { background-color: transparent;\
                                        font-size: %(font_size_large)spt; \
                                        color: %(red_bright)s; \
                                        border-left: none; \
                                        border-right: none; \
                                        border-bottom: none; \
                                        border-top: none; \
} \
\
\
\
\
\
\
/* QMenu */\
QMenu { background-color: %(white)s; \
        color: %(grey)s; \
        border-left: none; \
        border-top: 1px solid %(red)s; \
        border-bottom: none; \
        border-right: none; \
} \
\
\
/* QMenu -item - selected */\
QMenu::item:selected { color: %(red)s; \
                        border: none; \
} \
\
\
\
\
\
\
/* QSplitter - handle */\
QSplitter::handle { background-color: %(red)s; } \
\
\
\
\
\
\
/* QLabel - lbl_command_line */\
QLabel#lbl_command_line { background-color: transparent; \
                            color: %(white)s; } \
\
\
/* QLabel - lbl_log_header */\
QLabel#lbl_log_header { font-size: %(font_size_large)spt; } \
\
\
/* QLabel - lbl_nodes_header */\
QLabel#lbl_nodes_header { font-size: %(font_size_large)spt; } \
\
\
/* QLabel - lbl_threads_header */\
QLabel#lbl_threads_header { font-size: %(font_size_large)spt; } \
\
\
/* QLabel - lbl_queue_header */\
QLabel#lbl_queue_header { font-size: %(font_size_large)spt; } \
\
\
/* QLabel - lbl_command_line_header */\
QLabel#lbl_command_line_header { font-size: %(font_size_large)spt; } \
\
\
/* QLabel - lbl_constants_header */\
QLabel#lbl_constants_header { font-size: %(font_size_large)spt; } \
\
\
/* QLabel - lbl_general_options_header */\
QLabel#lbl_general_options_header { font-size: %(font_size_large)spt; } \
\
\
\
\
\
\
/* RenderThreadsDockWidget */\
RenderThreadsDockWidget { background: %(black)s; \
                            font-size: %(font_size_default)spt; \
                            color: %(grey)s; \
} \
\
\
/* RenderThreadsDockWidget - title */\
RenderThreadsDockWidget::title { background: %(black)s; \
                                text-align: left; \
                                font-size: %(font_size_large)spt; \
                                color: %(grey)s; \
                                border-left: none; \
                                border-top: 1px solid %(red)s; \
                                border-bottom: none; \
                                border-right: none; \
} \
\
\
RenderThreadsDockWidget::close-button, RenderThreadsDockWidget::float-button {background: %(red)s; \
                                                                                border: none; \
} \
\
\
RenderThreadsDockWidget::close-button:hover, RenderThreadsDockWidget::float-button:hover { background: %(red_dark)s; \
} \
\
\
RenderThreadsDockWidget::close-button:pressed, RenderThreadsDockWidget::float-button:pressed { background: %(red_dark)s; \
} \
\
\
\
\
\
\
/* RenderThreadsProgressBar */\
RenderThreadsProgressBar { border-left: none; \
                            border-top: 1px solid %(red)s; \
                            border-bottom: none; \
                            border-right: none; \
                            background-color: %(black)s;\
                            color: %(white)s;\
                            text-align: center;\
} \
\
\
/* RenderThreadsProgressBar - chunk */\
RenderThreadsProgressBar::chunk { border: none;\
                                    background-color: %(red)s;\
} \
\
\
\
\
\
\
/* QScrollBar - vertical */\
QScrollBar:vertical { background-color: %(black)s; \
                        border: none; \
} \
\
\
/* QScrollBar - handle - vertical */\
QScrollBar::handle:vertical { background-color: %(red)s; \
                                border: none; \
} \
\
\
\
\
\
\
/* QSlider - groove - horizontal */\
QSlider::groove:horizontal { background: %(red)s; \
                                height: 1px; \
} \
\
\
/* QSlider - handle - horizontal */\
QSlider::handle:horizontal { background: %(black)s; \
                                margin: -6px 0; \
                                width: 4px; \
} \
\
\
\
\
\
\
/* QPushButton */\
QPushButton { border: none;\
                background-color: %(white)s;\
                color: %(grey)s;\
                text-align: center;\
} \
\
\
/* QPushButton - pressed */\
QPushButton:pressed { border: none;\
                        background-color: %(white)s;\
                        color: %(red_bright)s;\
                        text-align: center;\
} \
\
\
\
\
\
\
/* QLCDNumber */\
QLCDNumber { background: transparent; \
                border: none; \
} \
\
\
\
\
\
\
/* QTableCornerButton */\
QTableCornerButton { background-color: %(white)s; \
                        border: none; \
}\
\
\
/* QTableCornerButton - section */\
QTableCornerButton::section { background-color: %(white)s; \
                                border: none; \
}\
\
\
\
\
\
\
/* RenderThreadsView - nodes_view */\
RenderThreadsView#nodes_view { background-color: %(white)s; \
                                alternate-background-color: %(white_dark)s; \
                                selection-background-color: %(red)s; \
                                color: %(black)s;\
                                border-left: none; \
                                border-top: none; \
                                border-bottom: none; \
                                border-right: none; \
} \
\
\
/* RenderThreadsView - nodes_view - item */\
RenderThreadsView#nodes_view::item { border-left: none; \
                                        border-top: none; \
                                        border-bottom: none; \
                                        border-right: none; \
} \
\
\
\
\
\
\
/* QHeaderView - nodes_view_horizontal_header*/\
QHeaderView#nodes_view_horizontal_header{ background-color: %(white)s; \
                                            border-left: none; \
                                            border-top: none; \
                                            border-bottom: 1px solid %(black)s; \
                                            border-right: none; \
} \
\
\
/* QHeaderView - nodes_view_horizontal_header - section */\
QHeaderView#nodes_view_horizontal_header::section { background-color: %(white)s; \
                                                    font-weight: bold; \
                                                    border-left: none; \
                                                    border-top: none; \
                                                    border-bottom: none; \
                                                    border-right: 1px solid %(red)s; \
} \
\
\
/* QHeaderView - nodes_view_vertical_header */\
QHeaderView#nodes_view_vertical_header { background-color: %(white)s; \
                                            border-left: none; \
                                            border-top: none; \
                                            border-bottom: none; \
                                            border-right: none; \
} \
\
\
/* QHeaderView - nodes_view_vertical_header - section */\
QHeaderView#nodes_view_vertical_header::section { background-color: %(white)s; \
                                                    border-left: none; \
                                                    border-top: none; \
                                                    border-bottom: none; \
                                                    border-right: none; \
} \
\
\
\
\
\
\
/* NodesContextMenu */\
NodesContextMenu { background-color: %(white)s; \
                    color: %(grey)s; \
                    border-left: none; \
                    border-top: 1px solid %(red)s; \
                    border-bottom: none; \
                    border-right: none; \
} \
\
\
/* NodesContextMenu -item - selected */\
NodesContextMenu::item:selected { background-color: %(white)s; \
} \
\
\
\
\
\
\
/* QTextEdit */\
QTextEdit { background-color: %(white)s; \
            selection-background-color: %(red)s; \
            color: %(black)s; \
            border-left: none; \
            border-top: none; \
            border-bottom: none; \
            border-right: none; \
} \
\
\
\
\
\
\
/* QLineEdit */\
QLineEdit { background-color: %(white)s; \
            selection-background-color: %(red)s; \
            color: %(black)s; \
            border-left: 1px solid %(grey)s; \
            border-top: 1px solid %(grey)s; \
            border-bottom: 1px solid %(grey)s; \
            border-right: 1px solid %(grey)s; \
} \
\
\
\
\
\
\
/* QSpinBox */\
QSpinBox { background-color: %(white)s; \
            selection-background-color: %(red)s; \
            color: %(black)s; \
            border-left: 1px solid %(grey)s; \
            border-top: 1px solid %(grey)s; \
            border-bottom: 1px solid %(grey)s; \
            border-right: 1px solid %(grey)s; \
} \
\
\
/* QSpinBox - up-button */\
QSpinBox::up-button { background-color: %(red)s; \
                        color: %(black)s; \
                        border-left: none; \
                        border-top: 1px solid %(black)s; \
                        border-bottom: none; \
                        border-right: 1px solid %(black)s; \
} \
\
\
/* QSpinBox - up-button - hover */\
QSpinBox::up-button:hover { background-color: %(red_bright)s; \
                            color: %(black)s; \
                            border-left: none; \
                            border-top: 1px solid %(black)s; \
                            border-bottom: none; \
                            border-right: 1px solid %(black)s; \
} \
\
\
/* QSpinBox - down-button */\
QSpinBox::down-button { background-color: %(red_dark)s; \
                        color: %(black)s; \
                        border-left: none; \
                        border-top: none; \
                        border-bottom: 1px solid %(black)s; \
                        border-right: 1px solid %(black)s; \
} \
\
\
/* QSpinBox - down-button - hover */\
QSpinBox::down-button:hover { background-color: %(red_bright)s; \
                                color: %(black)s; \
                                border-left: none; \
                                border-top: none; \
                                border-bottom: 1px solid %(black)s; \
                                border-right: 1px solid %(black)s; \
} \
\
\
\
\
\
\
/* QComboBox */\
QComboBox { background-color: %(white)s; \
            selection-background-color: %(red)s; \
            color: %(black)s; \
            border-left: 1px solid %(grey)s; \
            border-top: 1px solid %(grey)s; \
            border-bottom: 1px solid %(grey)s; \
            border-right: 1px solid %(grey)s; \
} \
\
\
/* QComboBox - drop-down */\
QComboBox::drop-down { background-color: %(white)s; \
                        selection-background-color: %(red)s; \
                        color: %(black)s; \
                        border-left: none; \
                        border-top: none; \
                        border-bottom: none; \
                        border-right: none; \
} \
\
\
/* QComboBox - down-arrow */\
QComboBox::down-arrow { border-image: url(%(header_image)s) 1; \
} \
\
\
\
\
\
\
/* QScrollArea */\
QScrollArea { border-left: none; \
                border-top: none; \
                border-bottom: none; \
                border-right: none; \
} \
\
\
\
\
\
\
/* QCheckBox */\
QCheckBox { background-color: %(white)s; \
} \
\
\
/* QCheckBox - disabled */\
QCheckBox:disabled { background-color: %(red)s; \
} \
" % ss_dict

    # return
    return str_stylesheet
