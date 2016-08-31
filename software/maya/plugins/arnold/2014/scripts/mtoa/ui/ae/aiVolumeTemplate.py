import re
import maya.cmds as cmds
import maya.mel as mel
from mtoa.ui.ae.utils import aeCallback
import mtoa.core as core
import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate
        
def ArnoldVolumeTypeChange(nodeName):
    type = cmds.getAttr(nodeName+'.type')
    dim = (type == 0) # "Custom"
    pm.editorTemplate(dimControl=(nodeName, "filename", dim))
    pm.editorTemplate(dimControl=(nodeName, "grids", dim))
    pm.editorTemplate(dimControl=(nodeName, "frame", dim))
    pm.editorTemplate(dimControl=(nodeName, "padding", dim))
    
    pm.editorTemplate(dimControl=(nodeName, "velocityGrids", dim))
    pm.editorTemplate(dimControl=(nodeName, "velocityScale", dim))
    pm.editorTemplate(dimControl=(nodeName, "velocityFps", dim))
    pm.editorTemplate(dimControl=(nodeName, "velocityShutterStart", dim))
    pm.editorTemplate(dimControl=(nodeName, "velocityShutterEnd", dim))
    
    pm.editorTemplate(dimControl=(nodeName, "dso", not dim))
    pm.editorTemplate(dimControl=(nodeName, "data", not dim))

def ArnoldVolumeDsoEdit(nodeName, mPath) :
    cmds.setAttr(nodeName,mPath,type='string')

def LoadVolumeDsoButtonPush(nodeName):
    basicFilter = 'Volume Plugin(*.so *.dll *.dylib)'
    projectDir = cmds.workspace(query=True, directory=True)     
    ret = cmds.fileDialog2(fileFilter=basicFilter, cap='Load Volume Plugin',okc='Load',fm=1, startingDirectory=projectDir)
    if ret is not None and len(ret):
        ArnoldVolumeDsoEdit(nodeName, ret[0])
        cmds.textField('arnoldVolumeDsoPath', edit=True, text=ret[0])
    
def ArnoldVolumeTemplateDsoNew(nodeName) :
    cmds.rowColumnLayout( numberOfColumns=3, columnAlign=[(1, 'right'),(2, 'right'),(3, 'left')], columnAttach=[(1, 'right', 0), (2, 'both', 0), (3, 'left', 5)], columnWidth=[(1,145),(2,220),(3,30)] )
    cmds.text(label='DSO ')
    path = cmds.textField('arnoldVolumeDsoPath',changeCommand=lambda *args: ArnoldVolumeDsoEdit(nodeName, *args))
    cmds.textField( path, edit=True, text=cmds.getAttr(nodeName) )
    cmds.symbolButton('arnoldVolumeDsoPathButton', height=20, image='navButtonBrowse.png', command=lambda *args: LoadVolumeDsoButtonPush(nodeName))
    
def ArnoldVolumeTemplateDsoReplace(plugName) :
    cmds.textField( 'arnoldVolumeDsoPath', edit=True, changeCommand=lambda *args: ArnoldVolumeDsoEdit(plugName, *args))
    cmds.textField( 'arnoldVolumeDsoPath', edit=True, text=cmds.getAttr(plugName) )
    cmds.symbolButton('arnoldVolumeDsoPathButton', edit=True, image='navButtonBrowse.png' , command=lambda *args: LoadVolumeDsoButtonPush(plugName))
    

def ArnoldVolumeFilenameEdit(nodeName, mPath) :
    cmds.setAttr(nodeName,mPath,type='string')

def LoadVolumeFilenameButtonPush(nodeName):
    basicFilter = 'OpenVDB File(*.vdb)'
    projectDir = cmds.workspace(query=True, directory=True)     
    ret = cmds.fileDialog2(fileFilter=basicFilter, cap='Load OpenVDB File',okc='Load',fm=1, startingDirectory=projectDir)
    if ret is not None and len(ret):
        ArnoldVolumeFilenameEdit(nodeName, ret[0])
        cmds.textField('arnoldVolumeFilenamePath', edit=True, text=ret[0])
    
def ArnoldVolumeTemplateFilenameNew(nodeName) :
    cmds.rowColumnLayout( numberOfColumns=3, columnAlign=[(1, 'right'),(2, 'right'),(3, 'left')], columnAttach=[(1, 'right', 0), (2, 'both', 0), (3, 'left', 5)], columnWidth=[(1,145),(2,220),(3,30)] )
    cmds.text(label='Filename ')
    path = cmds.textField('arnoldVolumeFilenamePath',changeCommand=lambda *args: ArnoldVolumeFilenameEdit(nodeName, *args))
    cmds.textField( path, edit=True, text=cmds.getAttr(nodeName) )
    cmds.symbolButton('arnoldVolumeFilenamePathButton', height=20, image='navButtonBrowse.png', command=lambda *args: LoadVolumeFilenameButtonPush(nodeName))
    
