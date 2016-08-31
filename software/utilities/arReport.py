#*************************************************************
# TITLE         arReport
#
# SOFTWARE      Maya, Nuke, Houdini
#
# CONTENT       send an error or suggestion report
#
# AUTHOR        Alexander Richter 
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
import sys
import time
import shutil
import logging
import webbrowser

from datetime import datetime

from PySide import QtUiTools
from PySide.QtGui import *
from PySide.QtCore import *

import settings as s
from img import img_rc

import libLog
import libImage
import libRender
import libFunction
import libFileService
import libMessageBox


#************************
# REPORT
#************************
class Report:
    def __init__(self, software = "unknown", user = "John Doe", filePath = "", reason = "bug", script =  "other", comment = "", error = ""):        
        self.time       = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        self.software   = software  #maya
        self.user       = user      #arichter
        self.file       = filePath  #project/shot
        self.reason     = reason    #bug
        self.script     = script    #save
        self.comment    = comment   #breaks after save
        self.error      = error     #troubleshot: file input line:234

    def __call__(self):
        return (\
        "time:     " + self.time + "\n" +\
        "software: " + self.software + "\n" +\
        "user:     " + self.user + "\n" + "\n" +\
        "file:     " + self.file + "\n" + "\n" +\
        "reason:   " + self.reason + "\n" +\
        "script:   " + self.script + "\n" +\
        "comment:  " + self.comment + "\n" +\
        "error:    " + self.error + "\n")


#**********************
# VARIABLE
#**********************
TITLE           = os.path.splitext(os.path.basename(__file__))[0]
LOG             = ""

REPORTS         = ""
REPORT_INDEX    = 0
REPORT_DATA     = Report()

MSG_ERROR       = "Error Message"
MSG_COMMENT     = "Comment"
SAVE_DIR        = ""

PATH_IMG        = ""
PATH_UI         = s.PATH["utilities"] + "/ui/" + TITLE + ".ui"
 

#**********************
# RUN DOS RUN
#**********************
WIDGET   = QtUiTools.QUiLoader().load(PATH_UI)


#************************
# LOG
#************************
def log():
    global LOG
    import logging
    LOG = libLog.initLog(software=os.environ["SOFTWARE"], script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))
    LOG.info("START")


#**********************
# CLICKED_TRIGGER
#**********************
def clicked_btnAccept():
    saveReport()
    WIDGET.close() 


def clicked_cancel():
    global LOG
    LOG.info("END : CANCEL")
    WIDGET.close()


def clicked_btnHelp():
    global LOG
    LOG.info("HELP")
    libFunction.getHelp()


def clicked_showReport():
    global REPORTS
    
    if (WIDGET.edtComment.isReadOnly()):
        WIDGET.edtComment.setReadOnly(False)
        WIDGET.edtScript.setReadOnly(False)
        WIDGET.edtErrorMsg.setReadOnly(False)
        
        WIDGET.btnAccept.show()
        WIDGET.btnCancel.show()     
        WIDGET.btnScreenshot.show() 
        WIDGET.btnSnapshotRender.show()  
        WIDGET.btnSnapshotViewport.show()     

        WIDGET.btnBefore.hide()
        WIDGET.btnNext.hide()  
        WIDGET.btnSaveToHistory.hide()  
        WIDGET.btnFolder.hide()  
        WIDGET.btnOpenFile.hide()  

        WIDGET.cbxReport.clear()
        WIDGET.cbxScript.clear()

        init()
        WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(""))))

    else:
        WIDGET.edtComment.setReadOnly(True)
        WIDGET.edtScript.setReadOnly(True)
        WIDGET.edtErrorMsg.setReadOnly(True)
        
        WIDGET.btnAccept.hide()
        WIDGET.btnCancel.hide()    
        WIDGET.btnScreenshot.hide()  
        WIDGET.btnSnapshotRender.hide()  
        WIDGET.btnSnapshotViewport.hide()  
         
        WIDGET.btnBefore.show()
        WIDGET.btnNext.show() 
        WIDGET.btnSaveToHistory.show() 
        WIDGET.btnFolder.show() 
        WIDGET.btnOpenFile.show()  
       
        REPORTS = libFileService.getFolderList(s.PATH["data_report"], "*.json")

        setReports(len(REPORTS) - 1)


