#*************************************************************
# CONTENT       creates folder structure (assets & shots) 
#               saves a new file
#               loads pipeline files
#
# SOFTWARE      Maya, Nuke, Houdini
#
# DEPENDENCIES  "PYTHONPATH=%SOFTWARE_PATH%;%PYTHONPATH%"
#
# AUTHOR        Alexander Richter 
# EMAIL         contact@richteralexander.com
#*************************************************************

import os 
import sys
import datetime

from threading import Thread

from PySide import QtUiTools
from PySide.QtGui import *
from PySide.QtCore import *

import settings as s
from img import img_rc

from lib import libLog
from lib import libImage
from lib import libUser
from lib import libRender
from lib import libFunction
from lib import libMessageBox
from lib import libFileService

from utilities import arReport


#**********************
# VARIABLE
#**********************
TITLE       = os.path.splitext(os.path.basename(__file__))[0]
LOG         = ""

SAVE_DIR    = s.PATH["project"]
SAVE_FILE   = ""
PATH_IMG    = ""

MSG_SHOT    = "s010_shotName"
MSG_ASSET   = "assetName"

LOAD        = False
PATH_UI     = s.PATH["utilities"] + "/ui/" + TITLE + ".ui"
 

#**********************
# RUN DOS RUN
#**********************
WIDGET = QtUiTools.QUiLoader().load(PATH_UI)


#************************
# LOG
#************************
import logging
LOG = libLog.initLog(script=TITLE, logger=logging.getLogger(TITLE))


#**********************
# CLICKED_TRIGGER
#**********************
def clicked_btnAccept(ref = False):
    global LOG, SAVE_DIR, LOAD
    LOG.info("END  : CREATE : ")
    updatePath(False)
    
    if LOAD:
        if WIDGET.cbxShotChoice.currentText():
            loadFile(ref)
        else:
            LOG.warning("FAIL : LOAD : EMPTY - " + SAVE_DIR)
    else:
        if checkInput():    
            saveFile()
        else:
            if WIDGET.cbxShot.currentText() == s.TYPE["shots"]:
                failMsg = MSG_SHOT
            else:    
                failMsg = MSG_ASSET

            if QMessageBox.Cancel == libMessageBox.questionMsgBox("Fail : Pipeline Path", "File is not pipeline conform:", failMsg +"\n\nCreate file and path anyway?", QMessageBox.Warning):
                WIDGET.edtMsg.setText("FAIL : Wrong Input : " + failMsg)
                LOG.warning("FAIL : Wrong Input : " + SAVE_DIR)
            else:
                saveFile()


def clicked_btnAcceptRef():
    clicked_btnAccept(True)


def clicked_btnCancel():
    global LOG
    LOG.info("END  : CANCEL")
    WIDGET.close()


def clicked_btnOpenFolder():
    global SAVE_DIR
    WIDGET.edtMsg.setText(libFunction.openFolder(SAVE_DIR))


def clicked_btnReport():
    global LOG, LOAD
    LOG.info("REPORT")
    if LOAD:
        arReport.start("arLoad")
    else:
        arReport.start("arSave")


def clicked_btnHelp():
    global LOG
    LOG.info("HELP")
    libFunction.getHelp()


def clicked_btnFileSearch():
    global SAVE_DIR
    output = libMessageBox.folderMsgBox(WIDGET, os.environ["SOFTWARE"] + "files (*" + s.FILE_FORMAT[os.environ["SOFTWARE"]] + ")", "choose " + os.environ["SOFTWARE"] + " file to open", SAVE_DIR)
    initPath(output)


def clicked_btnAddShotName():
    global LOG

    LOG.info("ADD : SHOT")
    if WIDGET.cbxShot.currentText() in s.TYPE["shots"]:
        WIDGET.edtShotGroup.setPlaceholderText(MSG_SHOT)
    else:
        WIDGET.edtShotGroup.setPlaceholderText(MSG_ASSET)      
        
    WIDGET.edtShotGroup.setFrame(True)
    WIDGET.edtShotGroup.setEnabled(True)
    WIDGET.edtShotGroup.setText("")

    if not libRender.createSnapshotRender(WIDGET, WIDGET.btnPreviewImg, LOG):
        libRender.createSnapshotViewport(WIDGET, WIDGET.btnPreviewImg, LOG)

    WIDGET.edtMsg.setText("Add new " + WIDGET.cbxShot.currentText())


