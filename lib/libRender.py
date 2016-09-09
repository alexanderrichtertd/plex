#*************************************************************
# title         libRender
#
# content       set low and high render settings
#               create render or viewer snapshots
#
# author        Alexander Richter 
# email         contact@richteralexander.com
#*************************************************************

import os
import time

from PySide.QtGui import *
from PySide.QtCore import *

import settings as s

import libImage
import libFunction


#************************
# RENDER SETTINGS
#************************
def setRenderSettings(renderStatus):
    print "setRenderSettings"

    # print s.MAYA_RENDERER
    # if os.environ["SOFTWARE"] == "maya":
    #     if renderStatus:
    #         print "Render Settings : " + SOFTWARE + " : Low"
    #     else:
    #         print "Render Settings : " + SOFTWARE + " : High"


    # if os.environ["SOFTWARE"] == "nuke":
    #     if renderStatus:
    #         print "Render Settings : " + SOFTWARE + " : Low"
    #     else:
    #         print "Render Settings : " + SOFTWARE + " : High"


    # if os.environ["SOFTWARE"] == "houdini":
    #     if renderStatus:
    #         print "Render Settings : " + SOFTWARE + " : Low"
    #     else:
    #         print "Render Settings : " + SOFTWARE + " : High"


#************************
# SCREENSHOT
#************************
# creats a screenshot of the main screen and saves it
def takeScreenshot(saveDir):
    # app = QApplication(sys.argv)
    dst = saveDir
    QPixmap.grabWindow(QApplication.desktop().winId()).save(dst, dst.split(".")[-1]) 
    return dst


#************************
# RENDER | SNAPSHOT IMAGES
#************************
def nuke_viewerSnapshot(dirname):
    print "nuke_viewerSnapshot"

    import nuke
    viewer      = nuke.activeViewer()
    viewNode    = nuke.activeViewer().node()

    actInput    = nuke.ViewerWindow.activeInput(viewer)
    if actInput < 0 : 
        return False

    selInput    = nuke.Node.input(viewNode, actInput)

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
    print "maya_viewportSnapshot"

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
    print "maya_renderSnapshot"
        
    import maya.cmds as cmds
    import maya.mel as mel
    mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')
    return cmds.renderWindowEditor('renderView', e=True, writeImage=dirname)


def houdini_viewportSnapshot(dirname):
    print "houdini_viewportSnapshot"


def houdini_renderSnapshot(dirname):
    print "houdini_renderSnapshot"


#************************
# CREATE TEMP IMG
#************************
def createScreenshot(WIDGET, ui, LOG):
    print "createScreenshot"

    WIDGET.hide()
    imgPath = s.PATH_EXTRA["img_tmp"]

    if not os.path.exists(os.path.dirname(imgPath)):
        os.makedirs(os.path.dirname(imgPath))
    time.sleep(0.3)
    imgPath = takeScreenshot(imgPath)
    WIDGET.show()
    ui.setIcon(QPixmap(QImage(imgPath)))
    LOG.info("Screenshot")


def createSnapshotRender(WIDGET, ui, LOG):
    imgPath = s.PATH_EXTRA["img_tmp"]
    WIDGET.hide()

    if not os.path.exists(os.path.dirname(imgPath)):
        os.makedirs(os.path.dirname(imgPath))

    try:
        if os.environ["SOFTWARE"] == "maya":
            #RENDERER???
            if not maya_renderSnapshot(imgPath)[1]:
                print "no snapshot no"
                return False 
                
        elif os.environ["SOFTWARE"] == "nuke":    
            nuke_viewerSnapshot(imgPath)                
        
        elif os.environ["SOFTWARE"] == "houdini":    
            houdini_renderSnapshot(imgPath)

    except:
        LOG.error('FAIL : createSnapshotRender', exc_info=True) 
        return False

    ui.setIcon(QPixmap(QImage(libImage.getReportImg(imgPath))))
    WIDGET.show()
    WIDGET.setFocus()

    return True


def createSnapshotViewport(WIDGET, ui, LOG):
    print "createSnapshotViewport"
    imgPath = s.PATH_EXTRA["img_tmp"]
    
    try:
        if os.environ["SOFTWARE"] == "maya":
            maya_viewportSnapshot(imgPath) 
               
        # nuke has no viewport
        
        elif os.environ["SOFTWARE"] == "houdini":     
            houdini_viewportSnapshot(imgPath) 

    except:
        LOG.error('FAIL : createSnapshotViewport', exc_info=True) 
        return False

    ui.setIcon(QPixmap(QImage(libImage.getReportImg(imgPath))))

    WIDGET.show()
    return True


def saveSnapshotImg(saveDir, imgPath = "", usesaveDir = False):
    img = QImage()

    if not imgPath:
        imgPath = s.PATH_EXTRA["img_tmp"]
    
    img.load(imgPath)
    
    if usesaveDir:
        imgPath = saveDir
    else:
        tmpDir  = os.path.dirname(saveDir) + "/" + s.STATUS["thumbs"]
        imgPath = tmpDir.replace("\\", "/") + "/" + os.path.basename(saveDir).split(".")[0] + s.FILE_FORMAT["thumbs"]

    libFunction.createFolder(imgPath)
    img.save(imgPath, format = s.FILE_FORMAT_CODE[s.FILE_FORMAT["thumbs"]])