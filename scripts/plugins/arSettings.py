# content   = plex settings
#             executes other scripts on PUBLISH (on task in file name)
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import sys

from Qt import QtWidgets, QtGui, QtCore, QtCompat

from QSwitchControl import SwitchControl

import plex

LOG = plex.log(script=__name__)


class ArSettings():
    def __init__(self, project_name=''):
        path_ui = "/".join([os.path.dirname(__file__), __name__ + ".ui"])
        self.wgSettings = QtCompat.loadUi(path_ui)

        self.wgSettings.setWindowIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("icons/app_modify"))))
        self.wgSettings.setWindowTitle(__name__)

        self.wgSettings.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.wgSettings.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.wgSettings.edtSearch.returnPressed.connect(self.press_edtSearch)

        # config
        self.wgSettings.btnPlex.clicked.connect(lambda: self.press_setConfig('plex'))
        self.wgSettings.btnProject.clicked.connect(lambda: self.press_setConfig('project'))
        self.wgSettings.btnScripts.clicked.connect(lambda: self.press_setConfig('scripts'))
        self.wgSettings.btnUser.clicked.connect(lambda: self.press_setConfig('user'))

        # extra
        self.wgSettings.btnPlugins.clicked.connect(self.press_setPlugins)

        self.wgSettings.btnCancel.clicked.connect(self.press_lblCancel)
        # QtWidgets.QShortcut(QtCore.Qt.Key_Escape, self.wgSettings, self.press_lblCancel)

        # TODO: select project_name
        self.wgSettings.layContent.addWidget(SwitchControl(), QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)

        panel = self.wgSettings.centralwidget
        effect = QtWidgets.QGraphicsDropShadowEffect(panel, enabled=False, blurRadius=5)
        panel.setGraphicsEffect(effect)

        self.wgSettings.show()
        LOG.info('START : ArSettings')
    

    # PRESS ***************************************************************     
    def press_setConfig(self, config):
        print(config)

    def press_setPlugins(self):
        print('plugins')
        # TODO include all plugins

    def press_edtSearch(self):
        print('search')

    def press_lblCancel(self):
        self.wgSettings.close()
        # QtWidgets.QApplication.instance().quit()


# START ***************************************************************
def create(project_name=''):
    global main_widget
    app = QtWidgets.QApplication(sys.argv)
    main_widget = ArSettings(project_name)
    sys.exit(app.exec_())
    
def start(project_name=''):
    global main_widget
    main_widget = ArSettings(project_name)