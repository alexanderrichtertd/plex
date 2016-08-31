#*************************************************************
# title:        referenceSCENESHD
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


#**********************
# FUNCTIONS
#**********************
def start():

    LOG = libLog.initLog(script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))
    LOG.info("START")

    if not(s.PATH_EXTRA["scene_shd"].replace("\\","/") in mel.eval('file -q -l;')):
        
        try:
            cmds.file(s.PATH_EXTRA["scene_shd"], r=True )
            mel.eval('lookThroughModelPanel SCENE_SHD_cam_SHD_sceneShape modelPanel4;')
        
        except:
            LOG.warning("Scene or Camera is already used")
            # print ("** FAIL | Reference SCENE_SHD: Scene or Camera is already used **")
        
        LOG.info("END : Reference SCENE_SHD")
        # print("** DONE | Reference SCENE_SHD: Reference SCENE_SHD **")
    
    else:
        LOG.warning ("SCENE_SHD already exist")
        # print("** FAIL | Reference SCENE_SHD: SCENE_SHD already exist **")