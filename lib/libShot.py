#*************************************************************
# title:        libShot
#
# content:      shot informations
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import os
import sys

import settings as s

import libFileService


#************************
# SHOT
#************************
class Shot:
    def __init__(self, title = "000", resolution = "", fps = "", frames = [], comment = ""):        
        self.title      = title
        self.resolution = resolution
        self.fps        = fps
        self.frames     = frames
        self.comment    = comment

    def __call__(self):
        return (\
        "Resolution:   " + self.resolution + "\n" + "\n" +\
        "FPS:          " + self.fps + "\n" + "\n" +\
        "Frames:       " + self.frames + "\n" + "\n" +\
        "Comment:      " + self.comment)


def setShot (shot = Shot()):
    print "setShot"
    # set Google Docs


def getShot (shotNr):
    print "getShot"
    # get Google Docs