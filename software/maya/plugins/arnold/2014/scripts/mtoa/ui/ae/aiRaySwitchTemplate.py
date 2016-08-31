import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiRaySwitchTemplate(ShaderAETemplate):
    def setup(self):
        self.addSwatch()

        self.beginScrollLayout()

        self.addCustom('message', 'AEshaderTypeNew', 'AEshaderTypeReplace')

        self.addControl('camera', label='Camera')
        self.addControl('shadow', label='Shadow')
        self.addControl('reflection', label='Reflection')
        self.addControl('refraction', label='Refraction')
        self.addControl('diffuse', label='Diffuse')
        self.addControl('glossy', label='Glossy')

        pm.mel.AEdependNodeTemplate(self.nodeName)
        self.addExtraControls()
        self.endScrollLayout()
