#*********************************************************************
# content   = informs project members about changes
# version   = 0.1.0
# date      = 2017-09-20
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
import time
import webbrowser

from datetime import datetime
from threading import Timer

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import libLog
import libData
import libFunc


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#*********************************************************************
# NOTICE
class Notice():

    def __init__(self,
                 title    = 'Notice',
                 msg      = 'This is just a Notice Test',
                 user     = os.getenv('username'),
                 img      = 'lbl/default',
                 img_link = 'http://richteralexander.com',
                 func     = '',
                 timer    = int(libData.get_data('script')[TITLE].get('timer', 0))):

        self.title      = str(title)   #Pipeline Update
        self.msg        = str(msg)     #New Features for Pipeline
        self.img        = img         # lbl/lblPreview131
        self.img_link   = img_link    # path
        self.time       = datetime.now().strftime('%H:%M:%S %Y.%m.%d')
        self.user       = user
        self.func       = func
        self.timer      = timer

    def __call__(self):
        LOG.debug(  'time:     ' + self.time + '\n' +\
                    'user:     ' + self.user + '\n\n' +\
                    'func:     ' + self.func + '\n\n' +\
                    'title:    ' + self.title + '\n' +\
                    'msg:      ' + self.msg + '\n' +\
                    'img_link: ' + self.img_link)



#*********************************************************************
# NOTICE UI
class ArNotice():

    def __init__(self, notice):
        ui_path = ('/').join([os.path.dirname(__file__), 'ui', TITLE + '.ui'])
        self.wgNotice = QtCompat.loadUi(ui_path)
        self.notice   = notice

        self.wgNotice.btnCancel.clicked.connect(self.press_btnCancel)
        self.wgNotice.btnPreviewImg.clicked.connect(self.press_btnPreviewImg)

        self.wgNotice.edtTitle.setText(self.notice.title)
        self.wgNotice.edtMsg.setPlainText(self.notice.msg)

        self.wgNotice.btnUser.setIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path('user/' + self.notice.user))))
        self.wgNotice.btnUser.setToolTip(('').join([self.notice.user, '\n', self.notice.time]))
        self.wgNotice.btnUser.clicked.connect(libFunc.get_help)

        self.wgNotice.edtTitle.setText(self.notice.title)

        self.open_link = self.notice.img_link
        self.wgNotice.btnPreviewImg.setToolTip(self.open_link)

        if not os.path.exists(self.notice.img): self.notice.img = libData.get_img_path(self.notice.img)
        self.wgNotice.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(self.notice.img)))
        if self.notice.func: self.wgNotice.lblFunc.setText(self.notice.func)
        else:                self.wgNotice.lblFunc.hide()
        # self.wgNotice.btnCancel.hide()

        # WIDGET : delete border & always on top
        self.wgNotice.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)

        # WIDGET : move to right low corner
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.wgNotice.move(resolution.width() - self.wgNotice.width() - 5, resolution.height() - self.wgNotice.height() - 45)
        self.wgNotice.setWindowOpacity(0.9)

        # round edges
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.wgNotice.rect()), 3.0, 3.0)
        self.wgNotice.setMask(QtGui.QRegion(path.toFillPolygon().toPolygon()))

        self.wgNotice.show()

        self.start_timer()


    def start_timer(self):
        if(self.notice.timer):
            t = Timer(self.notice.timer, self.press_btnCancel)
            t.start()


    #*********************************************************************
    # PRESS_TRIGGER
    def press_btnCancel(self):
        self.wgNotice.close()

    def press_btnPreviewImg(self):
        if self.open_link: webbrowser.open(os.path.realpath(self.open_link))


def create():
    app = QtWidgets.QApplication(sys.argv)
    classVar = ArNotice(Notice())

    app.exec_()

# create()
