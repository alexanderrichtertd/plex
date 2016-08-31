#*************************************************************
# TITLE         libImport
#
# CONTENT:      main functions
#
# AUTHOR        Alexander Richter 
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
import sys

# from PySide.QtGui import *
# from PySide.QtCore import *

#sys.path.append("..")
import settings as s

#sys.path.append(s.PATH["lib"])
from lib import libLog
from lib import libUser
from lib import libRender
from lib import libFunction
from lib import libMessageBox
from lib import libFileService

from utilities import arReport


#**********************
# VARIABLE
#**********************
# TITLE           = os.path.splitext(os.path.basename(__file__))[0]
# LOG             = ""


#************************
# LOG
#************************
def log(title):
    import logging
    LOG = libLog.initLog(software=os.environ["SOFTWARE"], script=title, level=logging.INFO, logger=logging.getLogger(title))
    LOG.info("START")
    return LOG


#**********************
# CLICKED_TRIGGER
#**********************
def clicked_btnCancel():
    global LOG
    LOG.info("END : CANCEL")
    WIDGET.close() 


def clicked_btnReport():
    global LOG
    LOG.info("REPORT")
    arReport.start("Save", os.environ["SOFTWARE"])


def clicked_btnHelp():
    global LOG
    LOG.info("HELP")
    libFunction.getHelp()


def clicked_btnOpenFolder():
    global SAVE_DIR
    ui.edtMsg.setText(libFunction.openFolder(SAVE_DIR))


def clicked_btnFileSearch():
    global SAVE_DIR
    # TODO: create new file
    output = libMessageBox.folderMsgBox(WIDGET, os.environ["SOFTWARE"] + "files (*" + s.FILE_FORMAT[os.environ["SOFTWARE"]] + ")", "choose " + os.environ["SOFTWARE"] + " file to open", SAVE_DIR)
    initPath(output)


def clicked_btnScreenshot():
    global LOG
    libRender.createScreenshot(WIDGET, ui.lblShotImg, LOG)


def clicked_btnSnapshotRender():
    global LOG
    libRender.createSnapshotRender(WIDGET, ui.lblShotImg, LOG)


def clicked_btnSnapshotViewport():
    global LOG
    libRender.createSnapshotViewport(WIDGET, ui.lblShotImg, LOG)