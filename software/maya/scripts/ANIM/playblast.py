#*********************************************************************
# content   = create playblast
#             executes other scripts on PUBLISH (on task in file name)
# version   = 0.1.0
# date      = 2020-06-19
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
from os import startfile

import maya.mel as mel
import maya.cmds as cmds

from tank import Tank


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)


#*********************************************************************
def start():
    LOG.info("CREATE playblast")
    file_path = cmds.file(q=True, sn=True)

    if not file_path:
        LOG.warning("No Save Path")
        return

    save_path = os.path.dirname(file_path) + "/" + "playblast" + "/" + os.path.basename(file_path).split(".")[0] + '.' + Tank().data_project['EXTENSION']['playblast']
    mel.eval('playblast -format avi -filename "{}" -forceOverwrite -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 100 -compression "none" -quality 100;'.format(save_path))

    startfile(os.path.normpath(save_path))


def turntable():
    pass
