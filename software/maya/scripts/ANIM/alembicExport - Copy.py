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

from PySide import QtUiTools
from PySide.QtGui import *
from PySide.QtCore import *

import maya.cmds as cmds
import maya.mel as mel

# from scripts.ui import alembicExport
import settings as s
from img import img_rc

import libLog
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
ERROR       = ""
ASSETS      = ["char", "prop", "set", "fx", "CHAR", "PROP", "SET", "FX"]
PATH_UI     = s.PATH["maya_scripts"] + "/ui/alembicExport.ui"
 

#**********************
# RUN DOS RUN
#**********************
WIDGET   = QtUiTools.QUiLoader().load(PATH_UI)
ui       = WIDGET


#**********************
# CLICKED_TRIGGER
#**********************
def clicked_export():
    global WIDGET, ERROR, HIDDEN, MERGE

    HIDDEN = ui.cbxHidden.isChecked()
    MERGE = ui.cbxMerge.isChecked()
    
    ERROR = ""
    objectGroups = []
    
    if(ui.cbxSelected.isChecked()):
        objectGroups = cmds.ls (selection=True)
    else:
        objectGroups = selectObjects()
    
    print objectGroups

    ui.edtMsg.setText("Alembic Export | In Progress ... 1 of " + str(len(objectGroups)))
    WIDGET.update() 
    if not (objectGroups):
        ui.edtMsg.setText("Fail: Nothing was selected!")
    elif(ui.cbxMerge.isChecked()):
        ui.edtMsg.setText(exportAlembic(objectGroups))
    elif (len(objectGroups) < 2):
        ui.edtMsg.setText(exportAlembic(objectGroups[0], False))
    else:
        for obj in objectGroups:
            ui.edtMsg.setText(exportAlembic(obj, False))

    if not(ERROR == ""):
        QMessageBox.information( WIDGET, "FAIL | Wrong names", ERROR)
    else:
        QMessageBox.information( WIDGET, "DONE | ALEMBIC EXPORT", ui.edtMsg.text())


# def clicked_exportFx():
#     ui.cbxCam.setChecked(True)
#     ui.cbxLight.setChecked(False)
#     ui.cbxAssets.setChecked(False)
#     ui.cbxAssetsChar.setChecked(True)
#     ui.cbxAssetsProp.setChecked(True)
#     ui.cbxAssetsSet.setChecked(True)
#     ui.cbxAssetsFx.setChecked(True)
#     ui.cbxMerge.setChecked(False)
#     clicked_export()


def clicked_cancel():
    global LOG
    LOG.info("END : CANCEL")
    global WIDGET
    WIDGET.close()


def clicked_help():
    global LOG
    LOG.info("HELP")
    webbrowser.open(s.LINK["software"])


def clicked_btnReport():
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
    ui.cbxAssets.setChecked(status)

    for check in CHECKBOX:
        check.setChecked(status)


def checked_assets():
    ui.cbxAssetsChar.setChecked(ui.cbxAssets.isChecked())
    ui.cbxAssetsSet.setChecked(ui.cbxAssets.isChecked())
    ui.cbxAssetsProp.setChecked(ui.cbxAssets.isChecked())
    ui.cbxAssetsFx.setChecked(ui.cbxAssets.isChecked())


def checked_selected():
    if(ui.cbxSelected.isChecked()):
        checked_allObjects(False)
        ui.cbxSelected.setChecked(True)


