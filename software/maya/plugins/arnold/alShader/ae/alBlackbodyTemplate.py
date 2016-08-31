import pymel.core as pm
from alShaders import *

class AEalBlackbodyTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["temperature"] = Param("temperature", "Temperature", "The temperature value used to generate the color. From low to high the spectrum goes through red, orange, yellow, white, blue.", "float", presets=None)
		self.params["strength"] = Param("strength", "Strength", "Multiplier on the brightness of the generated color.", "float", presets=None)
		self.params["physicalIntensity"] = Param("physicalIntensity", "Physical intensity", "When set to the default of 1, the full range of physical brightness will be preserved. When set to 0, the generated colors will never be brighter than white.", "float", presets=None)
		self.params["physicalExposure"] = Param("physicalExposure", "Physical exposure", "An overall exposure value to apply to the color. This is useful to preserve the physical brightness curve but get low-temperature colors into a sensible range.", "float", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addCustomFlt("temperature")
		self.addCustomFlt("strength")
		self.beginLayout("Advanced", collapse=True)
		self.addCustomFlt("physicalIntensity")
		self.addCustomFlt("physicalExposure")
		self.endLayout() # END Advanced

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