def clicked_previousReport():
    setReports(-1)


def clicked_nextReport():
    setReports(1)


def clicked_saveToHistory():
    global LOG, REPORTS, REPORT_INDEX, PATH_IMG
    
    if(len(REPORTS) < 1):
        return

    src = s.PATH["data_report"] + "/" + REPORTS[REPORT_INDEX] + s.FILE_FORMAT["data"]
    dst = s.PATH["data_report_history"] + "/" + REPORTS[REPORT_INDEX] + s.FILE_FORMAT["data"]
    libFunction.createFolder(dst)
    
    if os.path.exists(src):
        shutil.move(src, dst)

    src = s.PATH["data_report_img"] + "/" + REPORTS[REPORT_INDEX] + s.FILE_FORMAT["thumbs"]
    dst = s.PATH["data_report_img"] + "/" + s.STATUS["history"] + "/" + REPORTS[REPORT_INDEX] + s.FILE_FORMAT["thumbs"]
    libFunction.createFolder(dst)

    if not (dst.endswith("000.png")): 
        if(os.path.exists(src)):
            shutil.move(src, dst)

    REPORTS = libFileService.getFolderList(s.PATH["data_report"], "*" + s.FILE_FORMAT["data"])
    libFunction.setErrorCount(WIDGET)
    setReports(1)
    WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG, True))))

    LOG.info("ReportToHistory : " + REPORTS[REPORT_INDEX])


def clicked_btnOpenFolder():
    WIDGET.edtMsg.setText(libFunction.openFolder(s.PATH["data_report"]))


def clicked_btnScreenshot():
    global LOG
    libRender.createScreenshot(WIDGET, WIDGET.btnPreviewImg, LOG)


def clicked_btnSnapshotRender():
    global LOG
    libRender.createSnapshotRender(WIDGET, WIDGET.btnPreviewImg, LOG)


def clicked_btnSnapshotViewport():
    global LOG
    libRender.createSnapshotViewport(WIDGET, WIDGET.btnPreviewImg, LOG)


#**********************
# CHANGED_TRIGGER
#**********************
def changed_report():
    global PATH_IMG
    currentImgPath = s.PATH['img_maya_shelf'] + "/" + "shelf_" + WIDGET.cbxReport.currentText() + "35.png"
    
    if(WIDGET.cbxScript.currentText() == s.REPORT_LIST[os.environ["SOFTWARE"]][-1]):
        WIDGET.edtScript.show()
        changeY = 30 
    else:
        WIDGET.edtScript.hide()
        changeY = 0

    if(WIDGET.cbxReport.currentText() == s.REPORT_LIST["report"][-1]):

        WIDGET.edtErrorMsg.hide()
        WIDGET.btnScreenshot.hide()
        WIDGET.btnPreviewImg.hide()
        WIDGET.lblPreviewImgBG.hide()

        WIDGET.resize(WIDGET.width(), 160 + changeY)

        WIDGET.edtComment.resize(386, 77)

        WIDGET.edtComment.move(10, 50 + changeY)
        WIDGET.edtMsg.move(10, 135 + changeY)

        WIDGET.btnAccept.move(405, 50 + changeY)
        WIDGET.btnCancel.move(405, 100 + changeY)

        WIDGET.btnBefore.move(405, 50 + changeY)
        WIDGET.btnNext.move(455, 50 + changeY)
        WIDGET.btnFolder.move(380, 135 + changeY)
        WIDGET.btnSaveToHistory.move(455, 98 + changeY)

        WIDGET.lblUser.move(405, 135 + changeY)
        WIDGET.btnOpenFile.move(430, 135 + changeY)
        WIDGET.btnReport.move(455, 135 + changeY)
        WIDGET.lblErrorCount.move(470, 130 + changeY)
        WIDGET.btnHelp.move(480, 135 + changeY)
            
    else:
        
        if not(WIDGET.edtComment.isReadOnly()):
            WIDGET.btnScreenshot.show()
            
        WIDGET.edtErrorMsg.show()
        WIDGET.btnPreviewImg.show()
        WIDGET.lblPreviewImgBG.show()
        
        WIDGET.resize(WIDGET.width(), 245 + changeY)
        WIDGET.edtComment.resize(486, 77)

        WIDGET.edtComment.move(10, 50 + changeY)
        WIDGET.edtMsg.move(10, 220 + changeY)
        WIDGET.edtErrorMsg.move(10, 138 + changeY)
        WIDGET.btnPreviewImg.move(270, 138 + changeY)
        WIDGET.lblPreviewImgBG.move(270, 138 + changeY)
        WIDGET.btnScreenshot.move(373, 141 + changeY)
        WIDGET.btnSnapshotRender.move(373, 165 + changeY)
        WIDGET.btnSnapshotViewport.move(373, 188 + changeY)

        WIDGET.btnAccept.move(405, 138 + changeY)
        WIDGET.btnCancel.move(405, 184 + changeY)

        WIDGET.btnBefore.move(405, 138 + changeY)
        WIDGET.btnNext.move(455, 138 + changeY)
        WIDGET.btnFolder.move(380, 220 + changeY)
        WIDGET.btnSaveToHistory.move(455, 184 + changeY)

        WIDGET.lblUser.move(405, 220 + changeY)
        WIDGET.btnOpenFile.move(430, 220 + changeY)
        WIDGET.btnReport.move(455, 220 + changeY)
        WIDGET.lblErrorCount.move(470, 215 + changeY)
        WIDGET.btnHelp.move(480, 220 + changeY)

    WIDGET.edtMsg.setText(WIDGET.cbxReport.currentText() + ": " + WIDGET.cbxScript.currentText())
    WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG))))


