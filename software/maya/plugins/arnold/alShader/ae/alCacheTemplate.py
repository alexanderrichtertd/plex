import pymel.core as pm
from alShaders import *

class AEalCacheTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["input"] = Param("input", "input", "The network you plug in here will be evaluated once and then have its result cached if it is reused in multiple outputs.", "rgb", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addCustomRgb("input")

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
