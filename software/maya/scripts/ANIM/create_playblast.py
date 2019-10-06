#*********************************************************************
# content   = create playblast
#             executes other scripts on PUBLISH (on task in file name)
# version   = 0.0.1
# date      = 2019-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os
from os import startfile
import sys

import maya.mel as mel
import maya.cmds as cmds

import pipelog


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = pipelog.init(script=TITLE)


#*********************************************************************
def start():
    LOG.info("createPlayblast")
    import maya.cmds as cmds
    filePath = cmds.file(q = True , sn = True)

    if not filePath:
        LOG.warning("No Save Path")
        return

    savePath = os.path.dirname(filePath) + "/" + "animatic" + "/" + os.path.basename(filePath).split(".")[0] + s.FILE_FORMAT["playblast"]
    mel.eval ('playblast  -format qt' + ' -filename "' + savePath + '" -forceOverwrite  -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 100 -compression "H.264" -quality 100;')

    startfile(os.path.normpath(savePath))

