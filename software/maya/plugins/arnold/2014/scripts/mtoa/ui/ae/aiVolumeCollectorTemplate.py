import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiVolumeCollectorTemplate(ShaderAETemplate):
    def scatteringSource(self, nodeName):
        source = self.nodeAttr('scattering_source')
        sourceVal = pm.getAttr(source)
        print sourceVal
        if(sourceVal == 0):
            pm.editorTemplate(dimControl=(nodeName, "scattering", False))
            pm.editorTemplate(dimControl=(nodeName, "scatteringChannel", True))
        else:
            pm.editorTemplate(dimControl=(nodeName, "scattering", True))
            pm.editorTemplate(dimControl=(nodeName, "scatteringChannel", False))
            
    def attenuationSource(self, nodeName):
        source = self.nodeAttr('attenuation_source')
        sourceVal = pm.getAttr(source)
        print sourceVal
        if(sourceVal == 0):
            pm.editorTemplate(dimControl=(nodeName, "attenuation", False))
            pm.editorTemplate(dimControl=(nodeName, "attenuationChannel", True))
        elif(sourceVal == 1):
            pm.editorTemplate(dimControl=(nodeName, "attenuation", True))
            pm.editorTemplate(dimControl=(nodeName, "attenuationChannel", False))
        else:
            pm.editorTemplate(dimControl=(nodeName, "attenuation", True))
            pm.editorTemplate(dimControl=(nodeName, "attenuationChannel", True))
            
    def emissionSource(self, nodeName):
        source = self.nodeAttr('emission_source')
        sourceVal = pm.getAttr(source)
        print sourceVal
        if(sourceVal == 0):
            pm.editorTemplate(dimControl=(nodeName, "emission", False))
            pm.editorTemplate(dimControl=(nodeName, "emissionChannel", True))
        else:
            pm.editorTemplate(dimControl=(nodeName, "emission", True))
            pm.editorTemplate(dimControl=(nodeName, "emissionChannel", False))
            
    def setup(self):
        self.beginScrollLayout()
        
        self.beginLayout('Scattering', collapse=False)
        self.addControl('scattering_source',changeCommand=self.scatteringSource)
        self.addControl('scattering', label='Scattering')
        self.addControl('scattering_channel')
        self.addControl('scattering_color')
        self.addControl('scattering_intensity')
        self.addControl('anisotropy')
        self.endLayout()
        
        self.beginLayout('Attenuation', collapse=False)
        self.addControl('attenuation_source',changeCommand=self.attenuationSource)
        self.addControl('attenuation')
        self.addControl('attenuation_channel')
        self.addControl('attenuation_color')
        self.addControl('attenuation_intensity')
        self.addControl('attenuation_mode', label='Attenuation Mode')
        self.endLayout()
        
        self.beginLayout('Emission', collapse=False)
        self.addControl('emission_source',changeCommand=self.emissionSource)
        self.addControl('emission', label='Emission')
        self.addControl('emission_channel')
        self.addControl('emission_color')
        self.addControl('emission_intensity')
        self.endLayout()
        
        self.beginLayout('Sampling', collapse=False)
        self.addControl('position_offset')
        self.addControl('interpolation')
        self.endLayout()
               
        pm.mel.AEdependNodeTemplate(self.nodeName)

        self.addExtraControls()
        self.endScrollLayout()