def errorMsg_In(event):
    if(WIDGET.edtErrorMsg.toPlainText() == MSG_ERROR):
        WIDGET.edtErrorMsg.setPlainText("")
        WIDGET.edtErrorMsg.setStyleSheet("color: rgb(255, 255, 255);")
    WIDGET.edtErrorMsg.setCursorWidth(1)


def errorMsg_Out(event):
    if(WIDGET.edtErrorMsg.toPlainText() == ""):
        WIDGET.edtErrorMsg.setPlainText(MSG_ERROR)
        WIDGET.edtErrorMsg.setStyleSheet("color: rgb(175, 175, 175);")
    WIDGET.edtErrorMsg.setCursorWidth(0)


def comment_In(event):
    if(WIDGET.edtComment.toPlainText() == MSG_COMMENT):
        WIDGET.edtComment.setPlainText("")
        WIDGET.edtComment.setStyleSheet("color: rgb(255, 255, 255);")
    WIDGET.edtComment.setCursorWidth(1)


def comment_Out(event):
    if(WIDGET.edtComment.toPlainText() == ""):
        WIDGET.edtComment.setPlainText(MSG_COMMENT)
        WIDGET.edtComment.setStyleSheet("color: rgb(175, 175, 175);")
    WIDGET.edtComment.setCursorWidth(0)


def clicked_errorImg():
    global PATH_IMG

    if (WIDGET.edtComment.isReadOnly()):
        os.system(PATH_IMG)
    else:
        PATH_IMG = libMessageBox.folderMsgBox(WIDGET, "Image Files (*.jpg *.png *.tiff)", "Choose image file", os.environ['USERPROFILE'] + "/Desktop")
        WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG))))


def clicked_openFile():
    global SAVE_DIR

    try:    
        if os.environ["SOFTWARE"] == "maya":
            import maya.mel as mel
            mel.eval('file -f -options "v=0;"  -ignoreVersion  -typ "' + s.FILE_FORMAT_CODE[s.FILE_FORMAT[os.environ["SOFTWARE"]]] + '" -o "' + SAVE_DIR + '"')
        
        elif os.environ["SOFTWARE"] == "nuke":
            import nuke
            nuke.scriptOpen(SAVE_DIR)  

        elif os.environ["SOFTWARE"] == "houdini":
            print "houdini open"
        
        LOG.info ('END  : LOAD : ' + SAVE_DIR)   
    except:
        LOG.error('FAIL : LOAD : ' + SAVE_DIR, exc_info=True)  


