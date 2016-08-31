import pymel.core as pm
from alShaders import *

class AEalTriplanarTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["input"] = Param("input", "Background", "Background color over which to project the texture.", "rgb", presets=None)
		self.params["texture"] = Param("texture", "Texture", "The texture image to project over the background.", "string", presets=None)
		self.params["space"] = Param("space", "Space", "Space in which to project the texture.", "enum", presets=None)
		self.params["normal"] = Param("normal", "Normal", "Normal to use for projection.", "enum", presets=None)
		self.params["tiling"] = Param("tiling", "Tiling", "Tiling pattern. regular gives a regular grid, cellnoise gives a random pattern.", "enum", presets=None)
		self.params["frequency"] = Param("frequency", "Frequency", "Frequency of the pattern. Higher numbers give more repetions, lower numbers give less.", "float", presets=None)
		self.params["blendSoftness"] = Param("blendSoftness", "Blend Softness", "The softness of the blends.", "float", presets=None)
		self.params["cellSoftness"] = Param("cellSoftness", "Cell Softness", "The softness of the cell borders.", "float", presets=None)
		self.params["scalex"] = Param("scalex", "X Scale", "", "float", presets=None)
		self.params["scaley"] = Param("scaley", "Y Scale", "", "float", presets=None)
		self.params["scalez"] = Param("scalez", "Z Scale", "", "float", presets=None)
		self.params["offsetx"] = Param("offsetx", "X Offset", "", "float", presets=None)
		self.params["offsety"] = Param("offsety", "Y Offset", "", "float", presets=None)
		self.params["offsetz"] = Param("offsetz", "Z Offset", "", "float", presets=None)
		self.params["rotx"] = Param("rotx", "X Rotation", "", "float", presets=None)
		self.params["roty"] = Param("roty", "Y Rotation", "", "float", presets=None)
		self.params["rotz"] = Param("rotz", "Z Rotation", "", "float", presets=None)
		self.params["rotjitterx"] = Param("rotjitterx", "X Rotation Jitter", "", "float", presets=None)
		self.params["rotjittery"] = Param("rotjittery", "Y Rotation Jitter", "", "float", presets=None)
		self.params["rotjitterz"] = Param("rotjitterz", "Z Rotation Jitter", "", "float", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addCustomRgb("input")
		self.addControl("texture", label="Texture", annotation="The texture image to project over the background.")
		self.addControl("space", label="Space", annotation="Space in which to project the texture.")
		self.addControl("normal", label="Normal", annotation="Normal to use for projection.")
		self.addControl("tiling", label="Tiling", annotation="Tiling pattern. regular gives a regular grid, cellnoise gives a random pattern.")
		self.addCustomFlt("frequency")
		self.beginLayout("Blending", collapse=False)
		self.addCustomFlt("blendSoftness")
		self.addCustomFlt("cellSoftness")
		self.endLayout() # END Blending
		self.beginLayout("Positioning", collapse=True)
		self.addCustomFlt("scalex")
		self.addCustomFlt("scaley")
		self.addCustomFlt("scalez")
		self.addCustomFlt("offsetx")
		self.addCustomFlt("offsety")
		self.addCustomFlt("offsetz")
		self.addCustomFlt("rotx")
		self.addCustomFlt("roty")
		self.addCustomFlt("rotz")
		self.addCustomFlt("rotjitterx")
		self.addCustomFlt("rotjittery")
		self.addCustomFlt("rotjitterz")
		self.endLayout() # END Positioning

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
