import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMaya as om
import mtoa.ui.ae.lightTemplate as lightTemplate
from mtoa.ui.ae.utils import aeCallback
import mtoa.ui.ae.templates as templates
import mtoa.callbacks as callbacks
import mtoa.core as core
import re
import mtoa.aovs as aovs

class ParticleTemplate(templates.ShapeTranslatorTemplate):
    def setup(self):
        self.commonShapeAttributes()
        self.addControl("aiRenderPointsAs", label="Render Points As")
        self.addControl("aiMinParticleRadius", label="Min Particle Radius")
        self.addControl("aiRadiusMultiplier", label="Radius Multiplier")
        self.addControl("aiMaxParticleRadius", label="Max Particle Radius")
        self.addControl("aiMinPixelWidth", label="Min Pixel Width")
        self.addSeparator()   
        self.addControl("aiExportParticleIDs", label="Export Particle Id")
        self.addControl("aiExportAttributes", label="Export Attributes")
        self.addSeparator()
        self.addControl("aiDeleteDeadParticles", label="Delete Dead Particles")
        self.addSeparator()
        self.addControl('aiStepSize', label="Volume Step Size")
        self.addSeparator()
        self.addControl("aiUserOptions", label="User Options")
        
templates.registerTranslatorUI(ParticleTemplate, "particle", "<built-in>")

class NParticleTemplate(templates.ShapeTranslatorTemplate):
    def setup(self):
        self.commonShapeAttributes()
        self.addControl("aiRenderPointsAs", label="Render Points As")
        self.addControl("aiMinParticleRadius", label="Min Particle Radius")
        self.addControl("aiRadiusMultiplier", label="Radius Multiplier")
        self.addControl("aiMaxParticleRadius", label="Max Particle Radius")
        self.addControl("aiMinPixelWidth", label="Min Pixel Width")
        self.addSeparator()   
        self.addControl("aiExportParticleIDs", label="Export Particle Id")
        self.addControl("aiExportAttributes", label="Export Attributes")
        self.addSeparator()
        self.addControl("aiInterpolateBlur", label="Interpolated Motion Blur")
        self.addControl("aiEvaluateEvery", label="nCache Evaluation Interval", annotation="Use nCache's \"Evaluate every # frame(s)\" param value")
        self.addSeparator()
        self.addControl("aiDeleteDeadParticles", label="Delete Dead Particles")
        self.addSeparator()
        self.addControl('aiStepSize', label="Volume Step Size")
        self.addSeparator()
        self.addControl("aiUserOptions", label="User Options")
    
templates.registerTranslatorUI(NParticleTemplate, "nParticle", "<built-in>")

class MeshTemplate(templates.ShapeTranslatorTemplate):
    def subdivDicingCameraNew(self, attrName):
        pm.setUITemplate('attributeEditorTemplate', pst=True)
        pm.attrNavigationControlGrp('aiSubdivDicingCameraCtrl',
                                    at=attrName,
                                    label="Subdivision Dicing Camera" )
        pm.setUITemplate(ppt=True)
    
    def subdivDicingCameraReplace(self, attrName):
        pm.attrNavigationControlGrp('aiSubdivDicingCameraCtrl', edit=True,
                                    at=attrName )
        # pm.editorTemplate("aiSubdivDicingCamera", label="Subdivision Dicing Camera", addDynamicControl=True)
        #pm.editorTemplate(aeCallback(self.subdivDicingCameraNew), aeCallback(self.subdivDicingCameraReplace), "aiSubdivDicingCamera", callCustom=True)

    def setup(self):
        self.commonShapeAttributes()
        
        self.addSeparator()
        self.addControl("aiExportTangents", label="Export Tangents")
        self.addControl("aiExportColors", label="Export Vertex Colors")
        self.addControl("aiExportRefPoints", label="Export Reference Positions")
        self.addControl("aiExportRefNormals", label="Export Reference Normals")
        self.addControl("aiExportRefTangents", label="Export Reference Tangents")
        
        self.addSeparator()
        self.addControl("aiSssSetname", label="SSS Set Name")
        self.addSeparator()
        self.addControl("aiMotionVectorSource", label="Motion Vector Source")
        self.addControl("aiMotionVectorUnit", label="Motion Vector Unit")
        self.addControl("aiMotionVectorScale", label="Motion Vector Scale")
        
        self.beginLayout('Subdivision', collapse=False)
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
        
        self.beginLayout('Displacement Attributes', collapse=False)
        self.addControl("aiDispHeight", label="Height")
        self.addControl("aiDispPadding", label="Bounds Padding")
        self.addControl("aiDispZeroValue", label="Scalar Zero Value")
        self.addControl("aiDispAutobump", label="Auto Bump")
        self.endLayout()
        self.beginLayout('Volume Attributes', collapse=False)
        self.addControl('aiStepSize', label='Step Size')
        self.endLayout()
        self.addControl("aiUserOptions", label="User Options")
        #pm.editorTemplate("aiExportHairIDs", label="Export Hair IDs", addDynamicControl=True)
        # FIXME: these are not on the shape node!
#       ui.addSeparator()
#       ui.addControl("enableProcedural")
#       ui.addControl("dso")
templates.registerTranslatorUI(MeshTemplate, "mesh", "polymesh")
core.registerDefaultTranslator("mesh", "polymesh")
templates.registerTranslatorUI(MeshTemplate, "nurbsSurface", "<built-in>")

