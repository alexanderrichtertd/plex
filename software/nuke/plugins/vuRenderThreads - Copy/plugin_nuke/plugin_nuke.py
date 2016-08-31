import os, sys
import nuke


ROOT_NUKE	= os.path.dirname(os.path.abspath(nuke.EXE_PATH))
ROOT_RT		= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def setEnvoriment():
	os.environ["PYTHONPATH"]	= ROOT_NUKE + "\pythonextensions\site-packages;" + str(os.getenv("PYTHONPATH"))
	os.environ["PATH"]			= ROOT_NUKE + ";" + str(os.getenv("PATH"))



WRITENODES = ["Write", "Jagon_Write_v003", "J_WriteUndistort", "Flut_Write", "Kryo_Write", "Kroeten_Write"]

def getWriteNodes():
	# Check Selection
	if len(nuke.selectedNodes()) == 0 :
		nodes = nuke.allNodes()
	else:
		nodes = nuke.selectedNodes()

	writeNodes = []
	for oNode in nodes:
		if oNode.Class() in WRITENODES and (False == oNode["disable"].value()):
			writeNodes += [oNode.name()]

	return writeNodes



def createThreads(frameStart, frameEnd, numThreads, writeNodes=None):
	nuke.scriptSave()

	if not writeNodes:
		writeNodes = getWriteNodes()


	os.environ["DCC"]			= "nuke"
	os.environ["EXE"]			= nuke.EXE_PATH
	os.environ["SCENE"]			= nuke.root().name()
	os.environ["WRITENODES"]	= str(writeNodes)

	os.environ["frameStart"] 	= str(frameStart)
	os.environ["frameEnd"]		= str(frameEnd)
	os.environ["numThreads"]	= str(numThreads)


	# Start
	setEnvoriment()
	os.chdir(ROOT_RT)
	print os.startfile("main.bat")



def showPopup():
	# Create Popup
	p = nuke.Panel("Batch Render Threads")
	p.addSingleLineInput("First Frame:",	nuke.value('root.first_frame'))
	p.addSingleLineInput("Last Frame:",		nuke.value('root.last_frame'))
	p.addSingleLineInput("Threads:",		"8")

	p.addButton("Cancel")
	p.addButton("OK")
	p.setWidth(200)
	result = p.show()


	if result == 1:
		frameStart	= p.value("First Frame:")
		frameEnd	= p.value("Last Frame:")
		numThreads	= p.value("Threads:")
		createThreads(frameStart, frameEnd, numThreads)
	else:
		print "Canceled!"


def main():
	showPopup()