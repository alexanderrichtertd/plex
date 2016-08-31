import pymel.core as pm
import mtoa.ui.ae.lightTemplate as lightTemplate
import mtoa.ui.ae.aiSwatchDisplay as aiSwatchDisplay
import mtoa.ui.ae.templates as templates

class AEaiAreaLightTemplate(lightTemplate.LightTemplate):
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

        self.beginLayout("Arnold Area Light Attributes", collapse=False)

        self.addControl("color")
        self.addControl("intensity")
        self.addControl("aiExposure", label = "Exposure")
        self.addSeparator()        
        self.setupColorTemperature("ArnoldArea")
        self.addCustom("instObjGroups", self.makeLightExclusive, self.replaceLightExclusive)
        self.addControl("emitDiffuse")
        self.addControl("emitSpecular")
        self.addControl("aiDecayType")
        
        self.addChildTemplate('aiTranslator', templates.getNodeTemplate('aiAreaLight'))
        
        self.addSeparator()

        self.commonLightAttributes()
        
        self.endLayout()

        # include/call base class/node attributes
        pm.mel.AEdependNodeTemplate(self.nodeName)

        self.addExtraControls()
        suppressList = ['aiShadowDensity', 'aiCastShadows', 'update',
            'aiSamples', 'aiNormalize', 'aiColorTemperature',
            'aiShadowColor', 'aiResolution', 'ghostFrames',
            'motionBlur', 'visibleInReflections', 'visibleInRefractions',
            'castsShadows', 'receiveShadows', 'maxVisibilitySamplesOverride',
            'maxVisibilitySamples', 'geometryAntialiasingOverride', 'antialiasingLevel',
            'shadingSamplesOverride', 'shadingSamples', 'maxShadingSamples',
            'volumeSamplesOverride', 'volumeSamples', 'layerRenderable',
            'ghostingControl', 'ghostCustomSteps', 'ghostColorPreA',
            'ghostColorPre', 'ghostColorPostA', 'ghostColorPost',
            'ghostRangeStart', 'ghostRangeEnd', 'ghostDriver',
            'depthJitter', 'ignoreSelfShadowing', 'primaryVisibility',
            'localPosition', 'localScale', 'pointCamera', 'normalCamera',
            'visibility', 'intermediateObject', 'template', 'ghosting',
            'objectColorRGB', 'useObjectColor', 'objectColor',
            'containerType', 'creationDate', 'creator',
            'customTreatment', 'uiTreatment', 'templateVersion',
            'viewMode', 'iconName', 'viewName', 'templatePath',
            'rmbCommand', 'blackBox', 'drawOverride',
            'renderInfo', 'renderLayerInfo', 'compInstObjGroups',
            'lodVisibility', 'templateName', 'selectionChildHighlighting']
        for sup in suppressList:
            self.suppress(sup)
        self.endScrollLayout()

class BaseAreaLightTemplate(lightTemplate.LightTemplate):
    def addCommonParameters(self):
        self.addControl("aiSamples")
        self.addControl("aiNormalize")

        self.addSeparator()

        self.addControl("aiCastShadows")
        self.addControl("aiShadowDensity")
        self.addControl("aiShadowColor")

    def setup(self):
        self.addCommonParameters()       
        
class QuadAreaLightTemplate(BaseAreaLightTemplate):
    def setup(self):
        self.addControl("aiResolution")
        self.addSeparator()
        self.addCommonParameters()

class MeshLightTemplate(BaseAreaLightTemplate):
    def setup(self):
        self.addControl("color")
        self.addControl("intensity")
        self.addControl("aiExposure", label = "Exposure")
        self.addSeparator()        
        self.setupColorTemperature("ArnoldArea")
        self.addControl("emitDiffuse")
        self.addControl("emitSpecular")
        self.addControl("aiDecayType")

        self.addSeparator()
        self.addControl("lightVisible")
        
        self.addSeparator()
        
        self.addCommonParameters()

        self.addSeparator()

        self.commonLightAttributes(False)

        self.beginLayout('Subdivision', collapse=True)
        self.addControl("aiSubdivType", label="Type")
        self.addControl("aiSubdivIterations", label="Iterations")
        self.addControl("aiSubdivAdaptiveMetric", label="Adaptive Metric")
        self.addControl("aiSubdivPixelError", label="Adaptative Error")
        self.addControl("aiSubdivAdaptiveSpace", label="Adaptative Space")
        # TODO: add dicing camera UI
        self.addControl("aiSubdivDicingCamera", label="Dicing Camera")
        self.addControl("aiSubdivUvSmoothing", label="UV Smoothing")
        self.addControl("aiSubdivSmoothDerivs", label="Smooth Tangents")
        self.endLayout()

        self.addControl("aiUserOptions", "User Options")


templates.registerAETemplate(templates.TranslatorControl, "aiAreaLight", label="Light Shape")
templates.registerTranslatorUI(QuadAreaLightTemplate, "aiAreaLight", "quad")
templates.registerTranslatorUI(BaseAreaLightTemplate, "aiAreaLight", "cylinder")
templates.registerTranslatorUI(BaseAreaLightTemplate, "aiAreaLight", "disk")
templates.registerDefaultTranslator('aiAreaLight', "quad")
templates.registerTranslatorUI(MeshLightTemplate, "mesh", "mesh_light")
