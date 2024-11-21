#*********************************************************************
# content   = informs artists about changes
# date      = 2024-11-13
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys
import glob
import time
import getpass
import webbrowser

from threading import Timer
from datetime import datetime

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import pipefunc
from tank import Tank


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)


#*********************************************************************
# NOTICE
class Notice():

    def __init__(self,
                 title    = 'Notice',
                 msg      = 'This is just a Notice Test',
                 quote    = 'plex it out',
                 img      = 'lbl/default',
                 img_link = 'https://www.alexanderrichtertd.com',
                 func     = '',
                 timer    = 7):

        self.title    = str(title)   # Pipeline Update
        self.msg      = str(msg)     # New Features for Pipeline
        self.quote    = str(quote)   # New Features for Pipeline
        self.img      = img          # lbl/lblPreview131
        self.img_link = img_link     # path
        self.time     = datetime.now().strftime('%H:%M:%S %Y.%m.%d')
        self.func     = func
        self.timer    = timer

    def __call__(self):
        LOG.debug(  'time:     ' + self.time + '\n' +\
                    'func:     ' + self.func + '\n\n' +\
                    'title:    ' + self.title + '\n' +\
                    'msg:      ' + self.msg + '\n' +\
                    'quote:    ' + self.quote + '\n' +\
                    'img_link: ' + self.img_link)



#*********************************************************************
# NOTICE UI
class ArNotice():

    def __init__(self, notice):
        ui_path = '/'.join([os.path.dirname(__file__), 'ui', __name__ + '.ui'])
        self.wgNotice = QtCompat.loadUi(ui_path)
        self.notice   = notice

        self.wgNotice.btnPreviewImg.clicked.connect(self.press_btnPreviewImg)

        self.wgNotice.edtTitle.setText(self.notice.title)
        self.wgNotice.edtMsg.setPlainText(self.notice.msg)
        if self.notice.quote: self.notice.quote = f'"{self.notice.quote}"'
        self.wgNotice.edtQuote.setPlainText(self.notice.quote)

        self.wgNotice.edtTitle.setText(self.notice.title)

        self.open_link = self.notice.img_link
        self.wgNotice.btnPreviewImg.setToolTip(self.open_link)

        # if not os.path.exists(self.notice.img): self.notice.img = Tank().get_img_path(self.notice.img)
        self.wgNotice.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(self.notice.img)))
        # if self.notice.func: self.wgNotice.lblFunc.setText(self.notice.func)
        # else:                self.wgNotice.lblFunc.hide()
        if not self.notice.img_link: self.wgNotice.btnPreviewImg.setEnabled(False)

        # WIDGET : delete border & always on top
        self.wgNotice.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)

        # WIDGET : move to right low corner
        width, height = QtWidgets.QApplication.screens()[0].size().toTuple()
        self.wgNotice.move(width - self.wgNotice.width() - 10, height - self.wgNotice.height() - 75)
        self.wgNotice.setWindowOpacity(0.95)

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
        if self.notice.func:
            exec(self.notice.func)
        elif self.notice.img_link:
            webbrowser.open(os.path.realpath(self.notice.img_link))


#*********************************************************************
def create_default_notice(script_string, msg=""):
    root, script_name = script_string.split(":")

    notice_config = Tank().config_notice

    if root in notice_config and script_name in notice_config[root]:
        notice_config = notice_config[root][script_name]
        notice_msg = [lambda: notice_config["msg"], lambda: msg][msg != ""]()
    else:
        notice_config['title'] = root
        notice_msg  = script_name
        # LOG.warning(f"notice.yml config doesn't exist: {script_name}")
        # return

    if "quote" in notice_config: notice_quote = notice_config["quote"]
    else: notice_quote = ''

    img_name = [lambda: script_name, lambda: notice_config["img"]]["img" in notice_config]()
    img_link = [lambda: "", lambda: notice_config["img_link"]]["img_link" in notice_config]()
    img_path = Tank().get_img_path("lbl/notice_" + img_name)
    img_path = [lambda: f'{img_path}/notice_default.png', lambda: img_path][os.path.exists(img_path)]()

    note = Notice(title = notice_config['title'],
                    msg = notice_msg,
                  quote = notice_quote,
                    img = img_path,
               img_link = img_link)

    classVar = ArNotice(note)
    # start(note)


def create_changelog_popup():
    import pwd
    import yaml

    # TODO: changelog_path undefined

    changelog_list = glob.glob(changelog_path + '/*.changelog')

    if changelog_list:
        last_changelog = changelog_list[-1]
    else:
        LOG.warning(f'NO changelog exists at: {changelog_path}')
        return

    current_date   = ("{}_{:02}_{:02}".format(datetime.now().year, datetime.now().month, datetime.now().day))
    changelog_date = os.path.basename(last_changelog).split(".")[0]

    if current_date != changelog_date:
        last_changelog = changelog_path + '/welcome'
        if not os.path.exists(last_changelog):
            LOG.warning(f'NO current and welcome changelog exists at: {changelog_path}')
            return

    # READ YAML file
    with open(last_changelog, 'r') as stream:
        changelog_config = yaml.load(stream, Loader=yaml.Loader)

    notice_config = changelog_config["notice"]
    popup_func  = ''

    if 'changelog' in changelog_config:
        popup_func  = f"""from Qt import QtWidgets, QtGui, QtCore, QtCompat
                        widget = QtGui.QMessageBox()
                        widget.setWindowTitle('{notice_config["title"]}')
                        widget.setText({changelog_config["changelog"]})
                        widget.show()"""

    notice_msg = notice_config["msg"]

    img_name = notice_config["img"] if "img" in notice_config else "changelog"
    img_path = f'{pipefunc.get_config_path("img_notice")}/notice_{img_name}.png'

    note = Notice(title    = notice_config["title"],
                  msg      = notice_msg,
                  # func   = popup_func,
                  img      = img_path,
                  quote    = notice_config["quote"],
                  img_link = notice_config["img_link"])

    ArNotice(note)



#******************************************************************************
# START
def start(note = Notice()):
    app = QtWidgets.QApplication(sys.argv)
    classVar = ArNotice(note)
    app.exec_()

# start()
# create_default_notice("shelf/submit")
