import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiWireframeTemplate(ShaderAETemplate):
    def setup(self):
        self.addSwatch()

        self.beginScrollLayout()

        self.addCustom('message', 'AEshaderTypeNew', 'AEshaderTypeReplace')

        self.beginLayout('Wireframe Attributes', collapse=False)
        self.addControl('edge_type', label='Edge Type')
        self.addControl('fill_color', label='Fill Color')
        self.addControl('line_color', label='Line Color')
        self.addControl('line_width', label='Line Width')
        self.addControl('raster_space', label='Raster Space')
        self.endLayout()

        pm.mel.AEdependNodeTemplate(self.nodeName)
        self.addExtraControls()
        self.endScrollLayout()

