#*************************************************************
# title: 		Create Playblast
#
# software:     Maya
#
# content:		creates pipeline playblast
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%;%PYTHONPATH%"
#
# author: 		Alexander Richter 
# email:		contact@richteralexander.com
#*************************************************************


import os
import sys
from os import startfile

import maya.cmds as cmds
import maya.mel as mel

import settings as s
# sys.path.append(s.PATH['lib'])
# import libUser


def start():
    print "createPlayblast"
    import maya.cmds as cmds
    filePath = cmds.file(q = True , sn = True)

    if not filePath:
        print "No Save Path"
        return

    savePath = os.path.dirname(filePath) + "/" + "animatic" + "/" + os.path.basename(filePath).split(".")[0] + s.FILE_FORMAT["playblast"]

    mel.eval ('playblast  -format qt' + ' -filename "' + savePath + '" -forceOverwrite  -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 100 -compression "H.264" -quality 100;')

    startfile(os.path.normpath(savePath))
    