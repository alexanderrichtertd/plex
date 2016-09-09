import maya.cmds as cmds
import pymel.core as pm
import os

def createNewScenes():
	
	# Get base directory
	basedir = pm.sceneName().parent
	basedir = basedir.lower()

	# Get list of all .abc
	os.chdir(basedir)
	
	# Create new scene for every .abc
	for file in os.listdir("."):
		if file.endswith(".abc"):
			print file
			cmds.file(rename=basedir+'/'+file.replace(".abc", ".mb"))
			cmds.file(save=True)

			
def importAbcInFolder():
	
	# Get base directory
	basedir = pm.sceneName().parent
	basedir = basedir.lower()
	
	# Get scene name
	sceneName = cmds.file(q=True, sceneName=True, shn=True)
	alembicName = sceneName.replace('.mb', '.abc')
	
	# Load Abc file
	pm.AbcImport(basedir + '/' + alembicName)

	
class AbcExporter():

	def __init__(self):
		
		self.title = "Alembic Exporter"
		self.name = "abcExporter"
		self.basedir = ""
		
		self.buildUI()
		
		
	# Building the UI
	def buildUI(self):
	
		if cmds.window(self.name, q=True, exists=True):
			cmds.deleteUI(self.name)
		cmds.window(self.name, title=self.title, sizeable=False, mxb=False, mnb=False, toolbox=False, w=100, h=30)
		cmds.columnLayout("mainLayout", parent=self.name)
		
		cmds.textFieldButtonGrp("tfbPath", label="Save Alembics to: ", bl="Set Folder", bc=self.setPath)
		
		# Set base directory
		self.basedir = pm.sceneName().parent
		self.basedir = self.basedir.lower()
		cmds.textFieldButtonGrp("tfbPath", e=True, tx=self.basedir)
		
		cmds.radioButtonGrp("rbFileName", label="Type: ", labelArray3=["None", "Char", "Prop"], numberOfRadioButtons=3, sl=2)
		cmds.textFieldGrp("tfShot", label="Shot: ")

		cmds.button("bExportAlembic", label = "Export Selection", w=500, h=30, parent="mainLayout", c=self.exportSelection)

		cmds.showWindow(self.name)
		
		
	# Setting the destination folder
	def setPath(self, *args):
	
		path = cmds.fileDialog2(fm=3)
		if path == None:
			return
		cmds.textFieldButtonGrp("tfbPath", e=True, tx=path[0])
	
		
	# Exporting the chars
	def exportSelection(self, *args):
		
		fileName=""

		# Get Selection
		selection = cmds.ls(sl=True)
		
		# Get Framerange
		frameIn = cmds.playbackOptions(q=True, ast=True)
		frameOut = cmds.playbackOptions(q=True, aet=True)
		
		# Get Destination Path
		dest_path = cmds.textFieldButtonGrp("tfbPath", q=True, tx=True) + "/"
		
		# Set Flags for Export
		flag1 = "-frameRange "+str(frameIn)+" "+str(frameOut) + " "
		flag2 = " -step 1 -attr visibility -noNormals -stripNamespaces -uvWrite -worldSpace -writeVisibility" + " -file %s"

		# Export every char
		for item in selection:
		
			# Set filename		
			if(cmds.radioButtonGrp("rbFileName", q=True, sl=True) == 2):
				fileName = "char_" + item.lower()
			elif(cmds.radioButtonGrp("rbFileName", q=True, sl=True) == 3):
				fileName = "prop_" + item.lower()
			else:
				fileName = item.lower()

			shot = cmds.textFieldGrp("tfShot", q=True, text=True)
			if len(shot) > 0:
				fileName = shot + "_" + fileName

			fileName = fileName.split(":")[0]
			if fileName[len(fileName)-1] == "_":
				fileName = fileName[:len(fileName)-2]

			# Exception for MIDDLEGROUND, FOREGROUND and BACKGROUND
			if item == "MIDDLEGROUND" or item == "FOREGROUND" or item == "BACKGROUND":
				flags = flag1 + "-root " + item + " " + flag2 % (dest_path + fileName + ".abc")
				pm.AbcExport(j=flags)
				continue

			cmds.select(item, hi=True)
			shapes = cmds.ls(sl=True, type='mesh', fl=True)
			deformer = cmds.ls(sl=True, type="deformBend", fl=True)

			meshes = ""

			for mesh in shapes:

				transformNode = cmds.listRelatives(mesh, parent=True, f=True)[0]

				# Kick hidden meshes
				parentNode = cmds.listRelatives(transformNode, parent=True, f=True)
				if cmds.getAttr(transformNode + ".visibility") == False or (parentNode == None and cmds.getAttr(parentNode[0] + ".visibility") == False):
					continue
				
				# Kick other unwanted meshes
				if "body_scale" in transformNode or "blendShape_master" in transformNode:
					continue
				
				meshes += "-root " + transformNode + " "
				

			print meshes
			meshes = meshes[0:(len(meshes)-1)]
			
			flags = flag1 + meshes + flag2 % (dest_path + fileName + ".abc") 
			pm.AbcExport(j=flags)