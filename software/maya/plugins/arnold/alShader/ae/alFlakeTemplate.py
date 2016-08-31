import pymel.core as pm
from alShaders import *

class AEalFlakeTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["space"] = Param("space", "space", "Select the space for normal computation. When 'world' is selected you should plug the output of this node directly into the normal override parameter of your desired lobe on alSurface.", "enum", presets=None)
		self.params["amount"] = Param("amount", "Amount", "Proportion of the surface that is covered by flakes", "float", presets=None)
		self.params["size"] = Param("size", "Size", "Size of the flakes", "float", presets=None)
		self.params["divergence"] = Param("divergence", "Divergence", "How much the flake normals diverge from the surface normal.", "float", presets=None)
		self.params["P"] = Param("P", "P", "Connect a point here to override the space used for flake calculation.", "vector", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addControl("space", label="space", annotation="Select the space for normal computation. When 'world' is selected you should plug the output of this node directly into the normal override parameter of your desired lobe on alSurface.")
		self.addCustomFlt("amount")
		self.addCustomFlt("size")
		self.addCustomFlt("divergence")
		self.addControl("P", label="P", annotation="Connect a point here to override the space used for flake calculation.")

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
