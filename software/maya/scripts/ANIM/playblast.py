#*********************************************************************
# content   = create playblast
#             executes other scripts on PUBLISH (on task in file name)
# version   = 0.1.0
# date      = 2019-12-01
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os
from os import startfile
import sys

import maya.mel as mel
import maya.cmds as cmds

from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
def start():
    LOG.info("createPlayblast")
    import maya.cmds as cmds
    file_path = cmds.file(q = True , sn = True)

    if not file_path:
        LOG.warning("No Save Path")
        return

    save_path = os.path.dirname(file_path) + "/" + "animatic" + "/" + os.path.basename(file_path).split(".")[0] + '.' + Tank().data_templates['EXTENSION']['playblast']
    mel.eval ('playblast  -format qt' + ' -filename "' + save_path + '" -forceOverwrite  -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 100 -compression "H.264" -quality 100;')

    startfile(os.path.normpath(save_path))



def turntable():
    pass
