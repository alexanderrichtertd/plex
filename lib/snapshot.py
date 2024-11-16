#*********************************************************************
# content   = snapshot
#             executes other scripts on PUBLISH (on task in file name)
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import time

from Qt import QtWidgets, QtGui, QtCore, __binding__

import pipefunc
from tank import Tank


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)
DEFAULT_PATH = os.path.normpath(os.getenv('CONFIG_USER_PATH').split(';')[0] + '/tmp_img.jpg')


#*********************************************************************
# SCREENSHOT
# creates a screenshot of the main screen and saves it
def create_any_screenshot(WIDGET, ui=''):
    # if not create_screenshot_render(WIDGET, ui):
    if not create_screenshot_viewport(WIDGET, ui):
        create_screenshot(WIDGET, ui)


def create_screenshot(WIDGET, ui=''):
    print("SCREENSHOT")
    # WIDGET.hide()
    if not os.path.exists(os.path.dirname(DEFAULT_PATH)):
        try: os.makedirs(os.path.dirname(DEFAULT_PATH))
        except: LOG.error('FAILED folder creation', exc_info=True)
    # time.sleep(0.6)

    if __binding__ == "PySide2":
        from PySide2 import QtWidgets, QtGui
        QtGui.QScreen.grabWindow(QtWidgets.QApplication.primaryScreen(), QtWidgets.QApplication.desktop().winId()).save(DEFAULT_PATH, DEFAULT_PATH.split(".")[-1])
    else:
        from Qt import QtWidgets, QtGui
        QtGui.QPixmap.grabWindow(QtWidgets.QApplication.desktop().winId()).save(DEFAULT_PATH, DEFAULT_PATH.split(".")[-1])

    # WIDGET.setFocus()
    # WIDGET.show()
    if ui: ui.setIcon(QtGui.QPixmap(QtGui.QImage(DEFAULT_PATH)))


def create_screenshot_render(WIDGET, ui=''):
    # WIDGET.hide()
    if not os.path.exists(os.path.dirname(DEFAULT_PATH)):
        try:
            os.makedirs(os.path.dirname(DEFAULT_PATH))
        except:
            LOG.error('FAILED folder creation', exc_info=True)
            return False

    try:
        if os.getenv("SOFTWARE") == "MAYA":
            if not maya_renderSnapshot(DEFAULT_PATH)[1]:
                LOG.warning("no snapshot no")
                return False
        elif os.getenv("SOFTWARE") == "HOUDINI": houdini_renderSnapshot(DEFAULT_PATH)
        else: return False
    except:
        LOG.error('FAIL', exc_info=True)
        return False

    if ui and os.path.exists(DEFAULT_PATH): ui.setIcon(QtGui.QPixmap(QtGui.QImage(DEFAULT_PATH)))
    # WIDGET.show()
    # WIDGET.setFocus()
    return True


def create_screenshot_viewport(WIDGET, ui=''):
    # WIDGET.hide()
    Tank().software.viewport_snapshot()

    # TODO: FIX for
    # "HOUDINI": create_screenshot(WIDGET, ui) # houdini_viewportSnapshot(DEFAULT_PATH)
    # "MAX":     create_screenshot(WIDGET, ui)

    if ui and os.path.exists(DEFAULT_PATH):
        ui.setIcon(QtGui.QPixmap(QtGui.QImage(DEFAULT_PATH)))
    else:
        return False
    # WIDGET.show()
    # WIDGET.setFocus()
    return True


#*********************************************************************
# FILE HANDLING
def save_snapshot(rlt_path, src_path=DEFAULT_PATH):
    img = QtGui.QImage()
    img.load(src_path)
    thumbnail_extension = '.' + Tank().config_project['EXTENSION']['thumbnail']

    tmpDir   = os.path.dirname(rlt_path) + '/' + Tank().config_project['META']['dir']
    rlt_path = tmpDir + "/" + os.path.basename(rlt_path).split(".")[0] + thumbnail_extension

    pipefunc.create_folder(rlt_path)
    img.save(rlt_path, format=thumbnail_extension)
    remove_tmp_img(src_path)
    return rlt_path

def remove_tmp_img(img_path=DEFAULT_PATH):
    try:    os.remove(img_path)
    except: LOG.error('FAIL : cant delete tmpFile : ' + img_path, exc_info=True)
