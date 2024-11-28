#*********************************************************************
# content   = OS startup file
# date      = 2024-11-08
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys
import getpass
import importlib

from Qt import QtWidgets, QtGui, QtCore

import pipefunc
from plex import Plex


#*********************************************************************
# VARIABLE
LOG = Plex().log(script=__name__)


#*********************************************************************
# CLASS
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, parent)
        # self.activated.connect(self.showMainWidget)
        self.setIcon(QtGui.QIcon(Plex().get_img_path('icons/p_yellow')))
        self.parent = parent

        menu = QtWidgets.QMenu()
        menu.setStyleSheet(Plex().config['script'][__name__]['style'])

        # ADMIN UI
        if Plex().admin:
            adminMenu = QtWidgets.QMenu('Admin')
            adminMenu.setStyleSheet(Plex().config['script'][__name__]['style'])
            menu.addMenu(adminMenu)

            menuItem = adminMenu.addAction(QtGui.QIcon(Plex().get_img_path('icons/folder_open')), 'Project Config')
            menuItem.triggered.connect(self.press_btnOpenProjectConfig)

            menuItem = adminMenu.addAction(QtGui.QIcon(Plex().get_img_path('icons/app_modify')), 'arConfig')
            menuItem.triggered.connect(self.press_btnConfigApp)

        menu.addSeparator()

        self.project_menu = QtWidgets.QMenu(Plex().context['project_name'])
        self.project_menu.setStyleSheet(Plex().config['script'][__name__]['style'])
        menu.addMenu(self.project_menu)

        for project in Plex().project_names:
            selected_icon = Plex().get_img_path('icons/check') if project == Plex().context['project_id'] else ''
            menuItem = self.project_menu.addAction(QtGui.QIcon(selected_icon), project)
            menuItem.triggered.connect(self.press_btnChangeProject)

        menu.addSeparator()

        # SUBMENU: software
        subMenu = QtWidgets.QMenu('Software')
        subMenu.setStyleSheet(Plex().config['script'][__name__]['style'])
        menu.addMenu(subMenu)

        for soft, soft_func in Plex().config['script'][__name__]['SOFTWARE'].items():
            menuItem = subMenu.addAction(QtGui.QIcon(Plex().get_img_path('software/default/' + soft)), soft.title())
            menuItem.triggered.connect(eval(soft_func))

        menuItem = menu.addAction(QtGui.QIcon(Plex().get_img_path('icons/load_yellow')), 'Load')
        menuItem.triggered.connect(self.press_btnLoad)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(Plex().get_img_path('icons/email_yellow')), 'Report')
        menuItem.triggered.connect(self.press_btnReport)

        menuItem = menu.addAction(QtGui.QIcon(Plex().get_img_path('icons/help')), 'Help')
        menuItem.triggered.connect(self.press_btnHelp)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(Plex().get_img_path('user/default')), Plex().user_id)
        menuItem.triggered.connect(self.press_btnShowUserSandbox)

        menuItem = menu.addAction(QtGui.QIcon(Plex().get_img_path('icons/cancel')), 'Quit')
        menuItem.triggered.connect(self.press_closeStartup)

        self.setContextMenu(menu)


    #**********************
    # PRESS
    def press_btnShowUserSandbox(self):
        pipefunc.open_folder(Plex().config_project['PATH']['sandbox'] + '/' + getpass.getuser())

    def press_btnLoad(self):
        import arLoad
        importlib.reload(arLoad)
        self.arLoad = arLoad.ArLoad(desktop=True)

    #------------------------------
    def press_btnOpenMaya(self):
        Plex().software.start('maya')

    def press_btnOpenNuke(self):
        Plex().software.start('nuke')

    def press_btnOpenHoudini(self):
        Plex().software.start('houdini')

    def press_btnOpenMax(self):
        Plex().software.start('max')

    #------------------------------
    def press_btnOpenProjectConfig(self):
        pipefunc.open_folder(Plex().paths['config_project'])
    
    def press_btnConfigApp(self):
        import arConfig
        arConfig.start(Plex().config_project['name'])
    
    def press_btnChangeProject(self):
        LOG.debug('Change project')

    #------------------------------
    def press_btnReport(self):
        Plex().report()

    def press_btnHelp(self):
        Plex().help(__name__)

    #------------------------------
    def press_closeStartup(self):
        self.parent.instance().quit()


def start():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    trayIcon = SystemTrayIcon(app)
    trayIcon.show()
    trayIcon.setToolTip(Plex().config_pipeline['name'] + ' [right click]')
    trayIcon.showMessage(Plex().config_pipeline['name'], '[right click]',
                         QtWidgets.QSystemTrayIcon.Information , 20000)

    app.exec_()
