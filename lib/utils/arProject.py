#*********************************************************************
# content   = setup project and user settings
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

import os
import sys

from PySide import QtGui, QtCore, QtUiTools

import libLog
from arUtils import ArUtils

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

THIS_DIR = ("/").join([os.path.dirname(__file__), "ui"])
PATH_UI  = ("/").join([THIS_DIR, TITLE + ".ui"])


class ArProject(ArUtils):

    def __init__(self, initProject, openMenu):
        super(ArProject, self).__init__()
        self.widget      = QtUiTools.QUiLoader().load(PATH_UI)
        self.initProject = initProject
        self.openMenu    = openMenu
        self.helpTitle   = TITLE
        self.wgAddition  = ""

        self.wgHeader.lblScriptName.setText(TITLE)
        self.mainWidgetHeight = self.widget.height() + self.wgHeader.height() - 80

        self.wgContent = {
            "settings"  : QtUiTools.QUiLoader().load(("/").join([THIS_DIR, TITLE, TITLE + "_settings.ui"])),
            "paths"     : QtUiTools.QUiLoader().load(("/").join([THIS_DIR, TITLE, TITLE + "_paths.ui"])),

            "advanced"  : QtUiTools.QUiLoader().load(("/").join([THIS_DIR, TITLE, TITLE + "_advanced.ui"])),

            "log"       : QtUiTools.QUiLoader().load(("/").join([THIS_DIR, TITLE, TITLE + "_log.ui"])),
            "reminder"  : QtUiTools.QUiLoader().load(("/").join([THIS_DIR, TITLE, TITLE + "_reminder.ui"])),
            "user"      : QtUiTools.QUiLoader().load(("/").join([THIS_DIR, TITLE, TITLE + "_user.ui"]))
        }

        self.iniUi()
        self.wgHeader.layMain.addWidget(self.widget, 2, 0)
        self.wgHeader.show()

    def iniUi(self):
       print('UI')


    def connectBtn(self):
        print('connect')

    #**********************
    # PRESS_TRIGGER
    def press_btnMenuSettings(self):
        self.showContent("settings")

    def press_btnMenuPaths(self):
        self.showContent("paths")

    def press_btnMenuAdvanced(self):
        self.showContent("advanced")

    def press_btnMenuLog(self):
        self.showContent("log")

    def press_btnReminder(self):
        self.showContent("reminder")

    def press_btnMenuUser(self):
        self.showContent("user")


    # ChangeContent
    def btnContentFolder(self):
        print("btnContentFolder")


    def press_nextWidget(self):
        print "nextWidget"


    #**********************
    # FUNCTION
    def showContent(self, contentName):
        if self.wgAddition == self.wgContent[contentName]:
            return

        for i in range(self.wgHeader.layMain.count()): self.wgHeader.layMain.itemAt(i).widget().hide()

        # self.wgAddition.font.setBold(False)   # SET BOLD
        if self.wgAddition:
            self.wgAddition.font().setBold(False)
        self.wgAddition = self.wgContent[contentName]
        self.wgAddition.font().setBold(True)

        self.wgHeader.layMain.addWidget(self.wgAddition)


def main(initProject = False, openMenu = -1):
    app = QtGui.QApplication(sys.argv)
    classVar = ArProject(initProject, openMenu)

    app.exec_()
