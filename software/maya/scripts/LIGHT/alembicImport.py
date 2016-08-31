#*************************************************************
# title:        ALEMBIC IMPORT
#
# content:      
#
# dependencies: 
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


def start():
    LOG = libLog.initLog(script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))
    LOG.info("START")
    #referenceNode
    mel.eval('file -r -type "mayaAscii"  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "SCENE_SHD" -options "v=0;" "//bigfoot/breakingpoint/2_production/0_footage/shader/SCENE_SHD/PUBLISH/SCENE_SHD.ma";')


