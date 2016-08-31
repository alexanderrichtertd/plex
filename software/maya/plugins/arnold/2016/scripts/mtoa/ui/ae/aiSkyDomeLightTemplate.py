import pymel.core as pm
import mtoa.ui.ae.lightTemplate as lightTemplate
import mtoa.ui.ae.aiSwatchDisplay as aiSwatchDisplay
import mtoa.ui.ae.templates as templates

class AEaiSkyDomeLightTemplate(lightTemplate.LightTemplate):
    def addSwatch(self):
        self.addCustom("message", aiSwatchDisplay.aiSwatchDisplayNew, aiSwatchDisplay.aiSwatchDisplayReplace)
        
    def makeLightExclusive(self, attr):
        lightName = attr.split(".")[0]
        pm.rowLayout(nc=2, cal=[2, 'left'])
        pm.text(label="")
        pm.exclusiveLightCheckBox('exclusiveButton', light=lightName, label="Illuminates By Default")
        pm.setParent('..')
        
    def replaceLightExclusive(self, attr):
        lightName = attr.split(".")[0]
        pm.exclusiveLightCheckBox('exclusiveButton', edit=True, light=lightName)
        
    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()
        
        self.beginLayout('SkyDomeLight Attributes', collapse=False)        
        self.addControl('color', label='Color')
        self.addControl('intensity', label='Intensity')
        self.addControl('resolution', label='Resolution')
        self.addSeparator()
        self.setupColorTemperature("ArnoldSkyDome")
        self.addCustom("instObjGroups", self.makeLightExclusive, self.replaceLightExclusive)
        self.addControl('emitDiffuse', label='Emit Diffuse')
        self.addControl('emitSpecular', label='Emit Specular')
        self.addSeparator()
        self.addControl('format', label='Format')
        self.addControl('aiExposure', label='Exposure')
        self.addControl('aiSamples', label='Samples')
        self.addControl('aiNormalize', label='Normalize')
        self.addSeparator()
        self.addControl('aiCastShadows', label='Cast Shadows')
        self.addControl('aiShadowColor', label='Shadow Color')
        self.addSeparator()
        self.commonLightAttributes()
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

