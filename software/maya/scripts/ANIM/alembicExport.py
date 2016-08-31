#*************************************************************
# title:        Alembic Export
#
# software:     Maya
#
# content:      exports selectiv or the whole scene
#
# dependencies: lib, settings
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import os 
import sys
import shutil
import logging
import webbrowser

from threading import Thread

from PySide import QtUiTools
from PySide.QtGui import *
from PySide.QtCore import *

import maya.cmds as cmds
import maya.mel as mel

# from scripts.ui import alembicExport
import settings as s
from img import img_rc

import libLog
import libUser
import libImage
import libFunction

from utilities import arReport


#**********************
# VARIABLE
#**********************
TITLE       = os.path.splitext(os.path.basename(__file__))[0]
LOG         = ""

HIDDEN      = False
MERGE       = True

CHECKBOX    = []
SAVE_DIR    = ""
SAVE_PATH   = ""
SAVE_FILE   = ""
ERROR       = ""
ASSETS      = ["char", "prop", "set", "fx", "CHAR", "PROP", "SET", "FX"]
PATH_UI     = s.PATH["maya_scripts"] + "/ui/alembicExport.ui"
 

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


#**********************
# CLICKED_TRIGGER
#**********************
def clicked_export():
    global WIDGET, ERROR, HIDDEN, MERGE, SAVE_PATH, SAVE_FILE

    HIDDEN      = WIDGET.cbxHidden.isChecked()
    MERGE       = WIDGET.cbxMerge.isChecked()
    SAVE_PATH   = s.PATH["shots_alembic"]   # SAVE_PATH.replace("WORK", "PUBLISH")
    SAVE_FILE   = os.path.basename(cmds.file(q=True,sn=True))
    
    ERROR = ""
    objectGroups = []
    
    if(WIDGET.cbxSelected.isChecked()):
        objectGroups = cmds.ls (selection=True)
    else:
        objectGroups = selectObjects()
    
    print objectGroups

    WIDGET.edtMsg.setText("Alembic Export | In Progress ... 1 of " + str(len(objectGroups)))
    WIDGET.update() 
    if not (objectGroups):
        WIDGET.edtMsg.setText("Fail: Nothing was selected!")
    elif(WIDGET.cbxMerge.isChecked()):
        WIDGET.edtMsg.setText(exportAlembic(objectGroups))
    elif (len(objectGroups) < 2):
        WIDGET.edtMsg.setText(exportAlembic(objectGroups[0], False))
    else:
        for obj in objectGroups:
            WIDGET.edtMsg.setText(exportAlembic(obj, False))

    if not(ERROR == ""):
        QMessageBox.information( WIDGET, "FAIL | Wrong names", ERROR)
    else:
        QMessageBox.information( WIDGET, "DONE | ALEMBIC EXPORT", WIDGET.edtMsg.text())


def clicked_cancel():
    global LOG
    LOG.info("END : CANCEL")
    global WIDGET
    WIDGET.close()


def clicked_help():
    global LOG
    LOG.info("HELP")
    webbrowser.open(s.LINK["software"])


def clicked_report():
    global LOG
    LOG.info("REPORT")
    arReport.start("Alembic Export")


def clicked_openFolder():
    global SAVE_PATH
    webbrowser.open(SAVE_PATH.replace("/", "\\"))


#**********************
# CHECKED_TRIGGER
#**********************
def checked_allObjects(status):
    global CHECKBOX
    WIDGET.cbxAssets.setChecked(status)

    for check in CHECKBOX:
        check.setChecked(status)


def checked_assets():
    WIDGET.cbxAssetsChar.setChecked(WIDGET.cbxAssets.isChecked())
    WIDGET.cbxAssetsSet.setChecked(WIDGET.cbxAssets.isChecked())
    WIDGET.cbxAssetsProp.setChecked(WIDGET.cbxAssets.isChecked())
    WIDGET.cbxAssetsFx.setChecked(WIDGET.cbxAssets.isChecked())


def checked_selected():
    if(WIDGET.cbxSelected.isChecked()):
        checked_allObjects(False)
        WIDGET.cbxSelected.setChecked(True)


def checked_other():
    if WIDGET.cbxAssetsChar.isChecked() or WIDGET.cbxAssetsSet.isChecked() or WIDGET.cbxAssetsProp.isChecked() or WIDGET.cbxAssetsFx.isChecked()\
    or WIDGET.cbxCam.isChecked() or WIDGET.cbxLight.isChecked():
        WIDGET.cbxSelected.setChecked(False)


