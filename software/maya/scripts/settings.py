#*********************************************************************
# content   = maya settings
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


import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as api


#*************************
# PLUG-IN MANAGER

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