class HairSystemTemplate(templates.ShapeTranslatorTemplate):
    def shaderCreate(self, attrName):
        cmds.setUITemplate('attributeEditorPresetsTemplate', pushTemplate=True)
        cmds.attrNavigationControlGrp("HairSystemTemplateShader", attribute=attrName, label="Hair Shader")
        cmds.setUITemplate(popTemplate=True)

    def shaderUpdate(self, attrName):
        cmds.attrNavigationControlGrp("HairSystemTemplateShader", edit=True, attribute=attrName)

    def minPixelCreate(self, attrName):
        cmds.setUITemplate('attributeEditorPresetsTemplate', pushTemplate=True)
        isEnabled = not (cmds.getAttr("%s.aiMode" % (attrName.split(".")[0])) is 1)
        cmds.attrFieldSliderGrp("HairTemplateMinPixelWidth", label="Min Pixel Width",
                            attribute=attrName, enable=isEnabled)
        cmds.setUITemplate(popTemplate=True)
    
    def minPixelUpdate(self, attrName):
        isEnabled = not (cmds.getAttr("%s.aiMode" % (attrName.split(".")[0])) is 1)
        cmds.attrFieldSliderGrp("HairTemplateMinPixelWidth", edit=True,
                            attribute=attrName, enable=isEnabled)

    def indirectDiffuseCreate(self, attrName):
        cmds.setUITemplate('attributeEditorPresetsTemplate', pushTemplate=True)
        isEnabled = not (cmds.getAttr("%s.aiMode" % (attrName.split(".")[0])) is 1)
        cmds.attrFieldSliderGrp("HairTemplateIndirectDiffuse", label="Indirect Diffuse",
                            attribute=attrName, enable=isEnabled)
        cmds.setUITemplate(popTemplate=True)
    
    def indirectDiffuseUpdate(self, attrName):
        isEnabled = not (cmds.getAttr("%s.aiMode" % (attrName.split(".")[0])) is 1)
        cmds.attrFieldSliderGrp("HairTemplateIndirectDiffuse", edit=True,
                            attribute=attrName, enable=isEnabled)

    def modeChanged(self, *args):
        try:
            if cmds.getAttr(self.nodeAttr('aiMode')) == 1:
                cmds.attrFieldSliderGrp("HairTemplateMinPixelWidth", edit=True, enable=False)
            else:
                cmds.attrFieldSliderGrp("HairTemplateMinPixelWidth", edit=True, enable=True)
        except RuntimeError:
            # this callback runs immediately, before HairTemplateMinPixelWidth exists
            pass

    def setup(self):
        self.addControl("primaryVisibility")
        self.addControl("castsShadows")
        self.addSeparator()
        self.commonShapeAttributes()
        self.addSeparator()
        self.addControl("aiExportHairIDs", label="Export Hair IDs")
        self.addControl("aiExportHairUVs", label="Export Hair UVs")
        self.addControl("aiExportHairColors", label="Export Hair Colors")
        self.addControl("aiOverrideHair", label="Override Hair")
        self.addCustom("aiHairShader", self.shaderCreate, self.shaderUpdate)
        self.addSeparator()
        self.addCustom("aiMinPixelWidth", self.minPixelCreate, self.minPixelUpdate)
        self.addCustom("aiIndirectDiffuse", self.indirectDiffuseCreate, self.indirectDiffuseUpdate)
        self.addControl("aiMode", label="Mode", changeCommand=self.modeChanged)
        self.addSeparator()
        self.addControl("aiUserOptions", label="User Options")
templates.registerAETemplate(HairSystemTemplate, "hairSystem")

class FLuidShapeTemplate(templates.ShapeTranslatorTemplate):
    def volumeNoiseCreate(self, attrName):
        cmds.setUITemplate('attributeEditorPresetsTemplate', pushTemplate=True)
        cmds.attrNavigationControlGrp("FluidTemplateVolumeTexture", attribute=attrName, label="Texture")
        cmds.setUITemplate(popTemplate=True)

    def volumeNoiseUpdate(self, attrName):
        cmds.attrNavigationControlGrp("FluidTemplateVolumeTexture", edit=True, attribute=attrName)
        
    def setup(self):
        self.addControl("aiStepSize", label="Step Size")
        self.addControl("aiEnableDeformationBlur", label="Enable Deformation Blur")
        self.addControl("aiMotionVectorScale", label="Motion Vector Scale")
        self.addControl("aiFilterType", label="Filter Type")
        self.addControl("aiPhaseFunc", label="Phase Function Anisotropy")
        self.addSeparator()
        self.addControl("aiVisibleInDiffuse", label="Visible In Diffuse")
        self.addControl("aiVisibleInGlossy", label="Visible In Glossy")
        self.beginLayout("Custom Texture", collapse=False)
        self.addControl("aiOverrideTextures", label="Override Fluid Texture")        
        self.addControl("aiTextureAffectColor", label="Texture Color")
        self.addControl("aiTextureAffectIncand", label="Texture Incandescence")
        self.addControl("aiTextureAffectOpacity", label="Texture Opacity")
        self.addControl("aiTextureCoordinateMethod", label="Coordinate Method")
        self.addCustom("aiVolumeTexture", self.volumeNoiseCreate, self.volumeNoiseUpdate)
        self.endLayout()
        self.addControl("aiUserOptions", label="User Options")
templates.registerAETemplate(FLuidShapeTemplate, "fluidShape")

class NurbsCurveTemplate(templates.ShapeTranslatorTemplate):
    def minPixelCreate(self, attrName):
        cmds.setUITemplate('attributeEditorPresetsTemplate', pushTemplate=True)
        isEnabled = not (cmds.getAttr("%s.aiMode" % (attrName.split(".")[0])) is 1)
        cmds.attrFieldSliderGrp("NurbsCurveTemplateMinPixelWidth", label="Min Pixel Width",
                            attribute=attrName, enable=isEnabled)
        cmds.setUITemplate(popTemplate=True)
    
    def minPixelUpdate(self, attrName):
        isEnabled = not (cmds.getAttr("%s.aiMode" % (attrName.split(".")[0])) is 1)
        cmds.attrFieldSliderGrp("NurbsCurveTemplateMinPixelWidth", edit=True,
                            attribute=attrName, enable=isEnabled)
    
    def modeChanged(self, *args):
        try:
            if cmds.getAttr(self.nodeAttr('aiMode')) == 1:
                cmds.attrFieldSliderGrp("NurbsCurveTemplateMinPixelWidth", edit=True, enable=False)
            else:
                cmds.attrFieldSliderGrp("NurbsCurveTemplateMinPixelWidth", edit=True, enable=True)
        except RuntimeError:
            # this callback runs immediately, before NurbsCurveTemplateMinPixelWidth exists
            pass
            
    def setup(self):
        #pm.mel.eval('AEaddRampControl("widthProfile")')
        #pm.mel.eval('AEaddRampControl("colorTable")')
        self.addControl("aiRenderCurve")
        self.addControl("aiCurveWidth")
        self.addControl("aiSampleRate")
        self.addControl("aiCurveShader")
        self.addSeparator()
        self.addControl("primaryVisibility")
        self.addControl("castsShadows")
        self.addSeparator()
        self.addControl("aiExportRefPoints", "Export Reference Points")
        self.addSeparator()
        self.commonShapeAttributes()
        self.addSeparator()
        self.addCustom("aiMinPixelWidth", self.minPixelCreate, self.minPixelUpdate)
        self.addControl("aiMode", label="Mode", changeCommand=self.modeChanged)
        self.addSeparator()
        self.addControl("aiUserOptions", label="User Options")