def ArnoldVolumeTemplateFilenameReplace(plugName) :
    cmds.textField( 'arnoldVolumeFilenamePath', edit=True, changeCommand=lambda *args: ArnoldVolumeFilenameEdit(plugName, *args))
    cmds.textField( 'arnoldVolumeFilenamePath', edit=True, text=cmds.getAttr(plugName) )
    cmds.symbolButton('arnoldVolumeFilenamePathButton', edit=True, image='navButtonBrowse.png' , command=lambda *args: LoadVolumeFilenameButtonPush(plugName))
        
class AEaiVolumeTemplate(ShaderAETemplate):
    def setup(self):
        self.beginScrollLayout()
        
        self.beginLayout('Volume Attributes', collapse=False)        
        self.addControl('type', changeCommand=ArnoldVolumeTypeChange)
        
        self.addSeparator()
        
        self.addCustom('dso', ArnoldVolumeTemplateDsoNew, ArnoldVolumeTemplateDsoReplace)
        self.addControl('data')
        
        self.addCustom('filename', ArnoldVolumeTemplateFilenameNew, ArnoldVolumeTemplateFilenameReplace)
        self.addControl('grids')
        self.addControl('frame')
        
        self.addControl('padding')
        self.addControl('MinBoundingBox')
        self.addControl('MaxBoundingBox')
        self.addControl('stepSize')
        self.addControl('loadAtInit')
        
        self.addSeparator()
        
        self.addControl('velocityGrids')
        self.addControl('velocityScale')
        self.addControl('velocityFps')
        self.addControl('velocityShutterStart')
        self.addControl('velocityShutterEnd')
        
        self.addSeparator()
        
        self.endLayout()
        
        
        self.beginLayout('Render Stats', collapse=True)
        self.beginNoOptimize()
        self.addControl("castsShadows")
        self.addControl("receiveShadows")
        self.addControl("primaryVisibility")
        self.addControl("visibleInReflections")
        self.addControl("visibleInRefractions")

        self.addSeparator()
    
        self.addControl("aiSelfShadows", label="Self Shadows")
        self.addControl("aiVisibleInDiffuse", label="Visible In Diffuse")
        self.addControl("aiVisibleInGlossy", label="Visible In Glossy")
        self.addControl("aiMatte", label="Matte")
        self.addControl("aiTraceSets", label="Trace Sets")
        
        self.endNoOptimize()
        
        self.endLayout()
    

        # include/call base class/node attributes
        pm.mel.AEdependNodeTemplate(self.nodeName)
        
        self.suppress('blackBox')
        self.suppress('containerType')
        self.suppress('templateName')
        self.suppress('viewName')
        self.suppress('iconName')
        self.suppress('templateVersion')
        self.suppress('uiTreatment')
        self.suppress('customTreatment')
        self.suppress('creator')
        self.suppress('creationDate')
        self.suppress('rmbCommand')
        self.suppress('templatePath')
        self.suppress('viewMode')
        self.suppress('ignoreHwShader')
        self.suppress('boundingBoxScale')
        self.suppress('featureDisplacement')
        self.suppress('boundingBoxScale')
        self.suppress('initialSampleRate')
        self.suppress('extraSampleRate')
        self.suppress('textureThreshold')
        self.suppress('normalThreshold')
        self.suppress('lodVisibility')
        self.suppress('ghostingControl')
        self.suppress('ghostPreSteps')
        self.suppress('ghostPostSteps')
        self.suppress('ghostStepSize')
        self.suppress('ghostRangeStart')
        self.suppress('ghostRangeEnd')
        self.suppress('ghostDriver')
        self.suppress('ghostFrames')
        self.suppress('ghosting')
        self.suppress('ghostCustomSteps')
        self.suppress('ghostColorPreA')
        self.suppress('ghostColorPre')
        self.suppress('ghostColorPostA')
        self.suppress('ghostColorPost')
        self.suppress('tweak')
        self.suppress('relativeTweak')
        self.suppress('currentUVSet')
        self.suppress('displayImmediate')
        self.suppress('displayColors')
        self.suppress('displayColorChannel')
        self.suppress('currentColorSet')
        self.suppress('smoothShading')
        self.suppress('drawOverride')
        self.suppress('shadingSamples')
        self.suppress('maxVisibilitySamplesOverride')
        self.suppress('maxVisibilitySamples')
        self.suppress('antialiasingLevel')
        self.suppress('maxShadingSamples')
        self.suppress('shadingSamplesOverride')
        self.suppress('geometryAntialiasingOverride')
        self.suppress('antialiasingLevel')
        self.suppress('volumeSamplesOverride')
        self.suppress('volumeSamples')
        self.suppress('depthJitter')
        self.suppress('ignoreSelfShadowing')
        self.suppress('controlPoints')
        self.suppress('colorSet')
        self.suppress('uvSet')
        self.suppress('weights')
        self.suppress('renderInfo')
        self.suppress('renderLayerInfo')
        self.suppress('compInstObjGroups')
        self.suppress('instObjGroups')
        self.suppress('collisionOffsetVelocityIncrement')
        self.suppress('collisionOffsetVelocityMultiplier')
        self.suppress('collisionDepthVelocityMultiplier')
        self.suppress('collisionDepthVelocityIncrement')
    
        self.addExtraControls()
        self.endScrollLayout()




  
