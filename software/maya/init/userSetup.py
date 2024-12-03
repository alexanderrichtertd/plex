# content   = setup maya
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import maya.cmds as cmds

from plex import Plex

LOG = Plex().log(script=__name__)


cmds.evalDeferred('print("")')
cmds.evalDeferred('print("START PLEX -------------------------------------")')
cmds.evalDeferred(f'from plex import Plex; Plex().software.create_menu()')

cmds.evalDeferred('print("FINISH -----------------------------------------")')
cmds.evalDeferred('print("")')