def clicked_btnPreviewImg():
    global WIDGET, LOAD, PATH_IMG
    PATH_IMG = PATH_IMG.replace("/", "\\")
    if LOAD and os.path.exists(PATH_IMG):
        os.system(PATH_IMG)
    elif not LOAD: 
        PATH_IMG = libMessageBox.folderMsgBox(WIDGET, "Image Files (*.jpg *.png *.tif)", "Choose image file", os.environ['USERPROFILE'] + "/Desktop")
        WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG))))


def clicked_btnScreenshot():
    global LOG
    libRender.createScreenshot(WIDGET, WIDGET.btnPreviewImg, LOG)


def clicked_btnSnapshotRender():
    global LOG
    libRender.createSnapshotRender(WIDGET, WIDGET.btnPreviewImg, LOG)


def clicked_btnSnapshotViewport():
    global LOG
    libRender.createSnapshotViewport(WIDGET, WIDGET.btnPreviewImg, LOG)


def clicked_btnShowPublish():
    updatePath()


#**********************
# CHANGED_TRIGGER
#**********************
def changed_cbxShot():
    global LOAD

    WIDGET.cbxTask.clear()
    WIDGET.cbxShotName.clear()
    WIDGET.cbxShotGroup.clear()
    WIDGET.cbxShotChoice.clear()

    taskList = []
    
    if LOAD: addGroupWidth = 30
    else:    addGroupWidth = 0
        
    if WIDGET.cbxShot.currentText() in s.TYPE_DIRECT:
        WIDGET.cbxShotName.hide()
        WIDGET.edtShotName.hide()

        WIDGET.cbxShotGroup.setGeometry(270, 15, 151 + addGroupWidth, 22) 
        WIDGET.edtShotGroup.setGeometry(270, 47, 181, 22)

        if os.environ["SOFTWARE"] == "nuke":
            shotList = sorted(libFileService.getFolderList(s.PATH["comp"]))
        else:
            shotList = sorted(libFileService.getFolderList(s.PATH[WIDGET.cbxShot.currentText().lower()]))
        WIDGET.cbxShotGroup.addItems(shotList)

    else:
        WIDGET.cbxShotName.show()
        WIDGET.edtShotName.show()

        WIDGET.cbxShotGroup.setGeometry(330, 15, 91 + addGroupWidth, 22) 
        WIDGET.edtShotGroup.setGeometry(330, 47, 121, 22)
        
        WIDGET.cbxShotName.addItems(sorted(libFileService.getFolderList(s.PATH[WIDGET.cbxShot.currentText().lower()])))   


    if WIDGET.cbxShot.currentText() in s.TYPE["shots"]:
        taskList = s.TASK_SHOTS_FOLDER.itervalues()    
    elif WIDGET.cbxShot.currentText() in s.TYPE["assets"]:
        taskList = s.TASK_ASSETS_FOLDER.itervalues()
    else:
        taskList = s.TASK_DEFAULT_FOLDER.itervalues()


    if not os.environ["SOFTWARE"] == "nuke" and not LOAD:
        itemList    = []
        for item in taskList:
            if not item == s.TASK_SHOTS_FOLDER["compositing"]:
                itemList.append(item)

        WIDGET.cbxTask.addItems(sorted(itemList))
    
    WIDGET.edtShot.setText(WIDGET.cbxShot.currentText())  


def changed_cbxShotName():
    if not WIDGET.cbxShot.currentText() in s.TYPE_DIRECT:
        WIDGET.cbxShotGroup.clear()
        WIDGET.cbxShotChoice.clear()
        WIDGET.cbxShotGroup.addItems(sorted(libFileService.getFolderList(s.PATH[WIDGET.cbxShot.currentText().lower()] + "/" + WIDGET.cbxShotName.currentText()))) 
        # WIDGET.edtShotGroup.setText(WIDGET.cbxShotGroup.currentText())
        WIDGET.edtShotName.setText(WIDGET.cbxShotName.currentText())


