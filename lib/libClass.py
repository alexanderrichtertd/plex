#*************************************************************
# CONTENT       main functions
#
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
import sys

from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools

# DELETE ******************
import sys
sys.path.append("..\settings")
import setEnv
setEnv.SetEnv()
#**************************
import getProject
DATA = getProject.GetProject()


# DEFAULT
import libLog

TITLE   = os.path.splitext(os.path.basename(__file__))[0]
LOG     = libLog.initLog(script=TITLE)
PATH_UI = DATA.PATH["ui"] + TITLE + ".ui"
# PATH_UI = r"D:\Dropbox\arPipeline\v002\WORK\software\_ui\arReport.ui"


class ClassName():
    def __init__(self, ui):
        # super(ClassName, self).__init__()
        self.widget = ui
        self.initUi()


    #**********************
    # UI
    def initUi(self):
        # SIGNAL
        # self.widget.connect(self.widget.btnAccept, SIGNAL("clicked()"), clicked_btnAccept)
        # self.widget.cbxPublish.toggled.connect(changed_publish)
        # self.widget.edtSaveFile.textChanged.connect(changed_edtSaveFile)

        # WIDGET : always on top
        self.widget.setWindowFlags(QTGui.Qt.WindowStaysOnTopHint) # | QTGui.Qt.CustomizeWindowHint | QTGui.Qt.FramelessWindowHint) | QTGui.Qt.Tool)
        self.widget.show()


    #**********************
    # PRESS_TRIGGER
    def press_btnReport(self):
        global LOG
        LOG.info("REPORT")
        arReport.start(self.TITLE)

    def press_btnHelp(self):
        global LOG
        LOG.info("HELP")
        libFunction.getHelp()


    #**********************
    # CHANGE_TRIGGER
    def change_edtComment(self):
        print "changed"


#**********************
# START UI
def start():
    app = QtGui.QApplication(sys.argv)
    ui  = QtUiTools.QUiLoader().load(PATH_UI)
    ex  = ClassName(ui)

    LOG.info("START")
    app.exec_()

start()