def checked_other():
    if ui.cbxAssetsChar.isChecked() or ui.cbxAssetsSet.isChecked() or ui.cbxAssetsProp.isChecked() or ui.cbxAssetsFx.isChecked()\
    or ui.cbxCam.isChecked() or ui.cbxLight.isChecked():
        ui.cbxSelected.setChecked(False)


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

                if(box.text() == "fx" and ui.cbxMerge.isChecked() == False):
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

    if(ui.cbxAssets.isChecked() and ui.cbxAssetsChar.isChecked() \
        and ui.cbxAssetsProp.isChecked() and ui.cbxAssetsSet.isChecked() \
        and ui.cbxAssetsFx.isChecked() and cmds.objExists("ASSETS")):
        
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
    global SAVE_DIR, SAVE_PATH, ERROR, HIDDEN, MERGE, LOG

    hidden = ""

    if not HIDDEN:
        hidden = " -writeVisibility"

    # add name to attributes
    if MERGE:
        setAttributeToMesh()

    SAVE_PATH = os.path.dirname(cmds.file(q=True,sn=True))
    SAVE_PATH = s.PATH["shots_alembic"]   # SAVE_PATH.replace("WORK", "PUBLISH")
    SAVE_FILE = os.path.basename(cmds.file(q=True,sn=True))

    if (len(SAVE_FILE.split('_')) > 2):
        tmpFile = SAVE_FILE.split('_')
        SAVE_FILE = tmpFile[0] + "_" + tmpFile[1]

    SAVE_DIR = (SAVE_PATH + '\\' + SAVE_FILE.split('.')[0] + ".abc").replace("\\", "/")

    try:
        FRAME_START     = str(ui.edtFrameStart.text())
        FRAME_END       = str(ui.edtFrameEnd.text()) 
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
        tmpExport   += hidden + ' -dataFormat hdf ' #' -stripNamespaces -dataFormat hdf ' 

        # if (objectGroup[1:4].isdigit() and objectGroup[0].isalpha()):
            
        #     # genericSplashGroundB:genericSplashGroundB_AlembicNode.offset
        #     alembic = cmds.listRelatives(objectGroup)[0].split(":")[0] + ":" + objectGroup.split("_")[1] + "_AlembicNode.offset"
        #     offset = ""

        #     try:
        #         offset = str(int(cmds.getAttr (alembic)))
        #     except:
        #         print "FAIL: " + str(objectGroup) + " " + alembic
            
        #     if(offset > 0):
        #         offset = "+" + '{0}'.format(offset.zfill(3))

        #     s1 = str("%0.3f" % cmds.getAttr(objectGroup + ".sx")).replace(".", ",")
        #     s2 = str("%0.3f" % cmds.getAttr(objectGroup + ".sy")).replace(".", ",")
        #     s3 = str("%0.3f" % cmds.getAttr(objectGroup + ".sz")).replace(".", ",")
        #     tmpSave += ".f" + offset + ".s" + s1 + ".s" + s2 + ".s" + s3
            # D0100_genericSplashGroundB.f+017.s1,388.s1,388.s1,388
        # SAVE_PATH += '/FX_GEO/'
        if not(os.path.exists(SAVE_PATH)):
            os.makedirs(SAVE_PATH)
        SAVE_DIR = (SAVE_PATH + tmpSave + ".abc").replace("\\", "/")
        
        if objectGroup in ["horse", "bull", "set"]:
            print "objectGroupSingle: " + objectGroup
            for obj in cmds.listRelatives(objectGroup):
                if mel.eval('getAttr ( "' + obj + '.visibility" );'):
                    tmpExport += "-root " + obj + " "
        else:
            tmpExport += "-root " + objectGroup + " "

    if "CAM" in SAVE_DIR:
        SAVE_DIR = SAVE_DIR.lower()

    tmpExport += '-file ' + SAVE_DIR + '";'
    try:
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

    SAVE_PATH = os.path.dirname(cmds.file(q=True,sn=True))
    SAVE_PATH = SAVE_PATH.replace("WORK", "PUBLISH")
    SAVE_FILE = os.path.basename(cmds.file(q=True,sn=True))

    if (len(SAVE_FILE.split('_')) > 2):
        tmpFile = SAVE_FILE.split('_')
        SAVE_FILE = tmpFile[0] + "_" + tmpFile[1]

    SAVE_DIR = (SAVE_PATH + '\\' + SAVE_FILE.split('.')[0] + ".abc").replace("\\", "/")

    CHECKBOX.append(ui.cbxCam)
    CHECKBOX.append(ui.cbxLight)
    CHECKBOX.append(ui.cbxAssetsChar)
    CHECKBOX.append(ui.cbxAssetsProp)
    CHECKBOX.append(ui.cbxAssetsSet)
    CHECKBOX.append(ui.cbxAssetsFx)

    for check in CHECKBOX:
        check.toggled.connect(checked_other)

    libFunction.setUserImg(imgObj = ui.lblUser)

    ui.edtFrameStart.setText(str(int(cmds.playbackOptions( query = True, animationStartTime = True))))
    ui.edtFrameEnd.setText(str(int(cmds.playbackOptions( query = True, animationEndTime = True))))


#**********************
# START PROZESS
#**********************
def start():
    global WIDGET, LOG
    #WIDGET  = QWidget()
    #ui.setupUi(WIDGET)

    LOG = libLog.initLog(script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))
    LOG.info("START")

    WIDGET.connect(ui.btnExport, SIGNAL("clicked()"), clicked_export)
    # WIDGET.connect(ui.btnExportFx, SIGNAL("clicked()"), clicked_exportFx)
    WIDGET.connect(ui.btnCancel, SIGNAL("clicked()"), clicked_cancel)
    WIDGET.connect(ui.btnHelp, SIGNAL("clicked()"), clicked_help)
    WIDGET.connect(ui.btnReport, SIGNAL("clicked()"), clicked_report)
    WIDGET.connect(ui.btnOpenFolder, SIGNAL("clicked()"), clicked_openFolder)

    ui.cbxAssets.toggled.connect(checked_assets) 
    ui.cbxSelected.toggled.connect(checked_selected) 

    ui.cbxHidden.setChecked(False)

    init()

    WIDGET.show() 