def changed_cbxShotGroup():
    global LOAD

    if LOAD:
        WIDGET.cbxTask.clear()

    if WIDGET.cbxShotGroup.currentText():
        WIDGET.edtShotGroup.setText(WIDGET.cbxShotGroup.currentText())
        updatePath()

    if LOAD:
        if WIDGET.cbxShot.currentText() in s.TYPE_DIRECT:
            pathPart = WIDGET.cbxShotGroup.currentText()
        else:
            pathPart = WIDGET.cbxShotName.currentText() + "/" + WIDGET.cbxShotGroup.currentText()

        tmpTaskList = sorted(libFileService.getFolderList(s.PATH[WIDGET.cbxShot.currentText().lower()] + "/" + pathPart))
        
        if tmpTaskList:
            if os.environ["SOFTWARE"] == "nuke":
                if s.TASK_FOLDER["compositing"] in tmpTaskList:
                    WIDGET.cbxTask.addItem(s.TASK_FOLDER["compositing"])

            else:    
                if s.TASK_FOLDER["compositing"] in tmpTaskList:
                    tmpTaskList.remove(s.TASK_FOLDER["compositing"])
                WIDGET.cbxTask.addItems(tmpTaskList) 

def changed_cbxTask():
    WIDGET.edtTask.setText(WIDGET.cbxTask.currentText())
    if WIDGET.cbxTask.currentText():
        updatePath()


def changed_cbxShotChoice ():
    global PATH_IMG
    
    updatePath(False)
    WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG, True))))


#**********************
# FUNCTIONS
#**********************
def updatePath(reloadDrop = True):
    global LOAD, SAVE_DIR, SAVE_FILE, PATH_IMG

    if WIDGET.cbxShot.currentText() in s.TYPE_DIRECT:
        if os.environ["SOFTWARE"] in ["maya", "houdini"]:    
            shotPath = s.PATH[WIDGET.cbxShot.currentText().lower()] + "/" + WIDGET.edtShotGroup.text()
        elif os.environ["SOFTWARE"] == "nuke":
            shotPath = s.PATH["comp"] + "/" + WIDGET.edtShotGroup.text()        
        else: 
            shotPath = s.PATH[WIDGET.cbxShot.currentText().lower()] + "/" + WIDGET.edtShotGroup.text()
    else:
        shotPath = s.PATH[WIDGET.cbxShot.currentText().lower()] + "/" + WIDGET.edtShotName.text() + "/" + WIDGET.edtShotGroup.text()

    workPath = shotPath + "/" + WIDGET.cbxTask.currentText() + "/" + s.STATUS["work"]

    if WIDGET.btnShowPublish.isChecked():
        workPath = workPath.replace(s.STATUS["work"], s.STATUS["publish"])

    if LOAD:
        try:
            if reloadDrop:
                excludePublish = "*"           
                WIDGET.cbxShotChoice.clear()

                # NEED : LOOP & LISTS
                for file_format_item in s.FILE_FORMAT_LOAD[os.environ["SOFTWARE"]]:
                    WIDGET.cbxShotChoice.addItems(sorted(libFileService.getFolderList(workPath, "*" + file_format_item, True,  excludePublish), reverse=True))
                
                for file_format_item in s.FILE_FORMAT_LOAD["texture"]:
                    WIDGET.cbxShotChoice.addItems(sorted(libFileService.getFolderList(workPath, "*" + file_format_item, True,  excludePublish), reverse=True))

            SAVE_FILE = WIDGET.cbxShotChoice.currentText()

        except:
            SAVE_FILE = ""
    else:      
        taskFileName = WIDGET.cbxTask.currentText()
        if taskFileName.split("_") > 2:
            taskFileName = taskFileName.split("_")[-1]
        SAVE_FILE = WIDGET.edtShotGroup.text() + "_" + taskFileName + "_v001_" + libUser.getUserInitials() + s.FILE_FORMAT[os.environ["SOFTWARE"]]
    
    SAVE_DIR = workPath + "/" + SAVE_FILE
    WIDGET.edtMsg.setText(SAVE_DIR.replace("/", "\\"))

    # set modification date & file size
    if LOAD:
        PATH_IMG = os.path.dirname(SAVE_DIR) + "/" + s.STATUS["thumbs"] + "/" + SAVE_FILE.split(".")[0] + s.FILE_FORMAT["thumbs"]
        
        if WIDGET.btnShowPublish.isChecked():
            PATH_IMG = PATH_IMG.replace(s.STATUS["work"], s.STATUS["publish"])
        
        if os.path.exists(SAVE_DIR):
            WIDGET.edtMsgDate.setText(str(datetime.datetime.fromtimestamp(os.path.getmtime(SAVE_DIR))).split(".")[0])
            WIDGET.edtMsgSize.setText(str("{0:.2f}".format(os.path.getsize(SAVE_DIR)/(1024*1024.0)) + " MB"))
        else:
            WIDGET.edtMsgDate.setText("")
            WIDGET.edtMsgSize.setText("")


