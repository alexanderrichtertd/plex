import pymel.core as pm
#from mtoa.callbacks import *
import mtoa.aovs as aovs
import mtoa.utils as utils
#import mtoa.ui.ae.shaderTemplate as shaderTemplate
#import mtoa.ui.ae.templates as templates
import mtoa.core as core
#import mtoa.callbacks as callbacks
import mtoa.hooks as hooks

#from collections import defaultdict
import sys, os

#import maya.OpenMaya as om

import maya.cmds as m
from maya.mel import eval as mel

if os.environ.get('PL_DIVISION_PATH') and os.path.exists(os.path.join(os.environ.get('PL_DIVISION_PATH'),'common/maya/python/sfRenderDictatorOverride')):
    try: import sfRenderDictatorOverride.presets as rdp
    except: print 'No presets found for this division - using defaults'
else:
    import sfRenderDictator.presets as rdp
reload(rdp)

print rdp.__file__

import sfTools.utils as sfu
import sfMayaTools.utils as sfmu
reload(sfu)
reload(sfmu)

import math

if not m.pluginInfo('mtoa.so', query=True, loaded=True ): m.loadPlugin('mtoa.so')
if not m.objExists("defaultArnoldRenderOptions"): m.createNode('aiOptions', n="defaultArnoldRenderOptions")
aovCtrl = aovs.AOVInterface()

renderOutputs = ['rgba', 'add','util','id']

def setArnoldPrefs(): # title="Set Arnold Preferences" # img="icons/aiTools_arnie01.png"
    '''
    Sets up general Arnold defaults that are basically universal
    and should not vary from job to job

    # set file naming to 'name.#.ext'
    # set procedural_searchpath to "[ARNOLD_PLUGIN_PATH]"
    # bucket scanning top down
    # disables swatches to keep maya usable
    # set display gamma to 1
    # set light gamma to 1
    # set shader gamma to 1
    # set texture gamma to 1
    # set verbosity to show FQ progress

    # 16bit half for beauty aovs
    # name exr channel by pass
    # makes half written files readable
    # multichannel exrs

    # set renderview input to linear
    # set renderview display to rec709
    '''
    mel('setMayaSoftwareFrameExt(3,0)') # set file naming to 'name.#.ext'
    m.setAttr("defaultArnoldRenderOptions.procedural_searchpath", "[ARNOLD_PLUGIN_PATH]", type="string") # set procedural_searchpath to "[ARNOLD_PLUGIN_PATH]"
    m.setAttr("defaultArnoldRenderOptions.bucketScanning", 0) # bucket scanning top down
    m.setAttr("defaultArnoldRenderOptions.enable_swatch_render", 0) # disables swatches to keep maya usable
    m.setAttr("defaultArnoldRenderOptions.display_gamma", 1.0) # set display gamma to 1
    m.setAttr("defaultArnoldRenderOptions.light_gamma", 1.0) # set light gamma to 1
    m.setAttr("defaultArnoldRenderOptions.shader_gamma", 1.0) # set shader gamma to 1
    m.setAttr("defaultArnoldRenderOptions.texture_gamma", 1.0) # set texture gamma to 1
    m.setAttr("defaultArnoldRenderOptions.log_verbosity", 1) # set verbosity to show FQ progress

    m.setAttr("defaultArnoldDriver.halfPrecision", 1) # 16bit half for beauty aovs
    m.setAttr("defaultArnoldDriver.preserveLayerName", 1) # name exr channel by pass
    m.setAttr("defaultArnoldDriver.tiled", 1) # makes half written files readable
    m.setAttr("defaultArnoldDriver.mergeAOVs", 1) # multichannel exrs

    m.setAttr("defaultViewColorManager.imageColorProfile", 4) # and set renderview input to linear
    m.setAttr("defaultViewColorManager.displayColorProfile", 5) # and set renderview display to rec709

#######################
# Quick Render Settings
#######################

