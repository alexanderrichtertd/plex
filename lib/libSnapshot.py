#*********************************************************************
# content   = snapshot
#             executes other scripts on PUBLISH (on task in file name)
# version   = 0.0.1
# date      = 2018-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import time

from Qt import QtWidgets, QtGui, QtCore, __binding__

import libLog
import libData
import libFunc

# DEFAULT
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

default_tmp_path = os.path.normpath(os.getenv('DATA_USER_PATH').split(';')[0] + '/tmp_img.jpg')


#*********************************************************************
# SCREENSHOT
# creats a screenshot of the main screen and saves it
def create_any_screenshot(WIDGET, ui=''):
    # if not create_screenshot_render(WIDGET, ui):
    if not create_screenshot_viewport(WIDGET, ui):
        create_screenshot(WIDGET, ui)

def create_screenshot(WIDGET, ui=''):
    print "SCREENSHOT"
    # WIDGET.hide()
    if not os.path.exists(os.path.dirname(default_tmp_path)):
        try: os.makedirs(os.path.dirname(default_tmp_path))
        except: LOG.error('FAILED folder creation', exc_info=True)
    # time.sleep(0.6)

    if __binding__ == "PySide2":
        from PySide2 import QtWidgets, QtGui
        QtGui.QScreen.grabWindow(QtWidgets.QApplication.primaryScreen(), QtWidgets.QApplication.desktop().winId()).save(default_tmp_path, default_tmp_path.split(".")[-1])
    else:
        from Qt import QtWidgets, QtGui
        QtGui.QPixmap.grabWindow(QtWidgets.QApplication.desktop().winId()).save(default_tmp_path, default_tmp_path.split(".")[-1])

    # WIDGET.setFocus()
    # WIDGET.show()
    if ui: ui.setIcon(QtGui.QPixmap(QtGui.QImage(default_tmp_path)))

def create_screenshot_render(WIDGET, ui=''):
    # WIDGET.hide()
    if not os.path.exists(os.path.dirname(default_tmp_path)):
        try:    os.makedirs(os.path.dirname(default_tmp_path))
        except: LOG.error('FAILED folder creation', exc_info=True)

    try:
        if os.getenv("SOFTWARE") == "MAYA":
            if not maya_renderSnapshot(default_tmp_path)[1]:
                LOG.warning("no snapshot no")
                return False
        elif os.getenv("SOFTWARE") == "HOUDINI": houdini_renderSnapshot(default_tmp_path)
        else: return False
    except:
        LOG.error('FAIL', exc_info=True)
        return False

    if ui and os.path.exists(default_tmp_path): ui.setIcon(QtGui.QPixmap(QtGui.QImage(default_tmp_path)))
    # WIDGET.show()
    # WIDGET.setFocus()
    return True

def create_screenshot_viewport(WIDGET, ui=''):
    # WIDGET.hide()
    try:
        if   os.getenv("SOFTWARE") == "MAYA":    create_screenshot(WIDGET, ui) # maya_viewportSnapshot(default_tmp_path)
        elif os.getenv("SOFTWARE") == "NUKE":    nuke_viewerSnapshot(default_tmp_path)
        elif os.getenv("SOFTWARE") == "HOUDINI": create_screenshot(WIDGET, ui) # houdini_viewportSnapshot(default_tmp_path)
        elif os.getenv("SOFTWARE") == "MAX":     create_screenshot(WIDGET, ui)
        else: return False
    except:
        LOG.error('FAIL', exc_info=True)
        return False

    if ui and os.path.exists(default_tmp_path): ui.setIcon(QtGui.QPixmap(QtGui.QImage(default_tmp_path)))
    else: return False
    # WIDGET.show()
    # WIDGET.setFocus()
    return True


#*********************************************************************
# RENDER | SNAPSHOT IMAGES
def nuke_viewerSnapshot(img_path=default_tmp_path):
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
    write1 = nuke.nodes.Write( file=img_path.replace("\\", "/"), name='writeNode1' , file_type=libData.THUMBS_FORMAT[1:])
    write1.setInput(0, selInput)

    # look up current frame
    curFrame = int(nuke.knob("frame"))
    # start the render
    nuke.execute( write1.name(), curFrame, curFrame )
    # clean up
    for n in [write1]: nuke.delete(n)

def maya_viewportSnapshot(img_path=default_tmp_path):
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

def maya_renderSnapshot(img_path=default_tmp_path):
    LOG.info("maya_renderSnapshot")
    import maya.cmds as cmds
    import maya.mel as mel
    mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')
    return cmds.renderWindowEditor('renderView', e=True, writeImage=img_path)

def houdini_viewportSnapshot(img_path=default_tmp_path):
    LOG.info("houdini_viewportSnapshot")

def houdini_renderSnapshot(img_path=default_tmp_path):
    LOG.info("houdini_renderSnapshot")


#*********************************************************************
# FILE HANDLING
def save_snapshot(rlt_path, src_path=default_tmp_path):
    img = QtGui.QImage()
    img.load(src_path)

    tmpDir   = os.path.dirname(rlt_path) + '/' + libData.META_FOLDER
    rlt_path = tmpDir + "/" + os.path.basename(rlt_path).split(".")[0] + libData.THUMBS_FORMAT

    libFunc.create_folder(rlt_path)
    img.save(rlt_path, format=libData.THUMBS_FORMAT)
    remove_tmp_img(src_path)
    return rlt_path

def remove_tmp_img(img_path=default_tmp_path):
    try:    os.remove(img_path)
    except: LOG.error('FAIL : cant delete tmpFile : ' + img_path, exc_info=True)