def saveFile():
    global LOG, SAVE_DIR, SAVE_FILE, PATH_IMG

    libFunction.createFolder(SAVE_DIR)

    if os.path.exists(SAVE_DIR):
        LOG.warning ("EXISTS : SAVE : Overwrite " + SAVE_DIR)
        
        # NUKE asks by itself
        if not os.environ["SOFTWARE"] == "nuke":
            if QMessageBox.Cancel == libMessageBox.questionMsgBox("Overwrite", "File exists", "Overwrite the file?", QMessageBox.Warning):
                LOG.info("CANCEL : SAVE : Overwrite " + SAVE_DIR)
                return
 
    try:    
        if os.environ["SOFTWARE"] == "maya":
            import maya.cmds as cmds
            cmds.file( rename = SAVE_DIR)
            cmds.file( save = True, type = s.FILE_FORMAT_CODE[s.FILE_FORMAT[os.environ["SOFTWARE"]]] )
            
        elif os.environ["SOFTWARE"] == "nuke":
            import nuke
            nuke.scriptSaveAs(SAVE_DIR) 
                           
        elif os.environ["SOFTWARE"] == "houdini":
            print "houdini"

        libRender.saveSnapshotImg(SAVE_DIR, PATH_IMG)
        LOG.info('END  : SAVE : ' + SAVE_DIR)   
    except:
        LOG.error('FAIL : SAVE : ' + SAVE_DIR, exc_info=True)  

    WIDGET.close() 


def loadFile(ref = False):
    global LOG, SAVE_DIR

    try: 

        if checkTexture():
            pass

        elif os.environ["SOFTWARE"] == "maya":
            import maya.mel as mel

            # reference or open 
            if ref or ".abc" in SAVE_DIR or ".obj" in SAVE_DIR or ".fbx" in SAVE_DIR:
                # file -r -type "mayaBinary"  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "bull_MODEL_v004_jo" -options "v=0;" "K:/30_assets/bull/10_MODEL/WORK/bull_MODEL_v004_jo.mb";
                mel.eval('file -r -type "' + s.FILE_FORMAT_CODE["." + SAVE_DIR.split(".")[-1]] + '" -ignoreVersion -gl -mergeNamespacesOnClash false "' + SAVE_DIR.replace("\\", "/") + '"')
            else:
                mel.eval('file -f -options "v=0;"  -ignoreVersion  -typ "' + s.FILE_FORMAT_CODE[s.FILE_FORMAT[os.environ["SOFTWARE"]]] + '" -o "' + SAVE_DIR.replace("\\", "/") + '"')

        elif os.environ["SOFTWARE"] == "nuke":
            import nuke
            nuke.scriptOpen(SAVE_DIR)  

        elif os.environ["SOFTWARE"] == "houdini":
            print "houdini open"
        
        LOG.info ('END  : LOAD : ' + SAVE_DIR)   
    except:
        LOG.error('FAIL : LOAD : ' + SAVE_DIR, exc_info=True)  

    # SET USER SETTINGS
    arLoadSet = {
        TITLE : [WIDGET.cbxShot.currentText(),
                WIDGET.cbxShotName.currentText(),
                WIDGET.cbxShotGroup.currentText(),
                WIDGET.cbxTask.currentText()]
                }
    libUser.setUserSettings(os.getenv('username'), arLoadSet)

    WIDGET.close() 


