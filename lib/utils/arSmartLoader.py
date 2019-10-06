

import os
import sys

from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools


TITLE    = os.path.splitext(os.path.basename(__file__))[0]

PATH_UI      = ("/").join([os.path.dirname(__file__), "ui"])
PATH_UI_FILE = ("/").join([PATH_UI, TITLE + ".ui"])

script_filter = ['software', 'scripts', 'Shots', 'Assets']
script_last   = "scripts"

# DELETE
SHOTS    = ['s010_halo', 's020_what']
ASSETS   = ['Max', 'Table']
SCRIPTS  = ['Load', 'Save']
SOFTWARE = ['Maya', 'Nuke']

class ScriptSelection(object):

    def __init__(self):
        super(ScriptSelection, self).__init__()
        self.widget = QtUiTools.QUiLoader().load(PATH_UI_FILE)
        self.default_size = QtCore.QSize(self.widget.width(), 24)

        self.options    = True
        self.checkItems = []
        self.set_comment()

        self.ui()

    #*****************************
    # UI
    def ui(self):

        # CONNECT
        self.widget.btnOptions.clicked.connect(self.press_btnOptions)

        # COMBO BOX
        self.cbxScript = SmartCombo(self)
        self.widget.layTop.addWidget(self.cbxScript)
        # self.cbxScript.resize(QtCore.QSize(50, 50))


        # CHECKBOX
        for item in script_filter:
            checkItem = QtGui.QCheckBox(item)
            self.checkItems.append(checkItem)
            self.widget.layOptions.addWidget(checkItem)

        # WINDOW
        self.widget.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)

        self.widget.setWindowOpacity(0.9)
        self.widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.widget.resize(self.default_size)
        self.widget.setTabOrder(self.cbxScript, self.widget.btnOptions)

        # WIDGET on MOUSE POS
        cursor = QtGui.QCursor()
        self.widget.move(cursor.pos().x() - 20, cursor.pos().y() - 12)

        # DEFAULT
        self.press_btnOptions()
        self.set_scripts()

        self.widget.show()


    #*****************************
    # PRESS
    def press_btnAccept(self):
        print("ACCEPT")
        currentText = self.cbxScript.currentText()

        # CHECK: exists
        findItem = self.cbxScript.findText(currentText)
        if findItem > -1:
            self.execute_script(currentText)
            self.press_btnCancel()
        else:
            self.set_comment("ITEM not found")

    def press_btnOptions(self):
        if self.options:
            self.widget.wgOptions.hide()
            self.widget.resize(self.default_size)
            self.widget.btnOptions.setIcon(QtGui.QPixmap(QtGui.QImage(PATH_UI + '/btnArrowDown20.png')))
            self.options = False
        else:
            self.widget.wgOptions.show()
            self.widget.btnOptions.setIcon(QtGui.QPixmap(QtGui.QImage(PATH_UI + '/btnArrowUp20.png')))
            self.options = True

    def press_btnCancel(self):
        print("close")
        self.widget.close()


    #*****************************
    # FUNCTIONS
    def execute_script(self, script):
        print(script)
        # EXE script

        if True:
            pass
        else:
            self.set_comment("Sorry! This ITEM is not executable ... error was reported")

        # SAVE last_script

    def set_scripts(self):
        # LIST
        wordList = SHOTS
        wordList.extend(SCRIPTS)
        wordList.extend(SOFTWARE)
        wordList.extend(ASSETS)
        self.cbxScript.addItems(wordList)

        # COMPLETER
        completer = QtGui.QCompleter(wordList, self.widget)
        completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        completer.setCompletionRole(QtCore.Qt.DisplayRole)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.cbxScript.setCompleter(completer)

        findItem = self.cbxScript.findText(script_last)
        if findItem > -1:
            self.cbxScript.setCurrentIndex(findItem)

        self.cbxScript.lineEdit().selectAll()

    def set_comment(self, text = ''):
        self.widget.lblComment.setText('  ' + text)

        if text:
            self.widget.wgFooter.show()
        else:
            self.widget.wgFooter.hide()


    #*****************************
    # EVENT
    def keyPressEvent(self, e):
        print(e.key())
        if e.key() == QtCore.Qt.Key_Escape:
            self.widget.close()


#************************
# CLASS
class SmartCombo(QtGui.QComboBox):
    def __init__(self, widget = None):
        super(SmartCombo, self).__init__()

        self.widget = widget
        self.setFrame(False)
        self.setEditable(True)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.widget.press_btnAccept()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.widget.press_btnCancel()
        else:
            QtGui.QComboBox.keyPressEvent(self, event)


#************************
# START
def start():
    app = QtGui.QApplication(sys.argv)

    def focus_handler():
        if app.focusWidget() is None:
            app.quit()

    app.focusChanged.connect(focus_handler)

    classVar = ScriptSelection()
    app.exec_()


start()
