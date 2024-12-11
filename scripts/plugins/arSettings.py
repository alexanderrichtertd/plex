# content   = plex settings
#             executes other scripts on PUBLISH (on task in file name)
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import sys

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import plex
import plexfunc

LOG = plex.log(script=__name__)


class ArSettings():
    def __init__(self):
        path_ui = "/".join([os.path.dirname(__file__), __name__ + ".ui"])
        self.wgSettings = QtCompat.loadUi(path_ui)

        # Add save button to toolbar area
        self.wgSettings.btnSave.clicked.connect(self.press_save)

        self.wgSettings.setWindowIcon(QtGui.QPixmap(QtGui.QImage(plex.get_img_path("icons/app_modify"))))
        self.wgSettings.setWindowTitle(__name__)

        self.wgSettings.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.wgSettings.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # config
        self.wgSettings.btnPlex.clicked.connect(lambda: self.press_setConfig('plex'))
        self.wgSettings.btnProject.clicked.connect(lambda: self.press_setConfig('project'))
        self.wgSettings.btnScripts.clicked.connect(lambda: self.press_setConfig('script'))

        # extra
        self.wgSettings.btnPlugins.clicked.connect(self.press_setPlugins)

        self.wgSettings.btnCancel.clicked.connect(self.press_lblCancel)
        # QtWidgets.QShortcut(QtCore.Qt.Key_Escape, self.wgSettings, self.press_lblCancel)

        panel = self.wgSettings.centralwidget
        effect = QtWidgets.QGraphicsDropShadowEffect(panel, enabled=False, blurRadius=5)
        panel.setGraphicsEffect(effect)

        self.app = QtWidgets.QApplication.instance()
        LOG.info('START : ArSettings')

        # Trigger plex config view
        self.press_setConfig('plex')

        self.wgSettings.show()
    

    # PRESS ***************************************************************     
    def press_setConfig(self, config):
        # Update button states
        button_map = {
            'plex': self.wgSettings.btnPlex,
            'project': self.wgSettings.btnProject,
            'script': self.wgSettings.btnScripts,
        }
        for btn in button_map.values():
            btn.setEnabled(btn != button_map.get(config))

        # Setup table model
        model = QtGui.QStandardItemModel(0, 2)
        table = self.wgSettings.tblContent
        table.setModel(model)
        
        # Table starts at the top
        table.scrollToTop()  

        # Get config data
        self.config_path = plex.get_config_path(config, full_path=True)
        if not os.path.exists(self.config_path):
            LOG.error(f"Config file not found: {self.config_path}")
            return
        
        yml_data = plex.get_config(config)

        # Configure table
        table.setShowGrid(False)
        table.setWordWrap(True)
        table.verticalHeader().hide()
        table.horizontalHeader().hide()
        
        table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # Process data
        rows = []
        last_was_dict = False
        def process_dict(d, parent_key=''):
            nonlocal last_was_dict
            for k, v in d.items():
                key = f"{parent_key}/{k}" if parent_key else k
                if isinstance(v, dict):
                    if not last_was_dict:
                        rows.append(None)
                    last_was_dict = True
                    process_dict(v, key)
                else:
                    last_was_dict = False
                    rows.append((key, str(v)))

        process_dict(yml_data)
        if rows and rows[0] is None:
            rows.pop(0)

        # Populate table
        row_idx = 0
        for row in rows:
            if row is None:
                model.insertRow(row_idx)
                for col in range(2):
                    item = QtGui.QStandardItem()
                    item.setFlags(QtCore.Qt.NoItemFlags)
                    model.setItem(row_idx, col, item)
                table.setRowHeight(row_idx, 8)
                row_idx += 1
                continue

            key, value = row
            key_item = QtGui.QStandardItem(key)
            value_item = QtGui.QStandardItem(value)

            # Setup key item
            key_item.setFlags(QtCore.Qt.NoItemFlags)
            font = key_item.font()
            font.setBold(True)
            key_item.setFont(font)

            # Set alignment
            key_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            value_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            model.setItem(row_idx, 0, key_item)
            model.setItem(row_idx, 1, value_item)
            row_idx += 1


    def table_to_dict(self):
        """Convert table data back to nested dictionary"""
        result = {}
        model = self.wgSettings.tblContent.model()
        if not model:
            return result

        # Process all rows
        for row in range(model.rowCount()):
            key_item = model.item(row, 0)
            value_item = model.item(row, 1)
            
            # Skip empty/separator rows
            if not key_item or not key_item.text() or not value_item:
                continue
                
            path = key_item.text().split('/')
            value = value_item.text()
            
            # Convert string representations to appropriate types
            try:
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                elif value.startswith('[') and value.endswith(']'):
                    # Convert list strings to actual lists without quotes
                    items = value[1:-1].split(',')
                    value = [x.strip().strip("'\"") for x in items]
            except:
                pass  # Keep as string if conversion fails
            
            current = result
            for i, key in enumerate(path):
                if i == len(path) - 1:
                    current[key] = value
                else:
                    current = current.setdefault(key, {})
        
        return result

    def press_save(self):
        """Save current table content back to yaml file"""
        if not hasattr(self, 'config_path'):
            LOG.warning("No configuration file loaded to save")
            return
            
        data = self.table_to_dict()
        orig_text = self.wgSettings.btnSave.text()

        if plexfunc.set_yaml_content(self.config_path, data):
            LOG.info(f"SAVED: Config {self.config_path}")
            self.wgSettings.btnSave.setText("SAVED")
        else:
            LOG.error(f"Failed to save configuration to {self.config_path}")
            self.wgSettings.btnSave.setText("SAVE FAILED")

        QtCore.QTimer.singleShot(1500, lambda: self.wgSettings.btnSave.setText(orig_text))

    def press_setPlugins(self):
        print('plugins')
        # TODO include all plugins

    def press_lblCancel(self):
        self.wgSettings.close()
        if getattr(self, 'app_started_here', False):
            self.app.quit()


# START ***************************************************************
def start():
    app = QtWidgets.QApplication.instance()
    app_started_here = False
    if not app:
        app = QtWidgets.QApplication(sys.argv)
        app_started_here = True
    
    global main_widget
    main_widget = ArSettings()
    main_widget.app_started_here = app_started_here
    
    if app_started_here:
        app.exec()