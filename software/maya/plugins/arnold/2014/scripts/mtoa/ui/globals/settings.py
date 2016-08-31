
from mtoa.ui.ae.templates import createTranslatorMenu
from mtoa.callbacks import *
import mtoa.core as core
import arnold as ai
import maya.cmds as cmds

def updateRenderSettings(*args):
    flag = pm.getAttr('defaultArnoldRenderOptions.threads_autodetect') == False
    pm.attrControlGrp('os_threads', edit=True, enable=flag)
    flag = pm.getAttr('defaultArnoldRenderOptions.renderUnit') == 1
    pm.attrControlGrp('os_scene_scale', edit=True, enable=flag)
    
def updateAutotileSettings(*args):
    flag = pm.getAttr('defaultArnoldRenderOptions.autotile')
    #if flag:
        
    pm.attrControlGrp('ts_texture_autotile', edit=True, enable=flag)

def updateSamplingSettings(*args):
    flag = (pm.getAttr('defaultArnoldRenderOptions.use_sample_clamp') == True) 
    pm.attrControlGrp('ss_max_value', edit=True, enable=flag)
    pm.attrControlGrp('ss_clamp_sample_values_AOVs', edit=True, enable=flag)

def calculateRayCounts(AASamples, rayTypeSamples, rayTypeDepth):
    computed = 0
    computedDepth = 0

    if rayTypeDepth > 1:
        computed = AASamples * rayTypeSamples * rayTypeSamples
        computedDepth = (rayTypeSamples * rayTypeSamples + rayTypeDepth - 1) * AASamples
    elif rayTypeDepth == 1:
        computed = AASamples * rayTypeSamples * rayTypeSamples
        computedDepth = computed

    return (computed, computedDepth)

def updateComputeSamples(*args):
    AASamples = pm.getAttr('defaultArnoldRenderOptions.AASamples')
    GISamples = pm.getAttr('defaultArnoldRenderOptions.GIDiffuseSamples')
    glossySamples = pm.getAttr('defaultArnoldRenderOptions.GIGlossySamples')
    refractionSamples = pm.getAttr('defaultArnoldRenderOptions.GIRefractionSamples')
    
    diffuseDepth = pm.getAttr('defaultArnoldRenderOptions.GIDiffuseDepth')
    glossyDepth = pm.getAttr('defaultArnoldRenderOptions.GIGlossyDepth')
    refractionDepth = pm.getAttr('defaultArnoldRenderOptions.GIRefractionDepth')
    
    if AASamples <= 0:
        AASamples = 1
    AASamplesComputed = AASamples * AASamples

    GISamplesComputed, GISamplesComputedDepth = calculateRayCounts(AASamplesComputed, GISamples, diffuseDepth)
    glossySamplesComputed, glossySamplesComputedDepth = calculateRayCounts(AASamplesComputed, glossySamples, glossyDepth)
    refractionSamplesComputed, refractionSamplesComputedDepth = calculateRayCounts(AASamplesComputed, refractionSamples, refractionDepth)
    
    totalSamples = AASamplesComputed + GISamplesComputed + glossySamplesComputed + refractionSamplesComputed
    totalSamplesDepth = AASamplesComputed + GISamplesComputedDepth + glossySamplesComputedDepth + refractionSamplesComputedDepth

    pm.text("textAASamples",
            edit=True, 
            label='Camera (AA) Samples : %i' % AASamplesComputed)

    pm.text("textGISamples",
            edit=True, 
            label='Diffuse Samples : %i (max : %i)' % (GISamplesComputed, GISamplesComputedDepth))
    
    pm.text("textGlossySamples",
            edit=True, 
            label='Glossy Samples : %i (max : %i)' % (glossySamplesComputed, glossySamplesComputedDepth))
        
    pm.text("textRefractionSamples",
            edit=True, 
            label='Refraction Samples : %i (max : %i)' % (refractionSamplesComputed, refractionSamplesComputedDepth))
        
    pm.text("textTotalSamples",
            edit=True, 
            label='Total (no lights) : %i (max : %i)' % (totalSamples, totalSamplesDepth))

def updateMotionBlurSettings(*args):
    flag = pm.getAttr('defaultArnoldRenderOptions.motion_blur_enable') == True
    pm.attrControlGrp('mb_object_deform_enable', edit=True, enable=flag)
    pm.attrControlGrp('mb_camera_enable', edit=True, enable=flag)
    pm.attrControlGrp('mb_motion_steps', edit=True, enable=flag)
    pm.attrControlGrp('mb_motion_frames', edit=True, enable=flag)
    pm.attrControlGrp('textArnoldMBAngle', edit=True, enable=flag)
    pm.attrControlGrp('mb_position', edit=True, enable=flag)
    if flag:
        arnoldMotionBlurPositionChanged()
    else:
        pm.attrControlGrp('mb_motion_frames', edit=True, enable=False)
        pm.attrControlGrp('mb_motion_range_start', edit=True, enable=False)
        pm.attrControlGrp('mb_motion_range_end', edit=True, enable=False)

def updateLogSettings(*args):
    name = pm.getAttr('defaultArnoldRenderOptions.log_filename')
    logToFile = pm.getAttr('defaultArnoldRenderOptions.log_to_file')

def getBackgroundShader(*args):
    if cmds.objExists('defaultArnoldRenderOptions.background'):
        conns = pm.listConnections('defaultArnoldRenderOptions.background', s=True, d=False, p=True)
        if conns:
            return conns[0].split('.')[0]
    return ""

def selectBackground(*args):
    node = getBackgroundShader()
    if node:
        pm.select(node, r=True)

def changeBackground(node, field, select):
    connection = pm.listConnections('defaultArnoldRenderOptions.background')
    if connection:
        if pm.nodeType(connection[0]) == 'transform':
            connection = pm.listRelatives(connection[0], s=True)
        if str(connection[0]) == str(node):
            selectBackground()
            return 0
    pm.connectAttr("%s.message"%node,'defaultArnoldRenderOptions.background', force=True)
    if field is not None:
        pm.textField(field, edit=True, text=node)
        pm.symbolButton(select, edit=True, enable=True)
    selectBackground()

def createBackground(type, field, select):
    bg = getBackgroundShader()
    #if bg:
        #pm.delete(bg)
    node = pm.shadingNode(type, asShader=True, name=type)
    changeBackground(node, field, select)

