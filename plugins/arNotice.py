# content   = informs artists about changes
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import webbrowser

from threading import Timer
from datetime import datetime

from Qt import QtWidgets, QtGui, QtCore, QtCompat
from Qt.QtCore import QPropertyAnimation, QEasingCurve

import plex

LOG = plex.log(script=__name__)


class ArNotice():
    def __init__(self,
                 title    = 'Notice',
                 msg      = 'This is a note test.',
                 img      = 'labels/default',
                 img_link = 'https://www.alexanderrichtertd.com',
                 duration    = 8):

        # IGNORE arNotice if disabled
        if not plex.config['script']['arNotice']['enable']: return
        
        self.title    = str(title)   # Pipeline Update
        self.msg      = str(msg)     # New Features for Pipeline
        self.img      = img          # lbl/lblPreview131
        self.img_link = img_link     # path
        self.time     = datetime.now().strftime('%H:%M:%S %Y.%m.%d')
        self.duration = duration     # 8 seconds

        ui_path = '/'.join([os.path.dirname(__file__), __name__ + '.ui'])
        self.wgNotice = QtCompat.loadUi(ui_path)

        self.wgNotice.btnPreviewImg.clicked.connect(self.press_btnPreviewImg)

        self.wgNotice.edtTitle.setText(self.title)
        self.wgNotice.edtMsg.setPlainText(self.msg)

        self.wgNotice.edtTitle.setText(self.title)

        self.open_link = self.img_link
        self.wgNotice.btnPreviewImg.setToolTip(self.open_link)

        # if not os.path.exists(self.img): self.img = plex.get_img_path(self.img)
        self.wgNotice.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(self.img)))
        if not self.img_link: self.wgNotice.btnPreviewImg.setEnabled(False)

        # WIDGET : delete border & always on top
        self.wgNotice.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)

        # Store screen dimensions
        self.screen_width, self.screen_height = QtWidgets.QApplication.screens()[0].size().toTuple()
        
        # Position top right corner
        self.final_x = self.screen_width - self.wgNotice.width() - 10
        self.final_y = 50
        
        # Set initial position (outside screen)
        self.wgNotice.move(self.screen_width, self.final_y)
        self.wgNotice.setWindowOpacity(0.95)

        # round edges
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.wgNotice.rect()), 3.0, 3.0)
        self.wgNotice.setMask(QtGui.QRegion(path.toFillPolygon().toPolygon()))

        self.wgNotice.show()
        self.animate_window()
        self.start_duration()

    def animate_window(self):
        # Create animation for x position
        self.anim = QPropertyAnimation(self.wgNotice, b"pos")
        self.anim.setDuration(500)  # Animation duration in milliseconds
        self.anim.setStartValue(QtCore.QPoint(self.screen_width, self.final_y))
        self.anim.setEndValue(QtCore.QPoint(self.final_x, self.final_y))
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()

    def start_duration(self):
        if(self.duration):
            t = Timer(self.duration, self.end_process)
            t.start()

    def end_process(self):
        self.wgNotice.close()

    def press_btnPreviewImg(self):
        if self.img_link:
            webbrowser.open(os.path.realpath(self.img_link))

    def __call__(self):
        LOG.debug('title:    ' + self.title + '\n' +\
                  'msg:      ' + self.msg + '\n' +\
                  'img:      ' + self.img + '\n' +\
                  'img_link: ' + self.img_link
                 )