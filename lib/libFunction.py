
#*************************************************************
# title         libFunction
#
# content       common functions
#
# dependencies  settings.py
# 
# author        Alexander Richter 
# email         contact@richteralexander.com
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
# FUNCTIONS
#************************
def rmTempImg():
    tmpImgPath = s.PATH_EXTRA["img_tmp"]
    if os.path.exists(tmpImgPath):
        try:
            os.remove(tmpImgPath)
        except:
            print('FAIL : cant delete tmpFile : ' + tmpImgPath) 

    return tmpImgPath


def openFolder(openPath):
    openPath = openPath.replace("/", "\\")

    if os.path.exists(openPath):
        if len(openPath.split(".")) > 1:
            openPath = os.path.dirname(openPath)
        webbrowser.open(openPath)
    else:
        return ("FAIL : Path is not valid")

    return openPath     


def getHelp(title = ""):
    if title == "": title = os.getenv('SOFTWARE')
    webbrowser.open(s.LINK[title])


def createFolder(path):
    if len(path.split(".")) > 1:
        path = os.path.dirname(path)

    if not os.path.exists(path):
        os.makedirs(path)


#************************
# REPORT
#************************
def setMetaData(shot, metaObj): 
    tmpShot = libShot.Shot()
    tmpShot.__dict__ = libShot.getShot(shot)

    # should check if one of the settings is empty then use the default (000)
    metaObj.setPlainText(tmpShot.__call__())


def setErrorCount(ui):
    ui.lblErrorCount.setText(str(len(libFileService.getFolderList(s.PATH["data_report"], "*.json"))))