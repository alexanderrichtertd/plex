import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiBarndoorTemplate(ShaderAETemplate):
    def setup(self):
        self.addSwatch()
        
        self.beginScrollLayout()
        
        self.beginLayout('Barndoor Attributes', collapse=False)
        self.addControl('barndoor_top_left', label='Top Left')
        self.addControl('barndoor_top_right', label='Top Right')
        self.addControl('barndoor_top_edge', label='Top Edge')        
        self.addSeparator()
        self.addControl('barndoor_bottom_left', label='Bottom Left')
        self.addControl('barndoor_bottom_right', label='Bottom Right')
        self.addControl('barndoor_bottom_edge', label='Bottom Edge')
        self.addSeparator()
        self.addControl('barndoor_left_top', label='Left Top')
        self.addControl('barndoor_left_bottom', label='Left Bottom')
        self.addControl('barndoor_left_edge', label='Left Edge')
        self.addSeparator()
        self.addControl('barndoor_right_top', label='Right Top')
        self.addControl('barndoor_right_bottom', label='Right Bottom')
        self.addControl('barndoor_right_edge', label='Right Edge')
        self.endLayout()
        
        pm.mel.AEdependNodeTemplate(self.nodeName)
        
        self.addExtraControls()
        self.endScrollLayout()

