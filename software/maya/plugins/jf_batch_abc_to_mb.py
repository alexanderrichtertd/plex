import maya.standalone
maya.standalone.initialize(name="python")
import pymel.core as pm
import maya.cmds as cmds
import sys
import os

abcMB = {}

# Create new scene for every .abc
def createNewScenes():
	
	# Get base directory
	basedir = pm.sceneName().parent
	basedir = basedir.lower()

	# Get list of all .abc
	os.chdir(basedir)
	
	# Create new scene for every .abc
	for file in os.listdir("."):
		if file.endswith(".abc"):
			print "Create .mb for " + file
			# fileName = file.replace(".abc", ".mb")
			fileName = file.split(".ab")[0]
			fileName = fileName.split("_v")[0] + ".mb"
			cmds.file(rename=basedir+'/'+ fileName)
			cmds.file(save=True)

			abcMB[fileName] = file

			
# Import .abc in .mb
def importAbcInFolder():
	
	# Get base directory
	basedir = pm.sceneName().parent
	basedir = basedir.lower()
	
	# Get scene name
	sceneName = cmds.file(q=True, sceneName=True, shn=True)
	alembicName = abcMB[sceneName]
	
	# Load Abc file
	pm.AbcImport(basedir + '/' + alembicName)
	

def main(argv = None):
	print "Initializing..."
		
	# Load Plugin
	cmds.loadPlugin("AbcImport.mll")
		
	# Get current dir
	basedir = os.getcwd()
	os.chdir(basedir)

	# Create new file
	cmds.file(basedir + "/" + "null.mb", o=True, force=True)
	
	# Create empty scenes
	createNewScenes()
	
	# Load Alembics in every scene
	for file in os.listdir("."):
		if file.endswith(".mb") and file != "null.mb":
			print "Opening " + file
			cmds.file(basedir+'/'+file, o=True, force=True)
			importAbcInFolder()
			cmds.file(save=True)
	
	quit()
	
if __name__ == "__main__":
	main()