import pymel.core as pm
from alShaders import *

class AEalJitterColorTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["input"] = Param("input", "Input", "The input color to be jittered.", "rgb", presets=None)
		self.params["minSaturation"] = Param("minSaturation", "Min Saturation", "Minimum random saturation scale to apply.", "float", presets=None)
		self.params["maxSaturation"] = Param("maxSaturation", "Max Saturation", "Maximum random saturation scale to apply.", "float", presets=None)
		self.params["minGain"] = Param("minGain", "Min Gain", "Minimum random gain to apply.", "float", presets=None)
		self.params["maxGain"] = Param("maxGain", "Max Gain", "Maximum random gain to apply.", "float", presets=None)
		self.params["minHueOffset"] = Param("minHueOffset", "Min Hue Offset", "Minimum hue offset to apply.", "float", presets=None)
		self.params["maxHueOffset"] = Param("maxHueOffset", "Max Hue Offset", "Maximum hue offset to apply.", "float", presets=None)
		self.params["clamp"] = Param("clamp", "Clamp", "If enabled, the output color will be clamped to 0-1.", "bool", presets=None)
		self.params["signal"] = Param("signal", "Signal", "Signal to use to drive the randomization. This wants to be a unique value per object such as the object id.", "float", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addCustomRgb("input")
		self.addCustomFlt("minSaturation")
		self.addCustomFlt("maxSaturation")
		self.addCustomFlt("minGain")
		self.addCustomFlt("maxGain")
		self.addCustomFlt("minHueOffset")
		self.addCustomFlt("maxHueOffset")
		self.addControl("clamp", label="Clamp", annotation="If enabled, the output color will be clamped to 0-1.")
		self.addCustomFlt("signal")

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
