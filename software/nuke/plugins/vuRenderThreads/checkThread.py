from PySide import QtGui, QtCore # Should be in PythonPath from Nuke
import time

class CheckThread(QtCore.QThread):
	signal_done = QtCore.Signal()

	def __init__(self, threadList=[], parent=None):
		super(CheckThread, self).__init__(parent)
		self.threadList = threadList


	def run(self):
		while True:
			time.sleep(0.2)
			if all(t.done for t in self.threadList):
				self.signal_done.emit()
				return True

