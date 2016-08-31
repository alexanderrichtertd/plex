import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiShadowCatcherTemplate(ShaderAETemplate):
    
    def setup(self):
        self.beginScrollLayout()

        self.addCustom('message', 'AEshaderTypeNew', 'AEshaderTypeReplace')

        self.addControl("backgroundColor", label="Background Color")
        self.addControl("reflection", label="Reflection")

        self.beginLayout("Shadows", collapse=False)
        self.addControl("catchShadows", label="Catch Shadows")
        self.addControl("shadowColor", label="Shadow Color")
        self.addControl("enableTransparency", label="Enable Transparency")
        self.addControl("shadowTransparency", label="Shadow Transparency")
        self.endLayout()

        self.beginLayout("Diffuse", collapse=False)
        self.addControl("catchDiffuse", label="Catch Diffuse")
        self.addControl("diffuseColor", label="Diffuse Color")
        self.endLayout()

        pm.mel.AEdependNodeTemplate(self.nodeName)

        self.addExtraControls()
        self.endScrollLayout()

