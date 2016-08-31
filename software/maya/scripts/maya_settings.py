#*************************************************************
# title:        Maya Settings
#
# content:      Start settings for Maya
#
# dependencies: userSetup
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import maya.cmds as cmds
import maya.OpenMaya as api
import maya.mel as mel

import settings as s

print (s.PROJECT_NAME + ": settings")


#*************************
# PLUG-IN MANAGER
#*************************
# LOAD PLUGIN
# try:
# 	mel.eval('catch(`loadPlugin "' + s.PATH["maya_plugins"] + '/SLiB.py' + '"`);')
# 	print "LOAD: SLiB"
# except:
# 	print "FAIL: Couldnt load SLiB"

# try:
# 	mel.eval('catch(`loadPlugin "' + s.PATH["maya_plugins_arnold"] + '/plug-ins/mtoa.mll' + '"`);')
# 	print "LOAD: MtoA (Arnold)"
# except:
# 	print "FAIL: Couldnt load MtoA"

# try:
# 	mel.eval('pluginInfo -edit -autoload true "' + s.PATH["maya_plugins_arnold"] + '/plug-ins/mtoa.mll' + '";')
# except:
# 	print "FAIL: Couldnt load MtoA Autoload"


# UNLOAD PLUGIN
# unloadPluginWithCheck( s.PATH["maya_plugins"]"/SLiB.py" );
# unloadPluginWithCheck( s.PATH["maya_plugins_arnold"]"/plug-ins/mtoa.mll" );


# Change the current time unit to pal
cmds.currentUnit( time=s.FPS_TYPE )
cmds.optionVar(sv = ("workingUnitTime", s.FPS_TYPE))
cmds.optionVar(sv = ("workingUnitTimeDefault", s.FPS_TYPE))

# cmds.optionVar(sv = ("preferredRenderer", s.MAYA_RENDERER))
# cmds.optionVar(sv = ("preferredRendererHold", s.MAYA_RENDERER))



# shortcut - SAVE
# cmd = 'python "from scripts import save;save.start()"'
# cmds.nameCommand( 'save', annotation="Save", sourceType="mel" ,c=cmd) 
# cmds.hotkey( k='s', alt=True, name='save' )


# def fixRenderLayer(*args):
#     mel.eval("fixRenderLayerOutAdjustmentErrors;")

# api.MSceneMessage.addCallback(api.MSceneMessage.kAfterOpen, fixRenderLayer)

# cmds.setAttr ("defaultArnoldRenderOptions.textureMaxMemoryMB", 10024)
# cmds.setAttr ("defaultArnoldRenderOptions.display_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.light_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.shader_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.texture_gamma", 1)
