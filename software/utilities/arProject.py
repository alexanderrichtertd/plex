#*************************************************************
__content__   = "settings widget"

__version__   = '0.0.1'
__date__      = "2017-01-01"

__license__   = "MIT"
__copyright__ = "Copyright 2017 Alexander Richter and contributors"
__author__    = "Alexander Richter <contact@richteralexander.com>"
#*************************************************************


import os
import sys

from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools

sys.path.append("..\..\lib")
import libEnv
libEnv.SetEnv()

import libLog

from arHeader import ArHeader

TITLE    = os.path.splitext(os.path.basename(__file__))[0]
LOG      = libLog.initLog(script=TITLE)

THIS_DIR = ("/").join([os.path.dirname(__file__), "ui"])
PATH_UI  = ("/").join([THIS_DIR, TITLE + ".ui"])


class ArProject(ArHeader):

    def __init__(self, initProject, openMenu):
        super(ArProject, self).__init__()
        self.widget      = QtUiTools.QUiLoader().load(PATH_UI)
        self.initProject = initProject
        self.openMenu    = openMenu
        self.helpTitle   = TITLE
        self.wgAddition  = ""

        self.wgHeader.lblProjectName_header.setText(TITLE)
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
        # EXTRA ITEMS for SETUP

        # if userRights == "user":
        #     menu_advanced.hide()

        if self.initProject:
            self.showContent("settings")

            self.widget.btnMenuPaths.setEnabled(False)
            self.widget.btnMenuAdvanced.setEnabled(False)

            self.widget.btnMenuPaths.setStyleSheet("""color: rgb(190, 190, 190);""")
            self.widget.btnMenuAdvanced.setStyleSheet("""color: rgb(190, 190, 190);""")
        else:
            if self.openMenu > -1:
                showContent(self.openMenu)
            else:
                self.showContent("paths")

            self.widget.btnMenuPaths.setEnabled(True)
            self.widget.btnMenuAdvanced.setEnabled(True)

            self.widget.btnMenuPaths.setStyleSheet("")
            self.widget.btnMenuAdvanced.setStyleSheet("")


        self.widget.setWindowIcon(QtGui.QIcon(libImg.getImgPath("btn/btnProject48")))

        self.widget.btnMenuLog.setIcon(QtGui.QPixmap(QtGui.QImage(libImg.getImgPath("btn/btnLog48"))))
        self.widget.btnMenuMessage.setIcon(QtGui.QPixmap(QtGui.QImage(libImg.getImgPath("btn/btnInboxE48"))))
        self.widget.btnMenuUser.setIcon(QtGui.QPixmap(QtGui.QImage(libImg.getImgPath("user/default"))))

        self.wgContent["settings"].lblSoftwareImgMaya_settings.setPixmap(QtGui.QPixmap(QtGui.QImage(libImg.getImgPath("program/maya"))))
        self.wgContent["settings"].lblSoftwareImgHoudini_settings.setPixmap(QtGui.QPixmap(QtGui.QImage(libImg.getImgPath("program/houdini"))))
        self.wgContent["settings"].lblSoftwareImgNuke_settings.setPixmap(QtGui.QPixmap(QtGui.QImage(libImg.getImgPath("program/nuke"))))
        self.wgContent["settings"].btnOpenProjectPath_settings.setIcon(QtGui.QPixmap(QtGui.QImage(libImg.getImgPath("btn/btnFolderSearchGet48"))))

        self.widget.btnArrowLeft_content.setIcon(QtGui.QPixmap(QtGui.QImage(libImg.getImgPath("btn/btnArrowLeft48"))))
        self.widget.btnArrowRight_content.setIcon(QtGui.QPixmap(QtGui.QImage(libImg.getImgPath("btn/btnArrowRight48"))))

        self.widget.btnArrowLeft_content.hide()
        self.widget.btnArrowRight_content.hide()


        self.setComment()
        # USER SETTINGS
        # set user img tooltip - userid
        # set user id

        # self.widget.contentLayout.addWidget(self.wgHeader, 2, 0)

        self.connectBtn()


    def connectBtn(self):
        # self.widget.connect(self.widget.btnMenuOverview, QtCore.SIGNAL('clicked()'), self.press_btnMenuOverview)
        self.widget.connect(self.widget.btnMenuSettings, QtCore.SIGNAL('clicked()'), self.press_btnMenuSettings)
        self.widget.connect(self.widget.btnMenuPaths, QtCore.SIGNAL('clicked()'), self.press_btnMenuPaths)
        self.widget.connect(self.widget.btnMenuAdvanced, QtCore.SIGNAL('clicked()'), self.press_btnMenuAdvanced)

        self.widget.connect(self.widget.btnMenuLog, QtCore.SIGNAL('clicked()'), self.press_btnMenuLog)
        self.widget.connect(self.widget.btnMenuMessage, QtCore.SIGNAL('clicked()'), self.press_btnReminder)
        self.widget.connect(self.widget.btnMenuUser, QtCore.SIGNAL('clicked()'), self.press_btnMenuUser)

        self.widget.connect(self.widget.btnArrowLeft_content, QtCore.SIGNAL('clicked()'), self.press_nextWidget)
        self.widget.connect(self.widget.btnArrowRight_content, QtCore.SIGNAL('clicked()'), self.press_nextWidget)

    #**********************
    # PRESS_TRIGGER
    # def press_btnMenuOverview(self):
    #     self.showContent("overview")

    def press_btnMenuSettings(self):
        self.showContent("settings")


    def press_btnMenuPaths(self):
        self.showContent("paths")
        # self.widget.btnArrowLeft_content.show()
        # self.widget.btnArrowRight_content.show()

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
        # LATER
        # if userRights == "user":
        #     wgChangeContent.hide()


    #**********************
    # FUNCTION
    def showContent(self, contentName):
        if self.wgAddition == self.wgContent[contentName]:
            return

        for i in range(self.widget.layContent.count()): self.widget.layContent.itemAt(i).widget().hide()

        # self.wgAddition.font.setBold(False)   # SET BOLD
        if self.wgAddition:
            self.wgAddition.font().setBold(False)
        self.wgAddition = self.wgContent[contentName]
        self.wgAddition.font().setBold(True)

        self.widget.layContent.addWidget(self.wgAddition)


def start(initProject = False, openMenu = -1):
    app = QtGui.QApplication(sys.argv)
    classVar = ArProject(initProject, openMenu)

    app.exec_()

start()

