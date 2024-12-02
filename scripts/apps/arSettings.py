# content   = plex settings
#             executes other scripts on PUBLISH (on task in file name)
# date      = 2024-12-01
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import sys

from Qt import QtWidgets, QtGui, QtCore, QtCompat

from plex import Plex

LOG = Plex().log(script=__name__)


class ArSettings():
    def __init__(self, project_name=''):
        path_ui = "/".join([os.path.dirname(__file__), __name__ + ".ui"])
        self.wgSettings = QtCompat.loadUi(path_ui)

        self.wgSettings.setWindowIcon(QtGui.QPixmap(QtGui.QImage(Plex().get_img_path("icons/app_modify"))))
        self.wgSettings.setWindowTitle(__name__)

        self.wgSettings.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)

        self.wgSettings.edtSearch.returnPressed.connect(self.press_edtSearch)

        # self.wgSettings.lblCancel.clicked.connect(self.press_lblCancel)
        self.wgSettings.lblCancel.linkActivated.connect(self.press_lblCancel)
        QtWidgets.QShortcut(QtCore.Qt.Key_Escape, self.wgSettings, self.press_lblCancel)

        # TODO: select project_name

        self.wgSettings.show()
        LOG.info('START : ArSettings')
    

    # PRESS ***************************************************************     
    def press_lblCancel(self):
        self.wgSettings.close()
        # QtWidgets.QApplication.instance().quit()

    def press_edtSearch(self):
        print('search')


# START ***************************************************************
def create(project_name=''):
    global main_widget
    app = QtWidgets.QApplication(sys.argv)
    main_widget = ArSettings(project_name)
    sys.exit(app.exec_())
    
def start(project_name=''):
    global main_widget
    main_widget = ArSettings(project_name)