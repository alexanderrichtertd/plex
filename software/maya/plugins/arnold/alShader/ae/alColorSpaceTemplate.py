import pymel.core as pm
from alShaders import *

class AEalColorSpaceTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["input"] = Param("input", "input", "Color to be transformed.", "rgb", presets=None)
		self.params["sourceSpace"] = Param("sourceSpace", "Source space", "Source color space. The input will be transformed from this space to linear Rec.709.", "enum", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addCustomRgb("input")
		self.addControl("sourceSpace", label="Source space", annotation="Source color space. The input will be transformed from this space to linear Rec.709.")

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
