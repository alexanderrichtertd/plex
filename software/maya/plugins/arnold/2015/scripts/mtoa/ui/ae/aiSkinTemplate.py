import pymel.core as pm
import mtoa.utils as utils
import mtoa.ui.ae.utils as aeUtils
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate


class AEaiSkinTemplate(ShaderAETemplate):

    def checkPrimarySpecularFresnel(self, nodeName):
        fullAttr = '%s.%s'%(nodeName, 'specular_enable_fresnel_falloff')
        useFresnel = pm.getAttr(fullAttr)
        dim = not useFresnel
        pm.editorTemplate(dimControl=(nodeName, 'specularIor', dim))

    def checkSecondarySpecularFresnel(self, nodeName):
        fullAttr = '%s.%s'%(nodeName, 'sheen_enable_fresnel_falloff')
        useFresnel = pm.getAttr(fullAttr)
        dim = not useFresnel
        pm.editorTemplate(dimControl=(nodeName, 'sheenIor', dim))

    def setup(self):
        self.addSwatch()
       
        self.beginScrollLayout()
        
        self.addCustom('message', 'AEshaderTypeNew', 'AEshaderTypeReplace')

        self.beginLayout('Matte', collapse=True)
        self.addControl('aiEnableMatte', label='Enable Matte')
        self.addControl('aiMatteColor', label='Matte Color')
        self.addControl('aiMatteColorA', label='Matte Opacity')
        self.endLayout()
        
        self.beginLayout('SSS', collapse=False)
        self.addControl('sss_weight', label='SSS Weight')
        self.addControl('global_sss_radius_multiplier', label='Radius Multiplier')

        self.beginLayout('Shallow Scatter', collapse=False)
        self.addControl('shallow_scatter_color', label='Color')
        self.addControl('shallow_scatter_weight', label='Weight')
        self.addControl('shallow_scatter_radius', label='Radius')
        self.endLayout()
        
        self.beginLayout('Mid Scatter', collapse=False)
        self.addControl('mid_scatter_color', label='Color')
        self.addControl('mid_scatter_weight', label='Weight')
        self.addControl('mid_scatter_radius', label='Radius')
        self.endLayout()
        
        self.beginLayout('Deep Scatter', collapse=False)
        self.addControl('deep_scatter_color', label='Color')
        self.addControl('deep_scatter_weight', label='Weight')
        self.addControl('deep_scatter_radius', label='Radius')
        self.endLayout()

        self.endLayout()
        
        self.beginLayout('Specular', collapse=False)
        self.addControl('specular_color', label='Color')
        self.addControl('specular_weight', label='Weight')
        self.addControl('specular_roughness', label='Roughness')
        self.addControl('specular_ior', label='IOR')
        self.endLayout()
        
        self.beginLayout('Sheen Layer', collapse=False)
        self.addControl('sheen_color', label='Color')
        self.addControl('sheen_weight', label='Weight')
        self.addControl('sheen_roughness', label='Roughness')
        self.addControl('sheen_ior', label='IOR')
        self.endLayout()
        
        self.beginLayout('Opacity', collapse=True)
        self.addControl('opacity', label='Weight')
        self.addControl('opacity_color', label='Color')
        self.endLayout()
        
        self.beginLayout('Advanced', collapse=True)
        self.beginNoOptimize()
        self.addControl('specular_in_secondary_rays', label='Specular in Secondary Rays')
        self.addControl('fresnel_affect_sss', label='Fresnel Affects SSS')
        self.endNoOptimize()
        self.endLayout()

        self.addBumpLayout()
        
        self.beginLayout('Hardware Texturing', collapse=True)
        
        self.endLayout()

        self.addAOVLayout(aovReorder = ['specular', 'sheen', 'sss', 'direct_sss', 'indirect_sss'])
        
        # include/call base class/node attributes
        pm.mel.AEdependNodeTemplate(self.nodeName)
        
        self.addExtraControls()
        
        self.endScrollLayout()
