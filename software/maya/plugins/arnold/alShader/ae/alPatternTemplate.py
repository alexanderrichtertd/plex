import pymel.core as pm
from alShaders import *

class AEalPatternTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["space"] = Param("space", "Space", "Space to generate the pattern in.", "enum", presets=None)
		self.params["axis"] = Param("axis", "Axis", "Axis to generate the pattern along.", "enum", presets=None)
		self.params["shape"] = Param("shape", "Shape", "Pattern to generate.", "enum", presets=None)
		self.params["frequency"] = Param("frequency", "Frequency", "Frequency of the pattern.", "float", presets=None)
		self.params["offset"] = Param("offset", "Offset", "Offset of the pattern. You can plug a noise in here to get warped patterns.", "float", presets=None)
		self.params["RMPinputMin"] = Param("RMPinputMin", "Input min", "Sets the minimum input value. Use this to pull values outside of 0-1 into a 0-1 range.", "float", presets=None)
		self.params["RMPinputMax"] = Param("RMPinputMax", "Input max", "Sets the maximum input value. Use this to pull values outside of 0-1 into a 0-1 range.", "float", presets=None)
		self.params["RMPcontrast"] = Param("RMPcontrast", "Contrast", "Scales the contrast of the input signal.", "float", presets=None)
		self.params["RMPcontrastPivot"] = Param("RMPcontrastPivot", "Pivot", "Sets the pivot point around which the input signal is contrasted.", "float", presets=None)
		self.params["RMPbias"] = Param("RMPbias", "Bias", "Bias the signal higher or lower. Values less than 0.5 push the average lower, values higher than 0.5 push it higher.", "float", presets=None)
		self.params["RMPgain"] = Param("RMPgain", "Gain", "Adds gain to the signal, in effect a different form of contrast. Values less than 0.5 increase the gain, values greater than 0.5 decrease it.", "float", presets=None)
		self.params["RMPoutputMin"] = Param("RMPoutputMin", "Output min", "Sets the minimum value of the output. Use this to scale a 0-1 signal to a new range.", "float", presets=None)
		self.params["RMPoutputMax"] = Param("RMPoutputMax", "Output max", "Sets the maximum value of the output. Use this to scale a 0-1 signal to a new range.", "float", presets=None)
		self.params["RMPclampEnable"] = Param("RMPclampEnable", "Enable", "When enabled, will clamp the output to Min-Max.", "bool", presets=None)
		self.params["RMPthreshold"] = Param("RMPthreshold", "Expand", "When enabled, will expand the clamped range to 0-1 after clamping.", "bool", presets=None)
		self.params["RMPclampMin"] = Param("RMPclampMin", "Min", "Minimum value to clamp to.", "float", presets=None)
		self.params["RMPclampMax"] = Param("RMPclampMax", "Max", "Maximum value to clamp to.", "float", presets=None)
		self.params["color1"] = Param("color1", "Color 1", "Color to use when the pattern value is 0.", "rgb", presets=None)
		self.params["color2"] = Param("color2", "Color 2", "Color to use when the pattern value is 1.", "rgb", presets=None)
		self.params["P"] = Param("P", "P", "", "vector", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addControl("space", label="Space", annotation="Space to generate the pattern in.")
		self.addControl("axis", label="Axis", annotation="Axis to generate the pattern along.")
		self.addControl("shape", label="Shape", annotation="Pattern to generate.")
		self.addCustomFlt("frequency")
		self.addCustomFlt("offset")
		self.beginLayout("Remap", collapse=True)
		self.addCustomFlt("RMPinputMin")
		self.addCustomFlt("RMPinputMax")
		self.beginLayout("Contrast", collapse=False)
		self.addCustomFlt("RMPcontrast")
		self.addCustomFlt("RMPcontrastPivot")
		self.endLayout() # END Contrast
		self.beginLayout("Bias and gain", collapse=False)
		self.addCustomFlt("RMPbias")
		self.addCustomFlt("RMPgain")
		self.endLayout() # END Bias and gain
		self.addCustomFlt("RMPoutputMin")
		self.addCustomFlt("RMPoutputMax")
		self.beginLayout("Clamp", collapse=False)
		self.addControl("RMPclampEnable", label="Enable", annotation="When enabled, will clamp the output to Min-Max.")
		self.addControl("RMPthreshold", label="Expand", annotation="When enabled, will expand the clamped range to 0-1 after clamping.")
		self.addCustomFlt("RMPclampMin")
		self.addCustomFlt("RMPclampMax")
		self.endLayout() # END Clamp
		self.endLayout() # END Remap
		self.addCustomRgb("color1")
		self.addCustomRgb("color2")
		self.addControl("P", label="P", annotation="")

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
