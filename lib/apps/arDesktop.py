#*********************************************************************
# content   = OS startup file
# version   = 0.6.0
# date      = 2024-11-08
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys
import getpass
import importlib
import webbrowser

from Qt import QtWidgets, QtGui, QtCore

import pipefunc
from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
# CLASS
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, parent)
        # self.activated.connect(self.showMainWidget)
        self.setIcon(QtGui.QIcon(Tank().get_img_path('software/default')))

        self.parent = parent

        Tank().init_os()

        menu = QtWidgets.QMenu()
        menu.setStyleSheet(Tank().data['script'][TITLE]['style'])

        # ADMIN UI
        if True: # Tank().user.is_admin:
            adminMenu = QtWidgets.QMenu('Admin')
            adminMenu.setStyleSheet(Tank().data['script'][TITLE]['style'])
            menu.addMenu(adminMenu)

            menuItem = adminMenu.addAction(QtGui.QIcon(Tank().get_img_path('btn/btn_folder')), 'Open Project Data')
            menuItem.triggered.connect(self.press_btnOpenProjectLog)
            menuItem = adminMenu.addAction(QtGui.QIcon(Tank().get_img_path('btn/btn_folder')), 'Open User Data')
            menuItem.triggered.connect(self.press_btnOpenLocalLog)

            menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(Tank().get_img_path('user/' + Tank().user.id)), Tank().user.id)
        menuItem.triggered.connect(self.press_btnShowUserData)

        menuItem = menu.addAction(QtGui.QIcon(Tank().get_img_path('btn/btn_folder')), Tank().data_project['name'])
        menuItem.triggered.connect(self.press_btnOpenProjectPath)

        menu.addSeparator()

        # SUBMENU: software
        subMenu = QtWidgets.QMenu('Software')
        subMenu.setStyleSheet(Tank().data['script'][TITLE]['style'])
        menu.addMenu(subMenu)

        for soft, soft_func in Tank().data['script'][TITLE]['SOFTWARE'].items():
            menuItem = subMenu.addAction(QtGui.QIcon(Tank().get_img_path('software/' + soft)), soft.title())
            menuItem.triggered.connect(eval(soft_func))

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(Tank().get_img_path('btn/btn_folder_get')), 'Load')
        menuItem.triggered.connect(self.press_btnLoad)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(Tank().get_img_path('btn/btn_report')), 'Report')
        menuItem.triggered.connect(self.press_btnReport)

        menuItem = menu.addAction(QtGui.QIcon(Tank().get_img_path('btn/btn_help')), 'Help')
        menuItem.triggered.connect(self.press_btnHelp)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(Tank().get_img_path('btn/btn_denial')), 'Quit')
        menuItem.triggered.connect(self.press_closeStartup)

        self.setContextMenu(menu)


    #**********************
    # PRESS_TRIGGER
    def press_btnShowUserData(self):
        pipefunc.open_folder(Tank().data_project['PATH']['sandbox'] + '/' + getpass.getuser())

    def press_btnOpenProjectPath(self):
        pipefunc.open_folder(Tank().data_project['path'])

    def press_btnLoad(self):
        import arLoad
        importlib.reload(arLoad)
        self.arLoad = arLoad.ArLoad()
    #------------------------------
    def press_btnOpenMaya(self):
        Tank().software.start('maya')

    def press_btnOpenNuke(self):
        Tank().software.start('nuke')

    def press_btnOpenHoudini(self):
        Tank().software.start('houdini')

    def press_btnOpenMax(self):
        Tank().software.start('max')
    #------------------------------
    def press_btnOpenProjectLog(self):
        pipefunc.open_folder(Tank().get_env('DATA_PROJECT_PATH'))

    def press_btnOpenLocalLog(self):
        pipefunc.open_folder(Tank().get_env('DATA_USER_PATH'))
    #------------------------------
    def press_btnReport(self):
        pipefunc.help('report')

    def press_btnHelp(self):
        pipefunc.help(TITLE)
    #------------------------------
    def press_closeStartup(self):
        self.parent.instance().quit()


def start():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    trayIcon = SystemTrayIcon(app)
    trayIcon.show()
    trayIcon.setToolTip(Tank().data_project['name'] + ' [right click]')
    trayIcon.showMessage(Tank().data_project['name'], '[right click]',
                         QtWidgets.QSystemTrayIcon.Information , 20000)

    app.exec_()
