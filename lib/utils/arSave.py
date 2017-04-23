#*********************************************************************
# content   = saves work and publish files
#             executes other scripts on PUBLISH (on task in file name)
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <contact@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys
import shutil

from PySide.QtGui import *
from PySide.QtCore import *
from PySide import QtUiTools

import settings as s
from img import img_rc

import libLog
import libUser
import libImage
import libRender
import libFunction
import libMessageBox
import libFileService

from utilities import arReport


#**********************
# VARIABLE
#**********************
TITLE       = os.path.splitext(os.path.basename(__file__))[0]
LOG         = ""

SAVE_DIR    = s.PATH["project"]
SAVE_FILE   = ""
MSG_COMMENT = "Comment"

PATH_UI     = s.PATH["utilities"] + "/ui/" + TITLE + ".ui"
PATH_IMG    = ""

#**********************
# RUN DOS RUN
#**********************
WIDGET = QtUiTools.QUiLoader().load(PATH_UI)


#************************
# LOG
#************************
def log():
    global LOG
    import logging
    LOG = libLog.initLog(software=os.environ["SOFTWARE"], script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))


#**********************
# CLICKED_TRIGGER
#**********************
def clicked_btnAccept():
    saveFile()
    WIDGET.close()


def clicked_btnCancel():
    global LOG
    LOG.info("END : CANCEL")
    WIDGET.close()


def clicked_btnOpenFolder():
    global SAVE_DIR
    WIDGET.edtMsg.setText(libFunction.openFolder(SAVE_DIR))


def clicked_btnReport():
    global LOG
    LOG.info("REPORT")
    arReport.start("Save")


def clicked_btnHelp():
    global LOG
    LOG.info("HELP")
    libFunction.getHelp()


def clicked_btnFileSearch():
    global SAVE_DIR
    output = libMessageBox.folderMsgBox(WIDGET, os.environ["SOFTWARE"] + "files (*" + s.FILE_FORMAT[os.environ["SOFTWARE"]] + ")", "choose " + os.environ["SOFTWARE"] + " file to open", SAVE_DIR)
    initPath(output)


def clicked_btnVersionUp():
    global SAVE_FILE
    updateVersion(SAVE_FILE)
    changed_edtComment()


def clicked_btnVersionDown():
    global SAVE_FILE
    updateVersion(SAVE_FILE, False)
    changed_edtComment()


def clicked_btnPreviewImg(event):
    global WIDGET, LOAD, PATH_IMG
    PATH_IMG = PATH_IMG.replace("\\", "/")
    if LOAD:
        if os.path.exists(PATH_IMG):
            os.system(PATH_IMG)
    else:
        PATH_IMG = libMessageBox.folderMsgBox(WIDGET, "Image Files (*.jpg *.png *.tif)", "Choose image file", os.environ['USERPROFILE'] + "/Desktop")
        WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libFunction.getReportImg(PATH_IMG))))


def clicked_btnScreenshot():
    global LOG
    libRender.createScreenshot(WIDGET, WIDGET.btnPreviewImg, LOG)


def clicked_btnSnapshotRender():
    global LOG
    libRender.createSnapshotRender(WIDGET, WIDGET.btnPreviewImg, LOG)


def clicked_btnSnapshotViewport():
    global LOG
    libRender.createSnapshotViewport(WIDGET, WIDGET.btnPreviewImg, LOG)


def clicked_btnSwitchToSaveAs():
    global LOG

    WIDGET.close()

    import arSaveAs
    reload(arSaveAs)
    arSaveAs.start()

    LOG.info("END : Switch To SaveAs")


#**********************
# CHANGED_TRIGGER
#**********************
def changed_publish():
    if(WIDGET.cbxPublish.isChecked()):
        WIDGET.edtComment.setEnabled(False)
        WIDGET.edtComment.setPlainText('')
    else:
        WIDGET.edtComment.setEnabled(True)


