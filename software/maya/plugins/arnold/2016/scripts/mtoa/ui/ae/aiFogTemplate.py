import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiFogTemplate(ShaderAETemplate):
    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()
        
        self.beginLayout('Fog Attributes', collapse=False)
        self.addControl('color', label='Color')
        self.addControl('distance', label='Distance')
        self.addControl('height', label='Height')
        self.addSeparator()
        self.addControl('ground_normal', label='Ground Normal')
        self.addControl('ground_point', label='Ground Point')
        self.endLayout()
        
        pm.mel.AEdependNodeTemplate(self.nodeName)

        self.addExtraControls()
        self.endScrollLayout()

