#*********************************************************************
# content   = setup maya
# version   = 0.1.0
# date      = 2019-12-01
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os
import sys

import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as api

import maya_utils
from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = 'userSetup' # os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
# INIT AND PRINT CONSOLE


Tank().init_software(os.getenv('SOFTWARE'))
# cmds.evalDeferred('Tank().init_software(os.getenv("SOFTWARE").lower)')


Tank().software.print_checked_header('menu', func=cmds.evalDeferred("maya_utils.load_menus()"))
Tank().software.print_checked_header('shelf')
Tank().software.print_checked_header('scene setup')
Tank().software.print_checked_header('render setup')

print("")


