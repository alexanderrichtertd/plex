#*********************************************************************
# content   = maya utils
# version   = 0.6.0
# date      = 2019-10-06
#
# license   = MIT <https://github.com/alexanderrichtertd> <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import maya.mel as mel
import maya.cmds as cmds
from pymel.core import *

from functools import wraps

from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)



#*********************************************************************
# MENU
# TODO: delete and reload shelf
def load_menus():
    if cmds.menu(os.getenv('PROJECT_NAME').replace(' ',''), query = True, exists = True):
        cmds.deleteUI(os.getenv('PROJECT_NAME').replace(' ',''), menu = True)

    menu = cmds.menu(os.getenv('PROJECT_NAME').replace(' ',''), hm = 1, p = 'MayaWindow',
                     l = os.getenv('PROJECT_NAME').replace(' ',''), to = 1, )

    Tank().software.add_menu(menu)
    Tank().software.add_shelf()



#*********************************************************************
# START SETUP
def setup_scene(file_path=''):
    project_data = Tank().data_project

    # RESOLUTION
    try:
        cmds.setAttr("defaultResolution.width", project_data['resolution'][0])
        cmds.setAttr("defaultResolution.height", project_data['resolution'][1])
        cmds.setAttr('defaultResolution.deviceAspectRatio', (( project_data['resolution'][0]) / (project_data['resolution'][1])))
    except: LOG.error('FAIL load resolution.', exc_info=True)

    # IMG FORMAT
    # try:
    #     cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
    # except: LOG.error('FAIL load img format.', exc_info=True)

    # FPS
    try:
        fps = SOFTWARE_DATA['SETTINGS']['FPS'][project_data['fps']]
        cmds.currentUnit(time=fps)
        cmds.optionVar(sv = ("workingUnitTime", fps))
        cmds.optionVar(sv = ("workingUnitTimeDefault", fps))
    except: LOG.error('FAIL load fps.', exc_info=True)

    # UNIT
    try:    cmds.currentUnit(linear=SOFTWARE_DATA['SETTINGS']['unit'])
    except: LOG.error('FAIL load unit.', exc_info=True)

    # RENDERER
    try:
        renderer = SOFTWARE_DATA['renderer']
        cmds.optionVar(sv = ("preferredRenderer", SOFTWARE_DATA['renderer']))
        cmds.optionVar(sv = ("preferredRendererHold", SOFTWARE_DATA['renderer']))
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
            render_path += "/" + Tank().data_project["STATUS"]["render"] + "/<Scene>/<Scene>"
            cmds.setAttr('defaultRenderGlobals.imageFilePrefix', render_path, type='string')
        except: LOG.error('FAIL set image path.', exc_info=True)

        try:
            import pymel.core as pm
            pm.mel.setProject(os.path.dirname(file_path))
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
def position_selected():
	selected = ls( selection=True )

	if len(selected) > 1:
	    origin = selected[0]
	    selected.pop(0)

	    for select in selected:
	        cam_new = general.PyNode(select)
	        cam_origin = general.PyNode(origin)

	        cam_new.translate.set(cam_origin.translate.get())
	        cam_new.rotate.set(cam_origin.rotate.get())
	        cam_new.scale.set(cam_origin.scale.get())
	else:
	    LOG.warning("Need at least 2 selections to set the rest on the 1. selection position.")


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



