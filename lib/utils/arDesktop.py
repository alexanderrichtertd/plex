#*********************************************************************
# content   = OS startup file
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

from PySide import QtGui, QtCore

import users
import libLog
import libData
import libFunc
from software import Software

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

#**********************
# CLASS
class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        #self.activated.connect(self.showMainWidget)
        self.setIcon(QtGui.QIcon(libData.get_img_path('program/default')))

        self.parent = parent
        menu = QtGui.QMenu()
        self.user = users.User()

        self.config_data = libData.get_data()
        menu.setStyleSheet(self.config_data['style']['arDesktop']['menu'])

        # ADMIN UI
        if self.user.is_admin:
            adminMenu = QtGui.QMenu('Admin')
            adminMenu.setStyleSheet(self.config_data['style']['arDesktop']['menu'])
            menu.addMenu(adminMenu)

            menuItem = adminMenu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnLogProjekt48')), 'Project Data')
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnOpenProjectLog)
            menuItem = adminMenu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnLogLocal48')), 'User Data')
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnOpenLocalLog)

            adminMenu.addSeparator()

            menuItem = adminMenu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnProject48')), 'Reminder')
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnWriteReminder)

            menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('user/default')), self.user.name)
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnShowUserData)

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('project/default')), self.config_data['project']['name'])
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnOpenProjectPath)

        menu.addSeparator()

        # menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnProject48')), 'Settings')
        # QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnProject)

        # menu.addSeparator()

        subMenu = QtGui.QMenu('Software')
        subMenu.setStyleSheet(self.config_data['style']['arDesktop']['menu'])
        menu.addMenu(subMenu)

        menuItem = subMenu.addAction(QtGui.QIcon(libData.get_img_path('program/maya')), 'Maya')
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnOpenMaya)
        menuItem = subMenu.addAction(QtGui.QIcon(libData.get_img_path('program/nuke')), 'Nuke')
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnOpenNuke)
        # menuItem = subMenu.addAction(QtGui.QIcon(libData.get_img_path('program/houdini')), 'Houdini')
        # QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnOpenHoudini)

        menu.addSeparator()

        # menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnReport48')), 'Report')
        # QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnReport)
        # self.setContextMenu(menu)
        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnHelp48')), 'Help')
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_btnHelp)
        self.setContextMenu(menu)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnDenial48')), 'Quit')
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL('triggered()'), self.press_closeStartup)
        self.setContextMenu(menu)

        # startarNotificator()

    def startArNotificator(self):
        import arNotificator
        self.reminder = arNotificator.main()


    #**********************
    # PRESS_TRIGGER
    def press_btnShowUserData(self):
        LOG.debug('showUserData')
        webbrowser.open(libData.getEnv('PROJECT_USER_PATH'))

    def press_btnOpenProjectPath(self):
        LOG.debug('openProjectPath')
        webbrowser.open(libData.getEnv('PROJECT_PATH'))
    #------------------------------
    def press_btnProject(self):
        import arProject
        arProject.start()
    #------------------------------
    def press_btnOpenMaya(self):
        LOG.debug('Maya')
        Software('maya').start_software()

    def press_btnOpenNuke(self):
        LOG.debug('Nuke')
        Software('nuke').start_software()


    def press_btnOpenHoudini(self):
        LOG.debug('Houdini')
        Software().start_software()

    #------------------------------
    def press_btnOpenProjectLog(self):
        webbrowser.open(libData.getEnv('DATA_PROJECT_PATH'))

    def press_btnOpenLocalLog(self):
        webbrowser.open(libData.getEnv('DATA_USER_PATH'))

    def press_btnWriteReminder(self):
        LOG.debug('writeReminder')
        from utilities import arNotificator
        arNotificator.main(True)
    #------------------------------
    def press_btnReport(self):
        import arReporter
        arReporter.start(TITLE)

    def press_btnHelp(self):
        libFunc.get_help(TITLE)
    #------------------------------
    def press_closeStartup(self):
        LOG.debug('closeStartup')
        self.parent.instance().quit()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    LOG.debug('START')

    trayIcon = SystemTrayIcon(app)
    trayIcon.show()
    trayIcon.setToolTip(trayIcon.config_data['project']['name'] + ' [right click]') # project name
    trayIcon.showMessage(trayIcon.config_data['project']['name'], 'Rick Click on Icon for options', QtGui.QSystemTrayIcon.Information , 20000) # project name

    app.exec_()