def quickDirtySettings(): # title="AA=1    MB=OFF" # img="icons/aiTools_render0.png"
    commonRenderSettings()
    m.setAttr("defaultArnoldRenderOptions.AASamples", 1)
    m.setAttr("defaultArnoldRenderOptions.motion_blur_enable", 0)
    # m.setAttr("defaultArnoldRenderOptions.GIDiffuseDepth", 0)
    # m.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 1)
    # m.setAttr("defaultArnoldRenderOptions.GIGlossySamples", 1)
    # m.setAttr("defaultArnoldRenderOptions.GIRefractionSamples", 1)

def previewRenderSettings(): # title="AA=3    MB=OFF" # img="/job/commsldn/AUDI_POWERWALK_2000661/common/maya/icons/aiTools_render1.png"
    commonRenderSettings()
    m.setAttr("defaultArnoldRenderOptions.AASamples", 3)
    m.setAttr("defaultArnoldRenderOptions.motion_blur_enable", 0)
    # m.setAttr("defaultArnoldRenderOptions.GIDiffuseDepth", 1)
    # m.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 1)
    # m.setAttr("defaultArnoldRenderOptions.GIGlossySamples", 1)
    # m.setAttr("defaultArnoldRenderOptions.GIRefractionSamples", 1)

def dailyFarmRenderSettings(): # title="AA=6    MB=ON" # img="/job/commsldn/AUDI_POWERWALK_2000661/common/maya/icons/aiTools_render2.png"
    commonRenderSettings()
    m.setAttr("defaultArnoldRenderOptions.AASamples", 6)
    m.setAttr("defaultArnoldRenderOptions.motion_blur_enable", 1)
    # m.setAttr("defaultArnoldRenderOptions.GIDiffuseDepth", 1)
    # m.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 1)
    # m.setAttr("defaultArnoldRenderOptions.GIGlossySamples", 2)
    # m.setAttr("defaultArnoldRenderOptions.GIRefractionSamples", 2)

def finalProductionRenderSettings(): # title="AA=10    MB=ON" # img="/job/commsldn/AUDI_POWERWALK_2000661/common/maya/icons/aiTools_render3.png"
    commonRenderSettings()
    m.setAttr("defaultArnoldRenderOptions.AASamples", 10)
    m.setAttr("defaultArnoldRenderOptions.motion_blur_enable", 1)
    # m.setAttr("defaultArnoldRenderOptions.GIDiffuseDepth", 1)
    # m.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 1)
    # m.setAttr("defaultArnoldRenderOptions.GIGlossySamples", 2)
    # m.setAttr("defaultArnoldRenderOptions.GIRefractionSamples", 2)

def commonRenderSettings(): # en=0
    # m.setAttr("defaultArnoldRenderOptions.lock_sampling_noise", 0)
    # m.setAttr("defaultArnoldRenderOptions.shutter_type", 1)
    # m.setAttr("defaultArnoldRenderOptions.motion_steps", 3)
    # m.setAttr("defaultArnoldRenderOptions.use_sample_clamp", 1)
    # m.setAttr("defaultArnoldRenderOptions.use_sample_clamp_AOVs", 1)
    # m.setAttr("defaultArnoldRenderOptions.AASampleClamp", 4)
    m.setAttr("defaultArnoldRenderOptions.kickRenderFlags", "-g 2.2", type="string")


###################
# AOVs
###################

def addAOV(name="", type="rgb"): # title="Add AOV" # img="aiTools_addAOV.png"
    '''
    Adds a new AOV to the scene

    This is the same as Add Custom in the AOV tab in the
    render globals but allows you to specify data type
    '''
    
    if not m.objExists('aiAOV_'+name):
        try:
            aovCtrl.addAOV(name, type)
        except:pass

