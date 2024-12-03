# content   = setup maya
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import maya.cmds as cmds

import plex

LOG = plex.log(script=__name__)


cmds.evalDeferred('print("")')
cmds.evalDeferred('print("START PLEX -------------------------------------")')
cmds.evalDeferred(f'import plex; plex.software.create_menu()')

cmds.evalDeferred('print("FINISH -----------------------------------------")')
cmds.evalDeferred('print("")')


