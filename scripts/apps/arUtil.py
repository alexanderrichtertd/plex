# content   = parent widget
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import sys

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import plexfunc
from plex import Plex

LOG = Plex().log(script=__name__)


class ArUtil(object):

    def __init__(self):
        path_ui = "/".join([os.path.dirname(__file__), __name__ + ".ui"])
        self.wgHeader = QtCompat.loadUi(path_ui)

        # IMPORTANT variables
        self.open_path = ""


        self.wgHeader.setWindowIcon(QtGui.QPixmap(QtGui.QImage(Plex().get_img_path("icons/app_modify"))))

        # BUTTONS ICONS
        self.wgHeader.btnReport.setIcon(QtGui.QPixmap(QtGui.QImage(Plex().get_img_path("icons/email"))))
        self.wgHeader.btnHelp.setIcon(QtGui.QPixmap(QtGui.QImage(Plex().get_img_path("icons/help"))))
        self.wgHeader.btnOpenFolder.setIcon(QtGui.QPixmap(QtGui.QImage(Plex().get_img_path("icons/folder_open"))))
        self.wgHeader.btnUser.setIcon(QtGui.QPixmap(QtGui.QImage(Plex().get_img_path("user/default")))) # current user
        self.wgHeader.btnUser.setToolTip("".join(['<html><head/><body><p><span style=" font-weight:600;">',
                                                   Plex().user_id, '</span><br>',
                                                  'Admin' if Plex().admin else 'Artist', '<br>[open user sandbox]</p></body></html>']))

        self.wgHeader.btnProject.setIcon(QtGui.QPixmap(QtGui.QImage(Plex().get_img_path('icons/project2')))) # current user
        self.wgHeader.btnProject.setToolTip(Plex().context['project_name'] + '\n[open project folder]')

        # SIGNAL
        self.wgHeader.btnAccept.clicked.connect(self.press_btnAccept)
        self.wgHeader.btnAccept.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.wgHeader.btnOpenFolder.clicked.connect(self.press_btnOpenFolder)
        self.wgHeader.btnUser.clicked.connect(self.press_btnUser)
        self.wgHeader.btnProject.clicked.connect(self.press_btnProject)
        self.wgHeader.btnReport.clicked.connect(self.press_btnReport)
        self.wgHeader.btnHelp.clicked.connect(self.press_btnHelp)

        # SHOW announcement from project or (if not existing) plex
        self.wgHeader.lblAnnouncement.setText(Plex().announcement)

        # SETUP
        self.wgHeader.setWindowIcon(QtGui.QIcon(Plex().get_img_path("icons/program")))
        self.wgHeader.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.wgHeader.show()


    # PRESS ***************************************************************
    def press_btnAccept(self):
        print('PRESS accept')

    def press_btnOpenFolder(self):
        plexfunc.open_dir(self.open_path)

    def press_btnUser(self):
        plexfunc.open_dir(Plex().user_sandbox)

    def press_btnProject(self):
        plexfunc.open_dir(Plex().config_project['PATH']['project'])

    def press_btnReport(self):
        Plex().help('report')

    def press_btnHelp(self, name=__name__):
        Plex().help(name)


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