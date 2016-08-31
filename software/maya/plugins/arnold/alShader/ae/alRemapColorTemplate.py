import pymel.core as pm
from alShaders import *

class AEalRemapColorTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["input"] = Param("input", "Input", "Input color to remap.", "rgb", presets=None)
		self.params["gamma"] = Param("gamma", "Gamma", "Gamma value to apply to input.", "float", presets=None)
		self.params["saturation"] = Param("saturation", "Saturation", "Saturation to apply to the input.", "float", presets=None)
		self.params["hueOffset"] = Param("hueOffset", "Hue offset", "Hue offset to apply to the input.", "float", presets=None)
		self.params["contrast"] = Param("contrast", "Contrast", "Contrast value to apply.", "float", presets=None)
		self.params["contrastPivot"] = Param("contrastPivot", "Pivot", "Value around which to pivot the contrast adjustment.", "float", presets=None)
		self.params["gain"] = Param("gain", "Gain", "Gain multiplier to apply to the input.", "float", presets=None)
		self.params["exposure"] = Param("exposure", "Exposure", "Exposure adjustment to apply to the input, i.e. input * 2^exposure.", "float", presets=None)
		self.params["mask"] = Param("mask", "Mask", "Use this to mask off the adjustment. This can be useful for only adjusting a certain region of a texture for instance.", "float", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addCustomRgb("input")
		self.addCustomFlt("gamma")
		self.addCustomFlt("saturation")
		self.addCustomFlt("hueOffset")
		self.beginLayout("Contrast", collapse=True)
		self.addCustomFlt("contrast")
		self.addCustomFlt("contrastPivot")
		self.endLayout() # END Contrast
		self.addCustomFlt("gain")
		self.addCustomFlt("exposure")
		self.addCustomFlt("mask")

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
