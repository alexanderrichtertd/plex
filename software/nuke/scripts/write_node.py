#*********************************************************************
# content   = write node functions
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys
import shutil
import webbrowser

import nuke

import libLog
import libFileFolder
from tank import Tank

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#************************
# INIT
#************************
def nodeCreate(this_node=''):
    if this_node == '': this_node = nuke.thisNode()

    if this_node["customRange"].getValue():
        this_node["frameStart"].setValue(int(nuke.Root()['first_frame'].getValue()))
        this_node["frameEnd"].setValue(int(nuke.Root()['last_frame'].getValue()))

    this_node["resolutionX"].setValue(this_node.width())
    this_node["resolutionY"].setValue(this_node.height())

    fileName   = os.path.basename(nuke.root().name()).split(".")[0]
    renderPath = os.path.dirname(nuke.root().name()) + "/RENDER/" + fileName + "/exr/" + fileName + ".%04d.exr"

    this_node["rootPath"].setValue(renderPath)
    this_node["exrPath"].setValue(renderPath)
    this_node["jpgPath"].setValue(renderPath.replace("exr","jpg"))
    this_node["tifPath"].setValue(renderPath.replace("exr","tif"))

    LOG.info("START : " + fileName)


def openRV(path):
    if not os.path.exists(os.path.dirname(path)) or not os.listdir(os.path.dirname(path)):
        LOG.warning("FOLDER : NOT EXISTS : " + path)
        return

    os.system('start "" "' + Tank().data['software']['RV']['path'] + '" ' + path)


def openFolder(path):
    path = os.path.dirname(path).replace("/","\\")

    if not os.path.exists(path) or not os.listdir(path):
        LOG.warning("FOLDER : NOT EXISTS : " + path)
        return

    webbrowser.open(path)


def render():
    this_node = nuke.thisNode()
    setCommentPath()

    frameStart  = int(this_node["frameStart"].getValue())
    frameEnd    = int(this_node["frameEnd"].getValue())

    if this_node["submit"].getValue() == 0.0:
        from plugins.vuRenderThreads.plugin_nuke import plugin_nuke

        threads = int(this_node["threads"].getValue())
        plugin_nuke.createThreads(frameStart, frameEnd, threads, [this_node.name()])
        LOG.info("END    : RENDERTHREADS : " + this_node["exrPathComment"].getValue())

    elif this_node["submit"].getValue() == 1.0:
        import rrenderSubmit
        nuke.load('rrenderSubmit')
        rrenderSubmit.rrSubmit_Nuke_Node(this_node, frameStart, frameEnd)
        LOG.info("END    : RRSUBMIT : " + this_node["exrPathComment"].getValue())

    else:
        try:
            nuke.execute(nuke.thisNode(), start=frameStart, end=frameEnd, incr=1)
            LOG.info("END    : LOCAL : " + this_node["exrPathComment"].getValue())
        except:
            print "END    : LOCAL : Execution failed"
            LOG.error("END    : LOCAL : " + this_node["exrPathComment"].getValue(), exc_info=True)


def setCommentPath():
    this_node = nuke.thisNode()

    if this_node["status"].value() != " " or this_node["chbPublish"].value():

        if this_node["chbPublish"].value():
            comment = "PUBLISH"

            # delete publish
            publishPath = os.path.dirname(os.path.dirname(nuke.root().name())) + "/PUBLISH"
            if  os.path.exists(publishPath):
                try:
                    print "Delete : " + publishPath
                    shutil.rmtree(publishPath, ignore_errors=True)
                except:
                    LOG.error("Delete : Failed : " + publishPath, exc_info=True)

        else:
            comment = this_node["status"].value()

        print "STATUS: " + comment
        exrPath  = this_node["exrPath"].getValue().split("/")
        fileName = exrPath[-1].split(".")
        newName  = fileName[0] + "_" + comment
        newPath  = this_node["exrPath"].getValue().replace(fileName[0], newName)

        this_node["exrPathComment"].setValue(newPath)

        jpgPath  = this_node["jpgPath"].getValue().split("/")
        fileName = jpgPath[-1].split(".")
        newName  = fileName[0] + "_" + comment
        newPath  = this_node["jpgPath"].getValue().replace(fileName[0], newName)

        this_node["jpgPathComment"].setValue(newPath)

        tifPath  = this_node["tifPath"].getValue().split("/")
        fileName = tifPath[-1].split(".")
        newName  = fileName[0] + "_" + comment
        newPath  = this_node["tifPath"].getValue().replace(fileName[0], newName)

        this_node["tifPathComment"].setValue(newPath)

    else:
        this_node["exrPathComment"].setValue(this_node["exrPath"].getValue())
        this_node["jpgPathComment"].setValue(this_node["jpgPath"].getValue())
        this_node["tifPathComment"].setValue(this_node["tifPath"].getValue())


def publishRender(writeNode):
    this_node = nuke.thisGroup()

    if this_node["chbPublish"].value():
        print "PUBLISH"

        fileName  = []
        splitFile = os.path.basename(nuke.root().name()).split(".")[0].split("_")

        for part in splitFile:
            fileName.append(part)
            if part == "COMP":
                break

        fileName    = ("_").join(fileName)
        publishPath = os.path.dirname(os.path.dirname(nuke.root().name())) + "/PUBLISH/exr"
        oldPath     = os.path.dirname(this_node["exrPathComment"].getValue())

        if writeNode == "exr":
            if not os.path.exists(publishPath):
                os.makedirs(publishPath)

            LOG.info("PUBLISH: EXR : " + publishPath)

            oldFrames = libFileFolder.getFolderList(oldPath, fileType='*exr', ex=True)

            for oldFrame in oldFrames:
                framePart    = oldFrame.split(".")
                framePart[0] = fileName

                newFrame = publishPath + "/" + (".").join(framePart)
                oldFrame = oldPath + "/" + oldFrame

                shutil.copyfile(oldFrame, newFrame)


        oldPath   = os.path.dirname(this_node["jpgPathComment"].getValue())

        if writeNode == "jpg":

            publishPath = publishPath.replace("exr", "jpg")

            if not os.path.exists(publishPath):
                os.makedirs(publishPath)

            LOG.info("PUBLISH: JPG : " + publishPath)

            oldFrames = libFileFolder.getFolderList(oldPath, fileType='*jpg', ex=True)

            for oldFrame in oldFrames:
                framePart    = oldFrame.split(".")
                framePart[0] = fileName

                newFrame = (".").join(framePart)

                oldFrame = oldPath + "/" + oldFrame
                newFrame = publishPath + "/" + newFrame

                shutil.copyfile(oldFrame, newFrame)

    else:
        print "WORK"
