#*************************************************************
# function: 	Starup script for Nuke
#			
# depencence: 	set "NUKE_PATH=%PLUGINS_PATH%;%NUKE_PATH%"
#
# author: 		Alexander Richter 
# email:		alexander.richter@filmakademie.de
#*************************************************************

import os
import nuke
import errno

import settings as s

sys.path.append(s.PATH["lib"])
import libUser


#*******************
# VARIABLES
#*******************
RESOLUTION 		= str(s.RESOLUTION[0]) + " " +  str(s.RESOLUTION[1]) + " " + s.PROJECT_NAME.replace(" ", "")


#************************
# LOG
#************************
import libLog
import logging

TITLE = "nuke"
LOG   = libLog.initLog(software=TITLE, script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))
LOG.info("START")


#************************
# FOLDER CREATION
#************************
def createWriteDir():

  file 	= nuke.filename(nuke.thisNode())
  dir 	= os.path.dirname( file )
  osdir = nuke.callbacks.filenameFilter( dir )
  # cope with the directory existing already by ignoring that exception
  try:
    os.makedirs( osdir )
  except OSError, e:
    if e.errno != errno.EEXIST:
      raise


#************************
# SYSTEM PATHS
#************************
# def myFilenameFilter(filename):
# 	if nuke.env['MACOS']:
# 		filename = filename.replace( s.PATH_SHORT, s.PATH_LONG )
# 	if nuke.env['WIN32']:
# 		filename = filename.replace( s.PATH_LONG, s.PATH_SHORT )
# 	if nuke.env['LINUX']:
# 		filename = filename.replace( s.PATH_SHORT, s.PATH_LONG )
		
# 	return filename

# nuke.addFilenameFilter(myFilenameFilter)


#************************
# INIT
#************************
print "\n "+chr(218)+chr(196)*37 + chr(191)+"\n "+ chr(179) + \
" 	     " + s.PROJECT_NAME + " 	       " +\
"\n "+chr(192)+chr(196)*37 + chr(217)

print ("\n	Welcome " + libUser.getCurrentUser() + "\n")


#************************
# PIPELINE
#************************
print "PATHS"

print " ", chr(254), " ON  - lib"

try:
	nuke.pluginAddPath( s.PATH["img"] )
	nuke.pluginAddPath( s.PATH["img_btn"] )
	nuke.pluginAddPath( s.PATH["img_program"] )
	nuke.pluginAddPath( s.PATH["img_nuke_menu"] )
	nuke.pluginAddPath( s.PATH["img_nuke_banner"] )

	print " ", chr(254), " ON  - img"
except:
	LOG.error(" OFF - img")
	print " ", chr(254), " OFF - img"


print " ", chr(254), " ON  - settings"


try:
	nuke.pluginAddPath( 'gizmos' )
	nuke.pluginAddPath( 'gizmos/menu' )
	print " ", chr(254), " ON  - gizmos"
except:
	LOG.error(" OFF - gizmos")
	print " ", chr(254), " OFF - gizmos"	
	

try:
	nuke.pluginAddPath( 'scripts' )
	print " ", chr(254), " ON  - scripts"
except:
	LOG.error(" OFF - scripts")
	print " ", chr(254), " OFF - scripts"	

	
try:
	nuke.pluginAddPath( 'utilities' )
	print " ", chr(254), " ON  - utilities"
except:
	LOG.error(" OFF - utilities")
	print " ", chr(254), " OFF - utilities"	


try:
	nuke.pluginAddPath( 'plugins' )
	print " ", chr(254), " ON  - plugins"
except:
	LOG.error(" OFF - plugins")
	print " ", chr(254), " OFF - plugins"

	
print ""


print "FUNCTIONS"	

# save **********************************
try:
	# from utilities import save
	print " ", chr(254), " ON  - Save"
except:
	LOG.error(" OFF - Save")
	print " ", chr(254), " OFF - Save"


# load **********************************
try:
	# from utilities import saveCreate
	print " ", chr(254), " ON  - Load"
except:
	LOG.error(" OFF - Load")
	print " ", chr(254), " OFF - Load"


# writeNode *****************************
try:
	from scripts import writeNode
	print " ", chr(254), " ON  - arWrite"
except:
	LOG.error(" OFF - Write")
	print " ", chr(254), " OFF - arWrite"


print " ", chr(254), " ON  - Report"


print ""


#************************
# PLUGINS
#************************
print "PLUGINS"
import plugins

# rrenderSubmit *************************
try:	
	import rrenderSubmit
	print " ", chr(254), " ON  - rrender (by Holger)"
except:
	LOG.error(" OFF - rrender")
	print " ", chr(254), " OFF - rrender (by Holger)"


# renderthreads**************************
try:
	from vuRenderThreads.plugin_nuke import plugin_nuke
	print " ", chr(254), " ON  - renderthreads (by Vincent)"
except:
	LOG.error(" OFF - renderthreads")
	print " ", chr(254), " OFF - renderthreads (by Vincent)"


# aton *****************************
print " ", chr(254), " ON  - AtoN"


print ""


#************************
# SETTINGS
#************************
print "SETTINGS"

# fps ***********************************
try:
	nuke.knobDefault('Root.fps', s.FPS)
	print " ", chr(254), " ON  - FPS: " + s.FPS
except:
	LOG.error(" OFF - FPS: " + s.FPS)
	print " ", chr(254), " OFF - FPS: " + s.FPS


# resolution ****************************
try:
	nuke.addFormat(RESOLUTION)
	nuke.knobDefault("Root.format", s.PROJECT_NAME.replace(" ", ""))
	print " ", chr(254), " ON  - RES: " + RESOLUTION
except:	
	LOG.error(" OFF - RES: " + RESOLUTION)
	print " ", chr(254), " OFF - RES: " + RESOLUTION


# createFolder ****************************
try:
	nuke.addBeforeRender(createWriteDir)
	print " ", chr(254), " ON  - BeR: createWriteDir"
except:	
	LOG.error(" ON  - BeforeRender: createWriteDir")
	print " ", chr(254), " OFF - BeR: createWriteDir"


print ""