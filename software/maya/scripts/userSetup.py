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
LOG = Tank().log.init(script=__name__)


#*********************************************************************
# INIT AND PRINT CONSOLE
menu_module = Tank().config_software['menu']

cmds.evalDeferred('print("")')
cmds.evalDeferred('print("START PLEX -------------------------------------")')
cmds.evalDeferred('print("create menu")')
cmds.evalDeferred('print("create shelf")')

# Tank().init_software(os.getenv('SOFTWARE'))
LOG.debug(f'userSetup: import {menu_module};{menu_module}.create_menu()')
cmds.evalDeferred(f'import {menu_module};{menu_module}.create_menu()')
cmds.evalDeferred(f'import {menu_module};{menu_module}.create_shelf()')

cmds.evalDeferred('print("FINISH -----------------------------------------")')
cmds.evalDeferred('print("")')