def changed_edtComment():
    global SAVE_FILE

    if not (WIDGET.edtComment.text() == MSG_COMMENT):
        if (WIDGET.edtComment.text().isalnum() == False and WIDGET.edtComment.text() != ""):
            WIDGET.edtComment.textCursor().deletePreviousChar()
            # WIDGET.edtMsg.setText("FAIL: Comment uses alphanumeric character. Please use lower camelCase!")
            print ("FAIL: Comment uses alphanumeric character. Please use lower camelCase!")
        elif (len(WIDGET.edtComment.text()) < 20):
            if not (WIDGET.edtComment.text() == ''):
                WIDGET.edtSaveFile.setText(SAVE_FILE + '_' + WIDGET.edtComment.text() + s.FILE_FORMAT[os.environ["SOFTWARE"]])
            else:
                WIDGET.edtSaveFile.setText(SAVE_FILE + s.FILE_FORMAT[os.environ["SOFTWARE"]])
        else:
            WIDGET.edtComment.textCursor().deletePreviousChar()
            WIDGET.edtMsg.setText("FAIL : Comment is to long")


def changed_edtSaveFile():
    # global SAVE_DIR, SOFTWARE, SAVE_FILE
    # currentFile = WIDGET.edtMsg.text()

    # if(len(currentFile.split('.')) > 1):
    #     tmpFile = currentFile.split('.')[0]

    #     if (len(tmpFile.split('_')) > 4):
    #         tmpFile = tmpFile.split('_')
    #     else:
    #         WIDGET.edtMsg.setText('NAME CONVENTION: Not conform name setting - ' + s.CONVENTION["shots"])

    WIDGET.edtMsg.setText(SAVE_DIR + "/" + WIDGET.edtSaveFile.text())


#**********************
# FUNCTIONS
#**********************
def initPath(filePath = ''):
    global SAVE_FILE, SAVE_DIR

    msg = checkCurrentFile()

    if(filePath == ''):
        if os.environ["SOFTWARE"] == "maya":
            import maya.cmds as cmds
            filePath = cmds.file(q = True , sn = True)

        elif os.environ["SOFTWARE"] == "nuke":
            import nuke
            filePath = nuke.toNode("root").name()

        elif os.environ["SOFTWARE"] == "houdini":
            print "file->houdini"

        if not filePath or filePath == "Root":
            return False

    SAVE_DIR  = os.path.dirname(filePath)
    SAVE_FILE = os.path.basename(filePath).split(".")[0]

    WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getShotImg(SAVE_FILE[0]))))

    updateVersion(SAVE_FILE)

    if(s.STATUS["publish"] in SAVE_DIR):
        SAVE_DIR = SAVE_DIR.replace(s.STATUS["publish"], s.STATUS["work"])

    if(msg == ""):
        msg = SAVE_DIR + "/" + str(SAVE_FILE) + s.FILE_FORMAT[os.environ["SOFTWARE"]]

    WIDGET.edtMsg.setText(msg.replace("/", "\\"))

    if not libRender.createSnapshotRender(WIDGET, WIDGET.btnPreviewImg, LOG):
        libRender.createSnapshotViewport(WIDGET, WIDGET.btnPreviewImg, LOG)

    return True


def checkCurrentFile():
    global SAVE_FILE
    # if not (SAVE_FILE == "" or len(SAVE_FILE.split("_")) < 2):
    #     return ""

    # # if len(part) == 4 and part.startswith("v") and part[1:].isdigit():
    # #     return ""

    # SAVE_FILE = s.CONVENTION["shots"] + s.FILE_FORMAT[os.environ["SOFTWARE"]]
    # return "FAIL : File is not pipeline conform"
    return ""