def add_shader_custom_AOVs(idsOnly=True):# title="Add Custom Shader AOVs" # img="aiTools_customAOVs.png"
    '''
    Searches all shaders for custom aovs plugs and Creates missing AOVs

    THis is necessary when shaders that expect certain custom aovs are
    imported into a scene in which these aovs do not exist. The shading
    groups retain a "memory" of the aovs in the form of dormant plugs.

    idsOnly - only create aovs starting with "id_"
    '''
    
    SGs = m.ls(typ="shadingEngine", r=1)
    aovs = []
    aovsAdded = []
    for SG in SGs:
        # print SG
        customAOVs = m.listAttr("%s.aiCustomAOVs"%SG, m=1)
        if customAOVs:
            for item in [i for i in customAOVs if "aovName" in i]:
                aovName = m.getAttr("%s.%s"%(SG,item))
                if not aovName in aovs: aovs.append(aovName)

    aovs = list(set(aovs))
    print "AOVS found", aovs
    existing_aovs = [m.getAttr("%s.name"%i) for i in m.ls(typ="aiAOV")]
    print "existing AOVS", existing_aovs
    for aov in aovs:
        if not aov in existing_aovs:
            if idsOnly and not aov.startswith("id_"): continue
            print aov
            aovsAdded.append(aov)
            addAOV(aov, "rgb")

    update_aov_outputs()
    m.inViewMessage(amg='Connected missing AOVs:\n\n%s'%'\n'.join(aovsAdded), pos='midCenter', dk=True)


def set_id_colour(colour=["R","G","B"][0], destAovName="id_[whatever]"): # title="Set ID Colour" # img="aiTools_ids.png"
    '''
    connects red green or blue ramp into chosen id of all selected shading group nodes
    '''
    sel = m.ls(sl=1)

    ramps = {"red" : [1,0,0],"green" : [0,1,0] ,"blue" : [0,0,1]}
    for ramp in ramps:
        if not m.objExists(ramp):
            rampNode = m.shadingNode("ramp", asTexture=1, n=ramp)
            m.removeMultiInstance("%s.colorEntryList[1]" % rampNode, b=1)
            m.setAttr("%s.colorEntryList[0].color" % rampNode, ramps[ramp][0], ramps[ramp][1], ramps[ramp][2], type="double3")

    srcNodes = {"R":"red.outColor", "G":"green.outColor","B":"blue.outColor"}
    #TODO auto create ramp nodes
    src = srcNodes[colour]

    addAOV(name=destAovName)

    for SG in sel:
        if not m.nodeType(SG) == "shadingEngine": continue
        #print SG
        customAOVs = m.listAttr("%s.aiCustomAOVs"%SG, m=1)
        if customAOVs:
            for item in [i for i in customAOVs if "aovName" in i]:
                aovName = m.getAttr("%s.%s"%(SG,item))
                if aovName == destAovName:
                    #print item
                    dst = "%s.%s"%(SG,item.replace("aovName","aovInput"))
                    print src, dst
                    try: m.connectAttr(src, dst, f=1)
                    except:pass


###################
# Geometry
###################

def selectNotOpaque():
    '''
    Selects all geo with aiOpaque flag turned off
    '''
    m.select([i for i in m.ls(typ="transform") if m.objExists("%s.aiOpaque"%i) and m.getAttr("%s.aiOpaque"%i) == False], r=1)

def loadAiStandIn(name="", path=""): # title="Load aiStandin"  # img="aiTools_standIn.png"
    '''
    Loads selected ass file and creates [name]_STD
    '''
    if not m.pluginInfo('mtoa.so', query=True, loaded=True ): m.loadPlugin('mtoa.so')
    standInShape = m.createNode('aiStandIn', n='%s_STDShape'%name, ss=1)
    print standInShape
    standInTransform = m.listRelatives(standInShape, p=1)[0]

    # m.expression(s="%s.frameNumber=frame"%standInShape)
    # m.setAttr("%s.useFrameExtension"%standInShape, 0)
    # m.setAttr("%s.frameOffset"%standInShape, self.offset * -1)
    m.setAttr("%s.deferStandinLoad"%standInShape, 1)
    m.setAttr("%s.overrideLightLinking"%standInShape, 0)
    m.setAttr("%s.overrideShaders"%standInShape, 0)
    m.setAttr('%s.dso'%standInShape, path, type='string')
    sfmu.addToSet(standInTransform, "aiStandIn_SEL")
    return standInTransform

