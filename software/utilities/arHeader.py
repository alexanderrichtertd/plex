#*********************************************************************
# content   = parent widget
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
import webbrowser

from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools

from PySide.QtGui import QLabel

# DELETE *************************
sys.path.append("D:/Dropbox/arPipeline/2000/data")
import setEnv
setEnv.SetEnv()
# ********************************

import libLog
import libUser
import libFunc
import libData

TITLE   = os.path.splitext(os.path.basename(__file__))[0]
LOG     = libLog.initLog(script=TITLE)
PATH_UI = ("/").join([os.path.dirname(__file__), "ui", TITLE + ".ui"])

PATH_MENU_UI    = ("/").join([os.path.dirname(__file__), "ui", TITLE + "_menu.ui"])
PATH_PREVIEW_UI = ("/").join([os.path.dirname(__file__), "ui", TITLE + "_preview.ui"])


class ArHeader(object):

    def __init__(self):
        self.wgHeader = QtUiTools.QUiLoader().load(PATH_UI)

        # VAR
        self.default_size = self.wgHeader.size()
        self.monitor_res  = QtGui.QDesktopWidget().screenGeometry()
        self.monitor_size = QtCore.QSize(self.monitor_res.width(), self.monitor_res.height())

        self.open_path    = ""
        self.config_data  = libData.getData()

        #********************
        # UI
        self.wgHeader.lblProjectName.setText(TITLE)
        self.wgHeader.setWindowIcon(QtGui.QPixmap(QtGui.QImage(libData.getImgPath("btn/btnProject48"))))

        # BUTTONS ICONS
        # + toolTips
        self.wgHeader.btnReport.setIcon(QtGui.QPixmap(QtGui.QImage(libData.getImgPath("btn/btnReport48"))))
        self.wgHeader.btnHelp.setIcon(QtGui.QPixmap(QtGui.QImage(libData.getImgPath("btn/btnHelp48"))))
        self.wgHeader.btnOpenFolder.setIcon(QtGui.QPixmap(QtGui.QImage(libData.getImgPath("btn/btnFolder48"))))

        self.wgHeader.lblScriptImg.setPixmap(QtGui.QPixmap(QtGui.QImage(libData.getImgPath("btn/btnProject48"))))
        self.wgHeader.lblArrowUp.setPixmap(QtGui.QPixmap(QtGui.QImage(libData.getImgPath("lbl/lblArrowU18"))))

        self.wgHeader.btnUser.setIcon(QtGui.QPixmap(QtGui.QImage(libData.getImgPath("user/Alex")))) # current user
        self.wgHeader.btnUser.setToolTip(("").join([libUser.getCurrentUser(), "\n", libUser.getRights()]))

        # SIGNAL
        clickable(self.wgHeader.wgHeader).connect(self.press_lblTitleBar)

        self.wgHeader.btnMinimize.clicked.connect(self.press_btnMinimize)
        self.wgHeader.btnMaximize.clicked.connect(self.press_btnMaximize)
        self.wgHeader.btnLayoutL.clicked.connect(self.press_btnLayoutL)
        self.wgHeader.btnLayoutR.clicked.connect(self.press_btnLayoutR)
        self.wgHeader.btnClose.clicked.connect(self.press_btnClose)

        self.wgHeader.btnAccept.clicked.connect(self.press_btnAccept)
        self.wgHeader.btnCancel.clicked.connect(self.press_btnCancel)

        self.wgHeader.btnOpenFolder.clicked.connect(self.press_btnOpenFolder)
        self.wgHeader.btnUser.clicked.connect(self.press_btnUser)
        self.wgHeader.btnReport.clicked.connect(self.press_btnReport)
        self.wgHeader.btnHelp.clicked.connect(self.press_btnHelp)

        self.setOpenFolder()
        self.addPreview()
        self.addMenu()

        # rounded edges
        # path = QtGui.QPainterPath()
        # path.addRoundedRect(QtCore.QRectF(self.wgHeader.rect()), 5.0, 5.0)
        # self.wgHeader.setMask(QtGui.QRegion(path.toFillPolygon().toPolygon()))

        self.wgHeader.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint) # | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint |
        self.wgHeader.show()

    def addPreview(self):
        print('preview')
        self.wgPreview = QtUiTools.QUiLoader().load(PATH_PREVIEW_UI)
        self.wgHeader.layMain.addWidget(self.wgPreview, 0, 0)

    def addMenu(self):
        self.wgMenu = QtUiTools.QUiLoader().load(PATH_MENU_UI)
        self.wgHeader.layMain.addWidget(self.wgMenu, 1, 1)

        menu01_img   = ["btn/btnWrite48", "btn/btnArrowRight48", "btn/btnHoneypot48", "btn/btnLog48", "btn/btnInboxE48", "user/default"]
        menu01_items = [self.wgMenu.btnMenu01_item01, self.wgMenu.btnMenu01_item02, self.wgMenu.btnMenu01_item03,
                        self.wgMenu.btnMenu01_item04, self.wgMenu.btnMenu01_item05, self.wgMenu.btnMenu01_item06]

        for index, each_item in enumerate(menu01_items):
            each_item.setIcon(QtGui.QPixmap(QtGui.QImage(libData.getImgPath(menu01_img[index]))))
            # each_item.clicked.connect(lambda: self.press_btnMenu("settings"))

        self.wgMenu.btnMenu01_item01.clicked.connect(lambda: self.press_btnMenu("settings"))
        self.wgMenu.btnMenu01_item02.clicked.connect(lambda: self.press_btnMenu("path"))
        self.wgMenu.btnMenu01_item03.clicked.connect(lambda: self.press_btnMenu("advanced"))
        self.wgMenu.btnMenu01_item04.clicked.connect(lambda: self.press_btnMenu("log"))
        self.wgMenu.btnMenu01_item05.clicked.connect(lambda: self.press_btnMenu("report"))
        self.wgMenu.btnMenu01_item06.clicked.connect(lambda: self.press_btnMenu("user"))

        self.select_menu = {
            "settings" : self.wgMenu.btnMenu01_item01,
            "path"     : self.wgMenu.btnMenu01_item02,
            "advanced" : self.wgMenu.btnMenu01_item03,
            "log"      : self.wgMenu.btnMenu01_item04,
            "report"   : self.wgMenu.btnMenu01_item05,
            "user"     : self.wgMenu.btnMenu01_item06
        }

        # for each_key in self.config_data.keys():
        #     print each_key
            # create menu02_items
            # connect
            #

        #settings_files = libFileFolder.getFileList(libData.getPipelinePath('settings'), fileType='*.yml', extension=True, exclude="*"):


    #**********************
    # PRESS
    def press_btnAccept(self):
        print("Accept")

    def press_btnCancel(self):
        print("Cancel")
        #reload data
        self.setOpenFolder("C:/")

    def press_btnOpenFolder(self):
        print("openfolder")
        webbrowser.open(self.open_path)

    def press_btnUser(self):
        print("user")

    def press_btnReport(self):
        print("report")
        #arReport.start()

    def press_btnHelp(self, name = ""):
        if name:
            name = os.getenv('SOFTWARE')
        if TITLE in self.config_data['project']['LINK']:
            webbrowser.open(self.config_data['project']['LINK'][TITLE])
        else:
            webbrowser.open(self.config_data['project']['LINK'].itervalues().next())

    # MENU
    def press_btnMenu(self, menu_tag):
        tmp_menu = self.select_menu[menu_tag]

        for eachMenu in self.select_menu.values():
            eachMenu.setStyleSheet("")
        tmp_menu.setStyleSheet("background-color: rgb(51, 140, 188);")
        # tmp_menu[2].setPixmap(QtGui.QPixmap(QtGui.QImage(libData.getImgPath("lbl/lblArrowR18"))))

    def press_btnMenuSettings(self):
        print('settings')

    def press_btnMenuPath(self):
        print('path')

    def press_btnMenuAdvanced(self):
        print('advanced')

    def press_btnMenuLog(self):
        print('log')

    def press_btnMenuReport(self):
        print('report')

    def press_btnMenuUser(self):
        print('user')


    # TOP
    def press_lblTitleBar(self):
        print('drag around')

    def press_btnMinimize(self):
        print("minimize")
        self.wgHeader.showMinimized()

    def press_btnMaximize(self):
        print("maximize")
        if self.wgHeader.size() == self.monitor_size:
            self.wgHeader.resize(self.default_size)
            self.wgHeader.move(QtGui.QApplication.desktop().screen().rect().center() - self.wgHeader.rect().center())
        else:
            self.wgHeader.setGeometry(self.monitor_res)

    def press_btnLayoutL(self):
        self.wgHeader.resize(self.monitor_res.width() / 2, (self.monitor_res.height()))
        self.wgHeader.move(0, 0)

    def press_btnLayoutR(self):
        self.wgHeader.resize(self.monitor_res.width() / 2, (self.monitor_res.height()))
        self.wgHeader.move(self.monitor_res.width() / 2, 0)


    def press_btnClose(self):
        print("close")
        self.wgHeader.close()

    #**********************
    # CHANGE
    def change_menuSelection():
        print "change"


    #**********************
    # FUNCTION
    def setStatus(self, msg = "", msg_type = 0):
        # 0 - neutral - blue
        # 1 - done    - green
        # 2 - warning - yellow
        # 3 - failed  - red

        self.wgHeader.edtComment.setText(msg)
        self.wgHeader.lblCommentImg.setPixmap(QtGui.QPixmap(QtGui.QImage(libData.getImgPath(self.config_data['style']['arHeader']['progress_img'][msg_type]))))

        template_css = """QProgressBar::chunk { background: %s; }"""
        css = template_css % self.config_data['style']['arHeader']['progress_color'][msg_type]
        self.wgHeader.prbStatus.setStyleSheet(css)
        self.setProgress(100)

    def setProgress(self, count = 0):
        self.wgHeader.prbStatus.setValue(count)

    def setOpenFolder(self, path = ""):
        if os.path.exists(path):
            # add a path button
            self.wgHeader.btnOpenFolder.setEnabled(True)
            self.open_path = os.path.normpath(path)
            self.wgHeader.edtPath.setText(self.open_path)
        else:
            # delete path button
            self.wgHeader.btnOpenFolder.setEnabled(False)
            LOG.info("PATH doesnt exists: {}".format(path))


def clickable(widget):
    class Filter(QtCore.QObject):
        clicked = QtCore.Signal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        print 'press'
                        return True
                if event.type() == QtCore.QEvent.MouseButtonRelease:
                    print 'release'
            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


#**********************
# START UI
def start():
    app = QtGui.QApplication(sys.argv)
    classVar = ArHeader()

    app.exec_()

start()
