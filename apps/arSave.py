# content   = saves work and publish files
#             executes other scripts on PUBLISH (on task in file name)
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import re
import sys
import shutil

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import arNotice
import snapshot

import plexfunc
import plex
from arUtil import ArUtil

LOG = plex.log(script=__name__)


class ArSave(ArUtil):
    def __init__(self, parent=None):
        super(ArSave, self).__init__()

        ui_path = f"{os.path.dirname(__file__)}/{__name__}.ui"
        self.wgSave = QtCompat.loadUi(ui_path)

        self.save_file = ''
        self.img_path  = snapshot.DEFAULT_PATH

        self.wgSave.btnVersionUp.clicked.connect(self.update_version)
        self.wgSave.btnVersionDown.clicked.connect(lambda: self.update_version(add=-1))

        self.wgSave.btnPreviewImg.clicked.connect(self.press_btnPreviewImg)
        self.wgSave.btnScreenshot.clicked.connect(self.press_btnScreenshot)
        self.wgSave.btnSnapshotViewport.clicked.connect(self.press_btnSnapshotViewport)
        self.wgSave.btnSnapshotRender.clicked.connect(self.press_btnSnapshotRender)

        self.wgSave.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("lbl/default"))))
        self.wgSave.btnScreenshot.setIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("btn/btn_camera"))))
        self.wgSave.btnSnapshotRender.setIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("btn/btn_viewport"))))
        self.wgSave.btnSnapshotViewport.setIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("btn/btn_render"))))

        self.resize_widget(self.wgSave)

        if not self.set_path():
            self.press_btnOption()
            return

        # self.wgSave : always on top
        # self.wgHeader.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.wgHeader.setWindowTitle(__name__)
        self.wgHeader.setWindowIcon(QtGui.QIcon(plex.get_img_path("btn/btn_save")))

        self.wgHeader.btnOption.setText('SaveAs')
        self.wgSave.btnSnapshotRender.hide()

        if plex.software.is_software('nuke'):
            self.wgSave.btnSnapshotRender.hide()

        self.wgHeader.layMain.addWidget(self.wgSave, 0)

        self.wgSave.show()
        LOG.info('START : arSave')


    # PRESS **************************************************************
    def press_btnAccept(self):
        if self.save_file_path(): self.wgHeader.close()

    def press_btnOption(self):
        # import arSaveAs
        # arSaveAs.start()
        self.wgHeader.close()

    def press_btnPreviewImg(self):
        self.img_path = self.folder_msg_box(self.wgSave, "Image Files (*.jpg *.png *.tif)",
                                            "Choose image file", os.environ['USERPROFILE'] + "/Desktop")
        if self.img_path: self.wgSave.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(self.img_path)))

    def press_btnScreenshot(self):
        snapshot.create_screenshot(self.wgSave, self.wgSave.btnPreviewImg)

    def press_btnSnapshotRender(self):
        snapshot.create_screenshot_render(self.wgSave, self.wgSave.btnPreviewImg)

    def press_btnSnapshotViewport(self):
        snapshot.create_screenshot_viewport(self.wgSave, self.wgSave.btnPreviewImg)

    def press_btnHelp(self, name=''):
        plex.help(__name__)

 
    # FUNCTIONS **************************************************************
    def set_path(self):
        self.save_file = plex.software.scene_path
        if not self.save_file or self.save_file == "Root": return False

        self.save_dir = os.path.dirname(self.save_file)
        self.set_open_folder(self.save_dir)

        self.update_version()

        if self.config['script'][__name__]['just_screenshot']: snapshot.create_screenshot(self.wgSave, self.wgSave.btnPreviewImg)
        else: snapshot.create_any_screenshot(self.wgSave, self.wgSave.btnPreviewImg)

        return True

    def update_version(self, add=1):
        found_version = re.search(plex.config['plex']['version'], os.path.basename(self.save_file))
        if found_version:
            old_version = re.search(r'\d+', found_version.group()).group()
            new_version = int(old_version) + add

            if new_version < 0:
                self.set_comment("CAN'T be smaller than 0")
                return

            new_version = ('{:0%sd}' % len(old_version)).format(new_version)
            new_version = found_version.group().replace(old_version, new_version)
            self.save_file = os.path.dirname(self.save_file) + '/' + os.path.basename(self.save_file).replace(found_version.group(), new_version)
            self.wgSave.edtSaveFile.setText(os.path.basename(self.save_file))
        else:
            self.set_status(f"CAN'T find version: {os.path.basename(self.save_file)}", 3)


    def save_file_path(self):
        # USE ADDITIONAL PUBLISH SCRIPTS
        if self.wgHeader.cbxAdd.isChecked(): self.update_version()
        
        try:
            plex.software.scene_save_as(self.save_file)
            self.set_meta_config()
            LOG.info(f'SAVE : {self.save_file}')
        except:
            LOG.error(f'FAIL : Couldn\'t save file : {self.save_file}', exc_info=True)
            return False

        if self.wgHeader.cbxAdd.isChecked():
            # COPY FILE WITH _PUBLISH
            tmp_copy_work = self.save_file.replace('.', f'_{plex.config['plex']['publish']}.')
            snapshot.save_snapshot(tmp_copy_work)
            self.set_meta_config(tmp_copy_work)

            found_version = re.search(plex.config['plex']['version'], os.path.basename(self.save_file))
            if found_version:
                old_version = re.search(r'\d+', found_version.group()).group()
                self.save_publish_file = self.save_file.split(found_version.group())[0] + '.' + plex.software.extension

            plexfunc.create_dir(os.path.dirname(self.save_publish_file))

            try:
                shutil.copy(self.save_file, tmp_copy_work)
                shutil.copy(tmp_copy_work, self.save_publish_file)
            except:
                LOG.error(f"FAIL : Copying publish file : {self.save_publish_file}", exc_info=True)
                return False

            LOG.info(f"PUBLISH : {self.save_publish_file}")
            snapshot.save_snapshot(self.save_publish_file)
            self.set_meta_config(self.save_publish_file)

        arNotice.ArNotice(title = os.path.basename(self.save_file).split('.')[0],
                          msg   = self.wgSave.edtComment.text(),
                          func  = 'SAVE' if not self.wgHeader.cbxAdd.isChecked() else 'PUBLISH',
                          img   = snapshot.DEFAULT_PATH,
                          img_link = os.path.dirname(self.save_file))

        snapshot.save_snapshot(self.save_file)
        return True


    def set_meta_config(self, save_path=''):
        if not save_path: save_path = self.save_file

        meta_path = os.path.dirname(save_path) + plex.config['plex']['meta']
        # LOG.info(meta_path)
        comment_dict = {'user': getpass.getuser(),
                        'comment': str(self.wgSave.edtComment.text())}
        plex.set_config(meta_path, os.path.basename(save_path), comment_dict)


    def folder_msg_box(self, bpS, configFilter, title = 'Choose file to open', path = ''): #configFilter = "Maya Files (*.mb *.ma)"
        result = QtGui.QFileDialog().getOpenFileName(bpS, title, path, configFilter)
        return str(result[0])



# START **************************************************************
def create():
    app = QtWidgets.QApplication(sys.argv)
    main_widget = ArSave()
    sys.exit(app.exec_())

def start():
    global main_widget
    main_widget = ArSave()
