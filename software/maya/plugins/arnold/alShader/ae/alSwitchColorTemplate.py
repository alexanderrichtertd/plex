import pymel.core as pm
from alShaders import *

class AEalSwitchColorTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["inputA"] = Param("inputA", "Input 0", "Connect a color here to have it selected by the mix value", "rgb", presets=None)
		self.params["inputB"] = Param("inputB", "Input 1", "Connect a color here to have it selected by the mix value", "rgb", presets=None)
		self.params["inputC"] = Param("inputC", "Input 2", "Connect a color here to have it selected by the mix value", "rgb", presets=None)
		self.params["inputD"] = Param("inputD", "Input 3", "Connect a color here to have it selected by the mix value", "rgb", presets=None)
		self.params["inputE"] = Param("inputE", "Input 4", "Connect a color here to have it selected by the mix value", "rgb", presets=None)
		self.params["inputF"] = Param("inputF", "Input 5", "Connect a color here to have it selected by the mix value", "rgb", presets=None)
		self.params["inputG"] = Param("inputG", "Input 6", "Connect a color here to have it selected by the mix value", "rgb", presets=None)
		self.params["inputH"] = Param("inputH", "Input 7", "Connect a color here to have it selected by the mix value", "rgb", presets=None)
		self.params["mix"] = Param("mix", "mix", "Signal that selects from one of the 8 inputs.", "float", presets=None)
		self.params["threshold"] = Param("threshold", "threshold", "Partial threshold at which the signal transitions from one input to the next.", "float", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addCustomRgb("inputA")
		self.addCustomRgb("inputB")
		self.addCustomRgb("inputC")
		self.addCustomRgb("inputD")
		self.addCustomRgb("inputE")
		self.addCustomRgb("inputF")
		self.addCustomRgb("inputG")
		self.addCustomRgb("inputH")
		self.addCustomFlt("mix")
		self.addCustomFlt("threshold")

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
