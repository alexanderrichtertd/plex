import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiWriteColorTemplate(ShaderAETemplate):

    def setup(self):
        self.beginScrollLayout()
        self.beginLayout("Write Color Attributes", collapse=False)

        self.addControl("beauty")
        self.addControl("input")
        self.addAOVControl('aovName')
        self.addControl("blend")

        self.endLayout()

        pm.mel.AEdependNodeTemplate(self.nodeName)
        self.addExtraControls()

        self.endScrollLayout()

