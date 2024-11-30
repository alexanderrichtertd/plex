#*********************************************************************
# content   = saves as
#             executes other scripts on PUBLISH (on task in file name)
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os
import sys
import getpass
from threading import Thread

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import arNotice
import snapshot
import plexfunc

from plex import Plex
from arUtil import ArUtil


#*********************************************************************
# VARIABLE
LOG = Plex().log(script=__name__)


#*********************************************************************
# CLASS
class ArSaveAs(ArUtil):
    def __init__(self, new_file=True):
        super(ArSaveAs, self).__init__()

        path_ui = "/".join([os.path.dirname(__file__), __name__ + ".ui"])
        self.wgSaveAs = QtCompat.loadUi(path_ui)

        self.all_task = '<all tasks>'

        self.new_file  = new_file
        self.save_file = ''
        self.save_dir  = Plex().config_project['path']
        self.inputs    = [self.wgSaveAs.cbxScene, self.wgSaveAs.cbxSet, self.wgSaveAs.cbxAsset, self.wgSaveAs.cbxTask]

        self.wgHeader.btnOption.hide()
        self.wgHeader.cbxAdd.hide()
        self.wgHeader.setWindowIcon(QtGui.QIcon(Plex().get_img_path("btn/btn_save")))

        btn_title = __name__ if self.new_file else 'Create New Folder'
        self.wgHeader.setWindowTitle(btn_title)
        btn_title = 'Save As' if self.new_file else 'Create'
        self.wgHeader.btnAccept.setText(btn_title)
        self.wgHeader.layMain.addWidget(self.wgSaveAs, 0)
        self.resize_widget(self.wgSaveAs)

        # self.wgSaveAs : always on top
        self.wgSaveAs.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setup()
        self.wgSaveAs.show()
        LOG.info('START : arSaveAs')


    #*********************************************************************
    # SETUP
    def setup(self):
        self.wgSaveAs.cbxScene.clear()
        self.wgSaveAs.cbxSet.clear()
        self.wgSaveAs.cbxAsset.clear()
        self.wgSaveAs.lblStatus.clear()
        self.set_open_folder(self.save_dir)
        self.wgHeader.edtComment.setText('PROJECT PATH: ' + self.save_dir)

        self.wgSaveAs.cbxScene.currentIndexChanged.connect(self.change_cbxScene)
        self.wgSaveAs.cbxTask.currentIndexChanged.connect(self.update_file)
        self.wgSaveAs.cbxAsset.editTextChanged.connect(self.update_file)

        for keys, items in Plex().config_project['SCENES'].items():
            self.wgSaveAs.cbxScene.addItem(keys)

        self.update_file()


    #*********************************************************************
    # PRESS
    def press_btnAccept(self):
        if self.create_folder_structure() and self.new_file:
            self.wgHeader.close()


    #*********************************************************************
    # CHANGE
    def change_cbxScene(self):
        self.wgSaveAs.cbxTask.clear()
        if not self.new_file: self.wgSaveAs.cbxTask.addItem(self.all_task)

        self.scene_steps = len(Plex().config_project['SCENES'][self.wgSaveAs.cbxScene.currentText()].split('/'))
        if self.scene_steps < 5:
            self.wgSaveAs.cbxSet.hide()
            self.wgSaveAs.lblSet.hide()
        else:
            self.wgSaveAs.cbxSet.show()
            self.wgSaveAs.cbxSet.clear()
            self.wgSaveAs.lblSet.show()

        try:
            if self.wgSaveAs.cbxScene.currentText():
                self.wgSaveAs.cbxTask.addItems(Plex().config_project['TASK'][self.wgSaveAs.cbxScene.currentText()])
        except: self.set_status('FAILED adding tasks items: config/projects/$project/project.yml : TASK', msg_type=3)

        if Plex().software.is_software('nuke'):
            index = self.wgSaveAs.cbxTask.findText('COMP', QtCore.Qt.MatchContains)
            if index >= 0: self.wgSaveAs.cbxTask.setCurrentIndex(index)

        try:
            self.save_dir = Plex().config_project['PATH'][self.wgSaveAs.cbxScene.currentText()]
            if self.wgSaveAs.cbxSet.isVisible():
                self.wgSaveAs.cbxSet.addItems(plexfunc.get_files(self.save_dir))
        except: LOG.error('FAILED adding PATH items: config/projects/$project/project.yml : PATH', exc_info=True)


    #*********************************************************************
    # FUNC
    def update_file(self):
        if self.wgSaveAs.cbxScene.currentText():

            if self.new_file: extension = Plex().software.extension
            else: extension = ''

            new_item = Plex().config_project['SCENES'][self.wgSaveAs.cbxScene.currentText()]
            new_item = new_item.format(sequence  = self.wgSaveAs.cbxSet.currentText(),
                                       entity    = self.wgSaveAs.cbxAsset.currentText(),
                                       task      = self.wgSaveAs.cbxTask.currentText(),
                                       version   = Plex().config_pipeline['version'].replace(r'\d','0').replace('_',''),
                                       user      = getpass.getuser()[:2].lower(),
                                       extension = extension,
                                       frame     = Plex().config_project['start_frame'])

            self.save_file = self.save_dir + '/' + new_item



    def create_folder_structure(self):
        # CHECK inputs
        for inputs in self.inputs:
            if not inputs.currentText():
                if self.scene_steps < 5 and self.wgSaveAs.cbxSet == inputs: continue
                self.set_status(f'Missing input: {inputs.objectName().replace("cbx", "")}', msg_type=2)
                return False

        self.update_file()

        # CHECK FILE
        if os.path.exists(self.save_file):
            self.set_status(f'PATH already exists: {self.save_file}', msg_type=2)
            return False

        save_list = []

        if self.all_task in self.save_file:
            for task in Plex().config_project['TASK'][self.wgSaveAs.cbxScene.currentText()]:
                new_path = self.save_file.replace(self.all_task, task)
                save_list.append(new_path)
        else:
            save_list.append(self.save_file)

        LOG.debug(f'Folder list {save_list}')
        for folder in save_list: plexfunc.create_folder(folder)

        if self.new_file:
            Plex().software.scene_save_as(self.save_file, setup_scene=True)
            snapshot.create_any_screenshot(self.wgSaveAs)
            tmp_img_path = snapshot.save_snapshot(self.save_file)

            tmp_title = os.path.basename(self.save_file).split('.')[0]
            tmp_func = 'SAVE AS'

            self.set_meta_config(self.save_file)
        else:
            try:    self.set_open_folder(save_list[0])
            except: LOG.error(f"CAN'T set folder: {save_list}")

            self.set_status(f'Created new {self.wgSaveAs.cbxScene.currentText()}', msg_type=1)

            tmp_img_path = 'lbl/lbl_create'
            tmp_title = self.wgSaveAs.cbxScene.currentText()
            tmp_func = 'CREATE'

        note = arNotice.Notice(title  = tmp_title,
                               msg    = f'CREATED a new {self.wgSaveAs.cbxScene.currentText()} with folders',
                               func   = tmp_func,
                               img    = tmp_img_path,
                               img_link = os.path.dirname(self.save_file))
        arNotice.ArNotice(note)

        return True


    def set_meta_config(self, save_path=''):
        meta_path    = os.path.dirname(save_path) + Plex().config_pipeline['meta']
        comment_dict = {'user': getpass.getuser(),
                        'comment': 'new scene'}
        Plex().set_config(meta_path, os.path.basename(save_path), comment_dict)



#******************************************************************************
# START
def create():
    app = QtWidgets.QApplication(sys.argv)
    main_window = ArSaveAs()
    sys.exit(app.exec_())


def start(new_file=True):
    global main_widget
    main_widget = ArSaveAs(new_file)

# create()
