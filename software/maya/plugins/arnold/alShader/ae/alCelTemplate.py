import pymel.core as pm
from alShaders import *

class AEalCelTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["surfaceShader"] = Param("surfaceShader", "Surface shader", "Connect an alSurface shader here to have its diffuse component run through the ramp for cel shading.", "rgb", presets=None)
		self.params["diffuseDirectStrength"] = Param("diffuseDirectStrength", "Diffuse strength", "A multiplier on the diffuse component before being passed through the ramp. This is useful to bring your diffuse illumination into the 0-1 range required by the ramp.", "float", presets=None)
		self.params["diffuseRamp"] = Param("diffuseRamp", "Diffuse ramp", "Plug a MayaRamp node here to control the cel shading colors.", "rgb", presets=None)
		self.params["diffuseColorRamp"] = Param("diffuseColorRamp", "Diffuse color ramp", "Plug a MayaRamp node here to tint the diffuse shading.", "rgb", presets=None)
		self.params["diffuseIndirectStrength"] = Param("diffuseIndirectStrength", "Indirect diffuse strength", "Multipler on the strength of the indirect diffuse illumination.", "float", presets=None)
		self.params["diffuseIndirectSaturation"] = Param("diffuseIndirectSaturation", "Indirect diffuse saturation", "Controls the saturation of the indirect diffuse illumination. It can be useful to increase this for more stylized effects.", "float", presets=None)
		self.params["diffuseIndirectTint"] = Param("diffuseIndirectTint", "Indirect diffuse tint", "Color tint on the indirect diffuse illumination.", "rgb", presets=None)
		self.params["aov_direct_diffuse_cel"] = Param("aov_direct_diffuse_cel", "Cel Diffuse", "", "rgb", presets=None)
		self.params["aov_direct_diffuse_raw_cel"] = Param("aov_direct_diffuse_raw_cel", "Cel Raw Diffuse", "", "rgb", presets=None)
		self.params["aov_indirect_diffuse_cel"] = Param("aov_indirect_diffuse_cel", "Cel Indirect Diffuse", "", "rgb", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.beginLayout("Shading", collapse=False)
		self.addCustomRgb("surfaceShader")
		self.addCustomFlt("diffuseDirectStrength")
		self.addCustomRgb("diffuseRamp")
		self.addCustomRgb("diffuseColorRamp")
		self.addCustomFlt("diffuseIndirectStrength")
		self.addCustomFlt("diffuseIndirectSaturation")
		self.addCustomRgb("diffuseIndirectTint")
		self.endLayout() # END Shading
		self.beginLayout("AOVs", collapse=True)
		self.addControl("aov_direct_diffuse_cel", label="Cel Diffuse", annotation="")
		self.addControl("aov_direct_diffuse_raw_cel", label="Cel Raw Diffuse", annotation="")
		self.addControl("aov_indirect_diffuse_cel", label="Cel Indirect Diffuse", annotation="")
		self.endLayout() # END AOVs
		self.addBumpLayout()

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