def removeBackground(field, doDelete, select):
    node = getBackgroundShader()
    if node:
        pm.disconnectAttr("%s.message"%node, 'defaultArnoldRenderOptions.background')
        pm.textField(field, edit=True, text="")
        pm.symbolButton(select, edit=True, enable=False)
        if doDelete:
            pm.delete(node)

def buildBackgroundMenu(popup, field, select):

    switches = pm.ls(type='aiRaySwitch')
    skies = pm.ls(type='aiSky')
    pSkies = pm.ls(type='aiPhysicalSky')

    pm.popupMenu(popup, edit=True, deleteAllItems=True)
    for item in skies:
        pm.menuItem(parent=popup, label=item, command=Callback(changeBackground, item, field, select))

    pm.menuItem(parent=popup, divider=True)
    
    for item in pSkies:
        pm.menuItem(parent=popup, label=item, command=Callback(changeBackground, item, field, select))

    pm.menuItem(parent=popup, divider=True)

    for item in switches:
        pm.menuItem(parent=popup, label=item, command=Callback(changeBackground, item, field, select))

    pm.menuItem(parent=popup, divider=True)
    

    pm.menuItem(parent=popup, label="Create Sky Shader", command=Callback(createBackground, "aiSky", field, select))
    pm.menuItem(parent=popup, label="Create Physical Sky Shader", command=Callback(createBackground, "aiPhysicalSky", field, select))
    pm.menuItem(parent=popup, label="Create RaySwitch Shader", command=Callback(createBackground, "aiRaySwitch", field, select))

    pm.menuItem(parent=popup, divider=True)

    pm.menuItem(parent=popup, label="Disconnect", command=Callback(removeBackground, field, False, select))
    pm.menuItem(parent=popup, label="Delete", command=Callback(removeBackground, field, True, select))

    
def getAtmosphereShader(*args):
    conns = pm.listConnections('defaultArnoldRenderOptions.atmosphere', s=True, d=False, p=True)
    if conns:
        return conns[0].split('.')[0]
    return ""

def selectAtmosphere(*args):
    node = getAtmosphereShader()
    if node:
        pm.select(node, r=True)
        
def changeAtmosphere(node, field, select):
    connection = pm.listConnections('defaultArnoldRenderOptions.atmosphere')
    if connection:
        if pm.nodeType(connection[0]) == 'transform':
            connection = pm.listRelatives(connection[0], s=True)
        if str(connection[0]) == str(node):
            selectAtmosphere()
            return 0
    pm.connectAttr("%s.message"%node,'defaultArnoldRenderOptions.atmosphere', force=True)
    if field is not None:
        pm.textField(field, edit=True, text=node)
        pm.symbolButton(select, edit=True, enable=True)
    selectAtmosphere()

def createAtmosphere(type, field, select):
    bg = getAtmosphereShader()
    node = pm.shadingNode(type, asShader=True, name=type)
    changeAtmosphere(node, field, select)

def removeAtmosphere(field, doDelete, select):
    node = getAtmosphereShader()
    if node:
        pm.disconnectAttr("%s.message"%node, 'defaultArnoldRenderOptions.atmosphere')
        pm.textField(field, edit=True, text="")
        pm.symbolButton(select, edit=True, enable=False)
        if doDelete:
            pm.delete(node)
    
def buildAtmosphereMenu(popup, field, select):

    pm.popupMenu(popup, edit=True, deleteAllItems=True)

    for typ in pm.listNodeTypes(['rendernode/arnold/shader/volume/atmosphere']) or []:
        shaders = pm.ls(type=typ)
        for item in shaders:
            pm.menuItem(parent=popup, label=item, command=Callback(changeAtmosphere, item, field, select))
    
    pm.menuItem(parent=popup, divider=True)
    
    for typ in pm.listNodeTypes(['rendernode/arnold/shader/volume/atmosphere']) or []:
        menuLabel = "Create "+typ
        pm.menuItem(parent=popup, label=menuLabel, command=Callback(createAtmosphere, typ, field, select))
        
    pm.menuItem(parent=popup, divider=True)

    pm.menuItem(parent=popup, label="Disconnect", command=Callback(removeAtmosphere, field, False, select))
    pm.menuItem(parent=popup, label="Delete", command=Callback(removeAtmosphere, field, True, select))
    
def changeRenderType():
    try:
        enabled = pm.getAttr('defaultArnoldRenderOptions.renderType') == 2
        pm.attrControlGrp('os_kickRenderFlags',
                            edit=True,
                            enable=enabled)
    except:
        pass

def setupOriginText():
    sel = cmds.listConnections('defaultArnoldRenderOptions.origin', d=0, s=1)
    if (sel != None) and (len(sel) > 0):
        tr = sel[0]
        pm.textField('defaultArnoldRenderOptionsOriginTextField', e=1, text=tr)

def selectOrigin(*args, **kwargs):
    sel = cmds.ls(sl=1, transforms=1, long=1)

    if (sel != None) and (len(sel) > 0):
        tr = sel[0]
        if cmds.objExists('%s.message' % tr):
            cmds.connectAttr('%s.message' % tr, 'defaultArnoldRenderOptions.origin', force=1)
    setupOriginText()

def createArnoldRenderSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout('arnoldRenderLayout', adjustableColumn=True)

    pm.attrControlGrp('os_renderType',
                        label="Render Type",
                        changeCommand=changeRenderType,
                        attribute='defaultArnoldRenderOptions.renderType')

    

    pm.separator()

    pm.attrControlGrp('os_bucket_scanning',
                        label="Bucket Scanning",
                        attribute='defaultArnoldRenderOptions.bucketScanning')

    pm.attrControlGrp('os_bucket_size',
                        label="Bucket Size",
                        attribute='defaultArnoldRenderOptions.bucketSize')

    
    pm.attrControlGrp('os_output_overscan',
                        label='Overscan',
                        attribute='defaultArnoldRenderOptions.outputOverscan')
    
    pm.separator()

    pm.checkBoxGrp('os_threads_autodetect',
                    cc=updateRenderSettings,
                    label='',
                    label1='Autodetect Threads')

    pm.connectControl('os_threads_autodetect', 'defaultArnoldRenderOptions.threads_autodetect', index=2)

    pm.attrControlGrp('os_threads',
                        label="Threads",
                        attribute='defaultArnoldRenderOptions.threads')

    pm.separator()

    pm.attrControlGrp('os_binary_ass',
                        label='Binary-encode ASS Files',
                        attribute='defaultArnoldRenderOptions.binaryAss')
    
                    
    pm.attrControlGrp('os_outputAssBoundingBox',
                        label="Export Bounding Box (.asstoc)",
                        attribute='defaultArnoldRenderOptions.outputAssBoundingBox')                   
                   
    pm.attrControlGrp('os_expandProcedurals',
                        label='Expand Procedurals',
                        attribute='defaultArnoldRenderOptions.expandProcedurals')

    pm.separator()

    enabled = pm.getAttr('defaultArnoldRenderOptions.renderType') == 2

    pm.attrControlGrp('os_kickRenderFlags',
                        label='Kick Render Flags',
                        enable=enabled,
                        attribute='defaultArnoldRenderOptions.kickRenderFlags')

    pm.separator()

    pm.attrControlGrp('os_render_unit',
                        label='Render Unit',
                        cc=updateRenderSettings,
                        attribute='defaultArnoldRenderOptions.renderUnit')

    enabled = pm.getAttr('defaultArnoldRenderOptions.renderUnit') == 1

    pm.attrControlGrp('os_scene_scale',
                        label='Scene Scale',
                        enable=enabled,
                        attribute='defaultArnoldRenderOptions.sceneScale')

    pm.separator()

    pm.attrControlGrp('os_offset_origin',
                        label='Offset Origin',
                        attribute='defaultArnoldRenderOptions.offsetOrigin')

    pm.rowLayout(numberOfColumns=2, adjustableColumn=1, columnWidth2=(200, 80))

    pm.textField('defaultArnoldRenderOptionsOriginTextField', editable=False)
    pm.button(label='Select Origin', command=selectOrigin)

    setupOriginText()

    pm.setParent('..')

    pm.frameLayout(label='Callbacks', collapse=True)

    pm.attrControlGrp(
            'os_iprRefinementStartedCallback',
            label='IPR Refinement Started',
            attribute='defaultArnoldRenderOptions.IPRRefinementStarted')

    pm.attrControlGrp(
            'os_iprRefinementFinishedCallback',
            label='IPR Refinement Finished',
            attribute='defaultArnoldRenderOptions.IPRRefinementFinished')
    
    pm.attrControlGrp(
            'os_iprStepStartedCallback',
            label='IPR Step Started',
            attribute='defaultArnoldRenderOptions.IPRStepStarted')

    pm.attrControlGrp(
            'os_iprStepFinishedCallback',
            label='IPR Step Finished',
            attribute='defaultArnoldRenderOptions.IPRStepFinished')

    pm.setParent('..')

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)

def updateArnoldFilterOptions(*args):
    pass

def createArnoldSamplingSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)

    pm.text( "textAASamples", 
               font = "smallBoldLabelFont",
               align='left',
               )
    
    pm.text( "textGISamples", 
               font = "smallBoldLabelFont",
               align='left',
               )
    
    pm.text( "textGlossySamples", 
               font = "smallBoldLabelFont",
               align='left',
               )

    pm.text( "textRefractionSamples", 
               font = "smallBoldLabelFont",
               align='left',
               )

    pm.text( "textTotalSamples", 
               font = "smallBoldLabelFont",
               align='left',
               )
                        
    pm.separator()

    pm.intSliderGrp('ss_AA_samples',
                        label="Camera (AA)",
                        minValue = 1,
                        maxValue = 10,
                        fieldMinValue=-10,
                        fieldMaxValue=100,
                        cc=lambda *args: pm.evalDeferred(updateComputeSamples)
                        )

    pm.connectControl('ss_AA_samples', 'defaultArnoldRenderOptions.AASamples', index=1)
    pm.connectControl('ss_AA_samples', 'defaultArnoldRenderOptions.AASamples', index=2)
    pm.connectControl('ss_AA_samples', 'defaultArnoldRenderOptions.AASamples', index=3)

    pm.intSliderGrp('ss_hemi_samples',
                        label="Diffuse",
                        maxValue = 10,
                        fieldMaxValue=100,
                        cc=lambda *args: pm.evalDeferred(updateComputeSamples))
    
    pm.connectControl('ss_hemi_samples', 'defaultArnoldRenderOptions.GIDiffuseSamples', index=1)
    pm.connectControl('ss_hemi_samples', 'defaultArnoldRenderOptions.GIDiffuseSamples', index=2)
    pm.connectControl('ss_hemi_samples', 'defaultArnoldRenderOptions.GIDiffuseSamples', index=3)
    
    pm.intSliderGrp('ss_glossy_samples',
                        label="Glossy",
                        maxValue = 10,
                        fieldMaxValue=100,
                        cc=lambda *args: pm.evalDeferred(updateComputeSamples))
    
    pm.connectControl('ss_glossy_samples', 'defaultArnoldRenderOptions.GIGlossySamples', index=1)
    pm.connectControl('ss_glossy_samples', 'defaultArnoldRenderOptions.GIGlossySamples', index=2)
    pm.connectControl('ss_glossy_samples', 'defaultArnoldRenderOptions.GIGlossySamples', index=3)    
    
    pm.intSliderGrp('ss_refraction_samples',
                        label='Refraction',
                        maxValue = 10,
                        fieldMaxValue=100,
                        cc=lambda *args: pm.evalDeferred(updateComputeSamples))
    
    pm.connectControl('ss_refraction_samples', 'defaultArnoldRenderOptions.GIRefractionSamples', index=1)
    pm.connectControl('ss_refraction_samples', 'defaultArnoldRenderOptions.GIRefractionSamples', index=2)
    pm.connectControl('ss_refraction_samples', 'defaultArnoldRenderOptions.GIRefractionSamples', index=3)    

    pm.attrControlGrp('ss_sss_samples',
                        label='SSS',
                        attribute='defaultArnoldRenderOptions.GI_sss_samples')
    
    pm.attrControlGrp('ss_volume_samples',
                        label='Volume Indirect',
                        attribute='defaultArnoldRenderOptions.GI_volume_samples')

    pm.separator()
    
    pm.attrControlGrp('ss_lock_sampling_noise',
                        label="Lock Sampling Pattern",
                        attribute='defaultArnoldRenderOptions.lock_sampling_noise')

    pm.attrControlGrp('ss_use_autobump',
                        label='Use Autobump in SSS',
                        attribute='defaultArnoldRenderOptions.sssUseAutobump',
                        annotation='WARNING : Enabling this checkbox triples shader evaluations in SSS.')
    
    pm.frameLayout(label='Clamping', collapse=True)

    pm.checkBoxGrp('ss_clamp_sample_values',
                    cc=updateSamplingSettings,
                    label='Clamp Sample Values')

    pm.connectControl('ss_clamp_sample_values', 'defaultArnoldRenderOptions.use_sample_clamp', index=1)
    pm.connectControl('ss_clamp_sample_values', 'defaultArnoldRenderOptions.use_sample_clamp', index=2)

    pm.checkBoxGrp('ss_clamp_sample_values_AOVs',
                    cc=updateSamplingSettings,
                    label='Affect AOVs')

    pm.connectControl('ss_clamp_sample_values_AOVs', 'defaultArnoldRenderOptions.use_sample_clamp_AOVs', index=1)
    pm.connectControl('ss_clamp_sample_values_AOVs', 'defaultArnoldRenderOptions.use_sample_clamp_AOVs', index=2)

    pm.attrControlGrp('ss_max_value',
                        label="Max Value",
                        attribute='defaultArnoldRenderOptions.AASampleClamp')
                        
    pm.setParent('..')
    
    pm.frameLayout(label="Filter", collapse=True)
    
    createTranslatorMenu('defaultArnoldFilter',
                            label='Type',
                            nodeType='aiAOVFilter',
                            default='gaussian')
     
    pm.setParent('..')
    pm.setParent('..') # column layout

    pm.setUITemplate(popTemplate=True)
    updateArnoldFilterOptions()


def createArnoldGammaSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)

    pm.attrControlGrp('ss_driver_gamma',
                        label="Display Driver gamma",
                        attribute='defaultArnoldRenderOptions.display_gamma')

    pm.separator()

    pm.attrControlGrp('ss_light_gamma',
                        label="Lights",
                        attribute='defaultArnoldRenderOptions.light_gamma')

    pm.attrControlGrp('ss_shader_gamma',
                   label="Shaders",
                   attribute='defaultArnoldRenderOptions.shader_gamma')

    pm.attrControlGrp('ss_texture_gamma',
                        label="Textures",
                        attribute='defaultArnoldRenderOptions.texture_gamma')

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)


def createArnoldRayDepthSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)

    pm.attrControlGrp('rs_total_depth',
                        label="Total",
                        attribute='defaultArnoldRenderOptions.GITotalDepth')

    pm.separator(style="none")

    
    pm.intSliderGrp('rs_diffuse_depth',
                        label="Diffuse",
                        maxValue = 16,
                        fieldMaxValue=100,
                        cc=lambda *args: pm.evalDeferred(updateComputeSamples))
    
    pm.connectControl('rs_diffuse_depth', 'defaultArnoldRenderOptions.GIDiffuseDepth', index=1)
    pm.connectControl('rs_diffuse_depth', 'defaultArnoldRenderOptions.GIDiffuseDepth', index=2)
    pm.connectControl('rs_diffuse_depth', 'defaultArnoldRenderOptions.GIDiffuseDepth', index=3)
    
    '''
    pm.attrControlGrp('rs_diffuse_depth',
                        label="Diffuse depth",
                        attribute='defaultArnoldRenderOptions.GIDiffuseDepth')
    '''
    
    pm.intSliderGrp('rs_glossy_depth',
                        label="Glossy",
                        maxValue = 16,
                        fieldMaxValue=100,
                        cc=lambda *args: pm.evalDeferred(updateComputeSamples))
    
    pm.connectControl('rs_glossy_depth', 'defaultArnoldRenderOptions.GIGlossyDepth', index=1)
    pm.connectControl('rs_glossy_depth', 'defaultArnoldRenderOptions.GIGlossyDepth', index=2)
    pm.connectControl('rs_glossy_depth', 'defaultArnoldRenderOptions.GIGlossyDepth', index=3)
    
    '''
    pm.attrControlGrp('rs_glossy_depth',
                        label="Glossy depth",
                        attribute='defaultArnoldRenderOptions.GIGlossyDepth')
    '''

    pm.attrControlGrp('rs_reflection_depth',
                        label="Reflection",
                        attribute='defaultArnoldRenderOptions.GIReflectionDepth')

    pm.intSliderGrp('rs_refraction_depth',
                        label="Refraction ",
                        maxValue = 16,
                        fieldMaxValue=100,
                        cc=lambda *args: pm.evalDeferred(updateComputeSamples))
    
    pm.connectControl('rs_refraction_depth', 'defaultArnoldRenderOptions.GIRefractionDepth', index=1)
    pm.connectControl('rs_refraction_depth', 'defaultArnoldRenderOptions.GIRefractionDepth', index=2)
    pm.connectControl('rs_refraction_depth', 'defaultArnoldRenderOptions.GIRefractionDepth', index=3)

    '''
    pm.attrControlGrp('rs_refraction_depth',
                        label="Refraction depth",
                        attribute='defaultArnoldRenderOptions.GIRefractionDepth')
    '''
    
    pm.attrControlGrp('rs_volume_depth',
                        label="Volume",
                        attribute='defaultArnoldRenderOptions.GIVolumeDepth')
    
    pm.separator(style="none")

    pm.attrControlGrp('rs_auto_transparency_depth',
                        label="Transparency Depth",
                        attribute='defaultArnoldRenderOptions.autoTransparencyDepth')

    pm.attrControlGrp('rs_auto_transparency_threshold',
                        label="Transparency Threshold",
                        attribute='defaultArnoldRenderOptions.autoTransparencyThreshold')

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)

def createArnoldEnvironmentSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)

    pm.rowLayout(adjustableColumn=2, numberOfColumns=4)
    pm.text(label="Background")
    backgroundTextField = pm.textField("defaultArnoldRenderOptionsBackgroundTextField",editable=False)
    backgroundButton = pm.symbolButton(image="navButtonUnconnected.png")
    backgroundSelectButton = pm.symbolButton("defaultArnoldRenderOptionsBackgroundSelectButton", image="navButtonConnected.png", command=selectBackground, enable=False)
    bgpopup = pm.popupMenu(parent=backgroundButton, button=1)
    pm.popupMenu(bgpopup, edit=True, postMenuCommand=Callback(buildBackgroundMenu, bgpopup, backgroundTextField, backgroundSelectButton))

    pm.setParent('..')

    conns = cmds.listConnections('defaultArnoldRenderOptions.background', s=True, d=False)
    if conns:
        pm.textField(backgroundTextField, edit=True, text=conns[0])
        pm.symbolButton(backgroundSelectButton, edit=True, enable=True)

    pm.separator(style="none")

    
    pm.rowLayout(adjustableColumn=2, numberOfColumns=4)
    pm.text(label="Atmosphere")
    atmosphereTextField = pm.textField("defaultArnoldRenderOptionsAtmosphereTextField",editable=False)
    atmosphereButton = pm.symbolButton(image="navButtonUnconnected.png")
    atmosphereSelectButton = pm.symbolButton("defaultArnoldRenderOptionsAtmosphereSelectButton", image="navButtonConnected.png", command=selectAtmosphere, enable=False)
    atpopup = pm.popupMenu(parent=atmosphereButton, button=1)
    pm.popupMenu(atpopup, edit=True, postMenuCommand=Callback(buildAtmosphereMenu, atpopup, atmosphereTextField, atmosphereSelectButton))
    
    pm.setParent('..')

    conns = cmds.listConnections('defaultArnoldRenderOptions.atmosphere', s=True, d=False)
    if conns:
        pm.textField(atmosphereTextField, edit=True, text=conns[0])
        pm.symbolButton(atmosphereSelectButton, edit=True, enable=True)
    
    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)

