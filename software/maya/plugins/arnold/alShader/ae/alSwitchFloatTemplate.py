import pymel.core as pm
from alShaders import *

class AEalSwitchFloatTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["inputA"] = Param("inputA", "InputA", "Connect a value here to have it selected by the mix value", "float", presets=None)
		self.params["inputB"] = Param("inputB", "InputB", "Connect a value here to have it selected by the mix value", "float", presets=None)
		self.params["inputC"] = Param("inputC", "InputC", "Connect a value here to have it selected by the mix value", "float", presets=None)
		self.params["inputD"] = Param("inputD", "InputD", "Connect a value here to have it selected by the mix value", "float", presets=None)
		self.params["inputE"] = Param("inputE", "InputE", "Connect a value here to have it selected by the mix value", "float", presets=None)
		self.params["inputF"] = Param("inputF", "InputF", "Connect a value here to have it selected by the mix value", "float", presets=None)
		self.params["inputG"] = Param("inputG", "InputG", "Connect a value here to have it selected by the mix value", "float", presets=None)
		self.params["inputH"] = Param("inputH", "InputH", "Connect a value here to have it selected by the mix value", "float", presets=None)
		self.params["mix"] = Param("mix", "mix", "Signal that selects from one of the 8 inputs.", "float", presets=None)
		self.params["threshold"] = Param("threshold", "threshold", "Partial threshold at which the signal transitions from one input to the next.", "float", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addCustomFlt("inputA")
		self.addCustomFlt("inputB")
		self.addCustomFlt("inputC")
		self.addCustomFlt("inputD")
		self.addCustomFlt("inputE")
		self.addCustomFlt("inputF")
		self.addCustomFlt("inputG")
		self.addCustomFlt("inputH")
		self.addCustomFlt("mix")
		self.addCustomFlt("threshold")

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