#**********************
# FUNCTIONS
#**********************
def saveReport():
    global LOG, PATH_IMG
    
    fileName = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    dataPath = s.PATH["data_report"] + '/' + fileName + s.FILE_FORMAT["data"]
    imgPath  = s.PATH["data_report_img"] + "/" + fileName + s.FILE_FORMAT["thumbs"]
    
    if(WIDGET.cbxScript.currentText() == "other"):
        script = WIDGET.edtScript.text()
    else:
        script = WIDGET.cbxScript.currentText()

    if(WIDGET.edtComment.toPlainText() == MSG_COMMENT):
        WIDGET.edtComment.setPlainText("")  

    if(WIDGET.edtErrorMsg.toPlainText() == MSG_ERROR):
        WIDGET.edtErrorMsg.setPlainText("")

    try:
        if(os.environ["SOFTWARE"] == "maya"):
            import maya.cmds as cmds
            filePath = cmds.file(q=True,sn=True)
        elif(os.environ["SOFTWARE"] == "nuke"):
            import nuke
            filePath = nuke.root()['name'].value()    
        elif(os.environ["SOFTWARE"] == "houdini"):
            print "houdini save path"
        else: 
            filePath = ""
    except:
        LOG.error('FAIL : GET PATH', exc_info=True)  
    
    report = Report(user = os.getenv('username'), filePath = filePath, reason = WIDGET.cbxReport.currentText(), script = script, comment = WIDGET.edtComment.toPlainText(), error = WIDGET.edtErrorMsg.toPlainText(), software = os.environ["SOFTWARE"])

    libFileService.setJsonFile(dataPath, report)
    libRender.saveSnapshotImg(imgPath, "", True)
    LOG.info("END : REPORT : " + fileName)

   
def setReports(index = len(REPORTS) - 1):
    global REPORTS, REPORT_INDEX, REPORT_DATA, PATH_IMG, SAVE_DIR

    WIDGET.cbxReport.clear()
    WIDGET.cbxScript.clear()

    if len(REPORTS) < 1:
        clicked_showReport() 
        WIDGET.edtMsg.setText("No Reports at the time")
        WIDGET.edtComment.setPlainText(MSG_COMMENT)
        WIDGET.edtErrorMsg.setPlainText(MSG_ERROR)
        return

    REPORT_INDEX += index

    if (REPORT_INDEX < 0):
        REPORT_INDEX = (len(REPORTS) - 1)
    elif (REPORT_INDEX > ((len(REPORTS) - 1))):
        REPORT_INDEX = 0

    REPORT_DATA = libFileService.getJsonFile(s.PATH["data_report"] + "/" + REPORTS[REPORT_INDEX] + s.FILE_FORMAT["data"])

    WIDGET.cbxReport.addItem(REPORT_DATA["reason"])
    WIDGET.cbxScript.addItem(REPORT_DATA["script"])

    WIDGET.edtErrorMsg.setPlainText(REPORT_DATA["error"]) 
    WIDGET.edtComment.setPlainText(REPORT_DATA["comment"]) 

    WIDGET.edtMsg.setText(str(REPORT_INDEX) + ":" + str((len(REPORTS) - 1)) + " - " + REPORT_DATA["time"])
    libImage.setUserImg(REPORT_DATA["user"], WIDGET.lblUser)
  
    # change errorImg
    PATH_IMG = s.PATH["data_report_img"] + "/" + REPORTS[REPORT_INDEX] + s.FILE_FORMAT["thumbs"]
    
    WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG, True))))
    WIDGET.btnOpenFile.setIcon(QPixmap(QImage(libImage.getProgramImg(REPORT_DATA["software"]))))

    if(REPORT_DATA["file"] == ""):
        WIDGET.btnOpenFile.setEnabled(False)
        WIDGET.btnOpenFile.setToolTip("Status Report [R]")
    else:
        WIDGET.btnOpenFile.setEnabled(True)
        WIDGET.btnOpenFile.setToolTip(REPORT_DATA["file"])
        SAVE_DIR = REPORT_DATA["file"]


