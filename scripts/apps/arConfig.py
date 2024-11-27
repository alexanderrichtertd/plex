#*********************************************************************
# content   = saves as
#             executes other scripts on PUBLISH (on task in file name)
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys

from Qt import QtWidgets, QtGui, QtCore, QtCompat

from tank import Tank
from arUtil import ArUtil


#*********************************************************************
# VARIABLE
LOG = Tank().log(script=__name__)


#*********************************************************************
# CLASS
class ArConfig(ArUtil):
    def __init__(self, project_name=''):
        super(ArConfig, self).__init__()

        path_ui = "/".join([os.path.dirname(__file__), __name__ + ".ui"])
        self.wgConfig = QtCompat.loadUi(path_ui)

        self.wgHeader.setWindowIcon(QtGui.QIcon(Tank().get_img_path("icons/app_modify")))
        self.wgConfig.btnAddProject.setIcon(QtGui.QIcon(Tank().get_img_path("icons/plus4")))

        self.wgHeader.setWindowTitle(__name__)
        self.wgHeader.btnAccept.setText('Save')
        self.wgHeader.layMain.addWidget(self.wgConfig, 0)
        self.resize_widget(self.wgConfig)

        # self.wgConfig : always on top
        # self.wgConfig.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.wgConfig.cbxProjects.addItems(Tank().project_names)
        # TODO: select project_name

        self.wgConfig.show()
        LOG.info('START : ArConfig')


#*********************************************************************
# START
def start(project_name=''):
    global main_widget
    app = QtWidgets.QApplication(sys.argv)
    main_widget = ArConfig(project_name)
    sys.exit(app.exec_())

