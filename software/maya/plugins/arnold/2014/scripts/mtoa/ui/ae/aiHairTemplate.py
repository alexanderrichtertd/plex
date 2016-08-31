import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiHairTemplate(ShaderAETemplate):
    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()
        
        self.addCustom('message', 'AEshaderTypeNew', 'AEshaderTypeReplace')

        self.beginLayout("Matte", collapse=True)
        self.addControl("aiEnableMatte", label="Enable Matte")
        self.addControl("aiMatteColor", label="Matte Color")
        self.addControl("aiMatteColorA", label="Matte Opacity")
        self.endLayout()
        
        self.beginLayout('Diffuse', collapse=False)
        self.addControl('rootcolor', label='Root Color')
        self.addControl('tipcolor', label='Tip Color')
        self.addSeparator()        
        self.addControl('ambdiff', label='Ambient Diffuse')
        self.addControl('kd_ind', label='Indirect Diffuse')
        self.addControl('diffuse_cache', label='Diffuse Cache')
        self.endLayout()
        
        self.beginLayout('Specular', collapse=False)
        self.addControl('gloss', label='Glossiness')
        self.addControl('spec', label='Weight')
        self.addControl('spec_color', label='Color')
        self.addControl('spec_shift', label='Angular Shift')
        
        self.beginLayout('Secondary Specular', collapse=True)        
        self.addControl('gloss2', label='Glossiness')
        self.addControl('spec2', label='Weight')
        self.addControl('spec2_color', label='Color')
        self.addControl('spec2_shift', label='Angular Shift')
        self.endLayout()

        self.endLayout()
        
        self.beginLayout('Transmission', collapse=False)
        self.addControl('transmission', label='Weight')
        self.addControl('transmission_color', label='Color')
        self.addControl('transmission_spread', label='Spread')
        self.endLayout()

        self.beginLayout('Opacity', collapse=False)
        self.addControl('opacity', label='Color')
        self.endLayout()

        self.beginLayout('UVs', collapse=True)
        self.addControl('uparam', label='U Param')
        self.addControl('vparam', label='V Param')
        self.endLayout()
        

        self.addAOVLayout()
        
        # include/call base class/node attributes
        pm.mel.AEdependNodeTemplate(self.nodeName)
        
        self.addExtraControls()
        self.endScrollLayout()

