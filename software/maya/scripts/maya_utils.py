#*********************************************************************
# content   = Maya utils
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os

import maya.mel as mel
import maya.cmds as cmds

from functools import wraps

from tank import Tank


#*********************************************************************
# START SETUP
def setup_scene(file_path=''):
    # RESOLUTION
    try:
        cmds.setAttr("defaultResolution.width", Tank().config_project['resolution'][0])
        cmds.setAttr("defaultResolution.height", Tank().config_project['resolution'][1])
        cmds.setAttr('defaultResolution.deviceAspectRatio', (( Tank().config_project['resolution'][0]) / (Tank().config_project['resolution'][1])))
    except: LOG.error('FAIL load resolution.', exc_info=True)

    # IMG FORMAT
    # try:
    #     cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
    # except: LOG.error('FAIL load img format.', exc_info=True)

    # FPS
    try:
        fps = Tank().config_project['fps']
        cmds.currentUnit(time=fps)
        cmds.optionVar(sv = ("workingUnitTime", fps))
        cmds.optionVar(sv = ("workingUnitTimeDefault", fps))
    except: LOG.error('FAIL load fps.', exc_info=True)


    # RENDERER
    try:
        renderer = Tank().config_project['SETTINGS']['renderer']
        cmds.optionVar(sv = ("preferredRenderer", renderer))
        cmds.optionVar(sv = ("preferredRendererHold", renderer))
    except: LOG.error('FAIL load renderer.', exc_info=True)

    # ANIMATION extension
    try:
        cmds.setAttr('defaultRenderGlobals.animation', 1)
        cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
        cmds.setAttr('defaultRenderGlobals.extensionPadding', 4)
    except: LOG.error('FAIL set extension.', exc_info=True)

    if file_path:
        try:
            render_path = os.path.dirname(os.path.dirname(file_path))
            render_path += "/RENDER/<Scene>/<Scene>"
            cmds.setAttr('defaultRenderGlobals.imageFilePrefix', render_path, type='string')
        except: LOG.error('FAIL set image path.', exc_info=True)

        try:
            pass 
            # pm.mel.setProject(os.path.dirname(file_path))
        except: LOG.error('FAIL set project path.', exc_info=True)

    # shortcut - SAVE
    # cmd = 'python "from scripts import save;save.start()"'
    # cmds.nameCommand( 'save', annotation="Save", sourceType="mel" ,c=cmd)
    # cmds.hotkey( k='s', alt=True, name='save' )
    # import maya.OpenMaya as api

    # FIX renderLayer
    # def fixRenderLayer(*args):
    #     mel.eval("fixRenderLayerOutAdjustmentErrors;")
    # api.MSceneMessage.addCallback(api.MSceneMessage.kAfterOpen, fixRenderLayer)


#*********************************************************************
# DECORATOR
def viewport_off(func):
    @wraps(func)
    def viewport(*args, **kwargs):
        try:
            # viewport OFF
            mel.eval("paneLayout -e -manage false $gMainPane")
            return func(*args, **kwargs)
        except Exception:
            LOG.error("FAIL : Viewport off", exc_info=True)
            raise
        finally:
            # viewport ON
            mel.eval("paneLayout -e -manage true $gMainPane")

    return viewport