def updateVersion(fileName, add = True, publish = False):
    global SAVE_FILE

    tmpFileName   = []
    for part in fileName.split("_"):
        # check for version
        if len(part) == 4 and part.startswith("v") and part[1:].isdigit():
            if publish:
                break

            version = part.replace('v', '')

            if add:
                part    = 'v' + str('{0:03d}'.format(int(version) + 1))
            elif not add and int(version) > 0:
                part    = 'v' + str('{0:03d}'.format(int(version) - 1))

        # check for user initials
        elif len(part) == 2 and part.isalpha():
            part = os.getenv('username')[0:2]
            tmpFileName.append(part)
            break

        tmpFileName.append(part)

    SAVE_FILE = ("_").join(tmpFileName)

    WIDGET.edtSaveFile.setText(SAVE_FILE + s.FILE_FORMAT[os.environ["SOFTWARE"]])


def saveFile():
    global LOG, SAVE_DIR, SAVE_FILE

    if os.environ["SOFTWARE"] == "maya":
        import maya.mel as mel
        import maya.cmds as cmds
    elif os.environ["SOFTWARE"] == "nuke":
        import nuke
    elif os.environ["SOFTWARE"] == "houdini":
        print "import houdini"

    msg = "File was saved!\n\n"
    sceneReference  = []

    # USE ADDITIONAL PUBLISH SCRIPTS
    if WIDGET.cbxPublish.isChecked():
        msg = "File was published!\n\n"

        clicked_btnVersionUp()

        try:
            # CUSTOM TASK SCRIPTS
            if s.TASK["modeling"] in SAVE_FILE:
                print ("PUBLISH: " + s.TASK["modeling"])

            if s.TASK["shading"] in SAVE_FILE:
                print ("PUBLISH: " + s.TASK["shading"])

            if s.TASK["rigging"] in SAVE_FILE:
                print ("PUBLISH: " + s.TASK["rigging"])

            if s.TASK["lighting"] in SAVE_FILE:
                print ("PUBLISH: " + s.TASK["lighting"])

        except:
            msgFailed = "SORRY : SAVE : A helping script failed"
            msg += msgFailed
            LOG.error(msgFailed, exc_info=True)

    tmpSavePath = SAVE_DIR + "/" + WIDGET.edtSaveFile.text()

    # MsgBox: File exists
    if os.path.exists(tmpSavePath):
        LOG.info("OVERWRITE")
        if QMessageBox.Cancel == libMessageBox.questionMsgBox("Overwrite", "File exists", "Overwrite the file?", QMessageBox.Warning):
            LOG.warning("FAIL : SAVE : Overwrite canceled")
            return

    if not libRender.createSnapshotRender(WIDGET, WIDGET.btnPreviewImg, LOG):
        libRender.createSnapshotViewport(WIDGET, WIDGET.btnPreviewImg, LOG)

    libRender.saveSnapshotImg(tmpSavePath)

    try:
        if os.environ["SOFTWARE"] == "maya":
            cmds.file( rename = tmpSavePath)
            cmds.file( save = True, type = s.FILE_FORMAT_CODE[s.FILE_FORMAT[os.environ["SOFTWARE"]]] )

        elif os.environ["SOFTWARE"] == "nuke":
            nuke.scriptSaveAs(tmpSavePath)

        elif os.environ["SOFTWARE"] == "houdini":
            print "houdini save"

        msg = tmpSavePath
        LOG.info('END  : SAVE : ' + tmpSavePath)

    except:
        msg = "FAIL : SAVE : Couldnt save file"
        LOG.error('FAIL : SAVE : Couldnt save file - ' + tmpSavePath, exc_info=True)


    if WIDGET.cbxPublish.isChecked():
        # COPY FILE WITH _PUBLISH
        clicked_btnVersionDown()
        tmpCopyWork = SAVE_DIR + "/" + SAVE_FILE + '_' + s.STATUS["publish"] + s.FILE_FORMAT[os.environ["SOFTWARE"]]
        libRender.saveSnapshotImg(tmpCopyWork)
        print "_PUBLISH: " + tmpCopyWork
        shutil.copy(tmpSavePath, tmpCopyWork)

        updateVersion(SAVE_FILE, True, True)

        if s.STATUS["work"] in SAVE_DIR:
            SAVE_DIR = SAVE_DIR.replace(s.STATUS["work"], s.STATUS["publish"])

        libFunction.createFolder(SAVE_DIR)
        # if s.TASK["animation"] in SAVE_FILE:
        #     print ("ANIM PUBLISH")
        #     # from scripts.ANIM import alembicExport
        #     # msg = "File was saved!\n\n" + alembicExport.exportAlembic()
        #     # LOG.info("PUBLISH : ALEMBIC")
        # else:
            # NEW

        tmpPath = SAVE_DIR + "/" + SAVE_FILE + s.FILE_FORMAT[os.environ["SOFTWARE"]]

        shutil.copy(tmpSavePath, tmpPath)
        LOG.info("PUBLISH : " + tmpPath)
        libRender.saveSnapshotImg(tmpPath)

    QMessageBox.information(WIDGET, "Save", msg.replace("/","\\"))

    LOG.info("END  : SAVE : " + tmpSavePath)


