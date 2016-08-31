import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiMotionVectorTemplate(ShaderAETemplate):
    def checkRaw(self, nodeName):
        fullAttr = '%s.%s'%(nodeName, "raw")
        rawValue = pm.getAttr(fullAttr)
        
        dim = rawValue
        pm.editorTemplate(dimControl=(nodeName, "maxDisplace", dim))
        
    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()
        
        self.beginLayout("Motion Vector Attributes", collapse=False)
    
        self.addControl("time0", label="Start Time")
        self.addControl("time1", label="End Time")
        self.addSeparator()
        self.addControl("raw", changeCommand=self.checkRaw, label="Encode Raw Vector")
        self.addControl("max_displace", label="Max Displace")
        
        self.endLayout()
        
        pm.mel.AEdependNodeTemplate(self.nodeName)

        self.addExtraControls()
        self.endScrollLayout()
    
