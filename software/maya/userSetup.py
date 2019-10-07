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


print("SETUP")
try:
    cmds.evalDeferred("maya_utils.load_menu()")
    print("  ON  - menu")
except: print("  OFF - menu")

print("  ON  - shelf")

# try:
#     cmds.evalDeferred("maya_utils.setup_scene()")
#     print("  ON  - scene setup")
# except: print("  OFF - scene setup")

try:
    cmds.evalDeferred("from RENDER. rendersettings import Rendersettings;Rendersettings().setup()")
    print("  ON  - default rendersettings")
except: print("  OFF - default rendersettings")

print("")


