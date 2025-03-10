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

import arUtil
import arNotice

import plex
import plexfunc

import importlib
importlib.reload(arUtil)

LOG = plex.log(script=__name__)


class ArLoad(arUtil.ArUtil):

    def __init__(self, desktop: bool = False) -> None:
        super(ArLoad, self).__init__()

        ui_path = f"{os.path.dirname(__file__)}/{__name__}.ui"
        self.wgLoad = QtCompat.loadUi(ui_path)

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
        self.software_formats = {y:x for x, y in plex.config['plex']['EXTENSION'].items()}
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
        
        self.wgLoad.edtSearch.textChanged.connect(self.filter_scenes)  # Add search connection

        self.wgHeader.layMain.addWidget(self.wgLoad, 0)

        self.wgHeader.setWindowTitle(__name__)
        self.wgHeader.btnAccept.setText('Load')
        self.wgHeader.setWindowIcon(QtGui.QIcon(plex.get_img_path("icons/load")))

        for status in plex.config['plex']['STATUS'].values():
            self.wgLoad.cbxStatus.addItem(status)

        # SELECT start
        self.press_btnEntity()
        self.resize_widget(self.wgLoad)

        # Show arUtil to avoid double show and popping.
        self.wgHeader.show()
        LOG.info('START : ArLoad')


    def clear_context(self) -> None:
        self.wgLoad.lblUser.setText('')
        self.wgLoad.lblDate.setText('')
        self.wgLoad.lblFileSize.setText('')
        self.wgLoad.edtComment.setPlainText('')

        self.wgLoad.lblSoftwareIcon.setPixmap(QtGui.QPixmap(QtGui.QImage('')))


    # PRESS **************************************************************
    def press_btnAccept(self) -> bool | None:
        if not os.path.exists(self.load_file):
            self.set_status(f"FAILED LOADING : Path doesn't exists: {self.load_file}", msg_type=3)
            return False

        software = self.software_formats[self.extension]
        self.wgHeader.close()

        # OPEN in current software
        if software == plex.software.name and not self.desktop:
            LOG.info(f'OPEN file: {self.load_file}')
            plex.software.scene_open(self.load_file)
        # OPEN in OS
        else:
            try:    plex.software.start(name=software, open_file=self.load_file)
            except: LOG.error('FAILED to open software', exc_info=True)

        arNotice.ArNotice(title = f'LOAD: {os.path.basename(self.load_file).split(".")[0]}',
                          msg   = self.wgLoad.edtComment.toPlainText(),
                          img   = self.meta_img_path,
                          img_link = os.path.dirname(self.load_file))


    def press_btnEntity(self, button_name: str = 'assets') -> None:
        self.wgLoad.lstScene.clear()

        if button_name == 'assets':
            self.wgLoad.btnAssets.setStyleSheet("background-color: rgb(80, 80, 80);")
            self.wgLoad.btnShots.setStyleSheet("background-color: rgb(41, 43, 51);")
        else:
            self.wgLoad.btnAssets.setStyleSheet("background-color: rgb(41, 43, 51);")
            self.wgLoad.btnShots.setStyleSheet("background-color: rgb(80, 80, 80);")

        self.entity_path = plex.config['project']['PATH'][button_name]

        # Add items directly
        for scene in plexfunc.get_sub_dirs(self.entity_path):
            self.wgLoad.lstScene.addItem(scene)
        self.wgLoad.lstScene.setCurrentRow(0)


    def press_btnPreviewImg(self) -> None:
        if os.path.exists(self.meta_img_path):
            webbrowser.open(self.meta_img_path)


    # CHANGE *************************************************************
    def change_lstScene(self) -> None:
        self.wgLoad.cbxTask.clear()

        self.scene_path = f'{self.entity_path}/{self.wgLoad.lstScene.currentItem().text()}'
        task_names = plexfunc.get_sub_dirs(self.scene_path)

        self.wgLoad.cbxTask.addItems(task_names)
        self.wgLoad.cbxTask.setCurrentIndex(0)


    def change_cbxTask(self) -> None:
        self.task_path = f'{self.scene_path}/{self.wgLoad.cbxTask.currentText()}'
        self.wgLoad.cbxStatus.setCurrentIndex(0)

        self.change_cbxStatus()


    def change_cbxStatus(self) -> None:
        self.wgLoad.lstVersion.clear()
        self.open_path = f'{self.task_path}/{self.wgLoad.cbxStatus.currentText()}'

        ext = plex.config['plex']['EXTENSION'].values()
        folder = pathlib.Path(self.open_path)
        version_files = sorted(filter(lambda path: path.suffix.replace('.', '') in ext, folder.glob('*')), reverse=True)
        
        for version_file in version_files:
            version_file = os.path.basename(str(version_file))
            self.wgLoad.lstVersion.addItem(version_file)
        self.wgLoad.lstVersion.setCurrentRow(0)


    def change_lstVersion(self) -> None:
        self.load_file = f'{self.open_path}/{self.wgLoad.lstVersion.currentItem().text()}'

        self.wgLoad.lblDate.setText(str(datetime.datetime.fromtimestamp(os.path.getmtime(self.load_file))).split(".")[0])
        self.wgLoad.lblFileSize.setText(str("{0:.2f}".format(os.path.getsize(self.load_file)/(1024*1024.0)) + " MB"))

        self.extension = self.wgLoad.lstVersion.currentItem().text().split('.')[-1]

        software_img = plex.get_img_path(f"software/default/{self.software_formats[self.extension]}")
        self.wgLoad.lblSoftwareIcon.setPixmap(QtGui.QPixmap(QtGui.QImage(software_img)))

        comment = ''
        user_id = 'unknown'

        current_file = self.wgLoad.lstVersion.currentItem().text()
        meta_file_path = plex.config['project']['PATH']['meta']
        self.meta_img_path = f'{meta_file_path}/{os.path.splitext(current_file)[0]}.jpg'

        if os.path.exists(self.meta_img_path):
            self.wgLoad.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(self.meta_img_path)))
        else:
            self.wgLoad.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("labels/default"))))

        file_config = plex.config['meta'].get(current_file, '')
        if file_config:
            comment = file_config.get('comment')
            user_id = file_config.get('user')

        self.wgLoad.edtComment.setPlainText(comment)
        self.wgLoad.lblUser.setText(user_id)


    def filter_scenes(self, text: str) -> None:
        """Filter lstScene based on search text"""
        self.wgLoad.lstScene.clear()
        search_text = text.lower()
        
        for scene in plexfunc.get_sub_dirs(self.entity_path):
            if search_text in scene.lower():
                self.wgLoad.lstScene.addItem(scene)
        
        if self.wgLoad.lstScene.count() > 0:
            self.wgLoad.lstScene.setCurrentRow(0)


# START ************************************************************************
def create() -> None:
    app = QtWidgets.QApplication(sys.argv)
    main_widget = ArLoad(desktop=True)
    sys.exit(app.exec())

def start() -> None:
    main_widget = ArLoad()