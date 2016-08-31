import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiVolumeScatteringTemplate(ShaderAETemplate):
    def setup(self):
        self.addSwatch()
        
        self.beginScrollLayout()
        
        self.beginLayout('Volume Attributes', collapse=False)
        self.addControl('rgb_density', label='Color')
        self.addControl('density', label='Density')
        self.addSeparator()
        self.addControl('rgb_attenuation', label='Attenuation Color')
        self.addControl('attenuation', label='Attenuation')
        self.addSeparator()
        self.addControl('eccentricity', label='Anisotropy')
        self.addSeparator()
        self.addControl('sampling_pattern', label='Sampling Pattern')
        self.addControl('samples', label='Samples')
        self.endLayout()
        
        self.beginLayout('Contribution Attributes')
        self.addControl('affect_camera', label='Camera')
        self.addControl('affect_diffuse', label='Diffuse')
        self.addControl('affect_reflection', label='Reflection')
        self.endLayout()
        
        pm.mel.AEdependNodeTemplate(self.nodeName)
        
        self.addExtraControls()
        self.endScrollLayout()

