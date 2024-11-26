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
cmds.evalDeferred('Tank().software.name = "maya"')
# Tank().init_software(os.getenv('SOFTWARE'))
cmds.evalDeferred(f'from maya_dcc import Maya; Maya().create_menu()')

cmds.evalDeferred('print("FINISH -----------------------------------------")')
cmds.evalDeferred('print("")')


