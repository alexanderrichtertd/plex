import pymel.core as pm
import maya.cmds as cmds
import mtoa.ui.ae.lightTemplate as lightTemplate
import mtoa.ui.ae.aiSwatchDisplay as aiSwatchDisplay
import mtoa.ui.ae.templates as templates

class AEaiPhotometricLightTemplate(lightTemplate.LightTemplate):
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
        
            
    def filenameEdit(self, mData) :
        attr = self.nodeAttr('aiFilename')
        cmds.setAttr(attr,mData,type="string")
        
    def LoadFilenameButtonPush(self, *args):
        basicFilter = 'IES Photometry File (*.ies);;All Files (*.*)'
        projectDir = cmds.workspace(query=True, directory=True)
        ret = cmds.fileDialog2(fileFilter=basicFilter,
                                cap='Load Photometry File',okc='Load',fm=4, startingDirectory=projectDir)
        if ret is not None and len(ret):
            self.filenameEdit(ret[0])
            cmds.textFieldGrp("filenameGrp", edit=True, text=ret[0])
            
    def filenameNew(self, nodeName):
        cmds.rowLayout(nc=2, cw2=(360,30), cl2=('left', 'left'), adjustableColumn=1, columnAttach=[(1, 'left', -4), (2, 'left', 0)])
        path = cmds.textFieldGrp("filenameGrp", label="Photometry File",
                                        changeCommand=self.filenameEdit)
        cmds.textFieldGrp(path, edit=True, text=cmds.getAttr(nodeName))
        cmds.symbolButton( image='navButtonBrowse.png', command=self.LoadFilenameButtonPush)
     
    def filenameReplace(self, nodeName):
        cmds.textFieldGrp("filenameGrp", edit=True,
                                    text=cmds.getAttr(nodeName) )
            
        
    def setup(self):
        self.addSwatch()
        self.beginScrollLayout()
        
        self.beginLayout('Photometric Light Attributes', collapse=False)     
        self.addCustom('aiFilename', self.filenameNew, self.filenameReplace)        
        self.addControl('color', label='Color')
        self.addControl('intensity', label='Intensity')
        self.addSeparator()
        self.setupColorTemperature("ArnoldPhotometric")
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
        self.addControl('aiShadowDensity', label='Shadow Density')
        self.addControl('aiShadowColor', label='Shadow Color')
        self.addSeparator()
        self.commonLightAttributes()
        self.endLayout()
        
        self.beginLayout('Hardware Texturing', collapse=True)
        self.addControl('sampling', label='Texture Resolution')
        self.addControl('hwtexalpha', label='Opacity')
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