#**********************
# FUNCTIONS
#**********************
def selectObjects():
    global CHECKBOX, ERROR
    print ("GO")
    checkList = []

    for box in CHECKBOX:
        if (box.isChecked()):
            if (cmds.objExists(box.text()) or cmds.objExists(box.text().upper())):
                tmpBox = box.text()
                if(cmds.objExists(box.text().upper())):
                    tmpBox = box.text().upper()

                if(box.text() == "fx" and WIDGET.cbxMerge.isChecked() == False):
                    if cmds.listRelatives(tmpBox) != None:
                        for boxNew in cmds.listRelatives(tmpBox):
                            if (boxNew[1:4].isdigit()): # and boxNew.objectGroup[0].isalpha()):
                                checkList.append(boxNew)
                            else:
                                ERROR += boxNew + "  "
                    else:
                        LOG.warning("fx : no fx relatives")    
                else:
                    checkList.append(tmpBox)

    if(WIDGET.cbxAssets.isChecked() and WIDGET.cbxAssetsChar.isChecked() \
        and WIDGET.cbxAssetsProp.isChecked() and WIDGET.cbxAssetsSet.isChecked() \
        and WIDGET.cbxAssetsFx.isChecked() and cmds.objExists("ASSETS")):
        
        checkList = [asset for asset in checkList if asset not in ASSETS]
        checkList.append("ASSETS")

    return checkList


def setAttributeToMesh(attribute = "Name"):
    objList = cmds.ls( type = "mesh")

    for obj in objList:

        if not (mel.eval('attributeExists "name" ' + obj)):
            try: 
                mel.eval('addAttr -ln "name"  -dt "string" ' + obj + ';')
            except:
                print "Name attribute cant be added: " + obj
        
        try:    
            mel.eval('setAttr -type "string" ' + (obj + ".name") + ' ' + obj + ';')
        except:
            print "Name attribute cant be set: " + obj


def exportAlembic(objectGroup = ["ASSETS", "CAM"], multiply = True):
    global SAVE_DIR, SAVE_PATH, SAVE_FILE, ERROR, HIDDEN, MERGE, LOG

    hidden = ""

    if not HIDDEN:
        hidden = " -writeVisibility"

    # add name to attributes
    if MERGE:
        setAttributeToMesh()

    # SAVE_PATH = os.path.dirname(cmds.file(q=True,sn=True))
   

    if (len(SAVE_FILE.split('_')) > 2):
        tmpFile = SAVE_FILE.split('_')
        SAVE_FILE = tmpFile[0] + "_" + tmpFile[1]

    SAVE_DIR = SAVE_PATH + '/' + SAVE_FILE.split('.')[0] + ".abc"

    try:
        FRAME_START     = str(WIDGET.edtFrameStart.text())
        FRAME_END       = str(WIDGET.edtFrameEnd.text()) 
    except:
        FRAME_START     = str(cmds.playbackOptions( query = True, animationStartTime = True ))
        FRAME_END       = str(cmds.playbackOptions( query = True, animationEndTime = True ))
    
    tmpExport       = 'AbcExport -j "-frameRange ' + FRAME_START  + ' ' + FRAME_END
    
    mel.eval('select -cl  ;')

    if(multiply):
        tmpExport += ' -attr name' + hidden + ' -dataFormat hdf '
        for obj in objectGroup:
            tmpExport += "-root " + obj + " "
    else:
        tmpSave     = objectGroup

        if "CAM" in tmpSave:
            tmpSave = tmpSave.lower()

        tmpExport   += hidden + ' -dataFormat hdf ' #' -stripNamespaces -dataFormat hdf ' 

        if not(os.path.exists(SAVE_PATH)):
            os.makedirs(SAVE_PATH)
        SAVE_DIR = (SAVE_PATH + "/" + SAVE_FILE + "_" + tmpSave + ".abc").replace("\\", "/")
        
        if objectGroup in ["horse", "bull", "set"]:
            print "objectGroupSingle: " + objectGroup
            for obj in cmds.listRelatives(objectGroup):
                if mel.eval('getAttr ( "' + obj + '.visibility" );'):
                    tmpExport += "-root " + obj + " "
        else:
            tmpExport += "-root " + objectGroup + " "

    tmpExport += '-file ' + SAVE_DIR + '";'
    try:
        # t = Thread(target=mel.eval, args=(tmpExport,))
        # t.start()
        mel.eval(tmpExport)
        #'AbcExport -j "-frameRange ' + str(FRAME_START) + ' ' + str(FRAME_END) + ' -attr name -stripNamespaces -dataFormat hdf -root |ASSETS -root |CAM -file ' + SAVE_DIR + '";'
    except:
        tmpMsg = "FAIL: Couldnt export - " + tmpExport
        if objectGroup == ["ASSETS", "CAM"]:
            tmpMsg = "FAIL: Couldnt export Alembic!\nNo ASSETS and/or CAM group in the scene!"
        
        LOG.error(tmpMsg + "\n" + tmpExport)
        return tmpMsg

    LOG.info("END : " + tmpExport)
    return "DONE | ALEMBIC EXPORT"