def arnoldMotionBlurPositionChanged(*args):
    sel = pm.optionMenuGrp('mb_position', q=True, select=True) - 1
    if (sel is 3):
        pm.attrControlGrp('mb_motion_frames', edit=True, enable=False)
        pm.attrControlGrp('mb_motion_range_start', edit=True, enable=True)
        pm.attrControlGrp('mb_motion_range_end', edit=True, enable=True)
        arnoldMotionCustomChanged()
    else:
        pm.attrControlGrp('mb_motion_frames', edit=True, enable=True)
        pm.attrControlGrp('mb_motion_range_start', edit=True, enable=False)
        pm.attrControlGrp('mb_motion_range_end', edit=True, enable=False)
        arnoldMotionFramesChanged()

def arnoldMotionFramesChanged(*args):
    length = pm.getAttr('defaultArnoldRenderOptions.motion_frames')
    angle = length * 360
    pm.text("textArnoldMBAngle",
                edit=True, 
                label=u'  Shutter Angle : %i°' % angle)
    
def arnoldMotionCustomChanged(*args):
    start = pm.getAttr('defaultArnoldRenderOptions.motion_start')
    end = pm.getAttr('defaultArnoldRenderOptions.motion_end')
    angle = abs(end-start) * 360
    pm.text("textArnoldMBAngle",
               edit=True, 
               label=u'  Shutter Angle : %i°' % angle)
    
def createArnoldMotionBlurRange(*args):

    pm.text("textArnoldMBAngle", 
                font = "smallBoldLabelFont",
                align='left',
                enable=False
            )
    
    pm.text( "textArnoldMBAngle",
                edit=True, 
                label=u'  Shutter Angle : %i°' % 180)

               
    cmds.optionMenuGrp('mb_position', label='Position')
    cmds.optionMenuGrp('mb_position', edit=True, changeCommand=pm.Callback(arnoldMotionBlurPositionChanged))
    cmds.menuItem( label='Start On Frame', data=0)
    cmds.menuItem( label='Center On Frame', data=1)
    cmds.menuItem( label='End On Frame', data=2)
    cmds.menuItem( label='Custom', data=3)
    
    cmds.connectControl('mb_position', 'defaultArnoldRenderOptions.range_type', index=1)
    cmds.connectControl('mb_position', 'defaultArnoldRenderOptions.range_type', index=2)

    
    
    pm.attrFieldSliderGrp('mb_motion_frames',
                            label="Length",
                            ann='Motion Range in Frames',
                            attribute='defaultArnoldRenderOptions.motion_frames',
                            cc=arnoldMotionFramesChanged)
                        
    pm.attrFieldSliderGrp('mb_motion_range_start',
                            label="Start",
                            ann='Motion Range Start in Frames',
                            attribute='defaultArnoldRenderOptions.motion_start',
                            cc=arnoldMotionCustomChanged)
                        
    pm.attrFieldSliderGrp('mb_motion_range_end',
                            label="End",
                            ann='Motion Range End in Frames',
                            attribute='defaultArnoldRenderOptions.motion_end',
                            cc=arnoldMotionCustomChanged)
    
def createArnoldMotionBlurSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)

    
                   
    pm.checkBoxGrp('mb_enable',
                    cc=updateMotionBlurSettings,
                    label='Enable')

    pm.connectControl('mb_enable', 'defaultArnoldRenderOptions.motion_blur_enable', index=1)
    pm.connectControl('mb_enable', 'defaultArnoldRenderOptions.motion_blur_enable', index=2)
    
    pm.checkBoxGrp('mb_object_deform_enable',
                    label='Deformation')
                     
    pm.connectControl('mb_object_deform_enable', 'defaultArnoldRenderOptions.mb_object_deform_enable', index=1)
    pm.connectControl('mb_object_deform_enable', 'defaultArnoldRenderOptions.mb_object_deform_enable', index=2)
    
    pm.checkBoxGrp('mb_camera_enable',
                    label='Camera')
                     
    pm.connectControl('mb_camera_enable', 'defaultArnoldRenderOptions.mb_camera_enable', index=1)
    pm.connectControl('mb_camera_enable', 'defaultArnoldRenderOptions.mb_camera_enable', index=2)
    
    pm.attrControlGrp('mb_motion_steps',
                        label="Keys",
                        attribute='defaultArnoldRenderOptions.motion_steps')                   
                        
    pm.separator()
    
    createArnoldMotionBlurRange()

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)

def createArnoldLightSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)

    pm.attrControlGrp('lightThreshold',
                        label="Low Light Threshold",
                        attribute='defaultArnoldRenderOptions.lowLightThreshold')

    pm.separator()

    pm.attrControlGrp('lightLinking',
                        label="Light Linking",
                        attribute='defaultArnoldRenderOptions.lightLinking')

    pm.attrControlGrp('shadowLinking',
                        label="Shadow Linking",
                        attribute='defaultArnoldRenderOptions.shadowLinking')

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)

def createArnoldSubdivSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)

    pm.attrControlGrp('sub_max_subdivisions',
                        label="Max. Subdivisions",
                        attribute='defaultArnoldRenderOptions.maxSubdivisions')

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)


def createArnoldTextureSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)

    pm.attrControlGrp('texture_automip',
                        label="Auto-mipmap",
                        attribute='defaultArnoldRenderOptions.textureAutomip')
                        
    pm.attrControlGrp('texture_accept_unmipped',
                        label="Accept Unmipped",
                        attribute='defaultArnoldRenderOptions.textureAcceptUnmipped')
                        
    cmds.separator()
    
    
    pm.checkBoxGrp('ts_autotile',
                    cc=updateAutotileSettings,
                    label='',
                    label1='Auto-tile')
                     
    pm.connectControl('ts_autotile', 'defaultArnoldRenderOptions.autotile', index=2)
    
    pm.intSliderGrp('ts_texture_autotile',
                        label="Tile Size",
                        minValue = 16,
                        maxValue = 64,
                        fieldMinValue=16,
                        fieldMaxValue=1024
                    )

    pm.connectControl('ts_texture_autotile', 'defaultArnoldRenderOptions.textureAutotile', index=1)
    pm.connectControl('ts_texture_autotile', 'defaultArnoldRenderOptions.textureAutotile', index=2)
    pm.connectControl('ts_texture_autotile', 'defaultArnoldRenderOptions.textureAutotile', index=3)
    
    '''pm.attrControlGrp('texture_autotile',
                        label="Auto-tile Size",
                        attribute='defaultArnoldRenderOptions.textureAutotile')'''

    pm.attrControlGrp('texture_accept_untiled',
                        label="Accept Untiled",
                        attribute='defaultArnoldRenderOptions.textureAcceptUntiled')

    pm.attrControlGrp('use_existing_tiled_textures', 
                        label="Use Existing .tx Textures", 
                        attribute='defaultArnoldRenderOptions.use_existing_tiled_textures')
    
    
    cmds.separator()
    

    pm.attrControlGrp('texture_max_memory_MB',
                        label="Max Cache Size (MB)",
                        attribute='defaultArnoldRenderOptions.textureMaxMemoryMB')

    pm.attrControlGrp('texture_max_open_files',
                        label="Max Open Files",
                        attribute='defaultArnoldRenderOptions.textureMaxOpenFiles')

    cmds.separator() 

    cmds.attrControlGrp('texture_diffuse_blur', 
                        label="Diffuse Blur", 
                        attribute='defaultArnoldRenderOptions.textureDiffuseBlur') 

    cmds.attrControlGrp('texture_glossy_blur', 
                        label="Glossy Blur", 
                        attribute='defaultArnoldRenderOptions.textureGlossyBlur') 

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)

def createArnoldOverrideSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)

    pm.attrControlGrp('ignore_textures',
                        attribute='defaultArnoldRenderOptions.ignore_textures')

    pm.attrControlGrp('ignore_shaders',
                        attribute='defaultArnoldRenderOptions.ignore_shaders')

    pm.attrControlGrp('ignore_atmosphere',
                        attribute='defaultArnoldRenderOptions.ignore_atmosphere')

    pm.attrControlGrp('ignore_lights',
                        attribute='defaultArnoldRenderOptions.ignore_lights')

    pm.attrControlGrp('ignore_shadows',
                        attribute='defaultArnoldRenderOptions.ignore_shadows')
                        
    pm.attrControlGrp('ignore_subdivision',
                        attribute='defaultArnoldRenderOptions.ignore_subdivision')

    pm.attrControlGrp('ignore_displacement',
                        attribute='defaultArnoldRenderOptions.ignore_displacement')

    pm.attrControlGrp('ignore_bump',
                        attribute='defaultArnoldRenderOptions.ignore_bump')

    pm.attrControlGrp('ignore_smoothing',
                        attribute='defaultArnoldRenderOptions.ignore_smoothing', label='Ignore Normal Smoothing')
                        
    pm.attrControlGrp('ignore_motion_blur',
                        attribute='defaultArnoldRenderOptions.ignore_motion_blur')

    pm.attrControlGrp('ignore_dof',
                        attribute='defaultArnoldRenderOptions.ignore_dof', label='Ignore Depth of Field')
                        
    pm.attrControlGrp('ignore_sss',
                        attribute='defaultArnoldRenderOptions.ignore_sss', label='Ignore Sub-Surface Scattering')

    pm.attrControlGrp('force_translate_shading_engines',
                       attribute='defaultArnoldRenderOptions.forceTranslateShadingEngines', label='Force Translation of Shading Engines')

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)

def createArnoldPathSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)
    
    pm.attrControlGrp('texture_absolute_paths',
                        label='Absolute Texture Paths',
                        attribute='defaultArnoldRenderOptions.absoluteTexturePaths')

    pm.attrControlGrp('os_absoluteProceduralPaths',
                        label='Absolute Procedural Paths',
                        attribute='defaultArnoldRenderOptions.absoluteProceduralPaths')

    pm.separator()


    pm.attrControlGrp('os_procedural_searchpath',
                        label="Procedural Search Path",
                        attribute='defaultArnoldRenderOptions.procedural_searchpath')

    pm.attrControlGrp('os_shader_searchpath',
                        label="Shader Search Path",
                        attribute='defaultArnoldRenderOptions.shader_searchpath')

    pm.attrControlGrp('os_texture_searchpath',
                        label="Texture Search Path",
                        attribute='defaultArnoldRenderOptions.texture_searchpath')

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)

def createArnoldMayaintegrationSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)
    
    pm.attrControlGrp('os_progressive_rendering',
                        label='Progressive Refinement',
                        attribute='defaultArnoldRenderOptions.progressive_rendering')

    pm.attrControlGrp('os_progressive_initial_level',
                        label="Initial Sampling Level",
                        attribute='defaultArnoldRenderOptions.progressive_initial_level')
                    
    pm.separator()
                    
    pm.attrControlGrp('os_clear_before_render',
                        label="Clear Before Render",
                        attribute='defaultArnoldRenderOptions.clear_before_render')
                   
    pm.attrControlGrp('os_force_scene_update_before_IPR_refresh',
                        label='Force Scene Update On IPR Refresh',
                        attribute='defaultArnoldRenderOptions.force_scene_update_before_IPR_refresh')
    
    pm.attrControlGrp('os_force_texture_cache_flush_after_render',
                        label='Force Texture Cache Flush After Render',
                        attribute='defaultArnoldRenderOptions.force_texture_cache_flush_after_render')
                   
    pm.separator()
                  
    pm.attrControlGrp('os_enable_swatch_render',
                        label="Enable Swatch Render",
                        attribute='defaultArnoldRenderOptions.enable_swatch_render')

    pm.attrControlGrp('os_standin_draw_override',
                        label="StandIn Viewport Override",
                        attribute='defaultArnoldRenderOptions.standin_draw_override')

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)
    
def createArnoldLicensingSettings():
    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)
    
    pm.attrControlGrp('os_abort_on_license_fail',
                        label="Abort On License Fail",
                        attribute='defaultArnoldRenderOptions.abortOnLicenseFail')

    pm.attrControlGrp('os_skip_license_check',
                        label="Skip License Check",
                        attribute='defaultArnoldRenderOptions.skip_license_check')

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)

