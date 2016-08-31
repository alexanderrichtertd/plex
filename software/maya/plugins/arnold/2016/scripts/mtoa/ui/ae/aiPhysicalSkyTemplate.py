import pymel.core as pm
import mtoa.utils as utils
import mtoa.ui.ae.utils as aeUtils
import maya.cmds as cmds
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiPhysicalSkyTemplate(ShaderAETemplate):
    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()
        
        self.beginLayout("Physical Sky Attributes", collapse=False)
        
        self.addControl("turbidity", label="Turbidity")
        self.addControl("ground_albedo", label="Ground Albedo")
        
        self.addControl("elevation", label="Elevation", annotation="WARNING : Linking rendertime graphs are not supported!")
        self.addControl("azimuth", label="Azimuth", annotation="WARNING : Linking rendertime graphs are not supported!")
        self.addControl("intensity", label="Intensity")
        
        self.addSeparator()
        
        self.addControl("sky_tint", label="Sky Tint")
        self.addControl("sun_tint", label="Sun Tint")
        self.addControl("sun_size", label="Sun Size")
        self.addControl("enable_sun", label="Enable Sun")
        
        self.endLayout()
        
        pm.mel.AEdependNodeTemplate(self.nodeName)
        self.addExtraControls()
        self.endScrollLayout()

