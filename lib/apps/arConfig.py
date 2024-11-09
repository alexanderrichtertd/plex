#*********************************************************************
# content   = saves as
#             executes other scripts on PUBLISH (on task in file name)
# version   = 0.1.0
# date      = 2020-06-19
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys

import datetime
from threading import Thread

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import arNotice

from tank import Tank
from users import User
from arUtil import ArUtil


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
# CLASS
class ArConfig(ArUtil):
    def __init__(self, new_file=True):
        super(ArConfig, self).__init__()

        path_ui = ("/").join([os.path.dirname(__file__), "ui", TITLE + ".ui"])
        self.wgArConfig = QtCompat.loadUi(path_ui)

        self.wgHeader.btnOption.hide()
        self.wgHeader.cbxAdd.hide()
        self.wgHeader.setWindowIcon(QtGui.QIcon(Tank().get_img_path("btn/btnConfig48")))

        self.wgHeader.setWindowTitle(TITLE)
        self.wgHeader.btnAccept.setText('Save')
        self.wgHeader.layMain.addWidget(self.wgArConfig, 0)
        self.resize_widget(self.wgArConfig)

        # self.wgArConfig : always on top
        # self.wgArConfig.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setup()
        self.wgArConfig.show()
        LOG.info('START : ArConfig')

    def setup(self):
        self.set_open_folder(os.getenv('DATA_PROJECT_PATH'))
        print("")


#*********************************************************************
# START
def start():
    global main_widget
    app = QtWidgets.QApplication(sys.argv)
    main_widget = ArConfig()
    sys.exit(app.exec_())

start()