#**********************
# INIT
#**********************
def init():
    global SAVE_DIR, SAVE_PATH, CHECKBOX

    CHECKBOX = []

    # set for (not) ADMIN
    if os.getenv('username') in s.TEAM["admin"]:
        libFunction.setErrorCount(WIDGET) 
    else:
        WIDGET.lblErrorCount.hide()

    SAVE_PATH = os.path.dirname(cmds.file(q=True,sn=True))
    SAVE_PATH = SAVE_PATH.replace("WORK", "PUBLISH")
    SAVE_FILE = os.path.basename(cmds.file(q=True,sn=True))

    SAVE_PATH = s.PATH["shots_alembic"]

    if (len(SAVE_FILE.split('_')) > 2):
        tmpFile = SAVE_FILE.split('_')
        SAVE_FILE = tmpFile[0] + "_" + tmpFile[1]

    SAVE_DIR = (SAVE_PATH + '\\' + SAVE_FILE.split('.')[0] + ".abc").replace("\\", "/")

    CHECKBOX.append(WIDGET.cbxCam)
    CHECKBOX.append(WIDGET.cbxLight)
    CHECKBOX.append(WIDGET.cbxAssetsChar)
    CHECKBOX.append(WIDGET.cbxAssetsProp)
    CHECKBOX.append(WIDGET.cbxAssetsSet)
    CHECKBOX.append(WIDGET.cbxAssetsFx)

    for check in CHECKBOX:
        check.toggled.connect(checked_other)

    libImage.setUserImg(imgObj = WIDGET.lblUser)

    WIDGET.edtFrameStart.setText(str(int(cmds.playbackOptions( query = True, animationStartTime = True))))
    WIDGET.edtFrameEnd.setText(str(int(cmds.playbackOptions( query = True, animationEndTime = True))))

    # GET USER SETTINGS & set on script
    # userSettings = libUser.getUserSettings(os.getenv('username'), TITLE)
    # if userSettings:
    #     userSettings = userSettings[0]    
    #     WIDGET.cbxShot.setCurrentIndex(WIDGET.cbxShot.findText(userSettings[0]))
    #     WIDGET.cbxShotName.setCurrentIndex(WIDGET.cbxShotName.findText(userSettings[1]))
    #     WIDGET.cbxShotGroup.setCurrentIndex(WIDGET.cbxShotGroup.findText(userSettings[2]))
    #     WIDGET.cbxTask.setCurrentIndex(WIDGET.cbxTask.findText(userSettings[3]))

#**********************
# START PROZESS
#**********************
def start():
    global LOG
    
    log()

    WIDGET.connect(WIDGET.btnExport, SIGNAL("clicked()"), clicked_export)
    # WIDGET.connect(WIDGET.btnCancel, SIGNAL("clicked()"), clicked_cancel)
    WIDGET.connect(WIDGET.btnHelp, SIGNAL("clicked()"), clicked_help)
    WIDGET.connect(WIDGET.btnReport, SIGNAL("clicked()"), clicked_report)
    WIDGET.connect(WIDGET.btnOpenFolder, SIGNAL("clicked()"), clicked_openFolder)

    WIDGET.cbxAssets.toggled.connect(checked_assets) 
    WIDGET.cbxSelected.toggled.connect(checked_selected) 

    WIDGET.cbxHidden.setChecked(False)

    WIDGET.btnExport.setIcon(QPixmap(QImage(s.PATH["img_btn"] + "/" + "btnAlembic91.png")))

    init()

    # WIDGET : Always on top
    WIDGET.setWindowFlags(Qt.WindowStaysOnTopHint)

    WIDGET.show() 