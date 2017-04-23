#*********************************************************************
# content   = setup maya
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <contact@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys

import maya.cmds as cmds

import libLog
import libFunc

TITLE = "maya"
LOG   = libLog.init(script=TITLE)


#************************
# PRINT CONSOLE
libFunc.console_header()

print "PATH"
print "  ON  - lib"
print "  ON  - img"
print "  ON  - data"
print "  ON  - plugins"
print "  ON  - settings"
print "  ON  - utilities"

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

print "PLUGINS"
print "  ON  - Arnold"

print ""

print "SCRIPTS"
print "  ON  - Utilities"

print ""

print "SETTINGS"
try:
	cmds.evalDeferred("from scripts import maya_settings")
	print "  ON  - TIME:   " + str(s.FPS)
	print "  ON  - RENDER: RenderMan"
except:
	print "  OFF - TIME:   " + str(s.FPS)
	print "  OFF - RENDER: RenderMan"

print ""
