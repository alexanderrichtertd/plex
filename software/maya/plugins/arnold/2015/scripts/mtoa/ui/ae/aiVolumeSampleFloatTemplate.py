import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiVolumeSampleFloatTemplate(ShaderAETemplate):
    def setup(self):
        self.beginScrollLayout()
        
        self.beginLayout('Volume Sample Float Attributes', collapse=False)
        self.addControl('channel')
        self.addControl('position_offset')
        self.addControl('interpolation')
        self.endLayout()
        
        self.beginLayout('Remap Attributes', collapse=False)
        
        self.addControl('input_min')
        self.addControl('input_max')
        self.addControl('contrast')
        self.addControl('contrast_pivot')
        self.addControl('bias')
        self.addControl('gain')
        self.addControl('output_min')
        self.addControl('output_max')
        self.addControl('clamp_min')
        self.addControl('clamp_max')
        self.endLayout()
        
        pm.mel.AEdependNodeTemplate(self.nodeName)
        
        self.addExtraControls()
        self.endScrollLayout()

