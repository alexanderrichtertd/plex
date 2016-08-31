import os, sys
from PySide import QtGui, QtCore


# SETTINGS
CMD_TEMPLATE = {}
CMD_TEMPLATE["nuke"]    = '"%(EXE)s" -i -X %(NODE)s -F %(fStart)s-%(fEnd)sx%(fStep)s "%(SCENE)s"'
CMD_TEMPLATE["houdini"] = '"%(EXE)s " ' + __file__ + ' %(SCENE)s %(NODE)s %(fStart)s %(fEnd)s %(fStep)s'



class RenderThread(QtCore.QProcess):
	signal_updateProgress	= QtCore.Signal(str)
	signal_updateOutput		= QtCore.Signal(str)
	signal_finished			= QtCore.Signal(int)

	"""docstring for RenderThread"""
	def __init__(self, threadNum, numThreads, frameStart, frameEnd, nodeName, parent=None):
		super(RenderThread, self).__init__(parent=None)


		# Values
		self.outText = ""
		self.text = nodeName + " | #" + str(threadNum+1) + " / " + str(numThreads) + " | "
		#self.startTime = None

		# Flags
		self.isLive	= False		# If true emit QtSignal for Updates
		self.done	= False
		self.failed = False		# If true be Red



		# Connections
		self.finished.connect(self.renderFinished)
		self.setProcessChannelMode(QtCore.QProcess.MergedChannels)
		self.readyReadStandardOutput.connect(self.readOutput)

		# Copy Env
		self.setProcessEnvironment(QtCore.QProcessEnvironment.systemEnvironment())



		# Build Command
		template = CMD_TEMPLATE[os.environ["DCC"]]

		values = {}
		values["EXE"]		= os.environ["EXE"]
		values["SCENE"]		= os.environ["SCENE"]
		values["NODE"]		= nodeName
		values["fStart"]	= str(frameStart + threadNum)
		values["fEnd"]		= str(frameEnd)
		values["fStep"]		= str(numThreads)

		self.cmd = template % values
		#self.cmd = "C:/Python27/python.exe D:/Vincent/Dropbox/btSyncFolders/Dev/026_vuRenderThreads/dummyThread.py"




	def render(self):
		self.start(self.cmd)


	def readOutput(self):
		text = str(self.readAllStandardOutput())
		self.outText += text

		if self.isLive:
			self.signal_updateOutput.emit(text)

		if text.startswith("Frame"):
			self.signal_updateProgress.emit(text)



	def renderFinished(self):
		"""
		ERROR_KEYWORDS = ["ERROR", "denied", "Read error"]

		for keyword in ERROR_KEYWORDS:
			if keyword in text:
				self.setProgress_Error()
				self.failed = True
		"""

		self.signal_finished.emit(self.exitCode())
		self.done = True


"""
# for HOUDINI
def renderScript():
	hipFile = sys.argv[1]
	rop = sys.argv[2]

	frameStart = int(sys.argv[3])
	frameEnd   = int(sys.argv[4])
	frameStep  = int(sys.argv[5])

	hou.hipFile.load(hipFile)
	ropNode = hou.node(rop)

	print "-------------\n" * 10
	print "hipFile", hipFile
	print "rop", rop
	print "frameStart", frameStart
	print "frameEnd", frameEnd
	print "frameStep", frameStep
	print "-------------\n" * 10

	# Count Frames for ProgressBar
	frames = [f for f in xrange(frameStart, frameEnd+1, frameStep)]
	for i, f in enumerate(frames):
		hou.setFrame(f)
		ropNode.render((f, f, 1), verbose=True)
		print "Frame:", f, "(" + str(i+1) + " of " + str(len(frames)) + ")"

if __name__ == '__main__':
	renderScript()
"""