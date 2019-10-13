#*********************************************************************
# content   = snapshot
#             executes other scripts on PUBLISH (on task in file name)
# version   = 0.1.0
# date      = 2019-10-06
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import time

from Qt import QtWidgets, QtGui, QtCore, __binding__

import pipefunc

from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)

DEFAULT_PATH = os.path.normpath(os.getenv('DATA_USER_PATH').split(';')[0] + '/tmp_img.jpg')


#*********************************************************************
# SCREENSHOT
# creats a screenshot of the main screen and saves it
def create_any_screenshot(WIDGET, ui=''):
    # if not create_screenshot_render(WIDGET, ui):
    if not create_screenshot_viewport(WIDGET, ui):
        create_screenshot(WIDGET, ui)

def create_screenshot(WIDGET, ui=''):
    print("SCREENSHOT")
    # WIDGET.hide()
    if not os.path.exists(os.path.dirname(DEFAULT_PATH)):
        try: os.makedirs(os.path.dirname(DEFAULT_PATH))
        except: LOG.error('FAILED folder creation', exc_info=True)
    # time.sleep(0.6)

    if __binding__ == "PySide2":
        from PySide2 import QtWidgets, QtGui
        QtGui.QScreen.grabWindow(QtWidgets.QApplication.primaryScreen(), QtWidgets.QApplication.desktop().winId()).save(DEFAULT_PATH, DEFAULT_PATH.split(".")[-1])
    else:
        from Qt import QtWidgets, QtGui
        QtGui.QPixmap.grabWindow(QtWidgets.QApplication.desktop().winId()).save(DEFAULT_PATH, DEFAULT_PATH.split(".")[-1])

    # WIDGET.setFocus()
    # WIDGET.show()
    if ui: ui.setIcon(QtGui.QPixmap(QtGui.QImage(DEFAULT_PATH)))

def create_screenshot_render(WIDGET, ui=''):
    # WIDGET.hide()
    if not os.path.exists(os.path.dirname(DEFAULT_PATH)):
        try:    os.makedirs(os.path.dirname(DEFAULT_PATH))
        except: LOG.error('FAILED folder creation', exc_info=True)

    try:
        if os.getenv("SOFTWARE") == "MAYA":
            if not maya_renderSnapshot(DEFAULT_PATH)[1]:
                LOG.warning("no snapshot no")
                return False
        elif os.getenv("SOFTWARE") == "HOUDINI": houdini_renderSnapshot(DEFAULT_PATH)
        else: return False
    except:
        LOG.error('FAIL', exc_info=True)
        return False

    if ui and os.path.exists(DEFAULT_PATH): ui.setIcon(QtGui.QPixmap(QtGui.QImage(DEFAULT_PATH)))
    # WIDGET.show()
    # WIDGET.setFocus()
    return True

def create_screenshot_viewport(WIDGET, ui=''):
    # WIDGET.hide()
    try:
        if   os.getenv("SOFTWARE") == "MAYA":    create_screenshot(WIDGET, ui) # maya_viewportSnapshot(DEFAULT_PATH)
        elif os.getenv("SOFTWARE") == "NUKE":    nuke_viewerSnapshot(DEFAULT_PATH)
        elif os.getenv("SOFTWARE") == "HOUDINI": create_screenshot(WIDGET, ui) # houdini_viewportSnapshot(DEFAULT_PATH)
        elif os.getenv("SOFTWARE") == "MAX":     create_screenshot(WIDGET, ui)
        else: return False
    except:
        LOG.error('FAIL', exc_info=True)
        return False

    if ui and os.path.exists(DEFAULT_PATH): ui.setIcon(QtGui.QPixmap(QtGui.QImage(DEFAULT_PATH)))
    else: return False
    # WIDGET.show()
    # WIDGET.setFocus()
    return True


#*********************************************************************
# RENDER | SNAPSHOT IMAGES
def nuke_viewerSnapshot(img_path=DEFAULT_PATH):
    LOG.info("nuke_viewerSnapshot")
    import nuke
    viewer   = nuke.activeViewer()
    viewNode = nuke.activeViewer().node()

    actInput = nuke.ViewerWindow.activeInput(viewer)
    if actInput < 0: return False

    selInput = nuke.Node.input(viewNode, actInput)

    # look up filename based on top read node
    topName ="[file tail [knob [topnode].file]]"

    # create writes and define render format
    write1 = nuke.nodes.Write( file=img_path.replace("\\", "/"), name='writeNode1' , file_type=Tank().data_project['EXTENSION']['thumnail'])
    write1.setInput(0, selInput)

    # look up current frame
    curFrame = int(nuke.knob("frame"))
    # start the render
    nuke.execute( write1.name(), curFrame, curFrame )
    # clean up
    for n in [write1]: nuke.delete(n)

def maya_viewportSnapshot(img_path=DEFAULT_PATH):
    LOG.info("maya_viewportSnapshot")
    import maya.cmds as mc
    import maya.mel as mel
    mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')
    # playblast one frame to a specific file
    currentFrame = str(mc.currentTime(q=1))
    snapshotStr = 'playblast -frame ' + currentFrame + ' -format "image" -cf "' + img_path + '" -v 0 -wh 1024 576 -p 100;'
    mel.eval(snapshotStr)
    # restore the old format
    mel.eval('setAttr "defaultRenderGlobals.imageFormat" `getAttr "defaultRenderGlobals.imageFormat"`;')

def maya_renderSnapshot(img_path=DEFAULT_PATH):
    LOG.info("maya_renderSnapshot")
    import maya.cmds as cmds
    import maya.mel as mel
    mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')
    return cmds.renderWindowEditor('renderView', e=True, writeImage=img_path)

def houdini_viewportSnapshot(img_path=DEFAULT_PATH):
    LOG.info("houdini_viewportSnapshot")

def houdini_renderSnapshot(img_path=DEFAULT_PATH):
    LOG.info("houdini_renderSnapshot")


#*********************************************************************
# FILE HANDLING
def save_snapshot(rlt_path, src_path=DEFAULT_PATH):
    img = QtGui.QImage()
    img.load(src_path)
    thumbnail_extension = '.' + Tank().data_project['EXTENSION']['thumbnail']

    tmpDir   = os.path.dirname(rlt_path) + '/' + Tank().data_project['META']['dir']
    rlt_path = tmpDir + "/" + os.path.basename(rlt_path).split(".")[0] + thumbnail_extension

    pipefunc.create_folder(rlt_path)
    img.save(rlt_path, format=thumbnail_extension)
    remove_tmp_img(src_path)
    return rlt_path

def remove_tmp_img(img_path=DEFAULT_PATH):
    try:    os.remove(img_path)
    except: LOG.error('FAIL : cant delete tmpFile : ' + img_path, exc_info=True)