def checkTexture():
    global SAVE_DIR
    for item in s.FILE_FORMAT_LOAD["texture"]:
        if SAVE_DIR.find(item) != -1:
            if ".ptx" in SAVE_DIR:
                t = Thread(target=openPtxView)
                t.start()
            else:
                os.system(SAVE_DIR)

            LOG.info('OPEN : TEX  : ' + SAVE_DIR)   
            return True
    return False


def openPtxView():
    global SAVE_DIR
    print "openPtxView : " + "\"" + s.SOFTWARE["ptxview"].replace("/","\\") + "\" " + SAVE_DIR.replace("/","\\")
    os.system("\"" + s.SOFTWARE["ptxview"].replace("/","\\") + "\" " + SAVE_DIR.replace("/","\\"))    


def checkInput():
    global SAVE_DIR, SAVE_FILE

    if WIDGET.edtShot.text() == s.TYPE["shots"]:

        if not WIDGET.edtShotGroup.text()[:3].isdigit():
            if not WIDGET.edtShotGroup.text()[0] == "s" or not WIDGET.edtShotGroup.text()[1:4].isdigit():
                return False 
        else:
            if len(WIDGET.edtShotGroup.text()) > 3:
                if WIDGET.edtShotGroup.text()[3].isalpha():
                    return False 

        if len(WIDGET.edtShotGroup.text().split("_")) > 2 : # or WIDGET.edtShotGroup.text()[3].isdigit():
            return False
            
    elif not WIDGET.edtShot.text() in s.TYPE_DIRECT:  
        if "_" in WIDGET.edtShotGroup.text():
            return False 

    if " " in WIDGET.edtShotGroup.text() or "-" in WIDGET.edtShotGroup.text() or ":" in WIDGET.edtShotGroup.text():
        return False

    return True


#**********************
# INIT
#**********************
def init():
    global LOAD, TITLE

    WIDGET.cbxShot.clear()
    WIDGET.cbxTask.clear()
    WIDGET.cbxShotName.clear()
    WIDGET.cbxShotGroup.clear()

    libImage.setUserImg(os.getenv('username'), WIDGET.lblUser)

    # set for (not) ADMIN
    if os.getenv('username') in s.TEAM["admin"]:
        libFunction.setErrorCount(WIDGET) 
    else:
        WIDGET.lblErrorCount.hide()

    # fill list
    if os.environ["SOFTWARE"] == "nuke":
        WIDGET.cbxShot.addItem(s.TYPE["shots"])
        
        if not LOAD:
            WIDGET.cbxTask.addItem(s.TASK_SHOTS_FOLDER["compositing"])

    else:
        for item in s.TYPE.itervalues():
            WIDGET.cbxShot.addItem(item)

    # GET USER SETTINGS & set on script
    userSettings = libUser.getUserSettings(os.getenv('username'), TITLE)
    if userSettings:
        userSettings = userSettings[0]    
        WIDGET.cbxShot.setCurrentIndex(WIDGET.cbxShot.findText(userSettings[0]))
        WIDGET.cbxShotName.setCurrentIndex(WIDGET.cbxShotName.findText(userSettings[1]))
        WIDGET.cbxShotGroup.setCurrentIndex(WIDGET.cbxShotGroup.findText(userSettings[2]))
        WIDGET.cbxTask.setCurrentIndex(WIDGET.cbxTask.findText(userSettings[3]))
        
    if LOAD:

        updatePath()


