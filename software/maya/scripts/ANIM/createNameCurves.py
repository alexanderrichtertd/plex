
#*************************************************************
# title:        create name curves
#
# software:     Maya
#
# content:      creates cuves of the name of the object near it
#               and turned to the camera
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%;%PYTHONPATH%"
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import os
import sys
import logging

import maya.cmds as cmds
import maya.mel as mel

import settings as s
sys.path.append(s.PATH['lib'])
import libLog


#**********************
# VARIABLE
#**********************
TITLE       = os.path.splitext(os.path.basename(__file__))[0]
LOG         = ""


#**********************
# FUNCTIONS
#**********************
def createNameCurves(objects):
    global LOG

    if cmds.objExists("TEXT"):
        cmds.delete("TEXT")
    
    OBJ_NAME    = ["D0100_splash", "D0200_crash", "D0300_dash"]
    MAIN_CAM    = "CAM_"
    TEXT        = ""
    FONT        = "Malgun Gothic|w400|h-150"
    OBJ_NAME    = listObjects(objects)
    
    filePath    = cmds.file(q=True,sn=True)
    currentFile = os.path.basename(filePath)

    if OBJ_NAME == "":
        LOG.warning("Nothing was selected")
        # print "WARNING: Nothing was selected"
        return

    if(currentFile[:3].isdigit()):
        MAIN_CAM += currentFile[:3]

    for geoName in OBJ_NAME:

        if(geoName.split("_") > 1):
            TEXT = geoName.split("_")[0]
        else:
            TEXT = geoName

        #create text
        currentText = cmds.textCurves(name = TEXT, font = FONT, text = TEXT)
          
        # position to OBJ_NAME
        if not cmds.objExists(MAIN_CAM):
            MAIN_CAM = "persp"

        # rotate TEXT to camera
        rotation = cmds.getAttr(MAIN_CAM + ".rotate")
        try:
            cmds.setAttr(TEXT + "Shape.rotate", rotation[0][0], rotation[0][1], rotation[0][2] )
        except:
            return
        # move TEXT to OBJ
        translation = cmds.getAttr(geoName + ".translate")[0]
        try:   
            cmds.setAttr(TEXT + "Shape.translate", translation[0], translation[1], translation[2] )
        except:
            return
            
        # add to group
        if cmds.objExists("TEXT"):
            cmds.parent(currentText, "TEXT")  
        else:
            cmds.group(currentText, name = 'TEXT')
            
        LOG.info("END : " + currentText)


def listObjects(objects):
    if not cmds.ls(selection=True):
        if not cmds.objExists(objects):
            objects = objects.upper()
        if cmds.objExists(objects):
            return cmds.listRelatives(objects)
        else:
            return ""
    else:
        return cmds.ls(selection=True)


#**********************
# START PROZESS
#**********************
def start(objects = "fx"):
    global LOG
    LOG = libLog.initLog(script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))
    LOG.info("START")
    createNameCurves(objects) 