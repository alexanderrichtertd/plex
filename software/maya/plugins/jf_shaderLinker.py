'''
	author: Johannes Franz 2013
'''

import maya.cmds as cmds
import pymel.core as pm
import sqlite3

class ShaderLinker():

	def __init__(self):
		
		self.title = "Shader Linker .9"
		self.name = "shaderLinker"
		self.help = self.name + "Help"

		self.instructions = "Export Links: Writes all the shader links into a sql file" + "\n\n" + "Link Shaders: Links the shaders to the meshes according to the sql file specified in the Links path." + "\n\n" + "Links: Path to the sql file which holds the links" + "\n\n" + "Shaders: Path to the .mb file which holds the shaders. Can be empty to no import any shaders." + "\n\n" + "Use Selection: Link only the selected mesh" + "\n\n" + "Workflow: " + "\n" + "1. Export all links into a .db file of choice. A new file must be specified each time." + "\n" + "2. To link all the shaders a path to the .db file must be specified." + "\n" + "Optional: Shaders can be imported into the scene via the shader path."

		# Set base directory
		self.basedir = pm.sceneName().parent
		self.basedir = self.basedir.lower()

		self.buildGUI()


	#  GUI
	def buildGUI(self):
	
		if cmds.window(self.name, q=True, exists=True):
			cmds.deleteUI(self.name)
		cmds.window(self.name, title=self.title, sizeable=False, mxb=False, mnb=False, toolbox=False, w=100, h=30)
		cmds.columnLayout("mainLayout", adj=True, parent=self.name, co=("left", 5))

		# Add onClose Event
		cmds.scriptJob(uiDeleted=(self.name, self.onClose))
		
		# Help Menu
		cmds.menuBarLayout("menuBar")
		cmds.menu(label="Show Help", helpMenu =True, pmc=self.showHelp)

		# Import paths
		cmds.textFieldButtonGrp("tfbDBPath", label="Links: ", bl="Set Link Path", cw=(1,50), parent="mainLayout", bc=self.setDBPath)
		cmds.textFieldButtonGrp("tfbShaderPath", label="Shaders: ", bl="Set Shader Path", cw=(1,50), parent="mainLayout", bc=self.setShaderPath)
		
		cmds.checkBox("cbSelection", label="Use Selection", parent="mainLayout")
		cmds.checkBox("cbSubstring", label="Substring prefix", parent="mainLayout", value=True)
		cmds.textField("tfSubstring", parent="mainLayout", text="s100_char")

		cmds.separator(h=10, style="none", parent="mainLayout")

		# Buttons
		cmds.rowColumnLayout("buttonsLayout", numberOfColumns=2, parent="mainLayout")
		cmds.button("bExportLinks", label = "Export Links", w=200, h=30, parent="buttonsLayout", c=self.exportLinks)
		cmds.button("bImportShader", label="Link Shaders", w=200, h=30, parent="buttonsLayout", c=self.linkShaders)

		cmds.showWindow(self.name)


	# Display the help dialog
	def showHelp(self, *args):

		if cmds.window(self.help, q=True, exists=True):
			cmds.deleteUI(self.help)
		cmds.window(self.help, title="Shader Linker - Help", sizeable=True, mxb=False, toolbox=False, w=300, h=50)
		cmds.columnLayout("lHelp", p=self.help)

		cmds.text(p="lHelp", label=self.instructions, align="left")

		cmds.showWindow(self.help)


	# Export shader links into a db
	def exportLinks(self, *args):

		# Get .db path
		fileFilters = "Database (*.db *.sqlite) (*.db *.sqlite)"
		path = cmds.fileDialog2(fileMode=0, caption="Export Links", dialogStyle=2, okCaption="Save", startingDirectory=self.basedir, fileFilter=fileFilters)
		if path == None:
			return
		cmds.textFieldButtonGrp("tfbDBPath", e=True, tx=path[0])

		# Open .db
		dbConnection = sqlite3.connect(path[0])
		dbCursor = dbConnection.cursor()

		# Create table
		dbCursor.execute('''CREATE TABLE links (mesh text, shader text)''')
		
		# Write a row for every mesh into .db
		meshes = cmds.ls(type="mesh")

		for mesh in meshes:

			# Get shader
			#shadingEngine = cmds.listHistory(mesh, f=True, pruneDagObjects=True)
			shadingEngine = cmds.listConnections(mesh, type="shadingEngine") # Works better :)

			if(cmds.polyEvaluate(mesh, f=True) == 0 or shadingEngine == None):
				continue

			shader = cmds.ls(cmds.listConnections(shadingEngine[0]),materials=True)

			if shader == None or len(shader) == 0:
				continue
			else:
				shader == shader[0][0]

			if cmds.checkBox("cbSubstring", q=True, value=True):
				substring = cmds.textField("tfSubstring", q=True, text=True)
				mesh = mesh[len(substring):]

			print "Saving link for '" + mesh + "'"
			# Write into .db
			dbCursor.execute("INSERT INTO links VALUES('%s', '%s')" %(mesh, shader[0]))


		# Commit changes & close connection
		dbConnection.commit()
		dbConnection.close()

		print "Done Exporting..."


	# Set ShaderPath
	def setShaderPath(self, *args):

		fileFilters = "Maya File(*.mb *.ma)"
		path = cmds.fileDialog2(fileMode=1, caption="Set Shader Path", dialogStyle=2, okCaption="Save", startingDirectory=self.basedir, fileFilter=fileFilters)
		if path == None:
			return
		cmds.textFieldButtonGrp("tfbShaderPath", e=True, tx=path[0])


	# Set DB Path
	def setDBPath(self, *args):

		fileFilters = "Database (*.db *.sqlite) (*.db *.sqlite)"
		path = cmds.fileDialog2(fileMode=1, caption="Open .db File", dialogStyle=2, okCaption="Open", startingDirectory=self.basedir, fileFilter=fileFilters)
		if path == None:
			return
		cmds.textFieldButtonGrp("tfbDBPath", e=True, tx=path[0])


	# Link Shaders
	def linkShaders(self, *args):

		links = self.getLinksFromDB()

		if links == None:
			return

		selection = cmds.ls(sl=True)
		if len(selection) > 0:
			selection = cmds.listRelatives(selection, allDescendents=True, noIntermediate=True)

		# If shader file is available import it
		shaderPath = cmds.textFieldButtonGrp("tfbShaderPath", q=True, tx=True)
		if len(shaderPath) > 0:
			cmds.file(shaderPath, i=True)
			cmds.textFieldButtonGrp("tfbShaderPath", e=True, tx="")

		# Link shaders
		for link in links:
			mesh = link[0]
			shader = link[1]

			if cmds.checkBox("cbSubstring", q=True, value=True):
				substring = cmds.textField("tfSubstring", q=True, text=True)
				mesh = substring + mesh

			if cmds.objExists(mesh):
				cmds.select(mesh)
				cmds.hyperShade(assign=shader)
				print "'" + mesh + "' linked"

		print "Finished linking."


	# Get Shaders
	def getLinksFromDB(self, *args):
		
		meshes = []
		links = []

		# Open .db
		path = cmds.textFieldButtonGrp("tfbDBPath", q=True, tx=True)
		if len(path) == 0:
			return None

		dbConnection = sqlite3.connect(path)
		dbCursor = dbConnection.cursor()

		# Get every row and save it into a list
		if (cmds.checkBox("cbSelection", q=True, value=True) == True):
			meshes = cmds.ls(sl=True)
			meshes = cmds.listRelatives(meshes, shapes=True)
		else:
			meshes = cmds.ls(type="mesh")

		for mesh in meshes:

			if cmds.checkBox("cbSubstring", q=True, value=True):
				substring = cmds.textField("tfSubstring", q=True, text=True)
				mesh = mesh[len(substring):]

			searchTerm = (mesh,)
			iterator = dbCursor.execute("SELECT * FROM links WHERE mesh=?", searchTerm)
			link = iterator.fetchone()

			if not link:
				cmds.warning(mesh + " not linked.")
				continue

			links.append(link)

		# Close connection & return links
		dbConnection.close()
		return links


	# Delete Help Window if open
	def onClose(self, *args):

		if(cmds.window(self.help, q=True, exists=True)):
			cmds.deleteUI(self.help)