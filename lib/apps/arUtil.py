#*********************************************************************
# content   = parent widget
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys
import webbrowser

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import pipefunc

from tank import Tank


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)


#*********************************************************************
# CLASS
class ArUtil(object):

    def __init__(self):
        path_ui = "/".join([os.path.dirname(__file__), "ui", __name__ + ".ui"])
        self.wgHeader = QtCompat.loadUi(path_ui)

        # VAR
        # self.monitor_res  = QtGui.QDesktopWidget().screenGeometry()
        # self.monitor_size = QtCore.QSize(self.monitor_res.width(), self.monitor_res.height())

        # IMPORTANT variables
        self.open_path = ""


        self.wgHeader.setWindowIcon(QtGui.QPixmap(QtGui.QImage(Tank().get_img_path("icons/app_modify"))))

        # BUTTONS ICONS
        self.wgHeader.btnReport.setIcon(QtGui.QPixmap(QtGui.QImage(Tank().get_img_path("icons/email"))))
        self.wgHeader.btnHelp.setIcon(QtGui.QPixmap(QtGui.QImage(Tank().get_img_path("icons/help"))))
        self.wgHeader.btnOpenFolder.setIcon(QtGui.QPixmap(QtGui.QImage(Tank().get_img_path("icons/folder_open"))))
        self.wgHeader.btnUser.setIcon(QtGui.QPixmap(QtGui.QImage(Tank().get_img_path("user/default")))) # current user
        self.wgHeader.btnUser.setToolTip("".join(['<html><head/><body><p><span style=" font-weight:600;">',
                                                    Tank().user_id, '</span><br>',
                                                    'Admin' if Tank().admin else 'Artist', '<br>[open user sandbox]</p></body></html>']))

        self.wgHeader.btnProject.setIcon(QtGui.QPixmap(QtGui.QImage(Tank().get_img_path('icons/project')))) # current user
        self.wgHeader.btnProject.setToolTip(Tank().plex_context['project_name'] + '\n[open project folder]')

        # SIGNAL
        self.wgHeader.btnAccept.clicked.connect(self.press_btnAccept)
        self.wgHeader.btnAccept.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.wgHeader.btnOpenFolder.clicked.connect(self.press_btnOpenFolder)
        self.wgHeader.btnUser.clicked.connect(self.press_btnUser)
        self.wgHeader.btnProject.clicked.connect(self.press_btnProject)
        self.wgHeader.btnReport.clicked.connect(self.press_btnReport)
        self.wgHeader.btnHelp.clicked.connect(self.press_btnHelp)

        # SETUP
        self.refresh_config()
        self.set_status()
        self.set_open_folder()
        self.wgHeader.setWindowIcon(QtGui.QIcon(Tank().get_img_path("icons/program")))
        #self.add_preview(self.wgHeader.layMain)
        #self.add_menu()

        self.wgHeader.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.wgHeader.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint) # | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.wgHeader.show()


    def add_menu(self):
        path_ui = "/".join([os.path.dirname(__file__), "ui", __name__ + "_menu.ui"])
        self.wgMenu = QtCompat.loadUi(path_ui)
        self.wgHeader.layMain.addWidget(self.wgMenu, 1)

        menu01_img   = ["icons/btn_write", "icons/btn_arrow_right", "icons/btn_honeypot", "icons/btn_log", "icons/btn_inbox_empty", "user/default"]
        menu01_items = [self.wgMenu.btnMenu01_item01, self.wgMenu.btnMenu01_item02, self.wgMenu.btnMenu01_item03,
                        self.wgMenu.btnMenu01_item04, self.wgMenu.btnMenu01_item05, self.wgMenu.btnMenu01_item06]

        self.select_menu = {
            "config"   : self.wgMenu.btnMenu01_item01,
            "path"     : self.wgMenu.btnMenu01_item02,
            "advanced" : self.wgMenu.btnMenu01_item03,
            "log"      : self.wgMenu.btnMenu01_item04,
            "report"   : self.wgMenu.btnMenu01_item05,
            "user"     : self.wgMenu.btnMenu01_item06
        }

        for index, each_item in enumerate(menu01_items):
            each_item.setIcon(QtGui.QPixmap(QtGui.QImage(Tank().get_img_path(menu01_img[index]))))
            # each_item.clicked.connect(lambda: self.press_btnMenu("settings"))

        self.wgMenu.btnMenu01_item01.clicked.connect(lambda: self.press_btnMenu("config"))
        self.wgMenu.btnMenu01_item02.clicked.connect(lambda: self.press_btnMenu("path"))
        self.wgMenu.btnMenu01_item03.clicked.connect(lambda: self.press_btnMenu("advanced"))
        self.wgMenu.btnMenu01_item04.clicked.connect(lambda: self.press_btnMenu("log"))
        self.wgMenu.btnMenu01_item05.clicked.connect(lambda: self.press_btnMenu("report"))
        self.wgMenu.btnMenu01_item06.clicked.connect(lambda: self.press_btnMenu("user"))

        menu01_items[0].click()


    #*********************************************************************
    # PRESS
    def press_btnAccept(self):
        pass

    def press_btnOpenFolder(self):
        pipefunc.open_folder(self.open_path)

    def press_btnUser(self):
        pipefunc.open_folder(Tank().user_sandbox)

    def press_btnProject(self):
        pipefunc.open_folder(Tank().plex_context['project_path'])

    def press_btnReport(self):
        pipefunc.help('report')

    def press_btnHelp(self, name=''):
        pipefunc.help(name)


    #*********************************************************************
    # MENU
    def press_btnMenu(self, menu_tag):
        tmp_menu = self.select_menu[menu_tag]

        for eachMenu in self.select_menu.values():
            eachMenu.setStyleSheet('')

        for count in range(self.wgMenu.layMenu02.count()):
            self.wgMenu.layMenu02.itemAt(0).widget().close()
            self.wgMenu.layMenu02.takeAt(0)

        tmp_menu.setStyleSheet("background-color: rgb(51, 140, 188);")

        if menu_tag == 'config':
            self.config = Tank().config
            for eachKey in self.config.keys():
                addButton = QtGui.QPushButton(eachKey)
                addButton.clicked.connect(lambda: self.press_btnSubMenu(eachKey))
                self.wgMenu.layMenu02.addWidget(addButton)

        try:    self.wgMenu.layMenu02.itemAt(0).widget().click()
        except: pass


    def press_btnSubMenu(self, key):
        for button_index in range(self.wgMenu.layMenu02.count()):
            btn_tmp  = self.wgMenu.layMenu02.itemAt(button_index).widget()
            btn_font = btn_tmp.font()

            if btn_tmp.text() == key: btn_font.setBold(True)
            else: btn_font.setBold(False)

            btn_tmp.setFont(btn_font)


    #*********************************************************************
    # FUNCTION
    def set_status(self, msg = '', msg_type = 0):
        # 0 - neutral - blue
        # 1 - done    - green
        # 2 - warning - yellow
        # 3 - failed  - red

        if msg: self.set_comment(msg)

        if not msg_type:
            template_css = """QProgressBar::chunk { background: %s; }"""
            css = template_css % self.config['script'][__name__]['progress_color'][msg_type]
            self.wgHeader.prbStatus.setStyleSheet(css)
            self.set_progress(100)


    def set_progress(self, count = 0):
        self.wgHeader.prbStatus.setValue(count)


    def set_comment(self, comment):
        self.wgHeader.lblContext.setText(comment)
        LOG.info(comment)


    def set_open_folder(self, path=''):
        if len(path.split('.')) > 1:
            path = os.path.dirname(path)

        if os.path.exists(path):
            self.wgHeader.btnOpenFolder.setEnabled(True)
            self.open_path = os.path.normpath(path)
            self.wgHeader.lblContext.setText(self.open_path)
        else:
            self.wgHeader.lblContext.setText('')
            self.wgHeader.btnOpenFolder.setEnabled(False)


    def refresh_config(self):
        self.config = Tank().config


    def resize_widget(self, widget):
        x = widget.frameGeometry().width()
        y = self.wgHeader.frameGeometry().height() + widget.frameGeometry().height() - 40
        self.wgHeader.resize(x, y)
        self.wgHeader.setMinimumSize(x, y)



#*********************************************************************
# START UI
def start():
    app = QtWidgets.QApplication(sys.argv)
    util = ArUtil()
    app.exec_()

# start()
