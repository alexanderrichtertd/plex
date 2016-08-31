import pymel.core as pm
import mtoa.utils as utils
import mtoa.ui.ae.utils as aeUtils
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate


class AEaiStandardTemplate(ShaderAETemplate):
    convertToMayaStyle = True
    
    def checkSpecularFresnel(self, nodeName):
        fullAttr = '%s.%s'%(nodeName, "Fresnel_use_IOR")
        fresIorValue = pm.getAttr(fullAttr)
    
        fullAttr = '%s.%s'%(nodeName, "specular_Fresnel")
        specFresValue = pm.getAttr(fullAttr)
        
        dim = (specFresValue is False) or (fresIorValue is True)
        pm.editorTemplate(dimControl=(nodeName, "Ksn", dim))

    def checkReflectionFresnel(self, nodeName):
        fullAttr = '%s.%s'%(nodeName, "Fresnel_use_IOR")
        fresIorValue = pm.getAttr(fullAttr)
        
        fullAttr = '%s.%s'%(nodeName, "Fresnel")
        refFresValue = pm.getAttr(fullAttr)
        
        dim = (refFresValue is False) or (fresIorValue is True)
        pm.editorTemplate(dimControl=(nodeName, "Krn", dim))
        
    def checkFresnelUseIOR(self, nodeName):
        fullAttr = '%s.%s'%(nodeName, "Fresnel_use_IOR")
        fresIorValue = pm.getAttr(fullAttr)
        
        fullAttr = '%s.%s'%(nodeName, "specular_Fresnel")
        specFresValue = pm.getAttr(fullAttr)
        dim = (specFresValue is False) or (fresIorValue is True)
        pm.editorTemplate(dimControl=(nodeName, "Ksn", dim))
        
        fullAttr = '%s.%s'%(nodeName, "Fresnel")
        refFresValue = pm.getAttr(fullAttr)
        dim = (refFresValue is False) or (fresIorValue is True)
        pm.editorTemplate(dimControl=(nodeName, "Krn", dim))

    def setup(self):
        self.addSwatch()

        self.beginScrollLayout()

        self.addCustom('message', 'AEshaderTypeNew', 'AEshaderTypeReplace')
        
        self.beginLayout("Matte", collapse=True)
        self.addControl("aiEnableMatte", label="Enable Matte")
        self.addControl("aiMatteColor", label="Matte Color")
        self.addControl("aiMatteColorA", label="Matte Opacity")
        self.endLayout()

        self.beginLayout("Diffuse", collapse=False)
        self.addControl("color",  label="Color", annotation="Diffuse Color")
        self.addControl("Kd", label="Weight")
        self.addControl("diffuse_roughness", label="Roughness")
        self.addControl("Kb", label="Backlighting")
        self.addSeparator()
        self.addControl("Fresnel_affect_diff", label="Fresnel affects Diffuse")

        self.beginLayout("Extended Controls", collapse=True)
        self.addControl("direct_diffuse", label="Direct Diffuse Scale")
        self.addControl("indirect_diffuse", label="Indirect Diffuse Scale")
        self.endLayout()
        self.endLayout()#End Diffuse Layout

        self.beginLayout("Specular", collapse=False)
        self.addControl("Ks_color", label="Color")
        self.addControl("Ks", label="Weight")
        self.addControl("specular_roughness", label="Roughness")
        self.addControl("specular_anisotropy", label="Anisotropy")
        self.addControl("specular_rotation", label="Rotation")        
        # depreciated
        # self.addControl("Phong_exponent", label="Glossiness")
        self.addSeparator()
        self.addControl("specular_Fresnel", changeCommand=self.checkSpecularFresnel, label="Fresnel")
        self.addControl("Ksn", label="Reflectance at Normal")

        self.beginLayout("Extended Controls", collapse=True)
        self.addControl("direct_specular", label="Direct Specular Scale")
        self.addControl("indirect_specular", label="Indirect Specular Scale")
        self.endLayout()
        self.endLayout()# End Specular Layout

        self.beginLayout("Reflection", collapse=True)
        self.addControl("Kr_color", label="Color")
        self.addControl("Kr", label="Weight")
        self.addControl("enable_internal_reflections", label="Enable Internal Reflections")
        self.addSeparator()
        self.addControl("Fresnel", changeCommand=self.checkReflectionFresnel, label="Fresnel")
        self.addSeparator()
        self.addControl("Krn", label="Reflectance at Normal")
        self.beginLayout("Exit Color", collapse=True)
        self.addControl("reflection_exit_use_environment", label="Use Environment")
        self.addControl("reflection_exit_color", label="Color")
        self.endLayout() # End Exit Color Layout
        self.endLayout() # End Reflection Layout

        self.beginLayout("Refraction", collapse=True)
        self.addControl("Kt_color", label="Color")
        self.addControl("Kt", label="Weight")
        self.addControl("IOR", label="IOR")
        self.addControl("dispersion_abbe", label="Dispersion Abbe Number")
        self.addControl("refraction_roughness", label="Roughness")
        self.addControl("Fresnel_use_IOR", changeCommand=self.checkFresnelUseIOR, label="Fresnel use IOR")
        self.addControl("transmittance", label="Transmittance")
        self.addControl("opacity", label="Opacity")        
        self.beginLayout("Exit Color", collapse=True)
        self.addControl("refraction_exit_use_environment", label="Use Environment")
        self.addControl("refraction_exit_color", label="Color")
        self.endLayout() # End Exit Color Layout
        self.endLayout() # End Refraction Layout

        self.addBumpLayout()

        self.beginLayout("Sub-Surface Scattering", collapse=True)
        self.addControl("Ksss_color", label="Color")
        self.addControl("Ksss", label="Weight")
        self.addControl("sss_radius", label="Radius")
        self.endLayout() # End SSS Layout

        self.beginLayout("Emission", collapse=True)
        self.addControl("emission_color", label="Color")
        self.addControl("emission", label="Scale")
        self.endLayout() # End Emission Layout

        self.beginLayout("Caustics", collapse=True)
        self.beginNoOptimize()
        self.addControl("enable_glossy_caustics", label="Enable Glossy Caustics")
        self.addControl("enable_reflective_caustics", label="Enable Reflective Caustics")
        self.addControl("enable_refractive_caustics", label="Enable Refractive Caustics")
        self.endNoOptimize()
        self.endLayout() # End Caustics Layout

        self.beginLayout("Advanced", collapse=True)
        self.addControl("bounce_factor", label="Bounce Factor")
        self.endLayout() # End Advanced Layout

        self.beginLayout("Hardware Texturing", collapse=True)
        pm.mel.eval('AEhardwareTextureTemplate "%s"' % self.nodeName + r'("color emission_color ")')
        self.endLayout()

        self.addAOVLayout(aovReorder = ['direct_diffuse', 'indirect_diffuse', 'direct_specular', 'indirect_specular',
                                        'reflection', 'refraction', 'refraction_opacity', 'emission', 'sss', 'direct_sss', 'indirect_sss'])

        # include/call base class/node attributes
        pm.mel.AEdependNodeTemplate(self.nodeName)

        self.suppress('PhongExponent')
       
        self.addExtraControls()
        self.endScrollLayout()

