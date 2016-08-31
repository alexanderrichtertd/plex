import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiGoboTemplate(ShaderAETemplate):
    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()
        
        self.beginLayout('Gobo Attributes', collapse=False)
        self.addControl('filter_mode', label='Filter Mode')
        self.addControl('slidemap', label='Slide Map')
        self.addControl('density', label='Density')
        self.endLayout()
        
        self.beginLayout('Placement Attributes', collapse=False)
        self.addControl('offset', label='Offset')
        self.addControl('rotate', label='Rotate')
        self.addControl('scale_s', label='Scale S')
        self.addControl('scale_t', label='Scale T')
        self.addControl('wrap_s', label='Wrap S')
        self.addControl('wrap_t', label='Wrap T')
        self.endLayout()
        
        pm.mel.AEdependNodeTemplate(self.nodeName)

        self.addExtraControls()
        self.endScrollLayout()
