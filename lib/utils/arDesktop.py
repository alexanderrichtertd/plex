#*********************************************************************
# content   = OS startup file
# version   = 0.6.0
# date      = 2017-07-07
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

from PySide import QtGui, QtCore

import libLog
import libData
import libFunc
import libFileFolder
from tank import Tank
from software import Software

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

#**********************
# CLASS
class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        # self.activated.connect(self.showMainWidget)
        self.setIcon(QtGui.QIcon(libData.get_img_path('software/default')))

        self.parent = parent

        Tank().init_os()
        self.data = Tank().data
        self.user = Tank().user
        self.project_data = Tank().data['project']

        menu = QtGui.QMenu()
        menu.setStyleSheet(self.data['style'][TITLE]['menu'])

        # ADMIN UI
        if True: # self.user.is_admin:
            adminMenu = QtGui.QMenu('Admin')
            adminMenu.setStyleSheet(self.data['style'][TITLE]['menu'])
            menu.addMenu(adminMenu)

            menuItem = adminMenu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnFolder48')), 'Open Project Data')
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnOpenProjectLog)
            menuItem = adminMenu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnFolder48')), 'Open User Data')
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnOpenLocalLog)

            menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('user/default')), self.user.name)
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnShowUserData)

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('project/default')), self.data['project']['name'])
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnOpenProjectPath)

        subMenu = QtGui.QMenu('Software')
        subMenu.setStyleSheet(self.data['style'][TITLE]['menu'])
        menu.addMenu(subMenu)

        for soft, soft_func in self.data['script'][TITLE]['SOFTWARE'].items():
            menuItem = subMenu.addAction(QtGui.QIcon(libData.get_img_path('software/' + soft)), soft.title())
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), eval(soft_func))

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnFolderSearchGet48')), 'Load')
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnLoad)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnReport48')), 'Report')
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnReport)

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnHelp48')), 'Help')
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnHelp)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnDenial48')), 'Quit')
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_closeStartup)

        self.setContextMenu(menu)


    #**********************
    # PRESS_TRIGGER
    def press_btnShowUserData(self):
        libFileFolder.open_folder(self.project_data['PATH']['user'] + '/' + os.getenv('username'))

    def press_btnOpenProjectPath(self):
        libFileFolder.open_folder(self.project_data['path'])
    #------------------------------
    def press_btnLoad(self):
        import arLoad
        self.arLoad = arLoad.ArLoad()
    #------------------------------
    def press_btnOpenMaya(self):
        Software().start('maya')

    def press_btnOpenNuke(self):
        Software().start('nuke')

    def press_btnOpenHoudini(self):
        Software().start('houdini')

    def press_btnOpenMax(self):
        Software().start('max')
    #------------------------------
    def press_btnOpenProjectLog(self):
        libFileFolder.open_folder(libData.get_env('DATA_PROJECT_PATH'))

    def press_btnOpenLocalLog(self):
        libFileFolder.open_folder(libData.get_env('DATA_USER_PATH'))
    #------------------------------
    def press_btnReport(self):
        libFunc.get_help('issues')

    def press_btnHelp(self):
        libFunc.get_help(TITLE)
    #------------------------------
    def press_closeStartup(self):
        self.parent.instance().quit()


def start():
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    trayIcon = SystemTrayIcon(app)
    trayIcon.show()
    trayIcon.setToolTip(trayIcon.data['project']['name'] + ' [right click]')
    trayIcon.showMessage(trayIcon.data['project']['name'], '[right click]', QtGui.QSystemTrayIcon.Information , 20000)

    app.exec_()

start()