templates.registerTranslatorUI(NurbsCurveTemplate, "nurbsCurve", "<built-in>")


class DirectionalLightTemplate(lightTemplate.LightTemplate):
    def setup(self):
        self.setupColorTemperature("Directional")
        self.addControl("aiExposure")
        self.addControl("aiAngle")
        
        self.addSeparator()
        
        self.addControl("aiSamples")
        self.addControl("aiNormalize")
        
        self.addSeparator()
        
        self.addControl("aiCastShadows")
        self.addControl("aiShadowDensity")
        
        self.addSeparator()                
        self.commonLightAttributes()

templates.registerTranslatorUI(DirectionalLightTemplate, "directionalLight")

class PointLightTemplate(lightTemplate.LightTemplate):
    def setup(self):
        self.setupColorTemperature("Point")
        self.addControl("aiDecayType")
        self.addControl("aiExposure")
        
        self.addSeparator()
        
        self.addControl("aiSamples")
        self.addControl("aiRadius")
        self.addControl("aiNormalize")

        self.addSeparator()

        self.addControl("aiCastShadows")
        self.addControl("aiShadowDensity")

        self.addSeparator()

        self.commonLightAttributes()

templates.registerTranslatorUI(PointLightTemplate, "pointLight")

class SpotLightTemplate(lightTemplate.LightTemplate):
    def setup(self):
        self.setupColorTemperature("Spot")
        self.addControl("aiDecayType")
        self.addControl("aiExposure")
        
        self.addSeparator()
                        
        self.addControl("aiSamples")
        self.addControl("aiRadius")
        self.addControl("aiNormalize")

        self.addSeparator()

        self.addControl("aiCastShadows")
        self.addControl("aiShadowDensity")

        self.addSeparator()

        self.addControl("aiAspectRatio")
        self.addControl("aiLensRadius")

        self.addSeparator()

        self.commonLightAttributes()

templates.registerTranslatorUI(SpotLightTemplate, "spotLight")

class AreaLightTemplate(lightTemplate.LightTemplate):
    def setup(self):
        self.setupColorTemperature("Area")
        self.addControl("aiDecayType")
        self.addControl("aiExposure")
        
        self.addSeparator()
        
        self.addControl("aiSamples")
        self.addControl("aiNormalize")

        self.addSeparator()

        self.addControl("aiCastShadows")
        self.addControl("aiShadowDensity")

        self.addSeparator()

        self.addControl("aiResolution")
        
        self.addSeparator()

        self.commonLightAttributes()

templates.registerTranslatorUI(AreaLightTemplate, "areaLight")

# Actually currently connecting the other way round, filter's decayRate
# to light's decay type which might be the best idea
"""
def lightDecayChanged(decayPlug, *args):
    "called to sync first found lightDecay filter when decayRate changes"
    # fnCam = om.MFnCamera(transPlug.node())
    # currTrans = transPlug.asString()
    #orthoPlug = fnCam.findPlug('orthographic')
    # isOrtho = orthoPlug.asBool()
    print "lightDecayChanged", decayPlug.name(), decayPlug.asInt()
    print "filters", lightTemplate.LightTemplate.getConnectedLightFilters()
    # aiLightDecay

print "Adding attribute changed callback for lights"
callbacks.addAttributeChangedCallback(lightDecayChanged, 'pointLight', 'decayRate')
callbacks.addAttributeChangedCallback(lightDecayChanged, 'spotLight', 'decayRate')
callbacks.addAttributeChangedCallback(lightDecayChanged, 'areaLight', 'decayRate')
callbacks.addAttributeChangedCallback(lightDecayChanged, 'aiAreaLight', 'decayRate')
"""

templates.registerAETemplate(templates.TranslatorControl, "camera", label="Camera Type")