#**********************
# INIT
#**********************
def init(currentScript = "other"):
    global PATH_IMG

    libImage.setUserImg(os.getenv('username'), WIDGET.lblUser)

    if os.getenv('username') in s.TEAM["admin"]:
        libFunction.setErrorCount(WIDGET) 
    else:
        WIDGET.btnReport.hide()
        WIDGET.btnFolder.hide()
        WIDGET.lblErrorCount.hide()

    WIDGET.cbxReport.addItems(s.REPORT_LIST["report"])
    
    try:
        WIDGET.cbxScript.addItems(s.REPORT_LIST[os.environ["SOFTWARE"]])
    except:
        WIDGET.cbxScript.addItems(s.REPORT_LIST["other"])
        
    WIDGET.edtComment.setPlainText(MSG_COMMENT)
    WIDGET.edtErrorMsg.setPlainText(MSG_ERROR)

    tmpIndex = WIDGET.cbxScript.findText(currentScript)
    if tmpIndex == -1:
        tmpIndex = WIDGET.cbxScript.findText("other")

    WIDGET.cbxScript.setCurrentIndex(tmpIndex)
    WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG))))

    if os.environ["SOFTWARE"] == "nuke":
        WIDGET.btnSnapshotViewport.hide()


#**********************
# START UI
#**********************
def start(currentScript = 'other'):
    global PATH_IMG

    log()
    PATH_IMG = libFunction.rmTempImg()

    WIDGET.connect(WIDGET.btnAccept, SIGNAL("clicked()"), clicked_btnAccept)
    WIDGET.connect(WIDGET.btnCancel, SIGNAL("clicked()"), clicked_cancel)
    WIDGET.connect(WIDGET.btnHelp, SIGNAL("clicked()"), clicked_btnHelp)
    WIDGET.connect(WIDGET.btnReport, SIGNAL("clicked()"), clicked_showReport)    

    WIDGET.connect(WIDGET.btnBefore, SIGNAL("clicked()"), clicked_previousReport)
    WIDGET.connect(WIDGET.btnNext, SIGNAL("clicked()"), clicked_nextReport)
    WIDGET.connect(WIDGET.btnSaveToHistory, SIGNAL("clicked()"), clicked_saveToHistory)
    WIDGET.connect(WIDGET.btnFolder, SIGNAL("clicked()"), clicked_btnOpenFolder)
    WIDGET.connect(WIDGET.btnOpenFile, SIGNAL("clicked()"), clicked_openFile)

    WIDGET.connect(WIDGET.btnScreenshot, SIGNAL("clicked()"), clicked_btnScreenshot)
    WIDGET.connect(WIDGET.btnSnapshotRender, SIGNAL("clicked()"), clicked_btnSnapshotRender)
    WIDGET.connect(WIDGET.btnSnapshotViewport, SIGNAL("clicked()"), clicked_btnSnapshotViewport)
    WIDGET.connect(WIDGET.btnPreviewImg, SIGNAL("clicked()"), clicked_errorImg)

    WIDGET.connect(WIDGET.cbxReport, SIGNAL("currentIndexChanged(const QString&)"), changed_report)
    WIDGET.connect(WIDGET.cbxScript, SIGNAL("currentIndexChanged(const QString&)"), changed_report)
    
    WIDGET.edtErrorMsg.focusInEvent     = errorMsg_In
    WIDGET.edtErrorMsg.focusOutEvent    = errorMsg_Out    

    WIDGET.edtComment.focusInEvent      = comment_In
    WIDGET.edtComment.focusOutEvent     = comment_Out


    WIDGET.btnBefore.hide()
    WIDGET.btnNext.hide() 
    WIDGET.btnSaveToHistory.hide() 
    WIDGET.btnFolder.hide() 
    WIDGET.btnOpenFile.hide() 

    init(currentScript)

    # WIDGET : always on top
    WIDGET.setWindowFlags(Qt.WindowStaysOnTopHint)

    WIDGET.show()