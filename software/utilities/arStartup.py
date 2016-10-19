#*************************************************************
# CONTENT       startup app
#
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
import sys
import webbrowser

from PySide import QtGui
from PySide import QtCore

# DELETE ******************
sys.path.append("../../settings")
sys.path.append("../../lib")
import setEnv
setEnv.SetEnv()
#**************************
import getProject
DATA = getProject.GetProject()

import libLog
import libImg
import libUser

import setMaya
#import setNuke
#import setHoudini

#**********************
# DEFAULT
TITLE    = os.path.splitext(os.path.basename(__file__))[0]
LOG      = libLog.initLog(script=TITLE)

ICON_IMG = "program/arpipeline"


#**********************
# CLASS
class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        #self.activated.connect(self.showMainWidget)
        self.setIcon(QtGui.QIcon(libImg.getImg(ICON_IMG)))

        self.parent = parent
        menu = QtGui.QMenu()

        menu.setStyleSheet("color: rgb(225, 225, 225);\nbackground-color: rgb(35, 35, 35);\nselection-background-color: rgb(60, 110, 190);")

        menuItem = menu.addAction(QtGui.QIcon(libImg.getImg("user/%s"%libUser.getCurrentUser())), libUser.getCurrentUser())
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.showUserData)
        menu.addSeparator()
        menuItem = menu.addAction(QtGui.QIcon(libImg.getImg("program/maya")), "Maya")
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.openMaya)
        menuItem = menu.addAction(QtGui.QIcon(libImg.getImg("program/nuke")), "Nuke")
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.openNuke)
        menuItem = menu.addAction(QtGui.QIcon(libImg.getImg("program/houdini")), "Houdini")
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.openHoudini)

        if libUser.isUserAdmin():
            menu.addSeparator()
            menuItem = menu.addAction(QtGui.QIcon(libImg.getImg("btn/btnProjectEdit248")), "project log")
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.openProjectLog)
            menuItem = menu.addAction(QtGui.QIcon(libImg.getImg("btn/btnProjectEdit48")), "local log")
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.openLocalLog)
            menu.addSeparator()
            menuItem = menu.addAction(QtGui.QIcon(libImg.getImg("btn/btnFolder48")), "project paths")
            QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.showProjectPaths)

        menu.addSeparator()
        menuItem = menu.addAction(QtGui.QIcon(libImg.getImg("btn/btnDenial48")), "Quit")
        QtCore.QObject.connect(menuItem, QtCore.SIGNAL("triggered()"), self.closeStartup)
        self.setContextMenu(menu)

    def showUserData(self):
        print "showUserData"

    def openMaya(self):
        print "openMaya"
        setMaya.SetMaya()

    def openNuke(self):
        print "openNuke"
        #setNuke.SetNuke()

    def openHoudini(self):
        print "openHoudini"
        #setHoudini.SetHoudini()

    def openProjectLog(self):
        print "openProjectLog"
        webbrowser.open(DATA.PATH["data_log"])

    def openLocalLog(self):
        print "openLocalLog"
        webbrowser.open(DATA.PATH["data_local"])

    def showProjectPaths(self):
        # show as a arReminder
        print DATA.PROJECT_PATH
        print "showProjectPaths"

    def closeStartup(self):
        print "closeStartup"
        self.parent.instance().quit()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    LOG.info("START")


    trayIcon = SystemTrayIcon(app)
    trayIcon.show()
    trayIcon.setToolTip('arPipeline [right click]')
    trayIcon.showMessage('arPipeline', 'Rick Click on Icon for options', QtGui.QSystemTrayIcon.Information , 20000)

    app.exec_()

if __name__ == '__main__':
    main()
