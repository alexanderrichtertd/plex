import sys, os
from PySide import QtGui, QtCore # Should be in PythonPath from Nuke

# vuRenderThreads
import mainWindow
import renderThread



def createThreads(window):
	# Get Vars
	writeNodes	= eval(os.getenv("WRITENODES"))
	frameStart	= int(os.getenv("frameStart"))
	frameEnd	= int(os.getenv("frameEnd"))
	numThreads	= int(os.getenv("numThreads"))

	# Build Threads
	for nodeName in writeNodes:

		#if len(WRITENODES) > 1:
		#	window.addSpacer(nodeName)
		#	window.widgets += [None]

		for threadNum in range(numThreads):
			thread	= renderThread.RenderThread(threadNum, numThreads, frameStart, frameEnd, nodeName)
			widget	= window.addThread(thread, "%s | #%d/%d" % (nodeName, threadNum+1, numThreads))
			thread.render()


def main():
	app = QtGui.QApplication([])


	# Build Window
	window = mainWindow.MainWindow()

	createThreads(window)
	window.createCheckThread()

	app.exec_()




if __name__ == '__main__':
	# DEBUG Vars
	#os.environ["DCC"]			= "nuke"
	#os.environ["EXE"]			= ""
	#os.environ["SCENE"]			= "SceneFile.scn"
	#os.environ["WRITENODES"]	= "['writeNode1', 'writeNode2']"
	#os.environ["frameStart"]	= "1001"
	#os.environ["frameEnd"]		= "1250"
	#os.environ["numThreads"]	= "4"
	main()