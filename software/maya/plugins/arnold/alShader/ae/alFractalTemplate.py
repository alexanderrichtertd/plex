import pymel.core as pm
from alShaders import *

class AEalFractalTemplate(alShadersTemplate):
	controls = {}
	params = {}
	def setup(self):
		self.params.clear()
		self.params["mode"] = Param("mode", "Mode", "Scalar outputs a black and white pattern, Vector outputs random colors.", "enum", presets=None)
		self.params["space"] = Param("space", "Space", "Space in which to calculate the noise pattern.", "enum", presets=None)
		self.params["scale"] = Param("scale", "Vector", "Scale values of the noise space for each axis. Use this to stretch the noise along a certain direction.", "vector", presets=None)
		self.params["frequency"] = Param("frequency", "Frequency", "Frequency of the noise pattern. Larger numbers make it smaller, lower numbers make it bigger.", "float", presets=None)
		self.params["time"] = Param("time", "Time", "4th dimension of the noise. Connect this to a time value to animate the noise.", "float", presets=None)
		self.params["octaves"] = Param("octaves", "Octaves", "Number of octaves to calculate. Higher numbers give more detail but take longer to compute.", "int", presets=None)
		self.params["distortion"] = Param("distortion", "Distortion", "Apply a random warp to the noise space.", "float", presets=None)
		self.params["lacunarity"] = Param("lacunarity", "Lacunarity", "How much the frequency is increased with each octave.", "float", presets=None)
		self.params["gain"] = Param("gain", "Gain", "How much the intensity of the noise is scaled with each object.", "float", presets=None)
		self.params["turbulent"] = Param("turbulent", "Turbulent", "Enable this to switch from fBM to Turbulent noise.", "bool", presets=None)
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
		self.params["color1"] = Param("color1", "Color 1", "Color to use when the noise result is 0.", "rgb", presets=None)
		self.params["color2"] = Param("color2", "Color 2", "Color to use when the noise result is 1.", "rgb", presets=None)
		self.params["P"] = Param("P", "P", "Connect a point here to define a custom space for the noise to be calculated in. You can use alInputVector to get and transform points. This can be useful for animating noises in coordinate systems.", "vector", presets=None)

		self.addSwatch()
		self.beginScrollLayout()

		self.addControl("mode", label="Mode", annotation="Scalar outputs a black and white pattern, Vector outputs random colors.")
		self.addControl("space", label="Space", annotation="Space in which to calculate the noise pattern.")
		self.addControl("scale", label="Vector", annotation="Scale values of the noise space for each axis. Use this to stretch the noise along a certain direction.")
		self.addCustomFlt("frequency")
		self.addCustomFlt("time")
		self.addControl("octaves", label="Octaves", annotation="Number of octaves to calculate. Higher numbers give more detail but take longer to compute.")
		self.addCustomFlt("distortion")
		self.addCustomFlt("lacunarity")
		self.addCustomFlt("gain")
		self.addControl("turbulent", label="Turbulent", annotation="Enable this to switch from fBM to Turbulent noise.")
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
		self.addControl("P", label="P", annotation="Connect a point here to define a custom space for the noise to be calculated in. You can use alInputVector to get and transform points. This can be useful for animating noises in coordinate systems.")

		pm.mel.AEdependNodeTemplate(self.nodeName)
		self.addExtraControls()

		self.endScrollLayout()
