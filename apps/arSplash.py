# content   = splash screen
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import plex

LOG = plex.log(script=__name__)


class ArSplash():
    def __init__(self):
        ui_path = f"{os.path.dirname(__file__)}/{__name__}.ui"
        self.wgSplash = QtCompat.loadUi(ui_path)

        # SKIP splash
        if not plex.config['plex']['splash']: return

        self.wgSplash.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.wgSplash.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # drop shadow effect
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self.wgSplash.fraSplash)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 60))

        self.wgSplash.lblName.setText(plex.context['name'])
        self.wgSplash.lblDescription.setText(plex.context['description'])
        self.wgSplash.lblVersion.setText(plex.context['version'])

        # TIMER
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(10) 
        self.counter = 0

        self.wgSplash.show()
        LOG.debug('START : arSplash')

    def progress(self):
        self.wgSplash.progressBar.setValue(self.counter)

        if self.counter > 100:
            self.timer.stop()
            self.wgSplash.close()

        self.counter += 1
