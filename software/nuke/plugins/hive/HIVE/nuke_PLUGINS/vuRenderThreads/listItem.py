from PySide import QtGui, QtCore # Should be in PythonPath from Nuke
import time, datetime

class ListItem(QtGui.QWidget):
	def __init__(self, threadName, offset=False, parent=None):
		super(ListItem, self).__init__()

		self.text = threadName + " | "
		self.startTime = None


		# Add ProgressBar
		self.pBar = QtGui.QProgressBar()
		self.pBar.setTextVisible(False)

		eff = QtGui.QGraphicsDropShadowEffect()
		self.pBar.setGraphicsEffect(eff)


		# Add Label
		self.label = QtGui.QLabel(threadName)
		self.label.setStyleSheet("color: black;border: 1px solid black")
		#self.label.setAlignment(QtCore.Qt.AlignCenter)

		# WrapperWidget
		layout = QtGui.QGridLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
		layout.addWidget(self.pBar, 0, 0)
		layout.addWidget(self.label, 0, 0)

		self.setLayout(layout)


	def setSelected(self, value):
		if value:
			self.label.setStyleSheet("color: white;border: 1px solid black")
		else:
			self.label.setStyleSheet("color: black;border: 1px solid black")


	def init(self):
		pass


	def eta(self):
		if not self.startTime:
			self.startTime = time.time()
			return ""

		elapsed = time.time() - self.startTime
		eta = elapsed * self.pBar.maximum()  / self.pBar.value() - elapsed
		return 'ETA: %s' % str(datetime.timedelta(seconds=int(eta)))


	def setMaximum(self, value):
		self.pBar.setRange(0, value)


	def setProgress(self, value, msg="inProgress"):
		# Value
		self.pBar.setValue(value)
		self.label.setText(self.text + " " + msg + " | " + self.eta())

		# Color
		m = float(self.pBar.value()) / float(self.pBar.maximum())
		r =  90*m +  255*(1-m)
		g = 170*m +  180*(1-m)
		b =  55*m +    0*(1-m)
		self.pBar.setStyleSheet("QProgressBar::chunk { background: rgb(%i, %i, %i) }" % (r, g, b))


	def setProgressDone(self):
		# Value
		self.pBar.setValue(self.pBar.maximum())
		self.label.setText(self.text + " Done!")

		# Color
		self.pBar.setStyleSheet("QProgressBar::chunk { background: rgb(38, 128, 43) }")


	def setProgressError(self):
		# Value
		self.pBar.setValue(self.pBar.maximum())
		self.label.setText(self.text + " ERROR!")

		# Color
		self.pBar.setStyleSheet("QProgressBar::chunk { background: rgb(149, 54, 54) }")




def createListItem(listWidget, threadName):

	# Create CustomWidgetItem
	widget = ListItem(threadName)

	# Create QListWidgetItem
	listWidgetItem = QtGui.QListWidgetItem("Hallo")
	listWidgetItem.setSizeHint(widget.sizeHint())

	# Add Items
	listWidget.addItem(listWidgetItem)
	listWidget.setItemWidget(listWidgetItem, widget)

	return widget
