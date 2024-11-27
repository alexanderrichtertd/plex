#*********************************************************************
# content   = setup maya
# date      = 2024-11-24
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import maya.cmds as cmds

from tank import Tank

#*********************************************************************
# VARIABLE
LOG = Tank().log(script=__name__)


#*********************************************************************
# INIT AND PRINT CONSOLE
cmds.evalDeferred('print("")')
cmds.evalDeferred('print("START PLEX -------------------------------------")')
cmds.evalDeferred(f'from tank import Tank; Tank().software.create_menu()')

cmds.evalDeferred('print("FINISH -----------------------------------------")')
cmds.evalDeferred('print("")')


