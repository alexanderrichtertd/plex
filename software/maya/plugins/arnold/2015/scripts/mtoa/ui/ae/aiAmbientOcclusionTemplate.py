import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiAmbientOcclusionTemplate(ShaderAETemplate):
    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()

        self.addCustom('message', 'AEshaderTypeNew', 'AEshaderTypeReplace')

        self.beginLayout('Ambient Occlusion Attributes', collapse=False)
        self.addControl('samples', label='Samples')
        self.addControl('spread', label='Spread')
        self.addControl('falloff', label='Falloff')
        self.addControl('near_clip', label='Near Clip')
        self.addControl('far_clip', label='Far Clip')
        self.addSeparator()
        self.addControl('white', label='White')
        self.addControl('black', label='Black')        
        self.addControl('opacity', label='Opacity')
        self.addSeparator()
        self.beginNoOptimize()
        self.addControl('invert_normals', label='Invert Normals')
        self.addControl('self_only', label='Self Only')
        self.endNoOptimize()
        self.endLayout()

        pm.mel.AEdependNodeTemplate(self.nodeName)

        self.addExtraControls()
        self.endScrollLayout()

