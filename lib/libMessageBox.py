#*************************************************************
# title         libMessageBox
#
# content     	standard message boxes
#
# author        Alexander Richter 
# email         contact@richteralexander.com
#*************************************************************

import os 
import sys

from PySide.QtGui import *
from PySide.QtCore import *

import settings as s


#**********************
# FOLDERSEARCH
#**********************
def folderMsgBox(bpS, dataFilter, title = "Choose file to open", path = ""): #dataFilter = "Maya Files (*.mb *.ma)"
    global SAVE_TESTIMG_PATH, IMG_PATH

    dialog = QFileDialog()
    result = dialog.getOpenFileName(bpS,
                title, path, dataFilter)
    print("RESULT: " + result[0])
    return str(result[0])


#**********************
# QUESTIONS
#**********************
def questionMsgBox (title = "", header = "", content = "", icon = QMessageBox.Warning):
    msgBox = QMessageBox()
    msgBox.setWindowTitle(title)
    msgBox.setText(header)
    msgBox.setInformativeText(content)
    msgBox.setIcon(icon)
    msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
    msgBox.setDefaultButton(QMessageBox.Save)
    return msgBox.exec_()