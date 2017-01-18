#*************************************************************
# CONTENT     	standard message boxes
#*********************************************************************
# content   = standard message boxes
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <contact@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

from PySide import QtGui
from PySide import QtCore

#**********************
# FOLDERSEARCH
def folderMsgBox(bpS, dataFilter, title = "Choose file to open", path = ""): #dataFilter = "Maya Files (*.mb *.ma)"
    global SAVE_TESTIMG_PATH, IMG_PATH

    dialog = QtGui.QFileDialog()
    result = dialog.getOpenFileName(bpS,
                title, path, dataFilter)
    print("RESULT: " + result[0])
    return str(result[0])


#**********************
# QUESTIONS
def questionMsgBox (title = "", header = "", content = "", icon = QtGui.QMessageBox.Warning):
    msgBox = QtGui.QMessageBox()
    msgBox.setWindowTitle(title)
    msgBox.setText(header)
    msgBox.setInformativeText(content)
    msgBox.setIcon(icon)
    msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel)
    msgBox.setDefaultButton(QtGui.QMessageBox.Save)
    return msgBox.exec_()
