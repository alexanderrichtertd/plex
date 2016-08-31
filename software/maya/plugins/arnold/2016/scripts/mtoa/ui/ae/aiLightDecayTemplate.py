import mtoa.ui.ae.utils as aeUtils
import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiLightDecayTemplate(ShaderAETemplate):
    def checkNearAtten(self, nodeName):
        fullAttr = '%s.%s'%(nodeName, "use_near_atten")
        rawValue = pm.getAttr(fullAttr)
        
        dim = not rawValue
        pm.editorTemplate(dimControl=(nodeName, "nearStart", dim))
        pm.editorTemplate(dimControl=(nodeName, "nearEnd", dim))

    def checkFarAtten(self, nodeName):
        fullAttr = '%s.%s'%(nodeName, "use_far_atten")
        rawValue = pm.getAttr(fullAttr)
        
        dim = not rawValue
        pm.editorTemplate(dimControl=(nodeName, "farStart", dim))
        pm.editorTemplate(dimControl=(nodeName, "farEnd", dim))

    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()
        
        self.beginLayout('Attenuation', collapse=False)

        self.addControl('use_near_atten', changeCommand=self.checkNearAtten, label='Use Near Attenuation')
        self.addControl('near_start', label='Near Start')
        self.addControl('near_end', label='Near End')

        self.addSeparator()
        
        self.addControl('use_far_atten', changeCommand=self.checkFarAtten, label='Use Far Attenuation')
        self.addControl('far_start', label='Far Start')
        self.addControl('far_end', label='Far End')
        
        self.endLayout()
        
        pm.mel.AEdependNodeTemplate(self.nodeName)

        self.addExtraControls()
        self.endScrollLayout()

