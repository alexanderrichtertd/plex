"""*************************************************************
content   = create render or viewer snapshots
version   = 0.0.1
date      = 2017-01-01

license   = MIT
copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
author    = Alexander Richter <contact@richteralexander.com>
*********************************************************************
This source file has been developed within the scope of the
Technical Director course at Filmakademie Baden-Wuerttemberg.
http://td.animationsinstitut.de
*********************************************************************"""

import os
import time

from PySide import QtGui
from PySide import QtCore

import libData
import libFunc

# DEFAULT
import log
LOG = log.initLog(script="lib")



#************************
# SCREENSHOT
# creats a screenshot of the main screen and saves it
def takeScreenshot(saveDir):
    # app = QApplication(sys.argv)
    dst = saveDir
    QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId()).save(dst, dst.split(".")[-1])
    return dst


#************************
# RENDER | SNAPSHOT IMAGES
def nuke_viewerSnapshot(dirname):
    LOG.info("nuke_viewerSnapshot")

    import nuke
    viewer   = nuke.activeViewer()
    viewNode = nuke.activeViewer().node()

    actInput = nuke.ViewerWindow.activeInput(viewer)
    if actInput < 0 :
        return False

    selInput = nuke.Node.input(viewNode, actInput)

    # look up filename based on top read node
    topName ="[file tail [knob [topnode].file]]"

    # create writes and define render format
    write1 = nuke.nodes.Write( file = dirname.replace("\\", "/"), name = 'writeNode1' , file_type = s.FILE_FORMAT["thumbs"] )
    write1.setInput(0, selInput)

    # look up current frame
    curFrame = int(nuke.knob("frame"))
    # start the render
    nuke.execute( write1.name(), curFrame, curFrame )
    # clean up
    for n in [write1]:
        nuke.delete(n)

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


#************************
# CREATE TEMP IMG
def createScreenshot(WIDGET, ui, LOG):
    WIDGET.hide()
    imgPath = data.PATH_EXTRA["img_tmp"]

    if not os.path.exists(os.path.dirname(imgPath)):
        os.makedirs(os.path.dirname(imgPath))
    time.sleep(0.3)
    imgPath = takeScreenshot(imgPath)
    WIDGET.show()
    ui.setIcon(QPixmap(QImage(imgPath)))
    LOG.info("Screenshot")

def createSnapshotRender(WIDGET, ui, LOG):
    imgPath = data.PATH_EXTRA["img_tmp"]
    WIDGET.hide()

    if not os.path.exists(os.path.dirname(imgPath)):
        os.makedirs(os.path.dirname(imgPath))

    try:
        if os.environ["SOFTWARE"] == "maya":
            #RENDERER???
            if not maya_renderSnapshot(imgPath)[1]:
                LOG.info("no snapshot no")
                return False

        elif os.environ["SOFTWARE"] == "nuke":
            nuke_viewerSnapshot(imgPath)

        elif os.environ["SOFTWARE"] == "houdini":
            houdini_renderSnapshot(imgPath)

    except:
        LOG.error('FAIL', exc_info=True)
        return False

    ui.setIcon(QtGui.QPixmap(QtGui.QImage(libData.getReportImg(imgPath))))
    WIDGET.show()
    WIDGET.setFocus()

    return True

def createSnapshotViewport(WIDGET, ui, LOG):
    LOG.info("createSnapshotViewport")
    imgPath = data.PATH_EXTRA["img_tmp"]

    try:
        if os.environ["SOFTWARE"] == "maya":
            maya_viewportSnapshot(imgPath)

        # nuke has no viewport

        elif os.environ["SOFTWARE"] == "houdini":
            houdini_viewportSnapshot(imgPath)

    except:
        LOG.error('FAIL', exc_info=True)
        return False

    ui.setIcon(QtGui.QPixmap(QtGui.QImage(libData.getReportImg(imgPath))))

    WIDGET.show()
    return True

def saveSnapshotImg(saveDir, imgPath = "", usesaveDir = False):
    img = QImage()

    if not imgPath:
        imgPath = data.PATH_EXTRA["img_tmp"]

    img.load(imgPath)

    if usesaveDir:
        imgPath = saveDir
    else:
        tmpDir  = os.path.dirname(saveDir) + "/" + s.STATUS["thumbs"]
        imgPath = tmpDir.replace("\\", "/") + "/" + os.path.basename(saveDir).split(".")[0] + s.FILE_FORMAT["thumbs"]

    libFunc.createFolder(imgPath)
    img.save(imgPath, format = s.FILE_FORMAT_CODE[s.FILE_FORMAT["thumbs"]])
