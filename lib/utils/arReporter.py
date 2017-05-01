#*********************************************************************
# content   = send a bug, feature or support request
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
import time
import shutil
import logging
import webbrowser
from datetime import datetime

from PySide import QtGui, QtCore, QtUiTools

import libLog
import libFunc
import libFileFolder

from arUtil import ArUtil


#**********************
# DEFAULT
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

#************************
# REPORT
#************************
class Report (ArUtil):

    def __init__(self, software=os.getenv('SOFTWARE'), user=os.getenv('username'), filePath='', reason='bug', script= 'other', comment='', error=''):
        self.time       = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        self.software   = software  #maya
        self.user       = user      #arichter
        self.projectId  = projectId #dastierindir
        self.file       = filePath  #project/shot
        self.reason     = reason    #bug
        self.script     = script    #save
        self.comment    = comment   #breaks after save
        self.error      = error     #troubleshot: file input line:234

        REPORTS      = ''
        REPORT_INDEX = 0
        REPORT_DATA  = Report()

        MSG_ERROR    = 'Error Message'
        MSG_COMMENT  = 'Comment'
        SAVE_DIR     = ''

        PATH_IMG     = ''

        self.software = os.environ['SOFTWARE']


    def __call__(self):
        return (\
        ().join([\
        'time:      ', self.time, '\n',\
        'software:  ', self.software, '\n',\
        'user:      ', self.user, '\n', '\n',\
        'projectId: ', self.projectId, '\n', '\n',\
        'file:      ', self.file, '\n', '\n',\
        'reason:    ', self.reason, '\n',\
        'script:    ', self.script, '\n',\
        'comment:   ', self.comment, '\n',\
        'error:     ', self.error, '\n']))


    #**********************
    # PRESS_TRIGGER
    #**********************
    def press_btnAccept(self):
        saveReport()
        WIDGET.close()

    def press_btnShowReport(self):
        if (WIDGET.edtComment.isReadOnly()):
            WIDGET.edtComment.setReadOnly(False)
            WIDGET.edtScript.setReadOnly(False)
            WIDGET.edtErrorMsg.setReadOnly(False)

            WIDGET.btnAccept.show()
            WIDGET.btnCancel.show()
            WIDGET.btnScreenshot.show()
            WIDGET.btnSnapshotRender.show()
            WIDGET.btnSnapshotViewport.show()

            WIDGET.btnBefore.hide()
            WIDGET.btnNext.hide()
            WIDGET.btnSaveToHistory.hide()
            WIDGET.btnFolder.hide()
            WIDGET.btnOpenFile.hide()

            WIDGET.cbxReport.clear()
            WIDGET.cbxScript.clear()

            init()
            WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(''))))

        else:
            WIDGET.edtComment.setReadOnly(True)
            WIDGET.edtScript.setReadOnly(True)
            WIDGET.edtErrorMsg.setReadOnly(True)

            WIDGET.btnAccept.hide()
            WIDGET.btnCancel.hide()
            WIDGET.btnScreenshot.hide()
            WIDGET.btnSnapshotRender.hide()
            WIDGET.btnSnapshotViewport.hide()

            WIDGET.btnBefore.show()
            WIDGET.btnNext.show()
            WIDGET.btnSaveToHistory.show()
            WIDGET.btnFolder.show()
            WIDGET.btnOpenFile.show()

            REPORTS = libFileService.getFolderList(s.PATH['data_report'], '*.json')

            setReports(len(REPORTS) - 1)

    def press_btnBeforeReport(self):
        setReports(-1)

    def press_btnNextReport(self):
        setReports(1)

    def press_btnToHistory(self):
        if(len(REPORTS) < 1):
            return

        src = DATA.PATH['data_report'] + '/' + REPORTS[REPORT_INDEX] + DATA.FILE_FORMAT['data']
        dst = DATA.PATH['data_report_history'] + '/' + REPORTS[REPORT_INDEX] + DATA.FILE_FORMAT['data']
        libFunction.createFolder(dst)

        if os.path.exists(src):
            shutil.move(src, dst)

        src = DATA.PATH['data_report_img'] + '/' + REPORTS[REPORT_INDEX] + DATA.FILE_FORMAT['thumbs']
        dst = DATA.PATH['data_report_img'] + '/' + DATA.STATUS['history'] + '/' + REPORTS[REPORT_INDEX] + DATA.FILE_FORMAT['thumbs']
        libFunction.createFolder(dst)

        if not (dst.endswith('000.png')):
            if(os.path.exists(src)):
                shutil.move(src, dst)

        REPORTS = libFileService.getFolderList(s.PATH['data_report'], '*' + DATA.FILE_FORMAT['data'])
        libFunction.setErrorCount(WIDGET)
        setReports(1)
        WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG, True))))

        LOG.info('ReportToHistory : ' + REPORTS[REPORT_INDEX])

    def press_btnOpenFolder(self):
        WIDGET.edtMsg.setText(libFunction.openFolder(s.PATH['data_report']))

    def press_btnScreenshot(self):
        libRender.createScreenshot(WIDGET, WIDGET.btnPreviewImg)

    def press_btnSnapshotRender(self):
        libRender.createSnapshotRender(WIDGET, WIDGET.btnPreviewImg)

    def press_btnSnapshotViewport(self):
        libRender.createSnapshotViewport(WIDGET, WIDGET.btnPreviewImg)


    #**********************
    # change_TRIGGER
    #**********************
    def change_report(self):
        currentImgPath = DATA.PATH['img_maya_shelf'] + '/' + 'shelf_' + WIDGET.cbxReport.currentText() + '35.png'

        if(WIDGET.cbxReport.currentText() == DATA.REPORT_LIST['report'][-1]):
            WIDGET.edtErrorMsg.hide()
            WIDGET.btnScreenshot.hide()
            WIDGET.btnPreviewImg.hide()
            WIDGET.lblPreviewImgBG.hide()

            WIDGET.resize(WIDGET.width(), 160 + changeY)

            WIDGET.edtComment.resize(386, 77)

            WIDGET.edtComment.move(10, 50 + changeY)
            WIDGET.edtMsg.move(10, 135 + changeY)

            WIDGET.btnAccept.move(405, 50 + changeY)
            WIDGET.btnCancel.move(405, 100 + changeY)

            WIDGET.btnBefore.move(405, 50 + changeY)
            WIDGET.btnNext.move(455, 50 + changeY)
            WIDGET.btnFolder.move(380, 135 + changeY)
            WIDGET.btnSaveToHistory.move(455, 98 + changeY)

            WIDGET.lblUser.move(405, 135 + changeY)
            WIDGET.btnOpenFile.move(430, 135 + changeY)
            WIDGET.btnReport.move(455, 135 + changeY)
            WIDGET.lblErrorCount.move(470, 130 + changeY)
            WIDGET.btnHelp.move(480, 135 + changeY)

        else:
            if not(WIDGET.edtComment.isReadOnly()):
                WIDGET.btnScreenshot.show()

            WIDGET.edtErrorMsg.show()
            WIDGET.btnPreviewImg.show()
            WIDGET.lblPreviewImgBG.show()

            WIDGET.resize(WIDGET.width(), 245 + changeY)
            WIDGET.edtComment.resize(486, 77)

            WIDGET.edtComment.move(10, 50 + changeY)
            WIDGET.edtMsg.move(10, 220 + changeY)
            WIDGET.edtErrorMsg.move(10, 138 + changeY)
            WIDGET.btnPreviewImg.move(270, 138 + changeY)
            WIDGET.lblPreviewImgBG.move(270, 138 + changeY)
            WIDGET.btnScreenshot.move(373, 141 + changeY)
            WIDGET.btnSnapshotRender.move(373, 165 + changeY)
            WIDGET.btnSnapshotViewport.move(373, 188 + changeY)

            WIDGET.btnAccept.move(405, 138 + changeY)
            WIDGET.btnCancel.move(405, 184 + changeY)

            WIDGET.btnBefore.move(405, 138 + changeY)
            WIDGET.btnNext.move(455, 138 + changeY)
            WIDGET.btnFolder.move(380, 220 + changeY)
            WIDGET.btnSaveToHistory.move(455, 184 + changeY)

            WIDGET.lblUser.move(405, 220 + changeY)
            WIDGET.btnOpenFile.move(430, 220 + changeY)
            WIDGET.btnReport.move(455, 220 + changeY)
            WIDGET.lblErrorCount.move(470, 215 + changeY)
            WIDGET.btnHelp.move(480, 220 + changeY)

        WIDGET.edtMsg.setText(WIDGET.cbxReport.currentText() + ': ' + WIDGET.cbxScript.currentText())
        WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG))))

    def press_btnErrorImg(self):
        if (WIDGET.edtComment.isReadOnly()):
            os.system(PATH_IMG)
        else:
            PATH_IMG = libMessageBox.folderMsgBox(WIDGET, 'Image Files (*.jpg *.png *.tiff)', 'Choose image file', os.environ['USERPROFILE'] + '/Desktop')
            WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG))))

    def press_btnOpenFile(self):
        try:
            if self.software == 'maya':
                import maya.mel as mel
                mel.eval('file -f -options 'v=0;'  -ignoreVersion  -typ '' + DATA.FILE_FORMAT_CODE[s.FILE_FORMAT[self.software]] + '' -o '' + SAVE_DIR + ''')

            elif self.software == 'nuke':
                import nuke
                nuke.scriptOpen(SAVE_DIR)

            elif self.software == 'houdini':
                print 'houdini open'

            LOG.info ('END  : LOAD : ' + SAVE_DIR)
        except:
            LOG.error('FAIL : LOAD : ' + SAVE_DIR, exc_info=True)


    #**********************
    # FUNCTIONS
    #**********************
    def errorMsg_In(self, event):
        if(WIDGET.edtErrorMsg.toPlainText() == MSG_ERROR):
            WIDGET.edtErrorMsg.setPlainText('')
            WIDGET.edtErrorMsg.setStyleSheet('color: rgb(255, 255, 255);')
        WIDGET.edtErrorMsg.setCursorWidth(1)

    def errorMsg_Out(self, event):
        if(WIDGET.edtErrorMsg.toPlainText() == ''):
            WIDGET.edtErrorMsg.setPlainText(MSG_ERROR)
            WIDGET.edtErrorMsg.setStyleSheet('color: rgb(175, 175, 175);')
        WIDGET.edtErrorMsg.setCursorWidth(0)

    def comment_In(self, event):
        if(WIDGET.edtComment.toPlainText() == MSG_COMMENT):
            WIDGET.edtComment.setPlainText('')
            WIDGET.edtComment.setStyleSheet('color: rgb(255, 255, 255);')
        WIDGET.edtComment.setCursorWidth(1)

    def comment_Out(self, event):
        if(WIDGET.edtComment.toPlainText() == ''):
            WIDGET.edtComment.setPlainText(MSG_COMMENT)
            WIDGET.edtComment.setStyleSheet('color: rgb(175, 175, 175);')
        WIDGET.edtComment.setCursorWidth(0)


    def saveReport(self):

        fileName = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        dataPath = DATA.PATH['data_report'] + '/' + fileName + DATA.FILE_FORMAT['data']
        imgPath  = DATA.PATH['data_report_img'] + '/' + fileName + DATA.FILE_FORMAT['thumbs']

        if(WIDGET.cbxScript.currentText() == 'other'):
            script = WIDGET.edtScript.text()
        else:
            script = WIDGET.cbxScript.currentText()

        if(WIDGET.edtComment.toPlainText() == MSG_COMMENT):
            WIDGET.edtComment.setPlainText('')

        if(WIDGET.edtErrorMsg.toPlainText() == MSG_ERROR):
            WIDGET.edtErrorMsg.setPlainText('')

        try:
            if(self.software == 'maya'):
                import maya.cmds as cmds
                filePath = cmds.file(q=True,sn=True)
            elif(self.software == 'nuke'):
                import nuke
                filePath = nuke.root()['name'].value()
            elif(self.software == 'houdini'):
                print 'houdini save path'
            else:
                filePath = ''
        except:
            LOG.error('FAIL : GET PATH', exc_info=True)

        report = Report(user = os.getenv('username'), filePath = filePath, reason = WIDGET.cbxReport.currentText(), script = script, comment = WIDGET.edtComment.toPlainText(), error = WIDGET.edtErrorMsg.toPlainText(), software = self.software)

        libFileService.setJsonFile(dataPath, report)
        libRender.saveSnapshotImg(imgPath, '', True)
        LOG.info('END : REPORT : ' + fileName)


    def setReports(self, index = len(REPORTS) - 1):

        WIDGET.cbxReport.clear()
        WIDGET.cbxScript.clear()

        if len(REPORTS) < 1:
            press_showReport()
            WIDGET.edtMsg.setText('No Reports at the time')
            WIDGET.edtComment.setPlainText(MSG_COMMENT)
            WIDGET.edtErrorMsg.setPlainText(MSG_ERROR)
            return

        REPORT_INDEX += index

        if (REPORT_INDEX < 0):
            REPORT_INDEX = (len(REPORTS) - 1)
        elif (REPORT_INDEX > ((len(REPORTS) - 1))):
            REPORT_INDEX = 0

        REPORT_DATA = libFileService.getJsonFile(s.PATH['data_report'] + '/' + REPORTS[REPORT_INDEX] + DATA.FILE_FORMAT['data'])

        WIDGET.cbxReport.addItem(REPORT_DATA['reason'])
        WIDGET.cbxScript.addItem(REPORT_DATA['script'])

        WIDGET.edtErrorMsg.setPlainText(REPORT_DATA['error'])
        WIDGET.edtComment.setPlainText(REPORT_DATA['comment'])

        WIDGET.edtMsg.setText(str(REPORT_INDEX) + ':' + str((len(REPORTS) - 1)) + ' - ' + REPORT_DATA['time'])
        libImage.setUserImg(REPORT_DATA['user'], WIDGET.lblUser)

        # change errorImg
        PATH_IMG = DATA.PATH['data_report_img'] + '/' + REPORTS[REPORT_INDEX] + DATA.FILE_FORMAT['thumbs']

        WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG, True))))
        WIDGET.btnOpenFile.setIcon(QPixmap(QImage(libImage.getProgramImg(REPORT_DATA['software']))))

        if(REPORT_DATA['file'] == ''):
            WIDGET.btnOpenFile.setEnabled(False)
            WIDGET.btnOpenFile.setToolTip('Status Report [R]')
        else:
            WIDGET.btnOpenFile.setEnabled(True)
            WIDGET.btnOpenFile.setToolTip(REPORT_DATA['file'])
            SAVE_DIR = REPORT_DATA['file']


    #**********************
    # INIT
    #**********************
    def init(self, currentScript = 'other'):

        libImage.setUserImg(os.getenv('username'), WIDGET.lblUser)

        if os.getenv('username') in DATA.TEAM['admin']: # RIGHTS
            libFunction.setErrorCount(WIDGET)
        else:
            WIDGET.btnReport.hide()
            WIDGET.btnFolder.hide()
            WIDGET.lblErrorCount.hide()

        WIDGET.cbxReport.addItems(s.REPORT_LIST['report'])

        try:
            WIDGET.cbxScript.addItems(s.REPORT_LIST[self.software])
        except:
            WIDGET.cbxScript.addItems(s.REPORT_LIST['other'])   # SCRIPTS CONFIG

        WIDGET.edtComment.setPlainText(MSG_COMMENT)
        WIDGET.edtErrorMsg.setPlainText(MSG_ERROR)

        tmpIndex = WIDGET.cbxScript.findText(currentScript)
        if tmpIndex == -1:
            tmpIndex = WIDGET.cbxScript.findText('other')

        WIDGET.cbxScript.setCurrentIndex(tmpIndex)
        WIDGET.btnPreviewImg.setIcon(QPixmap(QImage(libImage.getReportImg(PATH_IMG))))

        if self.software == 'nuke':
            WIDGET.btnSnapshotViewport.hide()


