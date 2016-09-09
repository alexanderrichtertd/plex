import pymel.core as pm
from alShaders import *

class AEalHairTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["melanin"] = Param("melanin", "Melanin", "The melanin content of the hair fibre. Use this to generated natural colors for mammalian hair. 0 will give white hair, 0.2-04 blonde, 0.4-0.6 red, 0.6-0.8 brown and 0.", "float", presets=None)
		self.params["dyeColor"] = Param("dyeColor", "Dye color", "Color tint to apply to the hair. You can also plug a MayaRamp in here to define the color along the lenght of the hair.", "rgb", presets=None)
		self.params["specularWidth"] = Param("specularWidth", "Highlight width", "The width of the hair highlights, essentially how shiny the hair appears. Values in the range 1-7 are sensible for human hair.", "float", presets=None)
		self.params["specularShift"] = Param("specularShift", "Highlight shift", "How much the highlights are shifted along the hair by the cuticles on the hair fibre. Generally this wants to be 1 to 1.5 times the value of the Width parameter.", "float", presets=None)
		self.params["opacity"] = Param("opacity", "Opacity", "Opacity of the hair fibre. Setting this to anything other than white can make the shader very slow. If you want to get a softer look and resolve fine hair better, it is often a better idea to raise your AA samples instead.", "rgb", presets=None)
		self.params["randomTangent"] = Param("randomTangent", "Tangent", "Adds a random offset to the hair tangent which can be useful for breaking up uniform-looking grooms. Note that this value is dependent on your scene scale.", "float", presets=None)
		self.params["randomMelanin"] = Param("randomMelanin", "Melanin", "Adds a random offset to the melanin content of the hair. Values from 0.05 to 0.2 give a very natural color variation.", "float", presets=None)
		self.params["randomHue"] = Param("randomHue", "Dye hue", "Add a random offest to the hue of the Dye color.", "float", presets=None)
		self.params["randomSaturation"] = Param("randomSaturation", "Dye saturation", "Add a random offest to the saturation of the Dye color.", "float", presets=None)
		self.params["glintRolloff"] = Param("glintRolloff", "Glint rolloff", "Controls the rolloff of the caustic glints in the hair. Lower values make the glints more pingy, higher values make them softer and less apparent.", "float", presets=None)
		self.params["transmissionRolloff"] = Param("transmissionRolloff", "Transmission rolloff", "Controls the rolloff of the transmission highlight. Essentially, if you want the transmission highlight to only appear when the light is directly behind the hair, set this value to 10 or lower.", "float", presets=None)
		self.params["diffuseStrength"] = Param("diffuseStrength", "Strength", "Multiplier on the strength of the diffuse illumination.", "float", presets=None)
		self.params["diffuseColor"] = Param("diffuseColor", "Tint", "Tint on the diffuse illumination. This is multiplied on top of the Fibre color specified above.", "rgb", presets=None)
		self.params["diffuseScatteringMode"] = Param("diffuseScatteringMode", "Scattering mode", "The algorithm to use for diffuse calculation. dual-scattering is a realistic approximation of multiple scattering in hair and is more appropriate for long, realistic hair.", "enum", presets=None)
		self.params["diffuseForward"] = Param("diffuseForward", "Forward scattering", "Controls the amount of light bleeding through the hair in dual-scattering mode.", "float", presets=None)
		self.params["diffuseBack"] = Param("diffuseBack", "Back scattering", "Controls the amount of light kicked back from the hair in dual-scattering mode.", "float", presets=None)
		self.params["specular1Strength"] = Param("specular1Strength", "Strength", "Multiplier on the strength of this lobe", "float", presets=None)
		self.params["specular1Color"] = Param("specular1Color", "Tint", "Color tint on the color automatically generated for this lobe by the Fibre color settings.", "rgb", presets=None)
		self.params["specular1WidthScale"] = Param("specular1WidthScale", "Width scale", "Multiplier on the width of this lobe's highlight.", "float", presets=None)
		self.params["specular1Shift"] = Param("specular1Shift", "Shift offset", "Offset on the shift of this lobe's highlight.", "float", presets=None)
		self.params["specular2Strength"] = Param("specular2Strength", "Strength", "Multiplier on the strength of this lobe", "float", presets=None)
		self.params["specular2Color"] = Param("specular2Color", "Tint", "Color tint on the color automatically generated for this lobe by the Fibre color settings.", "rgb", presets=None)
		self.params["specular2WidthScale"] = Param("specular2WidthScale", "Width scale", "Multiplier on the width of this lobe's highlight.", "float", presets=None)
		self.params["specular2Shift"] = Param("specular2Shift", "Shift offset", "Offset on the shift of this lobe's highlight.", "float", presets=None)
		self.params["glintStrength"] = Param("glintStrength", "Glint strength", "Strength of the caustic glints. Sensible values are in the range 1-5.", "float", presets=None)
		self.params["transmissionStrength"] = Param("transmissionStrength", "Strength", "Multiplier on the strength of this lobe", "float", presets=None)
		self.params["transmissionColor"] = Param("transmissionColor", "Tint", "Color tint on the color automatically generated for this lobe by the Fibre color settings.", "rgb", presets=None)
		self.params["transmissionWidthScale"] = Param("transmissionWidthScale", "Width scale", "Multiplier on the width of this lobe's highlight.", "float", presets=None)
		self.params["transmissionShift"] = Param("transmissionShift", "Shift offset", "Offset on the shift of this lobe's highlight.", "float", presets=None)
		self.params["id1"] = Param("id1", "id1", "Color to be output in id_1 AOV.", "rgb", presets=None)
		self.params["id2"] = Param("id2", "id2", "Color to be output in id_2 AOV.", "rgb", presets=None)
		self.params["id3"] = Param("id3", "id3", "Color to be output in id_3 AOV.", "rgb", presets=None)
		self.params["id4"] = Param("id4", "id4", "Color to be output in id_4 AOV.", "rgb", presets=None)
		self.params["id5"] = Param("id5", "id5", "Color to be output in id_5 AOV.", "rgb", presets=None)
		self.params["id6"] = Param("id6", "id6", "Color to be output in id_6 AOV.", "rgb", presets=None)
		self.params["id7"] = Param("id7", "id7", "Color to be output in id_7 AOV.", "rgb", presets=None)
		self.params["id8"] = Param("id8", "id8", "Color to be output in id_8 AOV.", "rgb", presets=None)
		self.params["aov_diffuse_color"] = Param("aov_diffuse_color", "Diffuse color", "", "rgb", presets=None)
		self.params["aov_direct_diffuse"] = Param("aov_direct_diffuse", "Direct diffuse", "", "rgb", presets=None)
		self.params["aov_indirect_diffuse"] = Param("aov_indirect_diffuse", "Indirect diffuse", "", "rgb", presets=None)
		self.params["aov_direct_local"] = Param("aov_direct_local", "Direct local", "", "rgb", presets=None)
		self.params["aov_indirect_local"] = Param("aov_indirect_local", "Indirect local", "", "rgb", presets=None)
		self.params["aov_direct_global"] = Param("aov_direct_global", "Direct global", "", "rgb", presets=None)
		self.params["aov_indirect_global"] = Param("aov_indirect_global", "Indirect global", "", "rgb", presets=None)
		self.params["aov_direct_specular"] = Param("aov_direct_specular", "Direct specular", "", "rgb", presets=None)
		self.params["aov_indirect_specular"] = Param("aov_indirect_specular", "Indirect specular", "", "rgb", presets=None)
		self.params["aov_direct_specular_2"] = Param("aov_direct_specular_2", "Direct specular 2", "", "rgb", presets=None)
		self.params["aov_indirect_specular_2"] = Param("aov_indirect_specular_2", "Indirect specular 2", "", "rgb", presets=None)
		self.params["aov_direct_glint"] = Param("aov_direct_glint", "Direct glint", "", "rgb", presets=None)
		self.params["aov_indirect_glint"] = Param("aov_indirect_glint", "Indirect glint", "", "rgb", presets=None)
		self.params["aov_direct_transmission"] = Param("aov_direct_transmission", "Direct transmission", "", "rgb", presets=None)
		self.params["aov_indirect_transmission"] = Param("aov_indirect_transmission", "Indirect transmission", "", "rgb", presets=None)
		self.params["aov_light_group_1"] = Param("aov_light_group_1", "Light group [1]", "", "rgb", presets=None)
		self.params["aov_light_group_2"] = Param("aov_light_group_2", "Light group [2]", "", "rgb", presets=None)
		self.params["aov_light_group_3"] = Param("aov_light_group_3", "Light group [3]", "", "rgb", presets=None)
		self.params["aov_light_group_4"] = Param("aov_light_group_4", "Light group [4]", "", "rgb", presets=None)
		self.params["aov_light_group_5"] = Param("aov_light_group_5", "Light group [5]", "", "rgb", presets=None)
		self.params["aov_light_group_6"] = Param("aov_light_group_6", "Light group [6]", "", "rgb", presets=None)
		self.params["aov_light_group_7"] = Param("aov_light_group_7", "Light group [7]", "", "rgb", presets=None)
		self.params["aov_light_group_8"] = Param("aov_light_group_8", "Light group [8]", "", "rgb", presets=None)
		self.params["aov_id_1"] = Param("aov_id_1", "ID [1]", "", "rgb", presets=None)
		self.params["aov_id_2"] = Param("aov_id_2", "ID [2]", "", "rgb", presets=None)
		self.params["aov_id_3"] = Param("aov_id_3", "ID [3]", "", "rgb", presets=None)
		self.params["aov_id_4"] = Param("aov_id_4", "ID [4]", "", "rgb", presets=None)
		self.params["aov_id_5"] = Param("aov_id_5", "ID [5]", "", "rgb", presets=None)
		self.params["aov_id_6"] = Param("aov_id_6", "ID [6]", "", "rgb", presets=None)
		self.params["aov_id_7"] = Param("aov_id_7", "ID [7]", "", "rgb", presets=None)
		self.params["aov_id_8"] = Param("aov_id_8", "ID [8]", "", "rgb", presets=None)
		self.params["dualDepth"] = Param("dualDepth", "Brute force bounces", "Number of brute-force, inter-hair bounces to calculate before falling back to dual scattering. THIS PARAMETER IS DEPRECATED AND WILL BE REMOVED IN A FUTURE RELEASE.", "int", presets=None)
		self.params["diffuseIndirectStrength"] = Param("diffuseIndirectStrength", "Diffuse indirect strength", "Multiplier on the intensity of the indirect diffuse illumination. The default value of 0 disables indirect illumination on the hair since in most cases you don't need it and it can be quite expensive.", "float", presets=None)
		self.params["extraSamplesDiffuse"] = Param("extraSamplesDiffuse", "Diffuse extra samples", "Number of extra samples to take when calculating indirect diffuse illumination.", "int", presets=None)
		self.params["glossyIndirectStrength"] = Param("glossyIndirectStrength", "Glossy indirect strength", "Multiplier on the intensity of the indirect glossy illumination. The default value of 0 disables indirect illumination on the hair since in most cases you don't need it and it can be quite expensive.", "float", presets=None)
		self.params["extraSamplesGlossy"] = Param("extraSamplesGlossy", "Glossy extra samples", "Number of extra samples to take when calculating indirect glossy illumination.", "int", presets=None)
		self.params["uparam"] = Param("uparam", "U param", "Name of the user data that contains the U coordinate of the surface for texturing.", "string", presets=None)
		self.params["vparam"] = Param("vparam", "V param", "Name of the user data that contains the V coordinate of the surface for texturing.", "string", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.beginLayout("Fibre properties", collapse=False)
		self.addCustomFlt("melanin")
		self.addCustomRgb("dyeColor")
		self.addCustomFlt("specularWidth")
		self.addCustomFlt("specularShift")
		self.addCustomRgb("opacity")
		self.beginLayout("Randomize", collapse=True)
		self.addCustomFlt("randomTangent")
		self.addCustomFlt("randomMelanin")
		self.addCustomFlt("randomHue")
		self.addCustomFlt("randomSaturation")
		self.endLayout() # END Randomize
		self.beginLayout("Advanced", collapse=True)
		self.addCustomFlt("glintRolloff")
		self.addCustomFlt("transmissionRolloff")
		self.endLayout() # END Advanced
		self.endLayout() # END Fibre properties
		self.beginLayout("Diffuse", collapse=False)
		self.addCustomFlt("diffuseStrength")
		self.addCustomRgb("diffuseColor")
		self.addControl("diffuseScatteringMode", label="Scattering mode", annotation="The algorithm to use for diffuse calculation. dual-scattering is a realistic approximation of multiple scattering in hair and is more appropriate for long, realistic hair.")
		self.addCustomFlt("diffuseForward")
		self.addCustomFlt("diffuseBack")
		self.endLayout() # END Diffuse
		self.beginLayout("Specular 1", collapse=False)
		self.addCustomFlt("specular1Strength")
		self.addCustomRgb("specular1Color")
		self.addCustomFlt("specular1WidthScale")
		self.addCustomFlt("specular1Shift")
		self.endLayout() # END Specular 1
		self.beginLayout("Specular 2", collapse=False)
		self.addCustomFlt("specular2Strength")
		self.addCustomRgb("specular2Color")
		self.addCustomFlt("specular2WidthScale")
		self.addCustomFlt("specular2Shift")
		self.addCustomFlt("glintStrength")
		self.endLayout() # END Specular 2
		self.beginLayout("Transmission", collapse=False)
		self.addCustomFlt("transmissionStrength")
		self.addCustomRgb("transmissionColor")
		self.addCustomFlt("transmissionWidthScale")
		self.addCustomFlt("transmissionShift")
		self.endLayout() # END Transmission
		self.beginLayout("IDs", collapse=True)
		self.addCustomRgb("id1")
		self.addCustomRgb("id2")
		self.addCustomRgb("id3")
		self.addCustomRgb("id4")
		self.addCustomRgb("id5")
		self.addCustomRgb("id6")
		self.addCustomRgb("id7")
		self.addCustomRgb("id8")
		self.endLayout() # END IDs
		self.beginLayout("AOVs", collapse=True)
		self.addControl("aov_diffuse_color", label="Diffuse color", annotation="")
		self.addControl("aov_direct_diffuse", label="Direct diffuse", annotation="")
		self.addControl("aov_indirect_diffuse", label="Indirect diffuse", annotation="")
		self.addControl("aov_direct_local", label="Direct local", annotation="")
		self.addControl("aov_indirect_local", label="Indirect local", annotation="")
		self.addControl("aov_direct_global", label="Direct global", annotation="")
		self.addControl("aov_indirect_global", label="Indirect global", annotation="")
		self.addControl("aov_direct_specular", label="Direct specular", annotation="")
		self.addControl("aov_indirect_specular", label="Indirect specular", annotation="")
		self.addControl("aov_direct_specular_2", label="Direct specular 2", annotation="")
		self.addControl("aov_indirect_specular_2", label="Indirect specular 2", annotation="")
		self.addControl("aov_direct_glint", label="Direct glint", annotation="")
		self.addControl("aov_indirect_glint", label="Indirect glint", annotation="")
		self.addControl("aov_direct_transmission", label="Direct transmission", annotation="")
		self.addControl("aov_indirect_transmission", label="Indirect transmission", annotation="")
		self.addControl("aov_light_group_1", label="Light group [1]", annotation="")
		self.addControl("aov_light_group_2", label="Light group [2]", annotation="")
		self.addControl("aov_light_group_3", label="Light group [3]", annotation="")
		self.addControl("aov_light_group_4", label="Light group [4]", annotation="")
		self.addControl("aov_light_group_5", label="Light group [5]", annotation="")
		self.addControl("aov_light_group_6", label="Light group [6]", annotation="")
		self.addControl("aov_light_group_7", label="Light group [7]", annotation="")
		self.addControl("aov_light_group_8", label="Light group [8]", annotation="")
		self.addControl("aov_id_1", label="ID [1]", annotation="")
		self.addControl("aov_id_2", label="ID [2]", annotation="")
		self.addControl("aov_id_3", label="ID [3]", annotation="")
		self.addControl("aov_id_4", label="ID [4]", annotation="")
		self.addControl("aov_id_5", label="ID [5]", annotation="")
		self.addControl("aov_id_6", label="ID [6]", annotation="")
		self.addControl("aov_id_7", label="ID [7]", annotation="")
		self.addControl("aov_id_8", label="ID [8]", annotation="")
		self.endLayout() # END AOVs
		self.beginLayout("Advanced", collapse=True)
		self.addControl("dualDepth", label="Brute force bounces", annotation="Number of brute-force, inter-hair bounces to calculate before falling back to dual scattering. THIS PARAMETER IS DEPRECATED AND WILL BE REMOVED IN A FUTURE RELEASE.")
		self.addCustomFlt("diffuseIndirectStrength")
		self.addControl("extraSamplesDiffuse", label="Diffuse extra samples", annotation="Number of extra samples to take when calculating indirect diffuse illumination.")
		self.addCustomFlt("glossyIndirectStrength")
		self.addControl("extraSamplesGlossy", label="Glossy extra samples", annotation="Number of extra samples to take when calculating indirect glossy illumination.")
		self.addControl("uparam", label="U param", annotation="Name of the user data that contains the U coordinate of the surface for texturing.")
		self.addControl("vparam", label="V param", annotation="Name of the user data that contains the V coordinate of the surface for texturing.")
		self.endLayout() # END Advanced

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()