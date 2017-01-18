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

from threading import Thread
from datetime import datetime

from PySide import QtUiTools
from PySide import QtGui
from PySide import QtCore

import libLog
import libFunc
import libFileFolder


#************************
# REPORT
class Reminder():

    to = ["arpipeline", "project", "pipeline"]

    def __init__(self,
                 title  = "arReminder Test",
                 msg    = "This is just a Reminder Test - Dont do it again!",
                 userTo = "arichter",
                 topic  = "info",
                 link   = " ",
                 timer  = " "):

        self.time       = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        self.title      = str(title)   #Pipeline Update
        self.msg        = str(msg)     #New Features for Pipeline
        self.userfrom   = os.getenv('username') #user from
        self.userto     = userto  #user to
        self.topic      = topic   #PDF
        self.link       = link    #path
        self.timer      = timer   #time when reminder is triggert

    def __call__(self):
        return (\
        "time:     " + self.time + "\n" +\
        "active:   " + str(self.active) + "\n" + "\n" +\
        "userFrom: " + self.userfrom + "\n" +\
        "userTo:   " + self.userto + "\n" + "\n" +\
        "title:    " + self.title + "\n" +\
        "msg:      " + self.msg + "\n" + "\n" +\
        "topic:    " + self.topic + "\n" +\
        "link:     " + self.link + "\n" +\
        "timer:    " + self.timer + "\n")


#**********************
# DEFAULT
TITLE   = os.path.splitext(os.path.basename(__file__))[0]
LOG     = libLog.initLog(script=TITLE)
PATH_UI = DATA.PATH["ui"] + TITLE + ".ui"

TIME        = ""
LINK        = ""
READY       = False

TOPICS      = ["preview", "pdf", "report", "info", "pipeline", "publish"]
USER        = ["all", "core", "anim"]

PATH_IMG    = ""
PATH_FILE   = ""
REMINDER    = ""


