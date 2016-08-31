import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiVolumeSampleRgbTemplate(ShaderAETemplate):
    def setup(self):
        self.beginScrollLayout()
        
        self.beginLayout('Volume Sample RGB Attributes', collapse=False)
        self.addControl('channel')
        self.addControl('position_offset')
        self.addControl('interpolation')
        self.endLayout()
        
        self.beginLayout('Color Correction Attributes', collapse=False)
        
        self.addControl('gamma')
        self.addControl('hue_shift')
        self.addControl('saturation')
        self.addControl('contrast')
        self.addControl('contrast_pivot')
        self.addControl('exposure')
        self.addControl('multiply')
        self.addControl('add')

        self.endLayout()
        
        pm.mel.AEdependNodeTemplate(self.nodeName)
        
        self.addExtraControls()
        self.endScrollLayout()
