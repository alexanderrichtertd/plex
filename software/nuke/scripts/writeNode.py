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

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

#************************
# INIT
#************************
def nodeCreate(currentNode = ""):

    if currentNode == "":
        currentNode = nuke.thisNode()

    global LOG
    # LOG = libLog.initLog(software=SOFTWARE, script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))

    if currentNode["frameRangeMode"].value() != "custom":
        currentNode["frameStart"].setValue(int(nuke.Root()['first_frame'].getValue()))
        currentNode["frameEnd"].setValue(int(nuke.Root()['last_frame'].getValue()))

    currentNode["resolutionX"].setValue(currentNode.width())
    currentNode["resolutionY"].setValue(currentNode.height())

    fileName    = os.path.basename(nuke.root().name()).split(".")[0]
    renderPath  = os.path.dirname(nuke.root().name()) + "/" + s.STATUS["render"] + "/" + fileName + "/exr/" + fileName + ".%04d.exr"

    currentNode["rootPath"].setValue(renderPath)
    currentNode["exrPath"].setValue(renderPath)
    currentNode["jpgPath"].setValue(renderPath.replace("exr","jpg"))
    currentNode["tifPath"].setValue(renderPath.replace("exr","tif"))

    # setCommentPath()
    LOG.info("START  : " + fileName)


def openRV (renderPath):
    global LOG

    if not os.path.exists(os.path.dirname(renderPath)) or not os.listdir(os.path.dirname(renderPath)):
        LOG.warning("FOLDER : NOT EXISTS : " + renderPath)
        return "WARNING: path doesnt exist: " + renderPath

    os.system('start "" "' + s.SOFTWARE["rv"] + '" ' + renderPath)
    LOG.info("RV : OPEN : " + renderPath)


def openFolder(path):
    global LOG
    renderPath = os.path.dirname(path).replace("/","\\")

    if not os.path.exists(renderPath) or not os.listdir(renderPath):
        LOG.warning("FOLDER : NOT EXISTS : " + renderPath)
        return "WARNING: path doesnt exist: " + renderPath

    webbrowser.open(renderPath)

    LOG.info("FOLDER : OPEN :" + renderPath)


def render():
    global LOG

    cn = nuke.thisNode()
    setCommentPath()

    frameStart  = int(cn["frameStart"].getValue())
    frameEnd    = int(cn["frameEnd"].getValue())

    if cn["submit"].getValue() == 0.0:
        threads     = int(cn["threads"].getValue())
        from plugins.vuRenderThreads.plugin_nuke import plugin_nuke
        plugin_nuke.createThreads(frameStart, frameEnd, threads, [cn.name()])
        LOG.info("END    : RENDERTHREADS : " + cn["exrPathComment"].getValue())

    elif cn["submit"].getValue() == 1.0:
        import rrenderSubmit
        nuke.load('rrenderSubmit')
        rrenderSubmit.rrSubmit_Nuke_Node(cn, frameStart, frameEnd)
        LOG.info("END    : RRSUBMIT : " + cn["exrPathComment"].getValue())

    else:
        try:
            nuke.execute(nuke.thisNode(), start=frameStart, end=frameEnd, incr=1)
            LOG.info("END    : LOCAL : " + cn["exrPathComment"].getValue())
        except:
            print "END    : LOCAL : Execution failed"
            LOG.error("END    : LOCAL : " + cn["exrPathComment"].getValue(), exc_info=True)


def setCommentPath():
    cn = nuke.thisNode()

    if cn["status"].value() != " " or cn["chbPublish"].value():

        if cn["chbPublish"].value():
            comment = "PUBLISH"

            # delete publish
            publishPath = os.path.dirname(os.path.dirname(nuke.root().name())) + "/" + s.STATUS["publish"]
            if  os.path.exists(publishPath):
                try:
                    print "Delete : " + publishPath
                    shutil.rmtree(publishPath, ignore_errors=True)
                except:
                    LOG.error("Delete : Failed : " + publishPath, exc_info=True)

        else:
            comment = cn["status"].value()

        print "STATUS: " + comment
        exrPath     = cn["exrPath"].getValue().split("/")
        fileName    = exrPath[-1].split(".")
        newName     = fileName[0] + "_" + comment
        newPath     = cn["exrPath"].getValue().replace(fileName[0], newName)

        cn["exrPathComment"].setValue(newPath)

        jpgPath     = cn["jpgPath"].getValue().split("/")
        fileName    = jpgPath[-1].split(".")
        newName     = fileName[0] + "_" + comment
        newPath     = cn["jpgPath"].getValue().replace(fileName[0], newName)

        cn["jpgPathComment"].setValue(newPath)

        tifPath     = cn["tifPath"].getValue().split("/")
        fileName    = tifPath[-1].split(".")
        newName     = fileName[0] + "_" + comment
        newPath     = cn["tifPath"].getValue().replace(fileName[0], newName)

        cn["tifPathComment"].setValue(newPath)

    else:
        cn["exrPathComment"].setValue(cn["exrPath"].getValue())
        cn["jpgPathComment"].setValue(cn["jpgPath"].getValue())
        cn["tifPathComment"].setValue(cn["tifPath"].getValue())


def publishRender(writeNode):
    cn = nuke.thisGroup()

    if cn["chbPublish"].value():
        print "PUBLISH"

        fileName    = []
        splitFile   = os.path.basename(nuke.root().name()).split(".")[0].split("_")

        for part in splitFile:
            fileName.append(part)
            if part == "COMP":
                break

        fileName    = ("_").join(fileName)
        publishPath = os.path.dirname(os.path.dirname(nuke.root().name())) + "/" + s.STATUS["publish"] + "/exr"
        oldPath     = os.path.dirname(cn["exrPathComment"].getValue())

        if writeNode == "exr":
            if not os.path.exists(publishPath):
                os.makedirs(publishPath)

            LOG.info("PUBLISH: EXR : " + publishPath)

            oldFrames = libFileService.getFolderList(oldPath, fileType='*exr', ex=True)

            for oldFrame in oldFrames:
                framePart    = oldFrame.split(".")
                framePart[0] = fileName

                newFrame = (".").join(framePart)

                oldFrame = oldPath + "/" + oldFrame
                newFrame = publishPath + "/" + newFrame

                shutil.copyfile(oldFrame, newFrame)


        oldPath   = os.path.dirname(cn["jpgPathComment"].getValue())

        if writeNode == "jpg":

            publishPath = publishPath.replace("exr", "jpg")

            if not os.path.exists(publishPath):
                os.makedirs(publishPath)

            LOG.info("PUBLISH: JPG : " + publishPath)

            oldFrames = libFileService.getFolderList(oldPath, fileType='*jpg', ex=True)

            for oldFrame in oldFrames:
                framePart    = oldFrame.split(".")
                framePart[0] = fileName

                newFrame = (".").join(framePart)

                oldFrame = oldPath + "/" + oldFrame
                newFrame = publishPath + "/" + newFrame

                shutil.copyfile(oldFrame, newFrame)

    else:
        print "WORK"