#**********************
# START PROZESS
#**********************
def start(loading = False):
    global LOG, LOAD, PATH_IMG, TITLE

    log()
    LOAD        = loading    
    PATH_IMG    = libFunction.rmTempImg()

    WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG))))

    if LOAD:
        LOG.info ("LOAD : START")
        WIDGET.btnAddShotName.hide()
        WIDGET.btnSnapshotRender.hide()
        WIDGET.btnSnapshotViewport.hide()
        WIDGET.btnScreenshot.hide()
        WIDGET.edtShot.hide()
        WIDGET.edtShotName.hide()
        WIDGET.edtShotGroup.hide()
        WIDGET.edtTask.hide()

        WIDGET.btnAccept.setIcon(QPixmap(QImage(s.PATH["img_btn"] + "/" + "btnLoad66.png")))
        WIDGET.btnAccept.setToolTip("Load File")
        WIDGET.btnAcceptRef.setIcon(QPixmap(QImage(s.PATH["img_btn"] + "/" + "btnAcceptRef21.png")))
        WIDGET.setWindowTitle("arLoad")
        WIDGET.setWindowIcon(QPixmap(QImage(s.PATH["img_btn"] + "/" + "btnLoad.png")))
        WIDGET.btnAccept.resize(66, WIDGET.btnAccept.height())
    
    else:
        LOG.info ("SAVEAS : START")
        WIDGET.cbxShotChoice.hide()
        WIDGET.btnShowPublish.hide()
        WIDGET.btnAcceptRef.hide()
        WIDGET.btnAccept.setIcon(QPixmap(QImage(s.PATH["img_btn"] + "/" + "btnSave91.png")))
        WIDGET.btnAccept.resize(91, WIDGET.btnAccept.height())
        WIDGET.btnAccept.setToolTip("Save File")

        if os.environ["SOFTWARE"] == "nuke":
            WIDGET.btnSnapshotViewport.hide()

    WIDGET.connect(WIDGET.btnAccept, SIGNAL("clicked()"), clicked_btnAccept)
    WIDGET.connect(WIDGET.btnAcceptRef, SIGNAL("clicked()"), clicked_btnAcceptRef)
    # WIDGET.connect(WIDGET.btnCancel, SIGNAL("clicked()"), clicked_btnCancel)

    WIDGET.connect(WIDGET.btnAddShotName, SIGNAL("clicked()"), clicked_btnAddShotName)

    WIDGET.connect(WIDGET.btnOpenFolder, SIGNAL("clicked()"), clicked_btnOpenFolder)
    WIDGET.connect(WIDGET.btnHelp, SIGNAL("clicked()"), clicked_btnHelp)
    WIDGET.connect(WIDGET.btnReport, SIGNAL("clicked()"), clicked_btnReport)
    WIDGET.connect(WIDGET.btnShowPublish, SIGNAL("clicked()"), clicked_btnShowPublish)
    WIDGET.connect(WIDGET.btnPreviewImg, SIGNAL("clicked()"), clicked_btnPreviewImg)

    WIDGET.connect(WIDGET.cbxShot, SIGNAL("currentIndexChanged(const QString&)"), changed_cbxShot)
    WIDGET.connect(WIDGET.cbxShotGroup, SIGNAL("currentIndexChanged(const QString&)"), changed_cbxShotGroup)
    WIDGET.connect(WIDGET.cbxShotName, SIGNAL("currentIndexChanged(const QString&)"), changed_cbxShotName)
    WIDGET.connect(WIDGET.cbxShotChoice, SIGNAL("currentIndexChanged(const QString&)"), changed_cbxShotChoice)
    WIDGET.connect(WIDGET.cbxTask, SIGNAL("currentIndexChanged(const QString&)"), changed_cbxTask)

    WIDGET.connect(WIDGET.btnScreenshot, SIGNAL("clicked()"), clicked_btnScreenshot)
    WIDGET.connect(WIDGET.btnSnapshotRender, SIGNAL("clicked()"), clicked_btnSnapshotRender)
    WIDGET.connect(WIDGET.btnSnapshotViewport, SIGNAL("clicked()"), clicked_btnSnapshotViewport)

    WIDGET.lblSoftware.hide()

    init()

    # WIDGET : always on top
    WIDGET.setWindowFlags(Qt.WindowStaysOnTopHint)

    WIDGET.show()

    #610 -493 = 117 = 20%