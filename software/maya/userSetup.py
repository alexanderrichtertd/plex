#*********************************************************************
# content   = setup maya
# date      = 2020-06-19
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys

import maya.cmds as cmds

import maya_utils
from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = 'userSetup' # os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
# INIT AND PRINT CONSOLE
cmds.evalDeferred("print('START PLEX -------------------------------------')")

Tank().init_software(os.getenv('SOFTWARE'))

Tank().software.print_checked_header('menu', func=cmds.evalDeferred("maya_utils.load_menus()"))
Tank().software.print_checked_header('shelf')
Tank().software.print_checked_header('scene setup')
Tank().software.print_checked_header('render setup')

cmds.evalDeferred("print('------------------------------------- FINISH')")


