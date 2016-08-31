#*************************************************************
# title:        libScript
#
# software:     Maya
#
# content:      do something
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%;%PYTHONPATH%"
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import os 
import sys
import shutil
import webbrowser

from PySide.QtGui import *
from PySide.QtCore import *

from scripts.ui import saveCreate

import maya.cmds as cmds
import maya.mel as mel

import settings as s
sys.path.append(s.PATH['lib'])

from lib import libFunction

from utilities import report


#**********************
# VARIABLE
#**********************
LOG      = ""
SAVE_DIR = s.PATH["project"]


#**********************
# RUN DOS RUN
#**********************
# app     = QApplication(sys.argv)
WIDGET  = QWidget()
ui      = saveCreate.Ui_saveCreate()


#************************
# LOG
#************************
def log():
    global LOG
    TITLE = os.path.splitext(os.path.basename(__file__))[0]
    LOG   = libLog.initLog(software="maya", script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))
    LOG.info("START")




#**********************
# CLICKED_TRIGGER
#**********************
def clicked_btnAccept():
    global WIDGET, LOG
    LOG.info("END : CREATE : ")
    saveFile()
    WIDGET.close() 


def clicked_cancel():
    global WIDGET, LOG
    LOG.info("END : CANCEL")
    WIDGET.close()


def clicked_btnOpenFolder():
    global SAVE_DIR
    webbrowser.open(SAVE_DIR)


def clicked_report():
    report.start("Save")


def clicked_help():
    webbrowser.open(s.LINK["software"])


#**********************
# CHANGED_TRIGGER
#**********************
def changed_cbxShot():
    print "SHOT"


def changed_cbxShotName():
    print "SHOTNAME"


def changed_cbxTask():
    print "TASK"


#**********************
# FUNCTIONS
#**********************


#**********************
# INIT
#**********************
def init():
    CURRENT_USER = os.getenv('username')

    libFunction.setUserImg(CURRENT_USER, ui.lblUser)

    if CURRENT_USER in s.ADMIN:
        libFunction.setErrorCount(ui) 
    else:
        ui.lblErrorCount.hide()


#**********************
# START PROZESS
#**********************
def start():
    global WIDGET
    WIDGET  = QWidget()
    ui.setupUi(WIDGET)

    WIDGET.connect(ui.btnAccept, SIGNAL("clicked()"), clicked_btnAccept)
    WIDGET.connect(ui.btnCancel, SIGNAL("clicked()"), clicked_cancel)

    WIDGET.connect(ui.btnOpenFolder, SIGNAL("clicked()"), clicked_btnOpenFolder)
    WIDGET.connect(ui.btnHelp, SIGNAL("clicked()"), clicked_help)
    WIDGET.connect(ui.btnReport, SIGNAL("clicked()"), clicked_report)

    WIDGET.connect(ui.cbxShot, SIGNAL("currentIndexChanged(const QString&)"), changed_cbxShot)
    WIDGET.connect(ui.cbxShotName, SIGNAL("currentIndexChanged(const QString&)"), changed_cbxShotName)
    WIDGET.connect(ui.cbxTask, SIGNAL("currentIndexChanged(const QString&)"), changed_cbxTask)

    # ui.cbxPublish.toggled.connect(changed_publish)  
    # ui.edtSavePath.textChanged.connect(changed_edtSavePath)
    # ui.cbxPublish.toggled.connect(changed_publish) 

    WIDGET.show() 

# start()
