#*************************************************************
# CONTENT       image functions
#
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
import sys
import glob

from PySide import QtGui
from PySide import QtCore

# DELETE ******************
sys.path.append("../settings")
import setEnv
setEnv.SetEnv()
#**************************
import getProject
DATA = getProject.GetProject()

import libUser
import libFileFolder

# DEFAULT
import libLog
LOG = libLog.initLog(script="lib")

##
# @BRIEF  get the img/icon for your btn/lbl of the project or master pipeline
#
# @PARAM  name string. folder and name of the image
#
# @RETURN string. image path
def getImgPath(name = "btn/btnHelp48"):
    path = ""
    for env in DATA.ENVIRON_PATH:
        env = "IMG" + env
        if env in os.environ:
            path = ("/").join([os.environ[env], name + DATA.FILE_FORMAT["img"]])
            if os.path.exists(path):
                return path
    LOG.warning("Path and Env is not valid: " + path)

def getReportImg(reportImgPath, image = False):
    if not os.path.isfile(reportImgPath):
        if (image):
            reportImgPath = DATA.PLACEHOLDER["image"]
        else:
            reportImgPath = DATA.PLACEHOLDER["report"]
    return reportImgPath


#************************
# SET IMAGE
# @BRIEF  sets user image to label
#
# @PARAM  QLabel imgObj, STRING userId
def setUserImg (imgObj, userId = ""):
    if (userId == ""):
        userId = os.getenv('username')

    currentImgPath = getImg("user/" + userId)
    try:
        imgObj.setPixmap(QtGui.QPixmap(QImage(currentImgPath)))
        imgObj.setToolTip(libUser.getUser(userId).__dict__["name"])
    except:
        LOG.warning("Wrong imgObj type : QtGui.QLabel")


#************************
# TEMP IMAGE
def rmTmpImg():
    tmpImgPath = DATA.PATH_EXTRA["img_tmp"]
    # if os.path.exists(tmpImgPath):
    #     try:
    #         os.remove(tmpImgPath)
    #     except:
    #         LOG.except('FAIL : cant delete tmpFile : ' + tmpImgPath)
    return tmpImgPath
