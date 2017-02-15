#*********************************************************************
# content   = informs project members about changes
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
import time
import shutil
import logging
import schedule
import webbrowser

from threading import Thread
from datetime import datetime

from PySide import QtUiTools
from PySide import QtGui
from PySide import QtCore

# DELETE *************************
sys.path.append('D:/Dropbox/arPipeline/2000/data')
import setEnv
setEnv.SetEnv()
# ********************************

import libLog
import libData
import libFunc
import libFileFolder


#************************
# REPORT
class Reminder():

    to = ['arpipeline', 'project', 'pipeline']

    def __init__(self,
                 title  = 'arReminder Test',
                 msg    = 'This is just a Reminder Test - Dont do it again!',
                 userTo = 'arichter',
                 img    = 'lbl/lblPreview131',
                 link   = 'www.richteralexander.com',
                 timer  = ''):

        self.title      = str(title)   #Pipeline Update
        self.msg        = str(msg)     #New Features for Pipeline
        self.userFrom   = os.getenv('username') #user from
        self.userTo     = userTo  #user to
        self.img        = img     # D:/img.png
        self.link       = link    #path
        self.timer      = timer   #time when reminder is triggert
        self.time       = datetime.now().strftime('%H:%M:%S %Y.%m.%d')

    def __call__(self):
        return (\
        'time:     ' + self.time + '\n' +\
        'active:   ' + str(self.active) + '\n' + '\n' +\
        'userFrom: ' + self.userfrom + '\n' +\
        'userTo:   ' + self.userto + '\n' + '\n' +\
        'title:    ' + self.title + '\n' +\
        'msg:      ' + self.msg + '\n' + '\n' +\
        'img:      ' + self.img + '\n' +\
        'link:     ' + self.link + '\n' +\
        'timer:    ' + self.timer + '\n')


#**********************
# DEFAULT
TITLE   = os.path.splitext(os.path.basename(__file__))[0]
LOG     = libLog.initLog(script=TITLE)
PATH_UI = ('/').join([os.path.dirname(__file__), 'ui', TITLE + '.ui'])

TIME        = ''
LINK        = ''

TOPICS      = ['preview', 'pdf', 'report', 'info', 'pipeline', 'publish']
USER        = ['all', 'core', 'anim']

PATH_IMG    = ''
PATH_FILE   = ''
REMINDER    = ''


class ArReminder():

    def __init__(self, new_reminder):

        self.reminder = QtUiTools.QUiLoader().load(PATH_UI)
        self.new_reminder = new_reminder

        if self.new_reminder:
            self.set_reminder()
        else:
            self.reminder.edtMsg.clear()
            self.reminder.cbxTopic.clear()
            self.reminder.edtTitle.clear()

            self.reminder.edtTitle.setEnabled(True)
            self.reminder.edtMsg.setEnabled(True)

            self.reminder.cbxTopic.addItems(TOPICS)

        self.reminder.btnCancel.clicked.connect(self.press_btnCancel)
        self.reminder.btnPreviewImg.clicked.connect(self.press_btnPreviewImg)

        # WIDGET : delete border & always on top
        self.reminder.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)

        # WIDGET : move to right low corner
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.reminder.move(resolution.width() - self.reminder.width() - 5, resolution.height() - self.reminder.height() - 5)

        self.reminder.setWindowOpacity(0.9)

        # round edges
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.reminder.rect()), 3.0, 3.0)
        self.reminder.setMask(QtGui.QRegion(path.toFillPolygon().toPolygon()))

        self.reminder.show()

    def set_reminder(self):
        self.reminder.edtTitle.setEnabled(False)
        self.reminder.edtMsg.setEnabled(False)

        self.reminder.edtTitle.setText(self.new_reminder.title)
        self.reminder.edtMsg.setPlainText(self.new_reminder.msg)

        self.reminder.lblUserFrom.setPixmap(QtGui.QPixmap(QtGui.QImage(libData.getImgPath('user/' + self.new_reminder.userFrom))))
        self.reminder.lblUserFrom.setToolTip(('').join([self.new_reminder.userFrom, '\n', self.new_reminder.time]))

        self.reminder.edtTitle.setText(self.new_reminder.title)

        self.open_link = self.new_reminder.link
        self.reminder.btnPreviewImg.setToolTip(self.open_link)

        if not os.path.exists(self.new_reminder.img):
          self.new_reminder.img = libData.getImgPath(self.new_reminder.img)
        self.reminder.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(self.new_reminder.img)))


    #**********************
    # PRESS_TRIGGER
    def press_btnAccept(self):
        saveUiReminder()
        LOG.info('CREATE')
        self.reminder.close()

    def press_btnCancel(self):
        self.reminder.close()

    def press_btnPreviewImg(self):
        if self.open_link:
            # ACHIEVEMENT Curious one
            webbrowser.open(self.open_link)

    #**********************
    # FUNCTION
    def saveUiReminder(self):
        fileName = self.reminder.cbxTo.currentText().lower()

        setTimer = self.reminder.edtDate.dateTime().toString('yyyy.MM.dd hh:mm:ss')

        if self.reminder.edtDate.dateTime() == TIME:
            setTimer = ''

        fileName = (fileName,) if not isinstance(fileName, (tuple, list)) else fileName

        for member in fileName:
            reminder = Reminder(title = self.reminder.edtTitle.text(), msg = self.reminder.edtMsg.toPlainText(), userTo = member, topic = self.reminder.cbxTopic.currentText().lower(), link = self.reminder.edtImgLink.text(), timer =  setTimer)
            dataPath = DATA.PATH['data_reminder'] + '/' + member + '/' + TIME.toString('yyyy_MM_dd_hh_mm_ss') + DATA.FILE_FORMAT['data']

            libFunc.createFolder(dataPath)
            libFileService.saveJsonFile(dataPath, reminder)

        LOG.info('CREATE : REMINDER : ' + self.reminder.edtTitle.text() + ' + ' + self.reminder.edtMsg.toPlainText())

    def saveReminder(reminder):
        print 'saveReminder'

        def job(self):
            print 'job'
            self.reminder.show()


#**********************
# START UI
def start(add_reminder = ''):
    app = QtGui.QApplication(sys.argv)
    classVar = ArReminder(add_reminder)

    app.exec_()

start(Reminder())
