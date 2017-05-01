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
from software import Software

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#************************
# PRINT CONSOLE
Software.print_header()

print ""

print "MENU"
try:
	cmds.evalDeferred("from scripts import menu\nmenu.arMenuLoad()")
	print "  ON  - menu"
	print "  ON  - shelf"
except:
	print "  OFF - menu"
	print "  OFF - shelf"

print ""