class CameraTemplate(templates.AttributeTemplate):
    def syncAttribute(self, attr, control, valueField, positionField):
        attr = self.nodeAttr('aiShutterCurve')
        values = cmds.gradientControlNoAttr( control, query=True, asString=True) 
        valuesSplit = values.split(',')

        points = []

        for i in range(0,len(valuesSplit)/3):
            points.append([valuesSplit[i*3+1],valuesSplit[i*3],0])
            
        current = cmds.gradientControlNoAttr( control, query=True, currentKey=True) 
        cmds.floatField(valueField, edit=True, value=float(points[current][1]))
        cmds.floatField(positionField, edit=True, value=float(points[current][0]))
        points[current][2] = 1
        points.sort()
        
        size = cmds.getAttr(attr, size=True)
        for i in range(0,size):
            cmds.removeMultiInstance(attr+'['+str(i)+']')
        
        curveString = ""
        for i in range(0,len(points)):
            cmds.setAttr(attr+'['+str(i)+'].aiShutterCurveX',float(points[i][0]))
            cmds.setAttr(attr+'['+str(i)+'].aiShutterCurveY',float(points[i][1]))
            if i is 0:
                curveString += points[i][1] +"," + points[i][0] +",1"
            else:
                curveString += ","+points[i][1] +"," + points[i][0] +",1"
            
        # We save the curve points sorted in the attribute, so we will also resort the points in
        #  the gradient control
        current = [x[2] for x in points].index(1)
        cmds.gradientControlNoAttr( control, edit=True, currentKey=current, asString=curveString) 
            
    def updateValue(self, attr, control, valueField, positionField):
        value = pm.floatField(valueField, query=True, value=True)
        
        values = cmds.gradientControlNoAttr( control, query=True, asString=True) 
        valuesSplit = values.split(',')
            
        current = cmds.gradientControlNoAttr( control, query=True, currentKey=True) 
        
        valuesSplit[current*3] = str(value)
        values = ",".join(valuesSplit)
        
        pm.gradientControlNoAttr( control, edit=True, asString=values)
        self.syncAttribute(attr, control, valueField, positionField)
        
    def updatePosition(self, attr, control, valueField, positionField):
        value = pm.floatField(positionField, query=True, value=True)
        
        values = cmds.gradientControlNoAttr( control, query=True, asString=True) 
        valuesSplit = values.split(',')
            
        current = cmds.gradientControlNoAttr( control, query=True, currentKey=True) 
        
        valuesSplit[current*3+1] = str(value)
        values = ",".join(valuesSplit)
        
        pm.gradientControlNoAttr( control, edit=True, asString=values)
        self.syncAttribute(attr, control, valueField, positionField)
        
    def createRamp( self, attr ):
        #Create the control fields
        pm.columnLayout( )
        
        cmds.rowLayout(nc=2, cw2=(142,220))
        pm.text("Shutter Curve");
        pm.text(" ");
        pm.cmds.setParent('..')
        
        cmds.rowLayout("ShutterCurveRowLayout",nc=2, cw2=(142,220))
        
        pm.columnLayout("ShutterCurveColumLayout")
        cmds.rowLayout("ShutterCurveValueLayout", nc=2, cw2=(60,45))
        pm.text("Value");
        valueField = pm.floatField("ShutterCurveValueField");
        pm.cmds.setParent('..')
        
        pm.rowLayout("ShutterCurvePositionLayout", nc=2, cw2=(60,45))
        pm.text("Position");
        
        positionField = cmds.floatField("ShutterCurvePositionField");
        pm.cmds.setParent('..')
        
        '''pm.rowLayout(nc=2, cw2=(60,65))
        pm.text("Interpol.");
        pm.optionMenu(changeCommand=self.updateRamp )
        pm.menuItem( label='None' )
        pm.menuItem( label='Linear' )
        pm.menuItem( label='Smooth' )
        pm.menuItem( label='Spline' )
        pm.cmds.setParent('..')'''
        pm.cmds.setParent('..')
        
        gradient = pm.gradientControlNoAttr("ShutterCurveGradientControl", w=200, h=100 )
        pm.gradientControlNoAttr( gradient, edit=True, changeCommand=pm.Callback(self.syncAttribute,attr,gradient, valueField, positionField) )
        
        #Initialize the curve with the values in the attribute
        curveString = ""
        attr = self.nodeAttr('aiShutterCurve')
        size = cmds.getAttr(attr, size=True)
        startX = 0
        startY = 1
        if size > 0:
            x = cmds.getAttr(attr+'[0].aiShutterCurveX')
            y = cmds.getAttr(attr+'[0].aiShutterCurveY')
            startX = x
            startY = y
            curveString += str(y) +"," + str(x) +",1"
        else:
            curveString += "1,0,1"
        for i in range(1,size):
            x = cmds.getAttr(attr+'['+str(i)+'].aiShutterCurveX')
            y = cmds.getAttr(attr+'['+str(i)+'].aiShutterCurveY')
            curveString += ","+str(y) +"," + str(x) +",1"
            
        cmds.gradientControlNoAttr( gradient, edit=True, asString=curveString) 
        
        pm.floatField(valueField, edit=True, value=startY, changeCommand=pm.Callback(self.updateValue, attr, gradient, valueField, positionField))
        pm.floatField(positionField, edit=True, value=startX, changeCommand=pm.Callback(self.updatePosition, attr, gradient, valueField, positionField))
        
    def updateRamp( self, attr ):
        name = self.nodeName
        translator = cmds.getAttr(self.nodeAttr('aiTranslator'))

        uiParent = pm.setParent( q = True )
        controls = pm.columnLayout( uiParent, q=True, ca=True )
        
        curveString = ""
        attr = self.nodeAttr('aiShutterCurve')
        size = cmds.getAttr(attr, size=True)
        if size > 0:
            x = cmds.getAttr(attr+'[0].aiShutterCurveX')
            y = cmds.getAttr(attr+'[0].aiShutterCurveY')
            curveString += str(y) +"," + str(x) +",1"
        else:
            curveString += "1,0,1"
        for i in range(1,size):
            x = cmds.getAttr(attr+'['+str(i)+'].aiShutterCurveX')
            y = cmds.getAttr(attr+'['+str(i)+'].aiShutterCurveY')
            curveString += ","+str(y) +"," + str(x) +",1"
            
        valuesSplit = curveString.split(",")
        
        if controls:
            for c in controls:
                control = c +"|ShutterCurveRowLayout|ShutterCurveGradientControl"
                valueField = c +"|ShutterCurveRowLayout|ShutterCurveColumLayout|ShutterCurveValueLayout|ShutterCurveValueField"
                positionField = c +"|ShutterCurveRowLayout|ShutterCurveColumLayout|ShutterCurvePositionLayout|ShutterCurvePositionField"
                cmds.gradientControlNoAttr( control, edit=True, asString=curveString)
                current = cmds.gradientControlNoAttr( control, query=True, currentKey=True) 
                
                pm.floatField(valueField, edit=True, value=float(valuesSplit[current*3]))
                pm.floatField(positionField, edit=True, value=float(valuesSplit[current*3+1]))

    
    def addCommonAttributes(self):
        self.addControl("aiExposure")
        self.addControl("aiFiltermap")
        self.addSeparator()
        self.addControl("aiRollingShutter")
        self.addControl("aiRollingShutterDuration")
        
    def addDOFAttributes(self):
        self.addSeparator()
        self.addControl("aiEnableDOF", label="Enable DOF")
        self.addControl("aiFocusDistance")
        self.addControl("aiApertureSize")
        self.addControl("aiApertureBlades")
        self.addControl("aiApertureBladeCurvature")
        self.addControl("aiApertureRotation")
        self.addControl("aiApertureAspectRatio")
        
    def addShutterAttributes(self):
        self.addSeparator()
        self.addControl("motionBlurOverride", label="Camera Motion Blur")
        self.addControl("aiShutterStart")
        self.addControl("aiShutterEnd")
        self.addControl("aiShutterType")
        self.addCustom( "aiShutterCurve", self.createRamp, self.updateRamp )
        

class PerspCameraTemplate(CameraTemplate):
    def setup(self):
        self.addCommonAttributes()
        self.addDOFAttributes()
        self.addSeparator()
        self.addControl('aiUvRemap', label="UV Remap")
        self.addShutterAttributes()
        self.addSeparator()
        self.addControl("aiUserOptions", label="User Options")

templates.registerTranslatorUI(PerspCameraTemplate, "camera", "perspective")
templates.registerTranslatorUI(PerspCameraTemplate, "stereoRigCamera", "perspective")


class OrthographicTemplate(CameraTemplate):
    def setup(self):
        self.addCommonAttributes()
        self.addShutterAttributes()
        self.addSeparator()
        self.addControl("aiUserOptions", label="User Options")

templates.registerTranslatorUI(OrthographicTemplate, "camera", "orthographic")
templates.registerTranslatorUI(OrthographicTemplate, "stereoRigCamera", "orthographic")

class FisheyeCameraTemplate(CameraTemplate):
    def setup(self):
        self.addCommonAttributes()
        self.addDOFAttributes()
        self.addSeparator()
        self.addControl('aiFov')
        self.addControl('aiAutocrop')
        self.addShutterAttributes()
        self.addSeparator()
        self.addControl("aiUserOptions", label="User Options")

