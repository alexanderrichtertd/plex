#*********************************************************************
# content   = setup maya
# version   = 0.0.1
# date      = 2019-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os
import sys

import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as api

import pipelog
from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = 'userSetup' # os.path.splitext(os.path.basename(__file__))[0]
LOG   = pipelog.init(script=TITLE)


#*********************************************************************
# INIT AND PRINT CONSOLE
Tank().init_software()
SOFTWARE_DATA = Tank().software.data


print("SETUP")
try:
    cmds.evalDeferred("load_menu()")
    print("  ON  - menu")
except: print("  OFF - menu")

print("  ON  - shelf")

# try:
#     cmds.evalDeferred("setup_scene()")
#     print("  ON  - scene setup")
# except: print("  OFF - scene setup")

try:
    cmds.evalDeferred("from RENDER. rendersettings import Rendersettings;Rendersettings().setup()")
    print("  ON  - default rendersettings")
except: print("  OFF - default rendersettings")

print("")


#*********************************************************************
# MENU
def load_menu():
    delete_menu()

    menu = cmds.menu(os.getenv('PROJECT_NAME').replace(' ',''), hm = 1, p = 'MayaWindow',
                     l = os.getenv('PROJECT_NAME').replace(' ',''), to = 1, )

    Tank().software.add_menu(menu)


def delete_menu():
    if cmds.menu(os.getenv('PROJECT_NAME').replace(' ',''), query = True, exists = True):
        cmds.deleteUI(os.getenv('PROJECT_NAME').replace(' ',''), menu = True)



#*********************************************************************
# START SETUP
def setup_scene(file_path=''):
    # RESOLUTION
    try:
        cmds.setAttr("defaultResolution.width", Tank().data_project['resolution'][0])
        cmds.setAttr("defaultResolution.height", Tank().data_project['resolution'][1])
        cmds.setAttr('defaultResolution.deviceAspectRatio', (( Tank().data_project['resolution'][0]) / (Tank().data_project['resolution'][1])))
    except: LOG.error('FAIL load resolution.', exc_info=True)

    # IMG FORMAT
    # try:
    #     cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
    # except: LOG.error('FAIL load img format.', exc_info=True)

    # FPS
    try:
        fps = SOFTWARE_DATA['SETTINGS']['FPS'][Tank().data_project['fps']]
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
            render_path += "/" + Tank().data_templates["STATUS"]["render"] + "/<Scene>/<Scene>"
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

    # FIX renderLayer
    # def fixRenderLayer(*args):
    #     mel.eval("fixRenderLayerOutAdjustmentErrors;")
    # api.MSceneMessage.addCallback(api.MSceneMessage.kAfterOpen, fixRenderLayer)



