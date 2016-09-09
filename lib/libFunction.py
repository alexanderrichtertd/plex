#*************************************************************
# CONTENT       common functions
# 
# AUTHOR        Alexander Richter 
# EMAIL         contact@richteralexander.com
#*************************************************************

import os 
import sys
import glob
import webbrowser
from time import gmtime, strftime

from PySide.QtGui import *
from PySide.QtCore import *

import settings as s

import libShot
import libUser
import libFileService


#************************
# FOLDER & FILES
#************************
def createFolder(path):
    if not os.path.exists(path):
        if len(path.split(".")) > 1:
            path = os.path.dirname(path)
        os.makedirs(path)


def openFolder(path):
    if os.path.exists(path):
        if len(path.split(".")) > 1:
            path = os.path.dirname(path)
        webbrowser.open(path)
    else:
        log.debug("FAIL : Path is not valid:" + path)
    return path     


# fileType="*.py", exclude="__init__.py", extention [True:return "file.py"; False "file"]
def getFileList(path, fileType='*', extension = False, exclude = "*"):
    getFile = []

    if(os.path.exists(path)):
        os.chdir(path)
        for fileName in glob.glob(fileType):
            if exclude in fileName:
                continue
            if extension:
                getFile.append(fileName)
            else:
                getFile.append((fileName.split('.')[0]))
    return (getFile)


# GET all subfolders in the path
def getDeepFolderList(path):
    getFile = []
    os.chdir(path)

    for fileName in os.walk(path):
        getFile.append(os.path.basename(fileName[0]))

    getFile.pop(0)
    return getFile


#************************
# HELP
#************************
def getHelp(title = ""):
    if title == "": title = os.getenv('SOFTWARE')
    if title in LINK:
        webbrowser.open(s.LINK[title])
    else:
        webbrowser.open(s.LINK["pipeline"])