def setup_aiSubdiv_set():
    aiSubdiv_SEL = "aiSubdiv_override_SEL"
    gesNodes = m.ls("*GES", r=1)
    if not m.objExists(aiSubdiv_SEL):
        m.sets(name=aiSubdiv_SEL)
        m.addAttr(aiSubdiv_SEL, ln="aiSubdivType", at="enum", en="none:catclark:linear", k=1, dv=1)
        m.addAttr(aiSubdiv_SEL, ln="aiSubdivIterations", at="long", min=0, max=10, dv=2, k=1)
        m.addAttr(aiSubdiv_SEL, ln="aiSubdivAdaptiveMetric", at="enum", en="auto:edge_length:flatness", k=1)
        m.addAttr(aiSubdiv_SEL, ln="aiSubdivPixelError", at="double", min=0, max=10, dv=1, k=1)
        m.addAttr(aiSubdiv_SEL, ln="aiSubdivUvSmoothing", at="enum", en="pin_corners:pin_borders:linear:smooth", k=1)
        m.addAttr(aiSubdiv_SEL, ln="aiSubdivUvSmoothDerivs", at="bool", k=1)
    sfmu.addToSet(gesNodes, aiSubdiv_SEL)


###################
# Shaders
###################

def getIorFromIncidenceReflectance(r=0.0, v=False):
    n = (1 + math.sqrt(r)) / (1 - math.sqrt(r))
    if v: print n
    return n

def getIncidenceReflectanceFromIor(ior=0.0, v=False):
    r = pow((ior-1),2) / pow((ior+1),2)
    if v: print r
    return v

###################
# AOVs - Legacy
###################


def update_aov_outputs(): # title="Update AOV Outputs" # img="icons/aiTools_AOVs.png"
    ''' Creates AOV output drivers for multi file exr outputs and connects relevant AOV nodes
        
        e.g. produces an RGBA beauty file, plus three addition AOV files (ADD, UTIL, ID)
        Please run this script everytime you add any AOVs to your scene. You must remember to set the aovType attribute on the AOV node to ensure it is plugged into the correct output
    '''

    if m.ls(type="aiAOV") == []: return
    add_aov_attrs()
    create_aov_drivers()
    create_aov_sets()

    for aov in m.ls(type='aiAOV'): # For all AOVs
        if m.objExists("%s.aovtype"%aov): # if the aovtype attribute exists
            aovtype = m.getAttr("%s.aovtype"%aov, asString=True) # get it's value
            # print aov, aovtype
            sfmu.tryConnect("aiAOVDriver_%s.message"%aovtype, "%s.outputs[0].driver"%aov) # attach it to the relevant AOV output driver

def setupAOVs(): # title="Setup AOVs"
    
    ##create render passes
    for renderPass in rdp.renderPasses:
        layerName = rdp.renderPasses[renderPass][1]
        passPrefix = rdp.renderPasses[renderPass][2]
        passName = passPrefix + '_'+ renderPass
        passType = rdp.renderPasses[renderPass][0]
        if not m.objExists('aiAOV_'+passName):
            try:
                aovCtrl.addAOV(passName, 'rgb')
            except:pass
        
        print passName.ljust(32), 'added to the', layerName.ljust(10), 'layer', '\ttype:', passType

#    sfmu.setImageFormat('exr')
#    m.setAttr("defaultRenderGlobals.multiCamNamingMode", 1)
#    mel('setTokenKeywordMenuCallback "<RenderPass>";')

def importAOVs(location=['show','division'][1]): # title="Import AOVs"
    if location == 'show': aovsFile = "/job/commsldn/ASSET_LIBRARY/asset/generic/aovs/aovs_v001.mb"
    if location == 'division': aovsFile = "/job/commsldn/%s/asset/generic/aovs/aovs_v001.mb" %os.getenv('PL_DIVISION')
    newNodes = m.file(aovsFile, i=1, rnn=1)
    newAOVs = [n for n in newNodes if m.nodeType(n) == 'aiAOV']
    m.inViewMessage(amg='Imported AOVs:\n\n%s\n\nPress <hl>Connect AOVs</hl> to enable'%'\n'.join(newAOVs), pos='midCenter', dk=True)