templates.registerTranslatorUI(FisheyeCameraTemplate, "camera", "fisheye")
templates.registerTranslatorUI(FisheyeCameraTemplate, "stereoRigCamera", "fisheye")

class CylCameraTemplate(CameraTemplate):
    def setup(self):
        self.addCommonAttributes()
        self.addControl('aiHorizontalFov')
        self.addControl('aiVerticalFov')
        self.addControl('aiProjective')
        self.addShutterAttributes()
        self.addSeparator()
        self.addControl("aiUserOptions", label="User Options")

templates.registerTranslatorUI(CylCameraTemplate, "camera", "cylindrical")
templates.registerTranslatorUI(CylCameraTemplate, "stereoRigCamera", "cylindrical")

class SphericalCameraTemplate(CameraTemplate):
    def setup(self):
        self.addCommonAttributes()
        self.addShutterAttributes()
        self.addSeparator()
        self.addControl("aiUserOptions", label="User Options")

templates.registerTranslatorUI(SphericalCameraTemplate, "camera", "spherical")
templates.registerTranslatorUI(SphericalCameraTemplate, "stereoRigCamera", "spherical")

def cameraOrthographicChanged(orthoPlug, *args):
    "called to sync .aiTranslator when .orthographic changes"
    if not core.arnoldIsCurrentRenderer(): return
    fnCam = om.MFnCamera(orthoPlug.node())
    transPlug = fnCam.findPlug('aiTranslator')
    if not transPlug.isNull():
        isOrtho = orthoPlug.asBool()
        
        currTrans = transPlug.asString()
        #print "cameraOrthographicChanged", fnCam.name(), currTrans, isOrtho
        newTrans = None
        if isOrtho and currTrans != 'orthographic':
            newTrans = 'orthographic'
        elif not isOrtho and currTrans == 'orthographic':
            newTrans = 'perspective'
        #print "newTrans", newTrans
        if newTrans:
            transPlug.setString(newTrans)

def cameraTranslatorChanged(transPlug, *args):
    "called to sync .orthographic when .aiTranslator changes"
    if not core.arnoldIsCurrentRenderer(): return
    fnCam = om.MFnCamera(transPlug.node())
    currTrans = transPlug.asString()
    orthoPlug = fnCam.findPlug('orthographic')
    isOrtho = orthoPlug.asBool()
    #print "cameraTranslatorChanged", fnCam.name(), currTrans, isOrtho
    # when a file is opening, we need to choose one attribute to lead, because
    # the order that attributes are set is unpredictable. This fixes a case
    # where translators may have gotten out of sync
    if om.MFileIO.isOpeningFile():
        if isOrtho and currTrans != 'orthographic':
            orthoPlug.setBool(True)
    else:
        if not isOrtho and currTrans == 'orthographic':
            orthoPlug.setBool(True)
        elif isOrtho and currTrans != 'orthographic':
            orthoPlug.setBool(False)

def getCameraDefault(obj):
    isOrtho = pm.api.MFnDependencyNode(obj).findPlug("orthographic").asBool()
    default = 'orthographic' if isOrtho else 'perspective'
    return default

templates.registerDefaultTranslator('camera', getCameraDefault)
templates.registerDefaultTranslator('stereoRigCamera', getCameraDefault)

callbacks.addAttributeChangedCallbacks('camera',
                                       [('aiTranslator', cameraTranslatorChanged),
                                        ('orthographic', cameraOrthographicChanged)])

callbacks.addAttributeChangedCallbacks('stereoRigCamera',
                                       [('aiTranslator', cameraTranslatorChanged),
                                        ('orthographic', cameraOrthographicChanged)])

def registerDriverTemplates():
    skipDrivers = ['exr', 'deepexr']
    # register driver templates
    for transName, arnoldNode in core.listTranslators("aiAOVDriver"):
        if not (transName in skipDrivers): # we want to use a custom ui for the EXR translator
            templates.registerAutoTranslatorUI(arnoldNode, "aiAOVDriver", transName, skipEmpty=True)

    templates.registerDefaultTranslator('aiAOVDriver', 'exr')

templatesNames = []
    
