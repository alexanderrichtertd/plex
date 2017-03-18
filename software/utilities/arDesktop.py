#*********************************************************************
# content   = OS startup file
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <contact@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys
import webbrowser

from PySide import QtGui
from PySide import QtCore

sys.path.append("D:/Dropbox/arPipeline/2000/data")
import setEnv
setEnv.SetEnv()

import libLog
import libData
import libFunc
import libUser

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.initLog(script=TITLE)

#**********************
# CLASS
class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        #self.activated.connect(self.showMainWidget)
        self.setIcon(QtGui.QIcon(libData.getImgPath("program/arpipeline")))

        self.parent = parent
        menu = QtGui.QMenu()

        self.config_data = libData.getData()
        menu.setStyleSheet(self.config_data['style']['arStartup']['menu'])

        # ADMIN UI
        if libUser.isUserAdmin():
            adminMenu = QtGui.QMenu("Admin")
            adminMenu.setStyleSheet(self.config_data['style']['arStartup']['menu'])
            menu.addMenu(adminMenu)

            menuItem = adminMenu.addAction(QtGui.QIcon(libData.getImgPath("btn/btnLogProjekt48")), "Project Data")
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_btnOpenProjectLog)
            menuItem = adminMenu.addAction(QtGui.QIcon(libData.getImgPath("btn/btnLogLocal48")), "User Data")
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_btnOpenLocalLog)

            adminMenu.addSeparator()

            menuItem = adminMenu.addAction(QtGui.QIcon(libData.getImgPath("btn/btnProject48")), "Reminder")
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_btnWriteReminder)

            menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.getImgPath("user/%s"%libUser.getCurrentUser())), libUser.getCurrentUser())
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_btnShowUserData)

        menuItem = menu.addAction(QtGui.QIcon(libData.getImgPath("project/arPipeline")), self.config_data['project']["PROJECT"]["name"])
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_btnOpenProjectPath)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.getImgPath("btn/btnProject48")), 'Settings')
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_btnProject)

        menu.addSeparator()

        subMenu = QtGui.QMenu("Software")
        subMenu.setStyleSheet(self.config_data['style']['arStartup']['menu'])
        menu.addMenu(subMenu)

        menuItem = subMenu.addAction(QtGui.QIcon(libData.getImgPath("program/maya")), "Maya")
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_btnOpenMaya)
        menuItem = subMenu.addAction(QtGui.QIcon(libData.getImgPath("program/nuke")), "Nuke")
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_btnOpenNuke)
        menuItem = subMenu.addAction(QtGui.QIcon(libData.getImgPath("program/houdini")), "Houdini")
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_btnOpenHoudini)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.getImgPath("btn/btnReport48")), "Report")
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_btnReport)
        self.setContextMenu(menu)
        menuItem = menu.addAction(QtGui.QIcon(libData.getImgPath("btn/btnHelp48")), "Help")
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_btnHelp)
        self.setContextMenu(menu)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.getImgPath("btn/btnDenial48")), "Quit")
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.press_closeStartup)
        self.setContextMenu(menu)

        # startArReminder()

    def startArReminder(self):
        import arReminder
        self.reminder = arReminder.main()


    #**********************
    # PRESS_TRIGGER
    def press_btnShowUserData(self):
        LOG.debug("showUserData")
        webbrowser.open(libData.getEnv('PROJECT_USER_PATH'))

    def press_btnOpenProjectPath(self):
        LOG.debug("openProjectPath")
        webbrowser.open(libData.getEnv('PROJECT_PATH'))
    #------------------------------
    def press_btnProject(self):
        import arProject
        arProject.start()
    #------------------------------
    def press_btnOpenMaya(self):
        LOG.debug("openMaya")
        from settings import setMaya
        setMaya.SetMaya()

    def press_btnOpenNuke(self):
        LOG.debug("openNuke")
        import setNuke
        #setNuke.SetNuke()

    def press_btnOpenHoudini(self):
        LOG.debug("openHoudini")
        import setHoudini
        #setHoudini.SetHoudini()
    #------------------------------
    def press_btnOpenProjectLog(self):
        webbrowser.open(libData.getEnv('DATA_PROJECT_PATH'))

    def press_btnOpenLocalLog(self):
        webbrowser.open(libData.getEnv('DATA_USER_PATH'))

    def press_btnWriteReminder(self):
        LOG.debug("writeReminder")
        from utilities import arReminder
        arReminder.main(True)
    #------------------------------
    def press_btnReport(self):
        import arReport
        arReport.start(TITLE)

    def press_btnHelp(self):
        libFunc.getHelp(TITLE)
    #------------------------------
    def press_closeStartup(self):
        LOG.debug("closeStartup")
        self.parent.instance().quit()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    LOG.debug("START")

    trayIcon = SystemTrayIcon(app)
    trayIcon.show()
    trayIcon.setToolTip(trayIcon.config_data['project']["PROJECT"]["name"] + ' [right click]') # project name
    trayIcon.showMessage(trayIcon.config_data['project']["PROJECT"]["name"], 'Rick Click on Icon for options', QtGui.QSystemTrayIcon.Information , 20000) # project name

    app.exec_()

if __name__ == '__main__':
    main()