def connectAOVs():# title="Connect AOVs"
    for item in m.ls(typ='aiAOV'):
        try:m.connectAttr(item+'.msg', 'defaultArnoldRenderOptions.aovList', na=1)
        except: print "%s is already connected" %item

def setAOVs(enable=True):# title="Set AOVs"
    for item in m.ls(sl=1):
        if not m.nodeType(item) == 'aiAOV': continue
        try:    m.editRenderLayerAdjustment(item+'.enabled')
        except: print 'setting on master layer'
        m.setAttr(item+'.enabled', enable)

def conformShaderAOVs(shaders=None, revert=False):# title="Conform Shader AOVs"
    if not shaders or shaders == '': shaders = m.ls(sl=1)
    for shader in shaders:
        for renderPass in rdp.renderPasses:
            layerName = rdp.renderPasses[renderPass][1]
            passPrefix = rdp.renderPasses[renderPass][2]
            passName = passPrefix + '_'+ renderPass
            passType = rdp.renderPasses[renderPass][0]
            print passName
            if m.objExists('aiAOV_'+passName) or True:
                defaultName = sfu.camel(passType, startLower=False)
                try:
                    if revert:
                        m.setAttr(shader+'.aov' + defaultName, passType, type= 'string')
                    else:
                        m.setAttr(shader+'.aov' + defaultName, passName, type= 'string')
                        print 'setting', shader, defaultName, 'to', passName
#                    aovCtrl.addAOV(passName, 'rgb')
                except:pass


def toggle_b_naming_convention(): # title="Toggle 'b_' naming convention"
    ''' Switches between default shader outputs and use of b_ to define beauty passes
        Just for testing alternate conforming ideas - not required for multifile approach
    '''
    beautyaovnames = []
    for aov in m.ls(type='aiAOV'):
        if m.objExists("%s.aovtype"%aov):
            aovtype = m.getAttr("%s.aovtype"%aov, asString=True)
            name = m.getAttr("%s.name"%aov, asString=True)
            if aovtype == 'beauty':
                if name.startswith('b_'):
                    m.setAttr("%s.name"%aov, name.lstrip('b_'), type='string') #change the name
                    m.rename(aov, aov.replace('aiAOV_b_', 'aiAOV_')) #rename the node
                    beautyaovnames.append(name.lstrip('b_')) #add this to the list to change on all shaders
                else:
                    m.setAttr("%s.name"%aov, "b_%s"%name, type='string')
                    m.rename(aov, aov.replace('aiAOV_', 'aiAOV_b_'))
                    beautyaovnames.append("b_%s"%name)

    for shader in m.ls(type=m.listNodeTypes('shader')):
        for beautyaovname in beautyaovnames:
            defaultName = sfu.camel(beautyaovname.lstrip('b_'), startLower=False) # find arnold builtin name
            if m.objExists(shader+'.aov' + defaultName):
                m.setAttr(shader+'.aov' + defaultName, beautyaovname, type= 'string') # set to new name



def add_aov_attrs(rm=False):
    '''Add aovtype attribute to all aiAOV nodes
    '''
    aovs = m.ls(type="aiAOV")
    if rm:
        for aov in aovs:
            m.deleteAttr("%s.aovtype"%aov)
    else:
        sfmu.addAttr('aovtype', renderOutputs[1:4], aovs)# adds enum attributes

    for aov in aovs:
        if m.getAttr("%s.name"%aov).startswith('id_'):
            m.setAttr("%s.aovtype"%aov, 2) # set aovType to 'ID'
        if m.getAttr("%s.name"%aov) in ["N","P","Z","ID","Pref","beauty","cputime","motionvector","opacity","raycount"]:
            m.setAttr("%s.aovtype"%aov, 1) # set aovType to 'UTIL'