class EXRDriverTranslatorUI(templates.AttributeTemplate):
    def changeAttrName(self, nodeName, attrNameText, index):
        # Get the attribute name, type and value
        attrName = nodeName+'['+str(index)+']'
        metadata = cmds.getAttr(attrName)
        result = metadata.split(' ', 2 )
        result += [""] * (3-len(result))
        
        # Get the new name
        name = cmds.textField(attrNameText, query=True, text=True)
        
        # Update the name in all the templates
        templatesNames[:] = [tup for tup in templatesNames if cmds.columnLayout(tup, exists=True)]
        for templateName in templatesNames:
            cmds.textField(templateName+"|mtoa_exrMetadataRow_"+str(index)+"|MtoA_exrMAttributeName", edit=True, text=name.replace(" ", ""))
        
        # Update the metadata value
        metadata = result[0]+" "+name.replace(" ", "")+" "+result[2]
        cmds.setAttr(attrName, metadata, type="string")
    
    def changeAttrType(self, nodeName, menu, index):
        # Get the attribute name, type and value
        attrName = nodeName+'['+str(index)+']'
        metadata = cmds.getAttr(attrName)
        result = metadata.split(' ', 2 )
        result += [""] * (3-len(result))
        
        # Get the new type
        typeNumber = cmds.optionMenu(menu, query=True, select=True)
        type = cmds.optionMenu(menu, query=True, value=True)
        
        # Update the type in all the templates
        templatesNames[:] = [tup for tup in templatesNames if cmds.columnLayout(tup, exists=True)]
        for templateName in templatesNames:
            cmds.optionMenu(templateName+"|mtoa_exrMetadataRow_"+str(index)+"|MtoA_exrMAttributeType", edit=True, select=typeNumber)
            
        # Update the metadata value
        metadata = type+" "+result[1]+" "+result[2]
        cmds.setAttr(attrName, metadata, type="string")
        
    def changeAttrValue(self, nodeName, attrValueText, index):
        # Get the attribute name, type and value
        attrName = nodeName+'['+str(index)+']'
        metadata = cmds.getAttr(attrName)
        result = metadata.split(' ', 2 )
        result += [""] * (3-len(result))

        # Get the new value
        value = cmds.textField(attrValueText, query=True, text=True)
        
        # Update the value in all the templates
        templatesNames[:] = [tup for tup in templatesNames if cmds.columnLayout(tup, exists=True)]
        for templateName in templatesNames:
            cmds.textField(templateName+"|mtoa_exrMetadataRow_"+str(index)+"|MtoA_exrMAttributeValue", edit=True, text=value)
        
        # Update the metadata value
        metadata = result[0]+" "+result[1]+" "+value
        cmds.setAttr(attrName, metadata, type="string")
        
    def removeAttribute(self, nodeName, index):
        cmds.removeMultiInstance(nodeName+'['+str(index)+']')
        self.updatedMetadata(nodeName)
        
    def addAttribute(self, nodeName):
        next = 0
        if cmds.getAttr(nodeName, multiIndices=True):
            next = cmds.getAttr(nodeName, multiIndices=True)[-1] + 1
        cmds.setAttr(nodeName+'['+str(next)+']', "INT", type="string")
        self.updatedMetadata(nodeName)
        
    def updateLine(self, nodeName, metadata, index):
        # Attribute controls will be created with the current metadata content
        result = metadata.split(' ', 2 )
        result += [""] * (3-len(result))
        
        # Attribute Name
        attrNameText = cmds.textField("MtoA_exrMAttributeName", text=result[1])
        cmds.textField(attrNameText, edit=True, changeCommand=pm.Callback(self.changeAttrName, nodeName, attrNameText, index))
        
        # Attribute Type
        menu = cmds.optionMenu("MtoA_exrMAttributeType")
        cmds.menuItem( label='INT', data=0)
        cmds.menuItem( label='FLOAT', data=1)
        cmds.menuItem( label='POINT2', data=2)
        cmds.menuItem( label='MATRIX', data=3)
        cmds.menuItem( label='STRING', data=4)
        if result[0] == 'INT':
            cmds.optionMenu(menu, edit=True, select=1)
        elif result[0] == 'FLOAT':
            cmds.optionMenu(menu, edit=True, select=2)
        elif result[0] == 'POINT2':
            cmds.optionMenu(menu, edit=True, select=3)
        elif result[0] == 'MATRIX':
            cmds.optionMenu(menu, edit=True, select=4)
        elif result[0] == 'STRING':
            cmds.optionMenu(menu, edit=True, select=5)
        cmds.optionMenu(menu, edit=True, changeCommand=pm.Callback(self.changeAttrType, nodeName, menu, index))
        
        # Attribute Value
        attrValueText = cmds.textField("MtoA_exrMAttributeValue", text=result[2])
        cmds.textField(attrValueText, edit=True, changeCommand=pm.Callback(self.changeAttrValue, nodeName, attrValueText, index))
        
        # Remove button
        cmds.symbolButton(image="SP_TrashIcon.png", command=pm.Callback(self.removeAttribute, nodeName, index))
        
    def updatedMetadata(self, nodeName):
        templatesNames[:] = [tup for tup in templatesNames if cmds.columnLayout(tup, exists=True)]
        for templateName in templatesNames:
            cmds.setParent(templateName)
            #Remove all attributes controls and rebuild them again with the metadata updated content
            for child in cmds.columnLayout(templateName, query=True, childArray=True) or []:
                cmds.deleteUI(child)
            for index in cmds.getAttr(nodeName, multiIndices=True) or []:
                attrName = nodeName+'['+str(index)+']'
                metadata = cmds.getAttr(attrName)
                if metadata:
                    cmds.rowLayout('mtoa_exrMetadataRow_'+str(index),nc=4, cw4=(120,80,120,20), cl4=('center', 'center', 'center', 'right'))
                    self.updateLine(nodeName, metadata, index)
                    cmds.setParent('..')
        
    def metadataNew(self, nodeName):
        cmds.rowLayout(nc=2, cw2=(200,140), cl2=('center', 'center'))
        cmds.button( label='Add New Attribute', command=pm.Callback(self.addAttribute, 'defaultArnoldDriver.custom_attributes'))
        cmds.setParent( '..' )
        layout = cmds.columnLayout(rowSpacing=5, columnWidth=340)
        # This template could be created more than once in different panels
        templatesNames.append(layout)
        self.updatedMetadata('defaultArnoldDriver.custom_attributes')
        cmds.setParent( '..' )

    def metadataReplace(self, nodeName):
        pass

    def setup(self):
        self.addControl('exrCompression', label='Compression')
        self.addControl('halfPrecision', label='Half Precision')
        self.addControl('preserveLayerName', label='Preserve Layer Name')
        self.addControl('tiled', label='Tiled')
        self.addControl('autocrop', label='Autocrop')
        self.addControl('append', label='Append')
        self.beginLayout("Metadata (name, type, value)", collapse=True)
        self.addCustom('custom_attributes', self.metadataNew, self.metadataReplace)
        self.endLayout()

templates.registerTranslatorUI(EXRDriverTranslatorUI, 'aiAOVDriver', 'exr')


deepexrToleranceTemplates = []
deepexrHalfPrecisionTemplates = []
deepexrEnableFilteringTemplates = []

