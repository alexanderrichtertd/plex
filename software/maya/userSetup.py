#*********************************************************************
# content   = setup maya
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
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
	cmds.evalDeferred("from scripts import menu\nmenu.load_menu()")
	print "  ON  - menu"
except:
    print "  OFF - menu"

print "  ON  - shelf"

print ""
