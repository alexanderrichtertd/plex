# content   = OS startup file
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import sys
import getpass
import importlib

from Qt import QtWidgets, QtGui, QtCore

import plexfunc
import plex

LOG = plex.log(script=__name__)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, parent)
        # self.activated.connect(self.showMainWidget)
        self.setIcon(QtGui.QIcon(plex.get_img_path('icons/p_yellow')))
        self.parent = parent

        menu = QtWidgets.QMenu()
        menu.setStyleSheet(plex.config['script'][__name__]['style'])

        # ADMIN UI
        if plex.admin:
            adminMenu = QtWidgets.QMenu('Admin')
            adminMenu.setStyleSheet(plex.config['script'][__name__]['style'])
            menu.addMenu(adminMenu)

            menuItem = adminMenu.addAction(QtGui.QIcon(plex.get_img_path('icons/folder_open')), 'Project Config')
            menuItem.triggered.connect(self.press_btnOpenProjectConfig)

            menuItem = adminMenu.addAction(QtGui.QIcon(plex.get_img_path('icons/app_modify')), 'arSettings')
            menuItem.triggered.connect(self.press_btnConfigApp)

        menu.addSeparator()

        self.project_menu = QtWidgets.QMenu(plex.context['project_name'])
        self.project_menu.setStyleSheet(plex.config['script'][__name__]['style'])
        menu.addMenu(self.project_menu)

        for project in plex.project_names:
            selected_icon = plex.get_img_path('icons/check') if project == plex.context['project_id'] else ''
            menuItem = self.project_menu.addAction(QtGui.QIcon(selected_icon), project)
            menuItem.triggered.connect(self.press_btnChangeProject)

        menu.addSeparator()

        # SUBMENU: software
        subMenu = QtWidgets.QMenu('Software')
        subMenu.setStyleSheet(plex.config['script'][__name__]['style'])
        menu.addMenu(subMenu)

        for soft, soft_func in plex.config['script'][__name__]['SOFTWARE'].items():
            menuItem = subMenu.addAction(QtGui.QIcon(plex.get_img_path('software/default/' + soft)), soft.title())
            menuItem.triggered.connect(eval(soft_func))

        menuItem = menu.addAction(QtGui.QIcon(plex.get_img_path('icons/load_yellow')), 'Load')
        menuItem.triggered.connect(self.press_btnLoad)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(plex.get_img_path('icons/email_yellow')), 'Report')
        menuItem.triggered.connect(self.press_btnReport)

        menuItem = menu.addAction(QtGui.QIcon(plex.get_img_path('icons/help')), 'Help')
        menuItem.triggered.connect(self.press_btnHelp)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(plex.get_img_path('user/default')), plex.user_id)
        menuItem.triggered.connect(self.press_btnShowUserSandbox)

        menuItem = menu.addAction(QtGui.QIcon(plex.get_img_path('icons/cancel')), 'Quit')
        menuItem.triggered.connect(self.press_closeStartup)

        self.setContextMenu(menu)


    # PRESS ***********************************************************
    def press_btnShowUserSandbox(self):
        plexfunc.open_dir(plex.config_project['PATH']['sandbox'] + '/' + getpass.getuser())

    def press_btnLoad(self):
        import arLoad
        importlib.reload(arLoad)
        self.arLoad = arLoad.ArLoad(desktop=True)

    #------------------------------
    def press_btnOpenMaya(self):
        plex.software.start('maya')

    def press_btnOpenNuke(self):
        plex.software.start('nuke')

    def press_btnOpenHoudini(self):
        plex.software.start('houdini')

    def press_btnOpenMax(self):
        plex.software.start('max')

    #------------------------------
    def press_btnOpenProjectConfig(self):
        plexfunc.open_dir(plex.paths['config_project'])
    
    def press_btnConfigApp(self):
        import arSettings
        arSettings.start(plex.config_project['name'])
    
    def press_btnChangeProject(self):
        LOG.debug('Change project')

    #------------------------------
    def press_btnReport(self):
        plex.help('report')

    def press_btnHelp(self):
        plex.help(__name__)

    #------------------------------
    def press_closeStartup(self):
        self.hide()
        self.setVisible(False)
        QtWidgets.QApplication.quit()


# START ***********************************************************
def start():
    app = QtWidgets.QApplication.instance()
    if not app: app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    trayIcon = SystemTrayIcon(app)
    trayIcon.show()
    trayIcon.setToolTip(plex.config_plex['name'] + ' [right click]')
    trayIcon.showMessage(plex.config_plex['name'], '[right click]',
                         QtWidgets.QSystemTrayIcon.Information , 20000)

    app.exec()
