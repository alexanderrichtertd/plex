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
        ui_path = ('/').join([os.path.dirname(__file__), 'ui', __name__ + '.ui'])
        self.wgNotice = QtCompat.loadUi(ui_path)
        self.notice   = notice

        self.wgNotice.btnCancel.clicked.connect(self.press_btnCancel)
        self.wgNotice.btnPreviewImg.clicked.connect(self.press_btnPreviewImg)

        self.wgNotice.edtTitle.setText(self.notice.title)
        self.wgNotice.edtMsg.setPlainText(self.notice.msg)
        if self.notice.quote: self.notice.quote = '"{}"'.format(self.notice.quote)
        self.wgNotice.edtQuote.setPlainText(self.notice.quote)

        self.wgNotice.edtTitle.setText(self.notice.title)

        self.open_link = self.notice.img_link
        self.wgNotice.btnPreviewImg.setToolTip(self.open_link)

        # if not os.path.exists(self.notice.img): self.notice.img = Tank().get_img_path(self.notice.img)
        self.wgNotice.btnPreviewImg.setIcon(QtGui.QPixmap(QtGui.QImage(self.notice.img)))
        # if self.notice.func: self.wgNotice.lblFunc.setText(self.notice.func)
        # else:                self.wgNotice.lblFunc.hide()
        if not self.notice.img_link: self.wgNotice.btnPreviewImg.setEnabled(False)
        # self.wgNotice.btnCancel.hide()

        # WIDGET : delete border & always on top
        self.wgNotice.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)

        # WIDGET : move to right low corner
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.wgNotice.move(resolution.width() - self.wgNotice.width() - 10, resolution.height() - self.wgNotice.height() - 75)
        self.wgNotice.setWindowOpacity(0.9)

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

    notice_data = Tank().data_notice

    if root in notice_data and script_name in notice_data[root]:
        notice_data = notice_data[root][script_name]
        notice_msg = [lambda: notice_data["msg"], lambda: msg][msg != ""]()
    else:
        notice_data['title'] = root
        notice_msg  = script_name
        # LOG.warning("notice.yml data doesn't exist: {}".format(script_name))
        # return

    if "quote" in notice_data: notice_quote = notice_data["quote"]
    else: notice_quote = ""

    img_name = [lambda: script_name, lambda: notice_data["img"]]["img" in notice_data]()
    img_link = [lambda: "", lambda: notice_data["img_link"]]["img_link" in notice_data]()
    img_path = Tank().get_img_path("lbl/notice_" + img_name)
    img_path = [lambda: "{}/notice_default.png".format(img_path), lambda: img_path][os.path.exists(img_path)]()

    note = Notice(title = notice_data["title"],
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

    changelog_list = glob.glob(changelog_path + "/*.changelog")

    if changelog_list:
        last_changelog = changelog_list[-1]
    else:
        LOG.warning("NO changelog exists at: {}".format(changelog_path))
        return

    current_date   = ("{}_{:02}_{:02}".format(datetime.now().year, datetime.now().month, datetime.now().day))
    changelog_date = os.path.basename(last_changelog).split(".")[0]

    if current_date != changelog_date:
        last_changelog = changelog_path + "/welcome"
        if not os.path.exists(last_changelog):
            LOG.warning("NO current and welcome changelog exists at: {}".format(changelog_path))
            return

    # READ YAML file
    with open(last_changelog, 'r') as stream:
        changelog_data = yaml.load(stream, Loader=yaml.Loader)

    notice_data = changelog_data["notice"]
    popup_func  = ""

    if "changelog" in changelog_data:
        popup_func  = """from Qt import QtWidgets, QtGui, QtCore, QtCompat
                        widget = QtGui.QMessageBox()
                        widget.setWindowTitle('{}')
                        widget.setText({})
                        widget.show()""".format(notice_data["title"], changelog_data["changelog"])

    notice_msg = notice_data["msg"]

    img_name = notice_data["img"] if "img" in notice_data else "changelog"
    img_path = "{}/notice_{}.png".format(pipefunc.get_data_path("img_notice"), img_name)

    note = Notice(title    = notice_data["title"],
                  msg      = notice_msg,
                  # func   = popup_func,
                  img      = img_path,
                  quote    = notice_data["quote"],
                  img_link = notice_data["img_link"])

    ArNotice(note)



#******************************************************************************
# START
def start(note = Notice()):
    app = QtWidgets.QApplication(sys.argv)
    classVar = ArNotice(note)
    app.exec_()

# start()
# create_default_notice("shelf/submit")
