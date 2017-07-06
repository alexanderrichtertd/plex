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
    # setCommentPath()

    frameStart = int(this_node["frameStart"].getValue())
    frameEnd   = int(this_node["frameEnd"].getValue())

    LOG.info('{}-{}'.format(frameStart, frameEnd))

    # RENDERTHREADS
    if this_node["submit"].getValue() == 0.0:
        from plugins.vuRenderThreads.plugin_nuke import plugin_nuke

        threads = int(this_node["threads"].getValue())
        plugin_nuke.createThreads(frameStart, frameEnd, threads, [this_node.name()])
        LOG.info("END    : RENDERTHREADS : " + this_node["exrPath"].getValue())

    # RENDERFARM
    elif this_node["submit"].getValue() == 1.0:
        import rrenderSubmit
        nuke.load('rrenderSubmit')
        rrenderSubmit.rrSubmit_Nuke_Node(this_node, frameStart, frameEnd)
        LOG.info("END    : RRSUBMIT : " + this_node["exrPath"].getValue())

    # LOCAL
    else:
        try:
            nuke.execute(nuke.thisNode(), start=frameStart, end=frameEnd, incr=1)
        except:
            LOG.error("END    : LOCAL : " + this_node["exrPath"].getValue(), exc_info=True)


def publishRender(file_type):
    this_node = nuke.thisGroup()
    if not this_node["chbPublish"].value(): return

    fileName  = []
    splitFile = os.path.basename(nuke.root().name()).split(".")[0].split("_")

    for part in splitFile:
        fileName.append(part)
        if part == "COMP": break

    fileName    = ("_").join(fileName)
    publishPath = os.path.dirname(os.path.dirname(nuke.root().name())) + "/PUBLISH/" + file_type
    oldPath     = os.path.dirname(this_node[file_type + "Path"].getValue())

    LOG.info("PUBLISH: " + publishPath)

    if not os.path.exists(publishPath): os.makedirs(publishPath)

    oldFrames = libFileFolder.getFolderList(oldPath, fileType='*' + file_type, ex=True)

    for oldFrame in oldFrames:
        framePart    = oldFrame.split(".")
        framePart[0] = fileName

        newFrame = publishPath + "/" + (".").join(framePart)
        oldFrame = oldPath + "/" + oldFrame

        shutil.copyfile(oldFrame, newFrame)

