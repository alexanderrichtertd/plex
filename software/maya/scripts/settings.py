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

import libLog
from tank import Tank

import libLog
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

all_data      = Tank().data
project_data  = all_data['project']
software_data = all_data['software'][Tank().software.software]


#*************************
# SETTINGS

# TIME
try:
    fps = software_data['SETTINGS']['FPS'][project_data['fps']]
    cmds.currentUnit(time=fps)
    cmds.optionVar(sv = ("workingUnitTime", fps))
    cmds.optionVar(sv = ("workingUnitTimeDefault", fps))
except: LOG.error('FAILED load fps.', exc_info=True)

# UNIT
try:    cmds.currentUnit(linear=software_data['SETTINGS']['unit'])
except: LOG.error('FAILED load unit.', exc_info=True)

# RENDERER
try:
    renderer = software_data['renderer']
    cmds.optionVar(sv = ("preferredRenderer", software_data['renderer']))
    cmds.optionVar(sv = ("preferredRendererHold", software_data['renderer']))
except: LOG.error('FAILED load renderer.', exc_info=True)


# shortcut - SAVE
# cmd = 'python "from scripts import save;save.start()"'
# cmds.nameCommand( 'save', annotation="Save", sourceType="mel" ,c=cmd)
# cmds.hotkey( k='s', alt=True, name='save' )

# FIX renderLayer
# def fixRenderLayer(*args):
#     mel.eval("fixRenderLayerOutAdjustmentErrors;")
# api.MSceneMessage.addCallback(api.MSceneMessage.kAfterOpen, fixRenderLayer)


# LINEAR WORKFLOW
# cmds.setAttr ("defaultArnoldRenderOptions.textureMaxMemoryMB", 10024)
# cmds.setAttr ("defaultArnoldRenderOptions.display_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.light_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.shader_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.texture_gamma", 1)