def LoadFilenameButtonPush(*args):
    import os
    basicFilter = 'All Files (*.*)'
    initFolder = cmds.textFieldGrp("ls_log_filename", query=True, text=True)
    if "$MTOA_LOG_PATH" in initFolder:
        logPath = pm.mel.eval('getenv "MTOA_LOG_PATH"')
        if not logPath:
            logPath = pm.workspace(query=True, rootDirectory=True)
        resolvedFolder = initFolder.replace("$MTOA_LOG_PATH",logPath)
    else:
        resolvedFolder = initFolder
    resolvedFolder = os.path.split(resolvedFolder)
    ret = cmds.fileDialog2(fileFilter=basicFilter, cap='Select Log File',okc='Select',fm=0,startingDirectory=resolvedFolder[0])
    if ret is not None and len(ret):
        cmds.textFieldGrp("ls_log_filename", edit=True, text=ret[0])
        cmds.setAttr("defaultArnoldRenderOptions.log_filename", ret[0], type="string")

def ChangeLogToConsole(*args):
    logToConsole = cmds.getAttr('defaultArnoldRenderOptions.log_to_console')
    logToFile = cmds.getAttr('defaultArnoldRenderOptions.log_to_file')
    pm.attrControlGrp('log_max_warnings', edit=True, enable=logToConsole or logToFile)

def ChangeLogToFile(*args):
    logToFile = cmds.getAttr('defaultArnoldRenderOptions.log_to_file')
    logToConsole = cmds.getAttr('defaultArnoldRenderOptions.log_to_console')
    cmds.textFieldGrp('ls_log_filename', edit=True, enable=logToFile)
    cmds.symbolButton("ls_log_filename_button", edit=True, enable=logToFile)
    pm.attrControlGrp('log_max_warnings', edit=True, enable=logToConsole or logToFile)

def createArnoldLogSettings():

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)

    logToFile = cmds.getAttr('defaultArnoldRenderOptions.log_to_file')
    logToConsole = cmds.getAttr('defaultArnoldRenderOptions.log_to_console')

    
    pm.attrControlGrp('log_verbosity',
                        label="Verbosity Level",
                        enable=logToConsole,
                        attribute='defaultArnoldRenderOptions.log_verbosity')                
                        
    
    pm.checkBoxGrp('log_to_console',
                    label='Console',
                    changeCommand=ChangeLogToConsole)

    pm.connectControl('log_to_console', 'defaultArnoldRenderOptions.log_to_console', index=1)
    pm.connectControl('log_to_console', 'defaultArnoldRenderOptions.log_to_console', index=2)
    
    pm.checkBoxGrp('log_to_file',
                    label='File',
                    changeCommand=ChangeLogToFile)

    pm.connectControl('log_to_file', 'defaultArnoldRenderOptions.log_to_file', index=1)
    pm.connectControl('log_to_file', 'defaultArnoldRenderOptions.log_to_file', index=2)
    
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(80,220), adjustableColumn=2, columnAttach=[(1, 'left', 0), (2, 'left', -10)])
    path = cmds.textFieldGrp('ls_log_filename',
                                label='Filename',
                                enable=logToFile,
                                cc=updateLogSettings,
                                width=325)
    cmds.symbolButton('ls_log_filename_button', image='navButtonBrowse.png', command=LoadFilenameButtonPush, enable=logToFile)
    pm.connectControl('ls_log_filename', 'defaultArnoldRenderOptions.log_filename', index=1)
    pm.connectControl('ls_log_filename', 'defaultArnoldRenderOptions.log_filename', index=2)
    pm.setParent('..')
    
    '''
    pm.attrControlGrp('log_filename',
                        label="Filename",
                        attribute='defaultArnoldRenderOptions.log_filename',
                        cc=updateLogSettings)
    '''

    pm.attrControlGrp('log_max_warnings',
                        label='Max. Warnings',
                        enable=logToConsole or logToFile,
                        attribute='defaultArnoldRenderOptions.log_max_warnings')

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)
    
def createArnoldErrorHandlingSettings():
    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)

    pm.attrControlGrp('os_abort_on_error',
                        label="Abort On Error",
                        attribute='defaultArnoldRenderOptions.abortOnError')
                   
    pm.separator()
    
    pm.attrControlGrp('os_error_color_bad_texture',
                        label="Texture Error Color",
                        attribute='defaultArnoldRenderOptions.errorColorBadTexture')
                   
    pm.attrControlGrp('os_error_color_bad_pixel',
                        label="NaN Error Color",
                        attribute='defaultArnoldRenderOptions.errorColorBadPixel')

    pm.setParent('..')

    pm.setUITemplate(popTemplate=True)

def createArnoldUserOptionsSettings():
    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.columnLayout(adjustableColumn=True)
    
    pm.attrControlGrp('os_user_options',
                        label="Options",
                        attribute='defaultArnoldRenderOptions.aiUserOptions')
    pm.setParent('..')
    
    pm.setUITemplate(popTemplate=True)

    
def createArnoldRendererOverrideTab():

    # Make sure the aiOptions node exists
    #core.createOptions()

    parentForm = pm.setParent(query=True)
    
    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.scrollLayout('arnoldOverrideScrollLayout', horizontalScrollBarThickness=0)
    pm.columnLayout('arnoldOverrideColumn', adjustableColumn=True)

    

    
    # User Options
    #
    pm.frameLayout('arnoldUserOptionsSettings', label="User Options", cll=True,  cl=0)
    createArnoldUserOptionsSettings()
    pm.setParent('..')
    
    # Overrides
    #
    pm.frameLayout('arnoldOverrideSettings', label="Feature Overrides", cll=True,  cl=0)
    createArnoldOverrideSettings()
    pm.setParent('..')
    
    # Subdivision Surfaces
    #
    pm.frameLayout('arnoldSubdivSettings', label="Subdivision", cll= True, cl=0)
    createArnoldSubdivSettings()
    pm.setParent('..')
    

    pm.formLayout(parentForm,
                    edit=True,
                    af=[('arnoldOverrideScrollLayout', "top", 0),
                        ('arnoldOverrideScrollLayout', "bottom", 0),
                        ('arnoldOverrideScrollLayout', "left", 0),
                        ('arnoldOverrideScrollLayout', "right", 0)])

    pm.setParent(parentForm)
    
def updateArnoldRendererOverrideTab(*args):
    pass

    