def create_aov_sets(): # en=0
    '''Creates maya sets for the aovs and drivers for easy selection and editing'''

    sfmu.addToSet(m.ls(type="aiAOV"), "aov_SEL")
    sfmu.addToSet(m.ls(type="aiAOVDriver"), "aov_driver_SEL")

def create_aov_drivers():# en=0
    '''Creates and sets attributes on aiAOVDriver nodes to write renders out to separate files 
    '''

    # path_prefix = "<RenderLayer>/<Scene>_<RenderLayer>_<AovDriver>"
    # path_prefix = "<Scene>_<AovDriver>"
    # path_prefix = "<Scene>_<Camera>_<RenderLayer>_<AovDriver>"
    path_prefix = "<RenderLayer>/<Scene>_<Camera>_<RenderLayer>_<AovDriver>"
    
    m.setAttr("defaultRenderGlobals.imageFilePrefix", "", type="string")

    driver = "defaultArnoldDriver"
    m.setAttr("%s.prefix"%driver, path_prefix.replace("_<AovDriver>",""), type="string")
    m.setAttr("%s.prefix"%driver, path_prefix.replace("<AovDriver>",renderOutputs[0]), type="string")
    m.setAttr("%s.exrCompression"%driver, 2)
    m.setAttr("%s.halfPrecision"%driver, 1)
    m.setAttr("%s.preserveLayerName"%driver, 1)
    m.setAttr("%s.tiled"%driver, 1)
    m.setAttr("%s.autocrop"%driver, 0)
    m.setAttr("%s.append"%driver, 0)
    m.setAttr("%s.mergeAOVs"%driver, 1)

    driver = "aiAOVDriver_%s"%renderOutputs[1]
    if not m.objExists(driver): driver = m.createNode("aiAOVDriver", n="aiAOVDriver_%s"%renderOutputs[1])
    m.setAttr("%s.prefix"%driver, path_prefix.replace("<AovDriver>",renderOutputs[1]), type="string")
    m.setAttr("%s.exrCompression"%driver, 2)
    m.setAttr("%s.halfPrecision"%driver, 1)
    m.setAttr("%s.preserveLayerName"%driver, 1)
    m.setAttr("%s.tiled"%driver, 0)
    m.setAttr("%s.autocrop"%driver, 1)
    m.setAttr("%s.append"%driver, 0)
    m.setAttr("%s.mergeAOVs"%driver, 1)

    driver = "aiAOVDriver_%s"%renderOutputs[2]
    if not m.objExists(driver): driver = m.createNode("aiAOVDriver", n="aiAOVDriver_%s"%renderOutputs[2])
    m.setAttr("%s.prefix"%driver, path_prefix.replace("<AovDriver>",renderOutputs[2]), type="string")
    m.setAttr("%s.exrCompression"%driver, 2)
    m.setAttr("%s.halfPrecision"%driver, 0)
    m.setAttr("%s.preserveLayerName"%driver, 1)
    m.setAttr("%s.tiled"%driver, 0)
    m.setAttr("%s.autocrop"%driver, 1)
    m.setAttr("%s.append"%driver, 0)
    m.setAttr("%s.mergeAOVs"%driver, 1)

    driver = "aiAOVDriver_%s"%renderOutputs[3]
    if not m.objExists(driver): driver = m.createNode("aiAOVDriver", n="aiAOVDriver_%s"%renderOutputs[3])
    m.setAttr("%s.prefix"%driver, path_prefix.replace("<AovDriver>",renderOutputs[3]), type="string")
    m.setAttr("%s.exrCompression"%driver, 2)
    m.setAttr("%s.halfPrecision"%driver, 1)
    m.setAttr("%s.preserveLayerName"%driver, 1)
    m.setAttr("%s.tiled"%driver, 0)
    m.setAttr("%s.autocrop"%driver, 1)
    m.setAttr("%s.append"%driver, 0)
    m.setAttr("%s.mergeAOVs"%driver, 1)
