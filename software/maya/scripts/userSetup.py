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


LOG = Tank().log.init(script=__name__)


#*********************************************************************
# INIT AND PRINT CONSOLE
menu_module = Tank().config_software['menu']

cmds.evalDeferred('print("START PLEX -------------------------------------")')

Tank().init_software(os.getenv('SOFTWARE'))
cmds.evalDeferred(f'import {menu_module};{menu_module}.create_menu()')
cmds.evalDeferred(f'import {menu_module};{menu_module}.create_shelf()')
LOG.debug(f'userSetup: import {menu_module};{menu_module}.create_menu()')

cmds.evalDeferred('print("FINISH -----------------------------------------")')