class ArRenubder():

    def __init__(self, ui, addReminder):

        self.ui = ui

        if addReminder:
            self.uiedtMsg.clear()
            self.uicbxTopic.clear()
            self.uiedtTitle.clear()

            self.uicbxTopic.addItems(TOPICS)
            self.uicbxTo.addItems(USER)
            self.uicbxTo.addItems(s.TEAM["core"])
            self.uiedtTitle.setEnabled(True)
            self.uiedtMsg.setEnabled(True)
            libFunc.setUserImg(os.getenv('username'), self.uilblUserFrom)

            self.uiedtDate.setDateTime(TIME)

            PATH_FILE = libFileService.getFolderList(s.PATH["data_reminder"] + "/" + os.getenv('username'), "*.json")[0]
            REMINDER  = libFileService.loadJsonFile(s.PATH["data_reminder"] + "/" + os.getenv('username') + "/" + PATH_FILE + DATA.FILE_FORMAT["data"])

            self.uiconnect(self.ui.btnAccept, SIGNAL("clicked()"), press_btnAccept)
            self.uiconnect(self.ui.btnCancel, SIGNAL("clicked()"), press_btnCancel)
            self.uiconnect(self.ui.btnPreviewImg, SIGNAL("clicked()"), press_btnCancel)

            self.uiconnect(self.ui.cbxTo, SIGNAL("currentIndexChanged(const QString&)"), change_cbxTo)
            self.uiconnect(self.ui.cbxTopic, SIGNAL("currentIndexChanged(const QString&)"), change_cbxTopic)

        else:
            self.uicbxTo.hide()
            self.uiedtDate.hide()
            self.uicbxTopic.hide()
            self.uibtnAccept.hide()
            self.uiedtImgLink.hide()
            self.uilblUserTo.hide()

            self.uiedtTitle.setEnabled(False)
            self.uiedtMsg.setEnabled(False)
            self.uilblPreviewImg.mousePressEvent = press_lblPreviewImg

        self.uiconnect(self.ui.btnPreviewImg, SIGNAL("clicked()"), press_btnPreviewImg)

        # WIDGET : delete border & always on top
        self.ui.setWindowFlags(QtGui.Qt.CustomizeWindowHint | QtGui.Qt.WindowStaysOnTopHint | QtGui.Qt.FramelessWindowHint)# | QtGui.Qt.Tool)

        # WIDGET : move to right low corner
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.uimove(resolution.width() - self.uiwidth() - 5, resolution.height() - self.uiheight() - 5)


        self.ui.edtTitle.setText(REMINDER["title"])
        self.ui.edtMsg.setPlainText(REMINDER["msg"])
        self.ui.edtTime.setText(REMINDER["time"])

        libFunc.setUserImg(REMINDER["userfrom"], self.ui.lblUserFrom)
        libFunc.setPreviewImg(REMINDER["topic"], self.ui.lblPreviewImg)

        self.ui.lblPreviewImg.setToolTip(REMINDER["link"])

        # PATH_FILE
        src = ("/").join([DATA.PATH["data_reminder"], os.getenv('username'), PATH_FILE +  DATA.FILE_FORMAT["data"]])
        dst = ("/").join([DATA.PATH["data_reminder"], os.getenv('username'), DATA.STATUS["history"], PATH_FILE + DATA.FILE_FORMAT["data"]])
        # put into history
        libFunc.createFolder(dst)

        if(os.path.exists(src)):
            shutil.move(src, dst)

        # SCHEDULE
        schedule.every(1).minutes.do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)


    #**********************
    # PRESS_TRIGGER
    def press_btnAccept(self):
        saveUiReminder()
        LOG.info("END : CREATE")
        self.ui.close()

    def press_btnCancel(self):
        READY = True
        LOG.info("END : CANCEL")
        self.ui.close()

    def press_btnPreviewImg(self):
        PATH_IMG = PATH_IMG.replace("/", "\\")
        os.system(PATH_IMG)


    #**********************
    # CHANGE_TRIGGER
    def change_cbxTo(self):
        libFunc.setUserImg(self.ui.cbxTo.currentText().lower(), self.ui.lblUserTo)

    def change_cbxTopic(self):
        libFunc.setPreviewImg(self.ui.cbxTopic.currentText().lower(), self.ui.lblPreviewImg)


    #**********************
    # FUNCTION
    def saveUiReminder(self):
        fileName = self.ui.cbxTo.currentText().lower()

        if fileName == "core" or fileName == "all" or fileName == "anim":
            fileName = DATA.TEAM[fileName]

        setTimer = self.ui.edtDate.dateTime().toString("yyyy.MM.dd hh:mm:ss")

        if self.ui.edtDate.dateTime() == TIME:
            setTimer = ""

        fileName = (fileName,) if not isinstance(fileName, (tuple, list)) else fileName

        for member in fileName:
            reminder = Reminder(title = self.ui.edtTitle.text(), msg = self.ui.edtMsg.toPlainText(), userTo = member, topic = self.ui.cbxTopic.currentText().lower(), link = self.ui.edtImgLink.text(), timer =  setTimer)
            dataPath = DATA.PATH["data_reminder"] + '/' + member + '/' + TIME.toString("yyyy_MM_dd_hh_mm_ss") + DATA.FILE_FORMAT["data"]

            libFunc.createFolder(dataPath)
            libFileService.saveJsonFile(dataPath, reminder)

        LOG.info("CREATE : REMINDER : " + self.ui.edtTitle.text() + " + " + self.ui.edtMsg.toPlainText())

    def saveReminder(reminder):
        print "saveReminder"

        def job(self):
            print "job"
            self.ui.show()


    #**********************
    # START PROZESS
def main(addReminder = False):
    # app      = QtGui.QApplication(sys.argv)
    arReminder(QtUiTools.QUiLoader().load(PATH_UI), addReminder)
    # app.exec_()




    # def sleeper():
    #     while True:

    #         if len(libFileService.getFolderList(s.PATH["data_reminder"] + "/" + os.getenv('username'), "*.json")) > 0:
    #             print "START : " + libFileService.getFolderList(s.PATH["data_reminder"] + "/" + os.getenv('username'), "*.json")[0]
    #             start()

    #             print "SLEEPY"

    #             while not READY:
    #                 time.sleep(10000)

    # def reminderLoop():
    #     t = Thread(target=sleeper)
    #     t.start()

    # startReminder()
    # from utilities import arReminder
    # reload(arReminder)
    # arReminder.reminderLoop()