class DeepEXRDriverTranslatorUI(templates.AttributeTemplate):
    def __init__(self, nodeType):
        
        aovs.addAOVChangedCallback(self.updateLayerTolerance, 'DeepEXRDriverTranslatorUITolerance')
        aovs.addAOVChangedCallback(self.updateLayerHalfPrecision, 'DeepEXRDriverTranslatorUIHalfPrecision')
        aovs.addAOVChangedCallback(self.updateLayerEnableFiltering, 'DeepEXRDriverTranslatorUIEnableFiltering')
        super(DeepEXRDriverTranslatorUI, self).__init__(nodeType)

    def updateLayerTolerance(self):

        aovList = aovs.getAOVs(enabled=True)

        deepexrToleranceTemplates[:] = [tup for tup in deepexrToleranceTemplates if cmds.columnLayout(tup, exists=True)]
        for templateName in deepexrToleranceTemplates:
            
            driverName = self.nodeName

            # note that this function may be called to fill the defaultArnoldDriver exposed params
            # but with self != defaultArnoldDriver
            # this is because we might want to add this aov name in the default layers* list
            
            # in the render settings window I only want to display the defaultArnoldDriver params
            if templateName[:26] == "unifiedRenderGlobalsWindow":
                driverName = "defaultArnoldDriver"

            cmds.setParent(templateName)
            for child in cmds.columnLayout(templateName, query=True, childArray=True) or []:
                cmds.deleteUI(child)
                
            cmds.attrFieldSliderGrp(label='alpha' , at=driverName + '.alphaTolerance' )
            cmds.attrFieldSliderGrp(label='depth' , at=driverName + '.depthTolerance' )

            if driverName == "defaultArnoldDriver":
                cmds.attrFieldSliderGrp(label='beauty' , at='defaultArnoldDriver.layerTolerance[0]')
                for i in range(0,len(aovList)):
                    if aovList[i].node.attr('outputs')[0].driver.inputs()[0].name() == 'defaultArnoldDriver':
                        labelStr = aovList[i].name
                        attrStr = 'defaultArnoldDriver.layerTolerance['+str(i+1)+']'
                        cmds.attrFieldSliderGrp(label=labelStr , at=attrStr )
            else:
                cmds.attrFieldSliderGrp(label='layer' , at=driverName + '.layerTolerance[0]' )
            
    def updateLayerHalfPrecision(self):
        aovList = aovs.getAOVs(enabled=True)
        
        deepexrHalfPrecisionTemplates[:] = [tup for tup in deepexrHalfPrecisionTemplates if cmds.columnLayout(tup, exists=True)]
        for templateName in deepexrHalfPrecisionTemplates:
            cmds.setParent(templateName)

            driverName = self.nodeName

            # note that this function may be called to fill the defaultArnoldDriver exposed params
            # but with self != defaultArnoldDriver
            # this is because we might want to add this aov name in the default layers* list
            
            # in the render settings window I only want to display the defaultArnoldDriver params
            if templateName[:26] == "unifiedRenderGlobalsWindow":
                driverName = "defaultArnoldDriver"

            for child in cmds.columnLayout(templateName, query=True, childArray=True) or []:
                cmds.deleteUI(child)

            cmds.attrControlGrp(label='alpha' , a=driverName+'.alphaHalfPrecision' )
            cmds.attrControlGrp(label='depth' , a=driverName+'.depthHalfPrecision' )

            if driverName == "defaultArnoldDriver":
                cmds.attrControlGrp(label='beauty' , a='defaultArnoldDriver.layerHalfPrecision[0]' )
           
                for i in range(0,len(aovList)):
                    if aovList[i].node.attr('outputs')[0].driver.inputs()[0].name() == 'defaultArnoldDriver':
                        labelStr = aovList[i].name
                        attrStr = 'defaultArnoldDriver.layerHalfPrecision['+str(i+1)+']'
                        cmds.attrControlGrp(label=labelStr , a=attrStr )
            else:
                cmds.attrControlGrp(label='layer' , a=driverName+'.layerHalfPrecision[0]' )


    def updateLayerEnableFiltering(self):
        aovList = aovs.getAOVs(enabled=True)
        
        deepexrEnableFilteringTemplates[:] = [tup for tup in deepexrEnableFilteringTemplates if cmds.columnLayout(tup, exists=True)]
        for templateName in deepexrEnableFilteringTemplates:
            cmds.setParent(templateName)

            # note that this function may be called to fill the defaultArnoldDriver exposed params
            # but with self != defaultArnoldDriver
            # this is because we might want to add this aov name in the default layers* list
            
            # in the render settings window I only want to display the defaultArnoldDriver params
            driverName = self.nodeName
            if templateName[:26] == "unifiedRenderGlobalsWindow":
                driverName = "defaultArnoldDriver"

            for child in cmds.columnLayout(templateName, query=True, childArray=True) or []:
                cmds.deleteUI(child)

            if driverName == "defaultArnoldDriver":
                cmds.attrControlGrp(label='beauty' , a='defaultArnoldDriver.layerEnableFiltering[0]' )
                for i in range(0,len(aovList)):
                    if aovList[i].node.attr('outputs')[0].driver.inputs()[0].name() == 'defaultArnoldDriver':
                        labelStr = aovList[i].name
                        attrStr = 'defaultArnoldDriver.layerEnableFiltering['+str(i+1)+']'
                        cmds.attrControlGrp(label=labelStr , a=attrStr )
            else:
                cmds.attrControlGrp(label='layer' , a=driverName +'.layerEnableFiltering[0]' )
     
    def layerToleranceNew(self, nodeName):
        layout = cmds.columnLayout(rowSpacing=5, columnWidth=340)
        deepexrToleranceTemplates.append(layout)
        
        self.updateLayerTolerance()
        cmds.setParent( '..' )
        
    def layerToleranceReplace(self, nodeName):

        self.updateLayerTolerance()
        cmds.setParent( '..' )
        
    def layerHalfPrecisionNew(self, nodeName):
        layout = cmds.columnLayout(rowSpacing=5, columnWidth=340)
        deepexrHalfPrecisionTemplates.append(layout)
        self.updateLayerHalfPrecision()
        cmds.setParent( '..' )
        
    def layerHalfPrecisionReplace(self, nodeName):
        self.updateLayerHalfPrecision()
        cmds.setParent( '..' )
        
    def layerEnableFilteringNew(self, nodeName):
        layout = cmds.columnLayout(rowSpacing=5, columnWidth=340)
        deepexrEnableFilteringTemplates.append(layout)
        self.updateLayerEnableFiltering()
        cmds.setParent( '..' )
        
    def layerEnableFilteringReplace(self, nodeName):
        self.updateLayerEnableFiltering()
        cmds.setParent( '..' )

    def changeAttrName(self, nodeName, attrNameText, index):
        # Get the attribute name, type and value
        attrName = nodeName+'['+str(index)+']'
        metadata = cmds.getAttr(attrName)
        result = metadata.split(' ', 2 )
        result += [""] * (3-len(result))
        
        # Get the new name
        name = cmds.textField(attrNameText, query=True, text=True)
        
        # Update the name in all the templates
        templatesNames[:] = [tup for tup in templatesNames if cmds.columnLayout(tup, exists=True)]
        for templateName in templatesNames:
            cmds.textField(templateName+"|mtoa_exrMetadataRow_"+str(index)+"|MtoA_exrMAttributeName", edit=True, text=name.replace(" ", ""))
        
        # Update the metadata value
        metadata = result[0]+" "+name.replace(" ", "")+" "+result[2]
        cmds.setAttr(attrName, metadata, type="string")
    
    def changeAttrType(self, nodeName, menu, index):
        # Get the attribute name, type and value
        attrName = nodeName+'['+str(index)+']'
        metadata = cmds.getAttr(attrName)
        result = metadata.split(' ', 2 )
        result += [""] * (3-len(result))
        
        # Get the new type
        typeNumber = cmds.optionMenu(menu, query=True, select=True)
        type = cmds.optionMenu(menu, query=True, value=True)
        
        # Update the type in all the templates
        templatesNames[:] = [tup for tup in templatesNames if cmds.columnLayout(tup, exists=True)]
        for templateName in templatesNames:
            cmds.optionMenu(templateName+"|mtoa_exrMetadataRow_"+str(index)+"|MtoA_exrMAttributeType", edit=True, select=typeNumber)
            
        # Update the metadata value
        metadata = type+" "+result[1]+" "+result[2]
        cmds.setAttr(attrName, metadata, type="string")
        
    def changeAttrValue(self, nodeName, attrValueText, index):
        # Get the attribute name, type and value
        attrName = nodeName+'['+str(index)+']'
        metadata = cmds.getAttr(attrName)
        result = metadata.split(' ', 2 )
        result += [""] * (3-len(result))

        # Get the new value
        value = cmds.textField(attrValueText, query=True, text=True)
        
        # Update the value in all the templates
        templatesNames[:] = [tup for tup in templatesNames if cmds.columnLayout(tup, exists=True)]
        for templateName in templatesNames:
            cmds.textField(templateName+"|mtoa_exrMetadataRow_"+str(index)+"|MtoA_exrMAttributeValue", edit=True, text=value)
        
        # Update the metadata value
        metadata = result[0]+" "+result[1]+" "+value
        cmds.setAttr(attrName, metadata, type="string")
        
    def removeAttribute(self, nodeName, index):
        cmds.removeMultiInstance(nodeName+'['+str(index)+']')
        self.updatedMetadata(nodeName)
        
    def addAttribute(self, nodeName):
        next = 0
        if cmds.getAttr(nodeName, multiIndices=True):
            next = cmds.getAttr(nodeName, multiIndices=True)[-1] + 1
        cmds.setAttr(nodeName+'['+str(next)+']', "INT", type="string")
        self.updatedMetadata(nodeName)
        
    def updateLine(self, nodeName, metadata, index):
        # Attribute controls will be created with the current metadata content
        result = metadata.split(' ', 2 )
        result += [""] * (3-len(result))
        
        # Attribute Name
        attrNameText = cmds.textField("MtoA_exrMAttributeName", text=result[1])
        cmds.textField(attrNameText, edit=True, changeCommand=pm.Callback(self.changeAttrName, nodeName, attrNameText, index))
        
        # Attribute Type
        menu = cmds.optionMenu("MtoA_exrMAttributeType")
        cmds.menuItem( label='INT', data=0)
        cmds.menuItem( label='FLOAT', data=1)
        cmds.menuItem( label='POINT2', data=2)
        cmds.menuItem( label='MATRIX', data=3)
        cmds.menuItem( label='STRING', data=4)
        if result[0] == 'INT':
            cmds.optionMenu(menu, edit=True, select=1)
        elif result[0] == 'FLOAT':
            cmds.optionMenu(menu, edit=True, select=2)
        elif result[0] == 'POINT2':
            cmds.optionMenu(menu, edit=True, select=3)
        elif result[0] == 'MATRIX':
            cmds.optionMenu(menu, edit=True, select=4)
        elif result[0] == 'STRING':
            cmds.optionMenu(menu, edit=True, select=5)
        cmds.optionMenu(menu, edit=True, changeCommand=pm.Callback(self.changeAttrType, nodeName, menu, index))
        
        # Attribute Value
        attrValueText = cmds.textField("MtoA_exrMAttributeValue", text=result[2])
        cmds.textField(attrValueText, edit=True, changeCommand=pm.Callback(self.changeAttrValue, nodeName, attrValueText, index))
        
        # Remove button
        cmds.symbolButton(image="SP_TrashIcon.png", command=pm.Callback(self.removeAttribute, nodeName, index))
        
    def updatedMetadata(self, nodeName):
        templatesNames[:] = [tup for tup in templatesNames if cmds.columnLayout(tup, exists=True)]
        for templateName in templatesNames:
            cmds.setParent(templateName)
            #Remove all attributes controls and rebuild them again with the metadata updated content
            for child in cmds.columnLayout(templateName, query=True, childArray=True) or []:
                cmds.deleteUI(child)
            for index in cmds.getAttr(nodeName, multiIndices=True) or []:
                attrName = nodeName+'['+str(index)+']'
                metadata = cmds.getAttr(attrName)
                if metadata:
                    cmds.rowLayout('mtoa_exrMetadataRow_'+str(index),nc=4, cw4=(120,80,120,20), cl4=('center', 'center', 'center', 'right'))
                    self.updateLine(nodeName, metadata, index)
                    cmds.setParent('..')
        
    def metadataNew(self, nodeName):
        cmds.rowLayout(nc=2, cw2=(200,140), cl2=('center', 'center'))
        cmds.button( label='Add New Attribute', command=pm.Callback(self.addAttribute, 'defaultArnoldDriver.custom_attributes'))
        cmds.setParent( '..' )
        layout = cmds.columnLayout(rowSpacing=5, columnWidth=340)
        # This template could be created more than once in different panels
        templatesNames.append(layout)
        self.updatedMetadata('defaultArnoldDriver.custom_attributes')
        cmds.setParent( '..' )

    def metadataReplace(self, nodeName):
        pass
        
    def setup(self):
        #self.addControl('tiled', label='Tiled')
        self.addControl('subpixelMerge', label='Subpixel Merge')
        self.addControl('useRGBOpacity', label='Use RGB Opacity')
        self.beginLayout("Tolerance Values", collapse=False)
        self.addCustom('layerToleranceSection', self.layerToleranceNew, self.layerToleranceReplace)
        self.endLayout()
        
        self.beginLayout("Half Precision", collapse=False)
        self.addCustom('layerHalfPrecisionSection', self.layerHalfPrecisionNew, self.layerHalfPrecisionReplace)
        self.endLayout()
        
        self.beginLayout("Enable Filtering", collapse=False)
        self.addCustom('layerEnableFilteringSection', self.layerEnableFilteringNew, self.layerEnableFilteringReplace)
        self.endLayout()
        
        self.beginLayout("Metadata (name, type, value)", collapse=True)
        self.addCustom('custom_attributes', self.metadataNew, self.metadataReplace)
        self.endLayout()

templates.registerTranslatorUI(DeepEXRDriverTranslatorUI, 'aiAOVDriver', 'deepexr')

def registerFilterTemplates():
    # register driver templates
    for transName, arnoldNode in core.listTranslators("aiAOVFilter"):
        templates.registerAutoTranslatorUI(arnoldNode, "aiAOVFilter", transName, skipEmpty=True)

    templates.registerDefaultTranslator('aiAOVFilter', 'gaussian')

registerDriverTemplates()
registerFilterTemplates()
