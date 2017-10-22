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

import os

import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as api


import libLog
from tank import Tank

import libLog

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

software_data = Tank().software.data


def setup_scene(file_path=''):
    # RESOLUTION
    try:
        cmds.setAttr("defaultResolution.width", Tank().data['project']['resolution'][0])
        cmds.setAttr("defaultResolution.height", Tank().data['project']['resolution'][1])
        cmds.setAttr('defaultResolution.deviceAspectRatio', ( ( Tank().data['project']['resolution'][0] ) / ( Tank().data['project']['resolution'][1] ) ) )
    except: LOG.error('FAILED load resolution.', exc_info=True)

    # IMG FORMAT
    # try:
    #     cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
    # except: LOG.error('FAILED load img format.', exc_info=True)

    # FPS
    try:
        fps = software_data['SETTINGS']['FPS'][Tank().data['project']['fps']]
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

    # ANIMATION extension
    try:
        cmds.setAttr('defaultRenderGlobals.animation', 1)
        cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
        cmds.setAttr('defaultRenderGlobals.extensionPadding', 4)
    except: LOG.error('FAILED set extension.', exc_info=True)

    if file_path:
        try:
            render_path = os.path.dirname(os.path.dirname(file_path))
            render_path += "/" + Tank().data['rules']["STATUS"]["render"] + "/<Scene>/<Scene>"
            cmds.setAttr('defaultRenderGlobals.imageFilePrefix', render_path, type='string')
        except: LOG.error('FAILED set image path.', exc_info=True)

        try:
            import pymel.core as pm
            pm.mel.setProject(os.path.dirname(file_path))
        except: LOG.error('FAILED set project path.', exc_info=True)

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
