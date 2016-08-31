import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiSkyTemplate(ShaderAETemplate):
    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()
        
        self.beginLayout('Sky Attributes', collapse=False)
        self.addControl('format', label='Format')
        self.addControl('color', label='Color')
        self.addControl('intensity', label='Intensity')
        self.endLayout()
        
        self.beginLayout('Render Stats', collapse=True)
        self.beginNoOptimize()
        self.addControl('castsShadows', label='Casts Shadows')
        self.addControl('primaryVisibility', label='Primary Visibility')
        self.addControl('aiVisibleInDiffuse', label='Visible in Diffuse')
        self.addControl('aiVisibleInGlossy', label='Visible in Glossy')
        self.addControl('visibleInReflections', label='Visible in Reflections')
        self.addControl('visibleInRefractions', label='Visible in Refractions')
        self.endNoOptimize()
        self.endLayout()
        
        self.beginLayout('Hardware Texturing', collapse=True)
        self.addControl('sampling', label='Texture Resolution')
        self.addControl('hwtexalpha', label='Opacity')
        self.endLayout()
        
        self.beginLayout('Viewport', collapse=True)
        self.addControl('skyRadius', label='Sky Radius')
        self.addControl('skyFacing', label='Facing')
        self.endLayout()

        # Do not show extra attributes
        extras = ["visibility",
                  "intermediateObject",
                  "template",
                  "ghosting",
                  "instObjGroups",
                  "useObjectColor",
                  "objectColor",
                  "drawOverride",
                  "lodVisibility",
                  "renderInfo",
                  "renderLayerInfo",
                  "ghostingControl",
                  "ghostCustomSteps",
                  "ghostFrames",
                  "ghostRangeStart",
                  "ghostRangeEnd",
                  "ghostDriver",
                  "ghostColorPreA",
                  "ghostColorPre",
                  "ghostColorPostA",
                  "ghostColorPost",
                  "motionBlur",
                  "visibleInReflections",
                  "visibleInRefractions",
                  "castsShadows",
                  "receiveShadows",
                  "maxVisibilitySamplesOverride",
                  "maxVisibilitySamples",
                  "geometryAntialiasingOverride",
                  "antialiasingLevel",
                  "shadingSamplesOverride",
                  "shadingSamples",
                  "maxShadingSamples",
                  "volumeSamplesOverride",
                  "volumeSamples",
                  "depthJitter",
                  "ignoreSelfShadowing",
                  "primaryVisibility",
                  "compInstObjGroups",
                  "localPosition",
                  "localScale"]

        for extra in extras:
            self.suppress(extra)
            
        pm.mel.AEdependNodeTemplate(self.nodeName)

        self.addExtraControls()
        self.endScrollLayout()

