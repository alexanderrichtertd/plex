# content   = load work and publishes files
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import sys
import pathlib
import webbrowser

import datetime

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import arNotice

import plexfunc
from plex import Plex
import arUtil

import importlib
importlib.reload(arUtil)

LOG = Plex().log(script=__name__)


class ArLoad(arUtil.ArUtil):

    def __init__(self, desktop=False):
        super(ArLoad, self).__init__()

        path_ui = "/".join([os.path.dirname(__file__), __name__ + ".ui"])
        self.wgLoad = QtCompat.loadUi(path_ui)

        self.load_file = ''
        self.task_path = ''
        self.desktop = desktop

        # CLEAR context
        self.wgLoad.lstScene.clear()
        self.wgLoad.cbxTask.clear()
        self.wgLoad.cbxStatus.clear()
        self.wgLoad.lstVersion.clear()

        self.wgLoad.edtComment.setReadOnly(True)

        self.clear_context()

        # SETUP content
        self.software_formats = {y:x for x, y in Plex().config_plex['EXTENSION'].items()}
        self.software_keys    = list(self.software_formats.keys())

        self.wgLoad.btnAssets.clicked.connect(lambda: self.press_btnEntity('assets'))
        self.wgLoad.btnShots.clicked.connect(lambda: self.press_btnEntity('shots'))

        self.wgLoad.cbxTask.currentIndexChanged.connect(self.change_cbxTask)
        self.wgLoad.cbxStatus.currentIndexChanged.connect(self.change_cbxStatus)

        self.wgLoad.lstScene.itemSelectionChanged.connect(self.change_lstScene)
        self.wgLoad.lstScene.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.wgLoad.lstVersion.itemSelectionChanged.connect(self.change_lstVersion)
        self.wgLoad.lstVersion.itemDoubleClicked.connect(self.press_btnAccept)
        self.wgLoad.lstVersion.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.wgLoad.btnPreviewImg.clicked.connect(self.press_btnPreviewImg)
        
        self.wgHeader.layMain.addWidget(self.wgLoad, 0)

        self.wgHeader.setWindowTitle(__name__)
        self.wgHeader.btnAccept.setText('Load')
        self.wgHeader.setWindowIcon(QtGui.QIcon(Plex().get_img_path("icons/load")))

        for status in Plex().config_plex['STATUS'].values():
            self.wgLoad.cbxStatus.addItem(status)

        # SELECT start
        self.press_btnEntity()

        self.resize_widget(self.wgLoad)
        self.wgLoad.show()
        LOG.info('START : ArLoad')


    def clear_context(self):
        self.wgLoad.lblUser.setText('')
        self.wgLoad.lblDate.setText('')
        self.wgLoad.lblFileSize.setText('')
        self.wgLoad.edtComment.setPlainText('')

        self.wgLoad.lblSoftwareIcon.setPixmap(QtGui.QPixmap(QtGui.QImage('')))


    # PRESS **************************************************************
    def press_btnAccept(self):
        if not os.path.exists(self.load_file):
            self.set_status(f"FAILED LOADING : Path doesn't exists: {self.load_file}", msg_type=3)
            return False

        software = self.software_formats[self.extension]
        self.wgHeader.close()

        # OPEN in current software
        if software == Plex().software.name and not self.desktop:
            LOG.info(f'OPEN file: {self.load_file}')
            Plex().software.scene_open(self.load_file)
        # OPEN in OS
        else:
            try:    Plex().software.start(name=software, open_file=self.load_file)
            except: LOG.error('FAILED to open software', exc_info=True)

        note = arNotice.Notice(title = f'LOAD: {os.path.basename(self.load_file).split(".")[0]}',
                               msg   = self.wgLoad.edtComment.toPlainText(),
                               img   = self.meta_img_path if os.path.exists(self.meta_img_path)
                                       else Plex().get_img_path('label/default'),
                               img_link = os.path.dirname(self.load_file))
        arNotice.ArNotice(note)


    def press_btnEntity(self, button_name='assets'):
        self.wgLoad.lstScene.clear()

        if button_name == 'assets':
            self.wgLoad.btnAssets.setStyleSheet("background-color: rgb(80, 80, 80);")
            self.wgLoad.btnShots.setStyleSheet("background-color: rgb(41, 43, 51);")
        else:
            self.wgLoad.btnAssets.setStyleSheet("background-color: rgb(41, 43, 51);")
            self.wgLoad.btnShots.setStyleSheet("background-color: rgb(80, 80, 80);")

        self.entity_path = Plex().config_project['PATH'][button_name]

        for scene in plexfunc.get_sub_dirs(self.entity_path):
            self.wgLoad.lstScene.addItem(scene)
        self.wgLoad.lstScene.setCurrentRow(0)


    def press_btnPreviewImg(self):
        if os.path.exists(self.meta_img_path):
            webbrowser.open(self.meta_img_path)


    # CHANGE *************************************************************
    def change_lstScene(self):
        self.wgLoad.cbxTask.clear()

        self.scene_path = f'{self.entity_path}/{self.wgLoad.lstScene.currentItem().text()}'
        task_names = plexfunc.get_sub_dirs(self.scene_path)

        self.wgLoad.cbxTask.addItems(task_names)
        self.wgLoad.cbxTask.setCurrentIndex(0)


    def change_cbxTask(self):
        self.task_path = f'{self.scene_path}/{self.wgLoad.cbxTask.currentText()}'
        self.wgLoad.cbxStatus.setCurrentIndex(0)

        self.change_cbxStatus()


    def change_cbxStatus(self):
        self.wgLoad.lstVersion.clear()
        self.open_path = f'{self.task_path}/{self.wgLoad.cbxStatus.currentText()}'

        ext = Plex().config_plex['EXTENSION'].values()
        folder = pathlib.Path(self.open_path)
        version_files = sorted(filter(lambda path: path.suffix.replace('.', '') in ext, folder.glob('*')), reverse=True)
        
        for version_file in version_files:
            version_file = os.path.basename(str(version_file))
            self.wgLoad.lstVersion.addItem(version_file)
        self.wgLoad.lstVersion.setCurrentRow(0)


    def change_lstVersion(self):
        self.load_file = f'{self.open_path}/{self.wgLoad.lstVersion.currentItem().text()}'

        self.wgLoad.lblDate.setText(str(datetime.datetime.fromtimestamp(os.path.getmtime(self.load_file))).split(".")[0])
        self.wgLoad.lblFileSize.setText(str("{0:.2f}".format(os.path.getsize(self.load_file)/(1024*1024.0)) + " MB"))

        self.extension = self.wgLoad.lstVersion.currentItem().text().split('.')[-1]

        software_img = Plex().get_img_path(f"software/default/{self.software_formats[self.extension]}")
        self.wgLoad.lblSoftwareIcon.setPixmap(QtGui.QPixmap(QtGui.QImage(software_img)))

        comment = ''
        user_id = 'unknown'

        current_file = self.wgLoad.lstVersion.currentItem().text()
        meta_file_path = Plex().config_project['PATH']['meta']
        self.meta_img_path = f'{meta_file_path}/{os.path.splitext(current_file)[0]}.jpg'

        if os.path.exists(self.meta_img_path):
            self.wgLoad.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(self.meta_img_path)))
        else:
            self.wgLoad.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(Plex().get_img_path("labels/default"))))

        file_config = Plex().config_meta.get(current_file, '')
        if file_config:
            comment = file_config.get('comment')
            user_id = file_config.get('user')

        self.wgLoad.edtComment.setPlainText(comment)
        self.wgLoad.lblUser.setText(user_id)


# START ************************************************************************
def create():
    app = QtWidgets.QApplication(sys.argv)
    main_widget = ArLoad(desktop=True)
    sys.exit(app.exec_())

def start():
    global main_widget
    main_widget = ArLoad()