#**********************
# START PROZESS
#**********************
def init():
    userData = libUser.getUser(os.getenv('username'))
    libImage.setUserImg(os.getenv('username'), WIDGET.lblUser)

    if os.getenv('username') in s.TEAM["admin"]:
        libFunction.setErrorCount(WIDGET)
    else:
        WIDGET.lblErrorCount.hide()

    return initPath()


#**********************
# START UI
#**********************
def start():
    global LOG, PATH_IMG, TITLE

    PATH_IMG = libFunction.rmTempImg()

    WIDGET.connect(WIDGET.btnAccept, SIGNAL("clicked()"), clicked_btnAccept)
    WIDGET.connect(WIDGET.btnHelp, SIGNAL("clicked()"), clicked_btnHelp)
    WIDGET.connect(WIDGET.btnOpenFolder, SIGNAL("clicked()"), clicked_btnOpenFolder)
    WIDGET.connect(WIDGET.btnReport, SIGNAL("clicked()"), clicked_btnReport)
    WIDGET.connect(WIDGET.btnFolder, SIGNAL("clicked()"), clicked_btnFileSearch)
    WIDGET.connect(WIDGET.btnVersionUp, SIGNAL("clicked()"), clicked_btnVersionUp)
    WIDGET.connect(WIDGET.btnVersionDown, SIGNAL("clicked()"), clicked_btnVersionDown)

    WIDGET.connect(WIDGET.btnPreviewImg, SIGNAL("clicked()"), clicked_btnPreviewImg)
    WIDGET.connect(WIDGET.btnScreenshot, SIGNAL("clicked()"), clicked_btnScreenshot)
    WIDGET.connect(WIDGET.btnSnapshotRender, SIGNAL("clicked()"), clicked_btnSnapshotRender)
    WIDGET.connect(WIDGET.btnSnapshotViewport, SIGNAL("clicked()"), clicked_btnSnapshotViewport)

    WIDGET.connect(WIDGET.btnSwitchToSaveAs, SIGNAL("clicked()"), clicked_btnSwitchToSaveAs)

    WIDGET.cbxPublish.toggled.connect(changed_publish)
    WIDGET.edtSaveFile.textChanged.connect(changed_edtSaveFile)

    WIDGET.edtComment.textChanged.connect(changed_edtComment)

    # WIDGET : always on top
    WIDGET.setWindowFlags(Qt.WindowStaysOnTopHint)

    if init():
        log()
        if os.environ["SOFTWARE"] == "nuke":
            saveFile()
        else:
            WIDGET.show()
    else:
        import arSaveAs
        reload(arSaveAs)
        arSaveAs.start()

# 587 - 442 = 145 * 100/587 = 25%    before: 86 rows - 14%
