# content   = parent widget
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import sys

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import plexfunc
import plex

LOG = plex.log(script=__name__)


class ArUtil(object):

    def __init__(self):
        ui_path = f"{os.path.dirname(__file__)}/{__name__}.ui"
        self.wgHeader = QtCompat.loadUi(ui_path)

        # IMPORTANT variables
        self.open_path = ""


        self.wgHeader.setWindowIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("icons/app_modify"))))

        # BUTTONS ICONS
        self.wgHeader.btnReport.setIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("icons/email"))))
        self.wgHeader.btnHelp.setIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("icons/help"))))
        self.wgHeader.btnOpenFolder.setIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("icons/folder_open"))))
        self.wgHeader.btnUser.setIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("user/default")))) # current user
        self.wgHeader.btnUser.setToolTip("".join(['<html><head/><body><p><span style=" font-weight:600;">',
                                                   plex.user_id, '</span><br>',
                                                  'Admin' if plex.admin else 'Artist', '<br>[open user sandbox]</p></body></html>']))

        self.wgHeader.btnProject.setIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path('icons/project2')))) # current user
        self.wgHeader.btnProject.setToolTip(plex.context['project_name'] + '\n[open project folder]')

        # SIGNAL
        self.wgHeader.btnAccept.clicked.connect(self.press_btnAccept)
        self.wgHeader.btnAccept.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.wgHeader.btnOpenFolder.clicked.connect(self.press_btnOpenFolder)
        self.wgHeader.btnUser.clicked.connect(self.press_btnUser)
        self.wgHeader.btnProject.clicked.connect(self.press_btnProject)
        self.wgHeader.btnReport.clicked.connect(self.press_btnReport)
        self.wgHeader.btnHelp.clicked.connect(self.press_btnHelp)

        # SHOW announcement from project or (if not existing) plex
        self.wgHeader.lblAnnouncement.setText(plex.announcement)

        # SETUP
        self.wgHeader.setWindowIcon(QtGui.QIcon(plex.get_img_path("icons/program")))
        self.wgHeader.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
        # NEED to show in used app to avoid double popup
        # self.wgHeader.show()


    # PRESS ***************************************************************
    def press_btnAccept(self):
        print('PRESS accept')

    def press_btnOpenFolder(self):
        plexfunc.open_dir(self.open_path)

    def press_btnUser(self):
        plexfunc.open_dir(plex.user_sandbox)

    def press_btnProject(self):
        plexfunc.open_dir(plex.config['project']['PATH']['project'])

    def press_btnReport(self):
        plex.help('report')

    def press_btnHelp(self, name=__name__):
        plex.help(name)


    # FUNCTION ***************************************************************
    def set_progress(self, count=0):
        self.wgHeader.prbStatus.setValue(count)

    def set_announcement(self, comment):
        self.wgHeader.lblAnnouncement.setText(comment)
        LOG.info(comment)

    def resize_widget(self, widget):
        x = widget.frameGeometry().width()
        y = self.wgHeader.frameGeometry().height() + widget.frameGeometry().height() - 40
        self.wgHeader.resize(x, y)
        self.wgHeader.setMinimumSize(x, y)


# START ***************************************************************
def start():
    app = QtWidgets.QApplication(sys.argv)
    util = ArUtil()
    app.exec_()