def createArnoldRendererDiagnosticsTab():

    # Make sure the aiOptions node exists
    #core.createOptions()

    parentForm = pm.setParent(query=True)
    
    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.scrollLayout('arnoldDiagnosticsScrollLayout', horizontalScrollBarThickness=0)
    pm.columnLayout('arnoldDiagnosticsColumn', adjustableColumn=True)

    # Log
    #
    pm.frameLayout('arnoldLogSettings', label="Log", cll=True, cl=0)
    createArnoldLogSettings()
    pm.setParent('..')
    
    # Error handling
    #
    pm.frameLayout('arnoldErrorHandlingSettings', label="Error Handling", cll=True, cl=0)
    createArnoldErrorHandlingSettings()
    pm.setParent('..')

    pm.formLayout(parentForm,
                    edit=True,
                    af=[('arnoldDiagnosticsScrollLayout', "top", 0),
                        ('arnoldDiagnosticsScrollLayout', "bottom", 0),
                        ('arnoldDiagnosticsScrollLayout', "left", 0),
                        ('arnoldDiagnosticsScrollLayout', "right", 0)])

    pm.setParent(parentForm)
    
def updateArnoldRendererDiagnosticsTab(*args):
    updateLogSettings()
    
def createArnoldRendererSystemTab():

    # Make sure the aiOptions node exists
    #core.createOptions()

    parentForm = pm.setParent(query=True)
    
    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.scrollLayout('arnoldSystemScrollLayout', horizontalScrollBarThickness=0)
    pm.columnLayout('arnoldSystemColumn', adjustableColumn=True)

    
    # Maya Integration
    #
    pm.frameLayout('arnoldMayaIntegrationSettings', label="Maya Integration", cll=True, cl=0)
    createArnoldMayaintegrationSettings()
    pm.setParent('..')
    
    # Render
    #
    pm.frameLayout('arnoldRenderSettings', label="Render Settings", cll= True, cl=0)
    createArnoldRenderSettings()
    pm.setParent('..')
    
    # Search paths
    #
    pm.frameLayout('arnoldPathSettings', label="Search Paths", cll=True, cl=0)
    createArnoldPathSettings()
    pm.setParent('..')
    
    # Licensing
    #
    pm.frameLayout('arnoldLicensingSettings', label="Licensing", cll=True, cl=0)
    createArnoldLicensingSettings()
    pm.setParent('..')
    
    

    pm.formLayout(parentForm,
                    edit=True,
                    af=[('arnoldSystemScrollLayout', "top", 0),
                        ('arnoldSystemScrollLayout', "bottom", 0),
                        ('arnoldSystemScrollLayout', "left", 0),
                        ('arnoldSystemScrollLayout', "right", 0)])

    pm.setParent(parentForm)
    
    updateRenderSettings()
    
def updateArnoldRendererSystemTab(*args):
    updateRenderSettings()

def createArnoldRendererGlobalsTab():

    # Make sure the aiOptions node exists
    core.createOptions()

    parentForm = pm.setParent(query=True)

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    pm.scrollLayout('arnoldGlobalsScrollLayout', horizontalScrollBarThickness=0)
    pm.columnLayout('arnoldTabColumn', adjustableColumn=True)

    # Sampling
    #
    pm.frameLayout('arnoldSamplingSettings', label='Sampling', cll=True, cl=0)
    createArnoldSamplingSettings()
    pm.setParent('..')

    # Ray depth
    #
    pm.frameLayout('arnoldRayDepthSettings', label="Ray Depth", cll= True, cl=1)
    createArnoldRayDepthSettings()
    pm.setParent('..')

    # Environment
    #
    pm.frameLayout('arnoldEnvironmentSettings', label="Environment", cll= True, cl=1)
    createArnoldEnvironmentSettings()
    pm.setParent('..')

    # Motion Blur
    #
    pm.frameLayout('arnoldMotionBlurSettings', label="Motion Blur", cll= True, cl=1)
    createArnoldMotionBlurSettings()
    pm.setParent('..')


    # Light Linking
    #
    pm.frameLayout('arnoldLightSettings', label="Lights", cll= True, cl=1)
    createArnoldLightSettings()
    pm.setParent('..')


    # Gamma correction
    #
    pm.frameLayout('arnoldGammaSettings', label="Gamma Correction", cll=True, cl=1)
    createArnoldGammaSettings()
    pm.setParent('..')

    # Gamma correction
    #
    pm.frameLayout('arnoldTextureSettings', label="Textures", cll=True, cl=1)
    createArnoldTextureSettings()
    pm.setParent('..')


    pm.setParent('..')

    pm.formLayout(parentForm,
                    edit=True,
                    af=[('arnoldGlobalsScrollLayout', "top", 0),
                        ('arnoldGlobalsScrollLayout', "bottom", 0),
                        ('arnoldGlobalsScrollLayout', "left", 0),
                        ('arnoldGlobalsScrollLayout', "right", 0)])

    pm.setParent(parentForm)

    updateArnoldRendererGlobalsTab()

def updateBackgroundSettings(*args):
    background = getBackgroundShader()
    if pm.textField( 'defaultArnoldRenderOptionsBackgroundTextField', query=True, exists=True):
        pm.textField('defaultArnoldRenderOptionsBackgroundTextField', edit=True, text=background)
    if pm.symbolButton( 'defaultArnoldRenderOptionsBackgroundSelectButton', query=True, exists=True):
        if not background:
            pm.symbolButton('defaultArnoldRenderOptionsBackgroundSelectButton', edit=True, enable=False)
        else:
            pm.symbolButton('defaultArnoldRenderOptionsBackgroundSelectButton', edit=True, enable=True)
            
def updateAtmosphereSettings(*args):
    atmosphere = getAtmosphereShader()
    if pm.textField( 'defaultArnoldRenderOptionsAtmosphereTextField', query=True, exists=True):
        pm.textField('defaultArnoldRenderOptionsAtmosphereTextField', edit=True, text=atmosphere)
    if pm.symbolButton( 'defaultArnoldRenderOptionsAtmosphereSelectButton', query=True, exists=True):
        if not atmosphere:
            pm.symbolButton('defaultArnoldRenderOptionsAtmosphereSelectButton', edit=True, enable=False)
        else:
            pm.symbolButton('defaultArnoldRenderOptionsAtmosphereSelectButton', edit=True, enable=True)

def updateArnoldRendererGlobalsTab(*args):
    updateComputeSamples()
    updateSamplingSettings()
    updateMotionBlurSettings()
    updateAutotileSettings()
    
