import pymel.core as pm
from alShaders import *

class AEalLayerFloatTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["layer1"] = Param("layer1", "Layer 1", "The background layer (will be blended over black if its alpha is not 1.", "float", presets=None)
		self.params["layer1a"] = Param("layer1a", "Layer 1 Alpha", "The alpha of the background layer", "float", presets=None)
		self.params["layer2"] = Param("layer2", "Layer 2", "The value plugged in here will be blended over the layers below according to its alpha.", "float", presets=None)
		self.params["layer2a"] = Param("layer2a", "Layer 2 Alpha", "The alpha used to blend this layer over the layers below.", "float", presets=None)
		self.params["layer3"] = Param("layer3", "Layer 3", "The value plugged in here will be blended over the layers below according to its alpha.", "float", presets=None)
		self.params["layer3a"] = Param("layer3a", "Layer 3 Alpha", "The alpha used to blend this layer over the layers below.", "float", presets=None)
		self.params["layer4"] = Param("layer4", "Layer 4", "The value plugged in here will be blended over the layers below according to its alpha.", "float", presets=None)
		self.params["layer4a"] = Param("layer4a", "Layer 4 Alpha", "The alpha used to blend this layer over the layers below.", "float", presets=None)
		self.params["layer5"] = Param("layer5", "Layer 5", "The value plugged in here will be blended over the layers below according to its alpha.", "float", presets=None)
		self.params["layer5a"] = Param("layer5a", "Layer 5 Alpha", "The alpha used to blend this layer over the layers below.", "float", presets=None)
		self.params["layer6"] = Param("layer6", "Layer 6", "The value plugged in here will be blended over the layers below according to its alpha.", "float", presets=None)
		self.params["layer6a"] = Param("layer6a", "Layer 6 Alpha", "The alpha used to blend this layer over the layers below.", "float", presets=None)
		self.params["layer7"] = Param("layer7", "Layer 7", "The value plugged in here will be blended over the layers below according to its alpha.", "float", presets=None)
		self.params["layer7a"] = Param("layer7a", "Layer 7 Alpha", "The alpha used to blend this layer over the layers below.", "float", presets=None)
		self.params["layer8"] = Param("layer8", "Layer 8", "The value plugged in here will be blended over the layers below according to its alpha.", "float", presets=None)
		self.params["layer8a"] = Param("layer8a", "Layer 8 Alpha", "The alpha used to blend this layer over the layers below.", "float", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addCustomFlt("layer1")
		self.addCustomFlt("layer1a")
		self.addCustomFlt("layer2")
		self.addCustomFlt("layer2a")
		self.addCustomFlt("layer3")
		self.addCustomFlt("layer3a")
		self.addCustomFlt("layer4")
		self.addCustomFlt("layer4a")
		self.addCustomFlt("layer5")
		self.addCustomFlt("layer5a")
		self.addCustomFlt("layer6")
		self.addCustomFlt("layer6a")
		self.addCustomFlt("layer7")
		self.addCustomFlt("layer7a")
		self.addCustomFlt("layer8")
		self.addCustomFlt("layer8a")

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
