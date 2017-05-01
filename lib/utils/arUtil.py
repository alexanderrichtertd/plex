#*********************************************************************
# content   = parent widget
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys
import webbrowser

from PySide import QtGui, QtCore, QtUiTools
from PySide.QtGui import QLabel

import users
import libLog
import libData
import libFileFolder

TITLE   = os.path.splitext(os.path.basename(__file__))[0]
LOG     = libLog.init(script=TITLE)
PATH_UI = ("/").join([os.path.dirname(__file__), "ui", TITLE + ".ui"])

PATH_MENU_UI    = ("/").join([os.path.dirname(__file__), "ui", TITLE + "_menu.ui"])
PATH_PREVIEW_UI = ("/").join([os.path.dirname(__file__), "ui", TITLE + "_preview.ui"])


class ArUtil(object):

    def __init__(self):
        self.wgHeader = QtUiTools.QUiLoader().load(PATH_UI)

        # VAR
        self.default_size = self.wgHeader.size()
        self.monitor_res  = QtGui.QDesktopWidget().screenGeometry()
        self.monitor_size = QtCore.QSize(self.monitor_res.width(), self.monitor_res.height())

        self.open_path    = ""
        self.user = users()

        self.ui()

        #*********************************************************************
        # UI
    def ui(self):
        self.wgHeader.lblProjectName.setText(TITLE)
        self.wgHeader.setWindowIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path("btn/btnProject48"))))

        # BUTTONS ICONS
        # + toolTips
        self.wgHeader.btnReport.setIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path("btn/btnReport48"))))
        self.wgHeader.btnHelp.setIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path("btn/default"))))
        self.wgHeader.btnOpenFolder.setIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path("btn/btnFolder48"))))

        self.wgHeader.lblScriptImg.setPixmap(QtGui.QPixmap(QtGui.QImage(libData.get_img_path("btn/btnProject48"))))
        self.wgHeader.lblArrowUp.setPixmap(QtGui.QPixmap(QtGui.QImage(libData.get_img_path("lbl/lblArrowU18"))))

        self.wgHeader.btnUser.setIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path("user/Alex")))) # current user
        self.wgHeader.btnUser.setToolTip(("").join(['<html><head/><body><p><span style=" font-weight:600;">',
                                                    self.user.name, '</span><br>',
                                                    self.user.rights, '</p></body></html>']))

        self.wgHeader.btnProject.setIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path('program/arPipeline')))) # current user
        self.wgHeader.btnProject.setToolTip(os.environ['PROJECT_NAME'])

        # SIGNAL
        clickable(self.wgHeader.wgHeader).connect(self.press_lblTitleBar)

        self.wgHeader.btnMinimize.clicked.connect(self.press_btnMinimize)
        self.wgHeader.btnMaximize.clicked.connect(self.press_btnMaximize)
        self.wgHeader.btnLayoutL.clicked.connect(self.press_btnLayoutL)
        self.wgHeader.btnLayoutR.clicked.connect(self.press_btnLayoutR)
        self.wgHeader.btnClose.clicked.connect(self.press_btnClose)

        self.wgHeader.btnAccept.clicked.connect(self.press_btnAccept)
        self.wgHeader.btnAccept.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.wgHeader.btnCancel.clicked.connect(self.press_btnCancel)

        self.wgHeader.btnOpenFolder.clicked.connect(self.press_btnOpenFolder)
        self.wgHeader.btnUser.clicked.connect(self.press_btnUser)
        self.wgHeader.btnProject.clicked.connect(self.press_btnProject)
        self.wgHeader.btnReport.clicked.connect(self.press_btnReport)
        self.wgHeader.btnHelp.clicked.connect(self.press_btnHelp)

        # CURSOR STYLE
        self.wgHeader.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        self.wgHeader.wg.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.wgHeader.wgHeader.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.wgHeader.wgHeaderBtn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        # self.wgHeader.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # SETUP
        self.refreshData()
        self.setStatus()
        self.setOpenFolder()
        #self.addPreview()
        #self.addMenu()

        self.wgHeader.wgHeader.hide()
        # self.wgHeader.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint) # | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
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

        self.select_menu = {
            "data"     : self.wgMenu.btnMenu01_item01,
            "path"     : self.wgMenu.btnMenu01_item02,
            "advanced" : self.wgMenu.btnMenu01_item03,
            "log"      : self.wgMenu.btnMenu01_item04,
            "report"   : self.wgMenu.btnMenu01_item05,
            "user"     : self.wgMenu.btnMenu01_item06
        }

        for index, each_item in enumerate(menu01_items):
            print each_item.objectName()
            each_item.setIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path(menu01_img[index]))))
            # each_item.clicked.connect(lambda: self.press_btnMenu("settings"))

        self.wgMenu.btnMenu01_item01.clicked.connect(lambda: self.press_btnMenu("data"))
        self.wgMenu.btnMenu01_item02.clicked.connect(lambda: self.press_btnMenu("path"))
        self.wgMenu.btnMenu01_item03.clicked.connect(lambda: self.press_btnMenu("advanced"))
        self.wgMenu.btnMenu01_item04.clicked.connect(lambda: self.press_btnMenu("log"))
        self.wgMenu.btnMenu01_item05.clicked.connect(lambda: self.press_btnMenu("report"))
        self.wgMenu.btnMenu01_item06.clicked.connect(lambda: self.press_btnMenu("user"))

        menu01_items[0].click()


    #*********************************************************************
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
        libFileFolder.openFolder(libData.getProjectUserPath())

    def press_btnProject(self):
        libFileFolder.openFolder(libData.getProjectPath())

    def press_btnReport(self):
        print("report")
        #arReport.start()

    def press_btnHelp(self, name = ''):
        libFunc.get_help(TITLE)

    # MENU
    def press_btnMenu(self, menu_tag):
        tmp_menu = self.select_menu[menu_tag]

        for eachMenu in self.select_menu.values():
            eachMenu.setStyleSheet('')

        for i in range(self.wgMenu.layMenu02.count()):
            self.wgMenu.layMenu02.itemAt(0).widget().close()
            self.wgMenu.layMenu02.takeAt(0)

        tmp_menu.setStyleSheet("background-color: rgb(51, 140, 188);")

        if menu_tag == 'data':
            self.config_data = libData.get_data()
            for eachKey in self.config_data.keys():
                print eachKey
                addButton = QtGui.QPushButton(eachKey)
                addButton.clicked.connect(lambda: self.press_btnSubMenu(eachKey))
                self.wgMenu.layMenu02.addWidget(addButton)
                print addButton.text()
        try:
            self.wgMenu.layMenu02.itemAt(0).widget().click()
        except:
            pass

    def press_btnSubMenu(self, key):
        print key
        for button_index in range(self.wgMenu.layMenu02.count()):
            btn_tmp  = self.wgMenu.layMenu02.itemAt(button_index).widget()
            btn_font = btn_tmp.font()
            if btn_tmp.text() == key:
                btn_font.setBold(True)
            else:
                btn_font.setBold(False)
            btn_tmp.setFont(btn_font)

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


    #*********************************************************************
    # FUNCTION
    def setStatus(self, msg = '', msg_type = 0):
        # 0 - neutral - blue
        # 1 - done    - green
        # 2 - warning - yellow
        # 3 - failed  - red

        self.wgHeader.edtComment.setText(msg)
        self.wgHeader.lblCommentImg.setPixmap(QtGui.QPixmap(QtGui.QImage(libData.get_img_path(self.config_data['style']['arHeader']['progress_img'][msg_type]))))

        if not msg_type:
            template_css = """QProgressBar::chunk { background: %s; }"""
            css = template_css % self.config_data['style']['arHeader']['progress_color'][msg_type]
            self.wgHeader.prbStatus.setStyleSheet(css)
            self.setProgress(100)

    def setProgress(self, count = 0):
        self.wgHeader.prbStatus.setValue(count)

    def setOpenFolder(self, path = ""):
        if os.path.exists(path):
            # active btnOpenFolder
            self.wgHeader.btnOpenFolder.setEnabled(True)
            self.open_path = os.path.normpath(path)
            self.wgHeader.edtPath.setText(self.open_path)
        else:
            # deactive btnOpenFolder
            self.wgHeader.btnOpenFolder.setEnabled(False)
            LOG.info("PATH doesnt exist: {}".format(path))

    def refreshData(self):
        self.config_data = libData.getData()

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