#**********************
# START UI
#**********************
def start(currentScript = 'other'):
    path_ui  = DATA.PATH['utilities'] + '/ui/' + TITLE + '.ui'
    WIDGET   = QtUiTools.QUiLoader().load(path_ui)
    PATH_IMG = libFunction.rmTempImg()

    # WIDGET.connect(WIDGET.btnAccept, SIGNAL('clicked()'), press_btnAccept)
    WIDGET.connect(WIDGET.btnReport, SIGNAL('clicked()'), press_btnShowReport)

    WIDGET.connect(WIDGET.btnBefore, SIGNAL('clicked()'), press_btnBeforeReport)
    WIDGET.connect(WIDGET.btnNext, SIGNAL('clicked()'), press_btnNextReport)
    WIDGET.connect(WIDGET.btnSaveToHistory, SIGNAL('clicked()'), press_btnToHistory)
    # WIDGET.connect(WIDGET.btnFolder, SIGNAL('clicked()'), press_btnOpenFolder)
    WIDGET.connect(WIDGET.btnOpenFile, SIGNAL('clicked()'), press_btnOpenFile)

    WIDGET.connect(WIDGET.btnScreenshot, SIGNAL('clicked()'), press_btnScreenshot)
    WIDGET.connect(WIDGET.btnSnapshotRender, SIGNAL('clicked()'), press_btnSnapshotRender)
    WIDGET.connect(WIDGET.btnSnapshotViewport, SIGNAL('clicked()'), press_btnSnapshotViewport)
    WIDGET.connect(WIDGET.btnPreviewImg, SIGNAL('clicked()'), press_btnErrorImg)

    WIDGET.connect(WIDGET.cbxReport, SIGNAL('currentIndexChanged(const QString&)'), change_report)
    WIDGET.connect(WIDGET.cbxScript, SIGNAL('currentIndexChanged(const QString&)'), change_report)

    WIDGET.edtErrorMsg.focusInEvent  = errorMsg_In
    WIDGET.edtErrorMsg.focusOutEvent = errorMsg_Out

    WIDGET.edtComment.focusInEvent   = comment_In
    WIDGET.edtComment.focusOutEvent  = comment_Out

    WIDGET.btnBefore.hide()
    WIDGET.btnNext.hide()
    WIDGET.btnSaveToHistory.hide()
    WIDGET.btnFolder.hide()
    WIDGET.btnOpenFile.hide()

    init(currentScript)

    # WIDGET : always on top
    WIDGET.setWindowFlags(Qt.WindowStaysOnTopHint)

    WIDGET.show()
