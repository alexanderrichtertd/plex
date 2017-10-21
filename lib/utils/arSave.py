#*********************************************************************
# content   = saves work and publish files
#             executes other scripts on PUBLISH (on task in file name)
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
import re
import sys
import shutil

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import libLog
import libFunc
import libData
import arNotice
import libSnapshot

from tank import Tank
from users import User
from arUtil import ArUtil

#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#*********************************************************************
# CLASS
class ArSave(ArUtil):
    def __init__(self, parent=None):
        super(ArSave, self).__init__()

        path_ui     = ("/").join([os.path.dirname(__file__), "ui", TITLE + ".ui"])
        self.wgSave = QtCompat.loadUi(path_ui)

        self.save_dir  = os.getenv('PROJECT_PATH')
        self.save_file = ''
        self.comment   = "Comment"
        self.img_path  = libSnapshot.default_tmp_path
        self.software  = Tank().software.software

        self.wgSave.btnVersionUp.clicked.connect(self.update_version)
        self.wgSave.btnVersionDown.clicked.connect(lambda: self.update_version(add=-1))

        self.wgSave.btnPreviewImg.clicked.connect(self.press_btnPreviewImg)
        self.wgSave.btnScreenshot.clicked.connect(self.press_btnScreenshot)
        self.wgSave.btnSnapshotViewport.clicked.connect(self.press_btnSnapshotViewport)
        self.wgSave.btnSnapshotRender.clicked.connect(self.press_btnSnapshotRender)

        self.wgSave.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path("lbl/default"))))
        self.wgSave.btnScreenshot.setIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path("btn/btnCamera48"))))
        self.wgSave.btnSnapshotRender.setIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path("software/maya/shelf/shelf_renderHigh35"))))
        self.wgSave.btnSnapshotViewport.setIcon(QtGui.QPixmap(QtGui.QImage(libData.get_img_path("software/maya/shelf/shelf_viewport35"))))

        self.resize_widget(self.wgSave)

        if not self.set_path():
            self.press_btnOption()
            return

        # self.wgSave : always on top
        # self.wgHeader.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.wgHeader.setWindowTitle(TITLE)
        self.wgHeader.setWindowIcon(QtGui.QIcon(libData.get_img_path("btn/btnSave48")))

        self.wgHeader.btnOption.setText('SaveAs')
        self.wgSave.btnSnapshotRender.hide()
        if self.software == 'nuke': self.wgSave.btnSnapshotRender.hide()

        self.wgHeader.layMain.addWidget(self.wgSave, 0, 0)

        self.wgSave.show()
        LOG.info('START : arSave')


    #********************************************************************
    # PRESS
    def press_btnAccept(self):
        if self.save_file_path(): self.wgHeader.close()

    def press_btnOption(self):
        import arSaveAs
        arSaveAs.start()
        self.wgHeader.close()

    def press_btnPreviewImg(self):
        self.img_path = self.folder_msg_box(self.wgSave, "Image Files (*.jpg *.png *.tif)",
                                            "Choose image file", os.environ['USERPROFILE'] + "/Desktop")
        if self.img_path: self.wgSave.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(self.img_path)))

    def press_btnScreenshot(self):
        libSnapshot.create_screenshot(self.wgSave, self.wgSave.btnPreviewImg)

    def press_btnSnapshotRender(self):
        libSnapshot.create_screenshot_render(self.wgSave, self.wgSave.btnPreviewImg)

    def press_btnSnapshotViewport(self):
        libSnapshot.create_screenshot_viewport(self.wgSave, self.wgSave.btnPreviewImg)

    def press_btnHelp(self, name=''):
        libFunc.get_help(TITLE)


    #*********************************************************************
    # FUNCTIONS
    def set_path(self):
        self.save_file = Tank().software.scene_path
        if not self.save_file or self.save_file == "Root": return False

        self.save_dir = os.path.dirname(self.save_file)
        self.set_open_folder(self.save_dir)

        self.update_version()

        if(self.data['rules']['STATUS']['publish'] in self.save_dir):
            self.save_dir = self.save_dir.replace(self.data['rules']['STATUS']['publish'], self.data['rules']['STATUS']['work'])

        if self.data['script'][TITLE]['just_screenshot']: libSnapshot.create_screenshot(self.wgSave, self.wgSave.btnPreviewImg)
        else: libSnapshot.create_any_screenshot(self.wgSave, self.wgSave.btnPreviewImg)

        return True

    def update_version(self, add=1):
        found_version = re.search(self.data['rules']['FILE']['version'], os.path.basename(self.save_file))
        if found_version:
            old_version = re.search(r'\d+', found_version.group()).group()
            new_version = int(old_version) + add
            if new_version < 0:
                self.set_comment('CANT be smaller than 0')
                return
            new_version = ('{:0%sd}' % len(old_version)).format(new_version)
            new_version = found_version.group().replace(old_version, new_version)
            self.save_file = os.path.dirname(self.save_file) + '/' + os.path.basename(self.save_file).replace(found_version.group(), new_version)
            self.wgSave.edtSaveFile.setText(os.path.basename(self.save_file))
        else:
            self.set_status('CANT find version: {}'.format(os.path.basename(self.save_file)), 3)


    def save_file_path(self):
        # USE ADDITIONAL PUBLISH SCRIPTS
        if self.wgHeader.cbxAdd.isChecked(): self.update_version()

        try:
            Tank().software.scene_saveAs(self.save_file)
            self.set_meta_data()
            LOG.info("SAVE : " + self.save_file)
        except:
            LOG.error("FAIL : Couldnt save file : {}".format(self.save_file), exc_info=True)
            return False

        if self.wgHeader.cbxAdd.isChecked():
            # COPY FILE WITH _PUBLISH
            tmpCopyWork = self.save_file.replace('.', '_{}.'.format(self.data['rules']['STATUS']['publish']))
            libSnapshot.save_snapshot(tmpCopyWork)
            self.set_meta_data(tmpCopyWork)

            found_version = re.search(self.data['rules']['FILE']['version'], os.path.basename(self.save_file))
            if found_version:
                old_version = re.search(r'\d+', found_version.group()).group()
                self.save_publish_file = self.save_file.split(found_version.group())[0] + '.' + Tank().software.extension

            if self.data['rules']['STATUS']['work'] in self.save_file:
                self.save_publish_file = self.save_publish_file.replace(self.data['rules']['STATUS']['work'], self.data['rules']['STATUS']['publish'])
            else:
                LOG.error("FAIL : NO {} in path : {}".format(self.data['rules']['STATUS']['work'], self.save_publish_file), exc_info=True)
                return False

            libFunc.create_folder(os.path.dirname(self.save_publish_file))

            try:
                shutil.copy(self.save_file, tmpCopyWork)
                shutil.copy(tmpCopyWork, self.save_publish_file)
            except:
                LOG.error("FAIL : Copying publish file : {}".format(self.save_publish_file), exc_info=True)
                return False

            LOG.info("PUBLISH : " + self.save_publish_file)
            libSnapshot.save_snapshot(self.save_publish_file)
            self.set_meta_data(self.save_publish_file)

        note = arNotice.Notice(title = os.path.basename(self.save_file).split('.')[0],
                               msg   = self.wgSave.edtComment.text(),
                               user  = User().id,
                               func  = 'SAVE' if not self.wgHeader.cbxAdd.isChecked() else 'PUBLISH',
                               img   = libSnapshot.default_tmp_path,
                               img_link = os.path.dirname(self.save_file))
        arNotice.ArNotice(note)

        libSnapshot.save_snapshot(self.save_file)
        return True

    def set_meta_data(self, save_path=''):
        if not save_path: save_path = self.save_file
        meta_path = os.path.dirname(save_path) + libData.META_INFO
        LOG.info(meta_path)
        comment_dict = {'user':   User().id,
                        'comment': str(self.wgSave.edtComment.text())}
        libData.set_data(meta_path, os.path.basename(save_path), comment_dict)

    def folder_msg_box(self, bpS, dataFilter, title = "Choose file to open", path = ""): #dataFilter = "Maya Files (*.mb *.ma)"
        result = QtGui.QFileDialog().getOpenFileName(bpS, title, path, dataFilter)
        return str(result[0])


def create():
    app = QtWidgets.QApplication(sys.argv)
    main_widget = ArSave()
    sys.exit(app.exec_())

def start():
    global main_widget
    main_widget = ArSave()

# create()
