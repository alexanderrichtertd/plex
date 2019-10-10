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
Tank().init_software()
SOFTWARE_DATA = Tank().software.data


Tank().software.print_checked_header('menu', func=cmds.evalDeferred("maya_utils.load_menu()"))
Tank().software.print_checked_header('shelf')
cmds.evalDeferred("Tank().software.add_shelf()")
Tank().software.print_checked_header('setup')
Tank().software.print_checked_header('rendersettings')

print("")


