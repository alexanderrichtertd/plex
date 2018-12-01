#*********************************************************************
# content   = setup maya
# version   = 0.0.1
# date      = 2018-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys

import maya.cmds as cmds

import libLog
from tank import Tank

TITLE = 'userSetup' # os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#************************
# PRINT CONSOLE
Tank().init_software()

print "MENU"
try:
    cmds.evalDeferred("load_menu()")
    print "  ON  - menu"
except: print "  OFF - menu"

print "  ON  - shelf"

print ""


#*************************
# MENU
def load_menu():
    delete_menu()

    menu = cmds.menu(os.getenv('PROJECT_NAME').replace(' ',''), hm = 1, p = 'MayaWindow',
                    l = os.getenv('PROJECT_NAME').replace(' ',''), to = 1, )

    Tank().software.add_menu(menu)


def delete_menu():
    if cmds.menu(os.getenv('PROJECT_NAME').replace(' ',''), query = True, exists = True):
        cmds.deleteUI(os.getenv('PROJECT_NAME').replace(' ',''), menu = True)

