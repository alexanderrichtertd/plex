#*************************************************************
# title: 		User Setup
#
# software:     Maya
#
# content:		start point for MAYA
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%;%PYTHONPATH%"
#
# author: 		Alexander Richter 
# email:		contact@richteralexander.com
#*************************************************************

import os
import sys

import maya.cmds as cmds

import settings as s

from lib import libLog
from lib import libUser


#************************
# LOG
#************************
TITLE = "maya"
os.environ["SOFTWARE"] = TITLE
os.environ["RENDERER"] = s.RENDERER[os.environ["SOFTWARE"]]


#************************
# LOG
#************************
import logging
LOG   = libLog.initLog(software=os.environ["SOFTWARE"], script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))


#************************
# START MAYA
#************************
print "-----------------------------------------"
print "           " + s.PROJECT_NAME
print "-----------------------------------------"
print ("\n	Welcome " + libUser.getCurrentUser() + "\n")


#************************
# PIPELINE
#************************
print "PATH"
print "  ON  - lib"
print "  ON  - img"
print "  ON  - data"
print "  ON  - plugins"
print "  ON  - utilities"
print "  ON  - settings"

print ""


# menu *************************
print "MENU"
try:
	cmds.evalDeferred("from scripts import menu\nmenu.arMenuLoad()")
	print "  ON  - menu"
	print "  ON  - shelf"
except:
	print "  OFF - menu"
	print "  OFF - shelf"

print ""


# plugins *************************
print "PLUGINS"
print "  ON  - RenderMan"
print "  ON  - Yeti"
print "  ON  - Arnold"

print ""


# scripts *************************
print "SCRIPTS"
print "  ON  - Tween Machine"
print "  ON  - Arctracker"
print "  ON  - prSelection"
print "  ON  - ngSkinTools"
print "  ON  - AtoN"
print "  ON  - SLibBrowser"
print "  ON  - Import/Export .obj Seq"

print ""


#************************
# SETTINGS
#************************
print "SETTINGS"
try:
	cmds.evalDeferred("from scripts import maya_settings")
	print "  ON  - TIME:   " + str(s.FPS)
	print "  ON  - RENDER: RenderMan"
except:
	print "  OFF - TIME:   " + str(s.FPS)
	print "  OFF - RENDER: RenderMan"

print ""

LOG.info("START")