#*********************************************************************
# content   = snapshot
#             executes other scripts on PUBLISH (on task in file name)
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
import time

from PySide import QtGui, QtCore

import libLog
import libData
import libFunc
import libFileFolder

# DEFAULT
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

default_tmp_path = os.path.normpath(os.getenv('DATA_USER_PATH') + '/tmp_img.jpg')


#*********************************************************************
# SCREENSHOT
# creats a screenshot of the main screen and saves it
def take_screenshot(save_dir):
    # app = QApplication(sys.argv)
    QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId()).save(save_dir, save_dir.split(".")[-1])
    return save_dir


#*********************************************************************
# RENDER | SNAPSHOT IMAGES
def nuke_viewerSnapshot(dirname):
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
    write1 = nuke.nodes.Write( file = dirname.replace("\\", "/"), name = 'writeNode1' , file_type = libData.THUMBS_FORMAT )
    write1.setInput(0, selInput)

    # look up current frame
    curFrame = int(nuke.knob("frame"))
    # start the render
    nuke.execute( write1.name(), curFrame, curFrame )
    # clean up
    for n in [write1]: nuke.delete(n)

def maya_viewportSnapshot(dirname):
    LOG.info("maya_viewportSnapshot")
    import maya.cmds as mc
    import maya.mel as mel
    mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')
    # playblast one frame to a specific file
    currentFrame = str(mc.currentTime(q=1))
    snapshotStr = 'playblast -frame ' + currentFrame + ' -format "image" -cf "' + dirname + '" -v 0 -wh 1024 576 -p 100;'
    mel.eval(snapshotStr)
    # restore the old format
    mel.eval('setAttr "defaultRenderGlobals.imageFormat" `getAttr "defaultRenderGlobals.imageFormat"`;')

def maya_renderSnapshot(dirname):
    LOG.info("maya_renderSnapshot")
    import maya.cmds as cmds
    import maya.mel as mel
    mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')
    return cmds.renderWindowEditor('renderView', e=True, writeImage=dirname)

def houdini_viewportSnapshot(dirname):
    LOG.info("houdini_viewportSnapshot")

def houdini_renderSnapshot(dirname):
    LOG.info("houdini_renderSnapshot")


#*********************************************************************
# CREATE TEMP IMG
def create_any_screenshot(WIDGET, ui=''):
    # if not create_screenshot_render(WIDGET, ui):
    if not create_screenshot_viewport(WIDGET, ui):
        create_screenshot(WIDGET, ui)

def create_screenshot(WIDGET, ui=''):
    # WIDGET.hide()
    if not os.path.exists(os.path.dirname(default_tmp_path)):
        try: os.makedirs(os.path.dirname(default_tmp_path))
        except: LOG.error('FAILED folder creation', exc_info=True)
    # time.sleep(0.3)
    img_path = take_screenshot(default_tmp_path)
    # WIDGET.show()
    if ui:  ui.setIcon(QtGui.QPixmap(QtGui.QImage(img_path)))

def create_screenshot_render(WIDGET, ui=''):
    WIDGET.hide()

    if not os.path.exists(os.path.dirname(default_tmp_path)):
        try: os.makedirs(os.path.dirname(default_tmp_path))
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
    WIDGET.show()
    WIDGET.setFocus()
    return True

def create_screenshot_viewport(WIDGET, ui=''):
    WIDGET.hide()
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
    WIDGET.show()
    WIDGET.setFocus()
    return True

def save_snapshot(saveDir, img_path='', usesaveDir=False):

    if not img_path: img_path = default_tmp_path

    img = QtGui.QImage()
    img.load(img_path)

    if usesaveDir: img_path = saveDir
    else:
        tmpDir  = os.path.dirname(saveDir) + "/" + libData.META_FOLDER
        img_path = tmpDir.replace("\\", "/") + "/" + os.path.basename(saveDir).split(".")[0] + libData.THUMBS_FORMAT

    libFileFolder.create_folder(img_path)
    img.save(img_path, format = libData.THUMBS_FORMAT)
    libFileFolder.rm_tmp_img()
