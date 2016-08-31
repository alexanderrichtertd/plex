import pymel.core as pm
from alShaders import *

class AEalInputVectorTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["input"] = Param("input", "Input", "The vector from the shader globals to output. When User is selected, the user data vector named in the User name parameter will be output. When Custom is selected, the vector specified by the Custom parameter will be output.", "enum", presets=None)
		self.params["userName"] = Param("userName", "User name", "Enter the name of a user data vector to output.", "string", presets=None)
		self.params["vector"] = Param("vector", "Custom", "A manually-specified vector to output.", "vector", presets=None)
		self.params["type"] = Param("type", "Type", "How to treat the vector when transorming it.", "enum", presets=None)
		self.params["matrix"] = Param("matrix", "Matrix", "A transformation matrix to apply to the vector. This can be useful for animating the position or scale of a point to drive a fractal.", "matrix", presets=None)
		self.params["coordinates"] = Param("coordinates", "Coordinates", "Coordinate system to interpret the vector as being in (result will be transformed to cartesian before being output).", "enum", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addControl("input", label="Input", annotation="The vector from the shader globals to output. When User is selected, the user data vector named in the User name parameter will be output. When Custom is selected, the vector specified by the Custom parameter will be output.")
		self.addControl("userName", label="User name", annotation="Enter the name of a user data vector to output.")
		self.addControl("vector", label="Custom", annotation="A manually-specified vector to output.")
		self.addControl("type", label="Type", annotation="How to treat the vector when transorming it.")
		self.beginLayout("Transform", collapse=True)
		self.addControl("matrix", label="Matrix", annotation="A transformation matrix to apply to the vector. This can be useful for animating the position or scale of a point to drive a fractal.")
		self.addControl("coordinates", label="Coordinates", annotation="Coordinate system to interpret the vector as being in (result will be transformed to cartesian before being output).")
		self.endLayout() # END Transform

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
