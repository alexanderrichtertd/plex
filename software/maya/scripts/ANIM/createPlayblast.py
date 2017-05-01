#*********************************************************************
# content   = create playblast
#             executes other scripts on PUBLISH (on task in file name)
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys
from os import startfile

import maya.cmds as cmds
import maya.mel as mel

import libLog

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


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
    