
#*************************************************************
# title         libImage
#
# content       common functions
#
# dependencies  settings.py
# 
# author        Alexander Richter 
# email         contact@richteralexander.com
#*************************************************************

import os 
import glob

from PySide.QtGui import *
from PySide.QtCore import *

import settings as s

import libUser
import libFileService


#************************
# IMAGE
#************************
def setUserImg (userId = "", imgObj = ""):
    if (userId == ""):
        userId = os.getenv('username')
  
    currentImgPath = os.path.join(s.PATH['img_user'], userId + s.FILE_FORMAT["img"])
    
    if(os.path.isfile(currentImgPath)):
        imgObj.setPixmap(QPixmap(QImage(currentImgPath)))
    else:
        imgObj.setPixmap(QPixmap(QImage(s.PLACEHOLDER["user"])))

    imgObj.setToolTip(libUser.getUser(userId).__dict__["name"])


def setPreviewImg (previewId = "", imgObj = ""):
    currentImgPath = os.path.join(s.PATH['img_placeholder'], "ph" + previewId + s.FILE_FORMAT["img"])

    if(os.path.isfile(currentImgPath)):
        imgObj.setPixmap(QPixmap(QImage(currentImgPath)))
    else:
        imgObj.setPixmap(QPixmap(QImage(s.PLACEHOLDER["image"])))


def getShotImg(shot):
    tmpShot = libFileService.getFolderList(s.PATH['comp'], shot + "*")
    
    if (tmpShot):
        tmpShot = tmpShot[0]

    currentPath = os.path.join( s.PATH['comp'], str(tmpShot), s.STATUS["render"])
    tmpImage = sorted(libFileService.getFolderList(currentPath), reverse = True)

    if (tmpImage):
        if("_old" in tmpImage[0] or "history" in tmpImage[0]):
            tmpImage.pop(0)
        tmpImage = tmpImage[0]

    shotImgPath = os.path.join(currentPath, str(tmpImage), "jpg")
    tmpVersion = sorted(glob.glob(shotImgPath + "/" + "*.jpg"), reverse = True)

    if (tmpVersion):
        tmpVersion = tmpVersion[0]

    shotImgPath = os.path.join(shotImgPath, str(tmpVersion))

    if not os.path.exists(shotImgPath): 
        # shotImgPath = os.path.join(s.PATH['img_shot'], shot + s.FILE_FORMAT["img"])
        
        if not os.path.exists(shotImgPath): 
            shotImgPath = s.PLACEHOLDER["shot"]
    return shotImgPath


def getBannerImg(task = ""):
    bannerImgPath = os.path.join(s.PATH['img'], 'banner', task + s.FILE_FORMAT["img"])
    
    if not os.path.isfile(bannerImgPath): 
        bannerImgPath = s.PLACEHOLDER["banner"]

    return bannerImgPath


def getReportImg(reportImgPath, image = False):    
    if not os.path.isfile(reportImgPath): 
        if (image):
            reportImgPath = s.PLACEHOLDER["image"]
        else:
            reportImgPath = s.PLACEHOLDER["report"]
    return reportImgPath


def getProgramImg(software):    
    softwareImgPath = os.path.join(s.PATH["img_program"], software + s.FILE_FORMAT["img"])
    
    if not os.path.isfile(softwareImgPath): 
        softwareImgPath = s.PLACEHOLDER["program"]
    return softwareImgPath