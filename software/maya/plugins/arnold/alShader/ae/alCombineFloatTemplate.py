import pymel.core as pm
from alShaders import *

class AEalCombineFloatTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["input1"] = Param("input1", "input1", "The first input to combine", "float", presets=None)
		self.params["input2"] = Param("input2", "input2", "The second input to combine", "float", presets=None)
		self.params["input3"] = Param("input3", "input3", "The third input used as a mix value when lerp mode is selected.", "float", presets=None)
		self.params["combineOp"] = Param("combineOp", "Combine Op", "The operation to use to combine inputs 1 and 2.", "enum", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addCustomFlt("input1")
		self.addCustomFlt("input2")
		self.addCustomFlt("input3")
		self.addControl("combineOp", label="Combine Op", annotation="The operation to use to combine inputs 1 and 2.")

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
