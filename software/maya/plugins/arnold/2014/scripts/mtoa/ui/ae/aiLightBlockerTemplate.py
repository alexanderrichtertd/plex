import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiLightBlockerTemplate(ShaderAETemplate):
    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()
        
        self.beginLayout('Light Blocker Attributes', collapse=False)
        self.addControl('geometry_type', label='Geometry Type')
        self.addControl('density', label='Density')
        self.addControl('shader', label='Shader')
        self.addSeparator()
        self.addControl('ramp_axis', label='Axis')
        self.addControl('ramp', label='Ramp')
        self.addControl('height_edge', label='Height Edge')
        self.addControl('width_edge', label='Width Edge')
        self.addControl('roundness', label='Roundness')
        self.endLayout()
        
        pm.mel.AEdependNodeTemplate(self.nodeName)
        
        self.addExtraControls()
        self.endScrollLayout()

