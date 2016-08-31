'''
functions for dealing with mtoa node types and classifications
'''

import pymel.core as pm
import mtoa.utils as utils
import mtoa.callbacks as callbacks
import maya.cmds as cmds
import os

CATEGORY_TO_RUNTIME_CLASS = {
                ('shader',):            'asShader',
                ('texture',):           'asTexture',
                ('light',):             'asLight',
                ('light', 'filter'):    'asUtility',
                ('utility',):           'asUtility',
                }

MTOA_GLOBALS = {}
ACTIVE_CAMERA = None

def _processClass(nodeType):
    '''
    convert the passed node type's classification string to a tuple containing a formatted path string
    compatible with the node lister and the runtime classification.
    
    e.g. from 'aiStandard' to ('rendernode/arnold/shader/surface', 'asShader', 'Arnold/Shader/Surface')
    '''
    for klass in pm.getClassification(nodeType):
        if klass.startswith('rendernode/arnold'):
            parts = klass.split('/')
            if len(parts) < 3:
                return (klass, 'asUtility', 'Arnold')
            else :
                # remove the rendernode first token
                parts.pop(0)
                label = '/'.join([utils.prettify(x) for x in parts])
                cat = 'asUtility'
                # find a runtime classification. try matching from most specific to most generic
                # first token is always 'arnold':
                parts.pop(0)
                while parts:
                    try:
                        cat = CATEGORY_TO_RUNTIME_CLASS[tuple(parts)]
                    except KeyError:
                        parts.pop(-1)
                    else:
                        break
                return (klass, cat, label)
    return (None, None, None)

def isSubClassification(testClass, otherClass):
    '''
    returns True if the first classification is contained within the second
    
    for example 'rendernode/arnold/shader/displacement' is a sub-filter of 'rendernode/arnold/shader'
    '''
    otherParts = otherClass.split('/')
    testParts = testClass.split('/')
    if len(testParts) < len(otherParts):
        return False
    return testParts[:len(otherParts)] == otherParts

def getRuntimeClass(nodeType):
    '''
    get the runtime classification of an arnold node
    '''
    return _processClass(nodeType)[1]

def createArnoldNode(nodeType, name=None, skipSelect=False, runtimeClassification=None):
    '''
    create an arnold node with the proper runtime classification
    '''
    kwargs = {}
    kwargs['skipSelect'] = skipSelect
    if name:
        kwargs['name'] = name
    if runtimeClassification is None:
        runtimeClassification = getRuntimeClass(nodeType)
    if runtimeClassification:
        kwargs[runtimeClassification] = True
        node = pm.shadingNode(nodeType, **kwargs)
    else:
        pm.warning("[mtoa] Could not determine runtime classification of %s: set maya.classification metadata" % nodeType)
        node = pm.createNode(nodeType, **kwargs)

    createOptions()

    return node

_mtoaNodes = None
def isMtoaNode(nodeType):
    """
    return whether the passed node type was created by mtoa
    """
    global _mtoaNodes
    if _mtoaNodes is None:
        _mtoaNodes = pm.pluginInfo('mtoa', query=True, dependNode=True)
    return nodeType in _mtoaNodes

def getAttributeData(nodeType):
    import maya.cmds as cmds
    data = cmds.arnoldPlugins(getAttrData=nodeType) or []
    # convert empty strings to None
    data = [x or None for x in data]
    return utils.groupn(data, 4)

def arnoldIsCurrentRenderer():
    "return whether arnold is the current renderer"
    return pm.getAttr('defaultRenderGlobals.currentRenderer') == 'arnold'

def listTranslators(nodeType):
    '''
    return a list of (translator, arnoldNode) pairs
    '''
    import maya.cmds as cmds
    data = cmds.arnoldPlugins(listTranslators=nodeType) or []
    # convert empty strings to None
    data = [x or None for x in data]
    return utils.groupn(data, 2)

def createStandIn(path=None):
    if not pm.objExists('ArnoldStandInDefaultLightSet'):
        pm.createNode("objectSet", name="ArnoldStandInDefaultLightSet", shared=True)
        pm.lightlink(object='ArnoldStandInDefaultLightSet', light='defaultLightSet')

    standIn = pm.createNode('aiStandIn', n='ArnoldStandInShape')
    # temp fix until we can correct in c++ plugin
    cmds.setAttr('%s.visibleInReflections' % standIn.name(), True)
    cmds.setAttr('%s.visibleInRefractions' % standIn.name(), True)
    pm.sets('ArnoldStandInDefaultLightSet', add=standIn)
    if path:
        standIn.dso.set(path)
    return standIn
    
def createVolume():
    pm.createNode('aiVolume', n='ArnoldVolumeShape')

def upgradeAOVOutput(options, defaultFilter=None, defaultDriver=None):
    """
    Upgrades scenes to use new node-base filter and drivers

    Unfortunately, in Maya 2012 old driver/filter attributes are extension attributes, so no longer
    exist on the aiAOV node.  As a result AOVs that override the global value will lose 
    driver/filter specific settings like compression and quality.
    """
    print "[mtoa] upgrading to new AOV driver/filter setup"
    aovNodes = pm.ls(type='aiAOV')
    if defaultDriver is None:
        defaultDriver = pm.PyNode('defaultArnoldDriver')
        
    if defaultFilter is None:
        defaultFilter = pm.PyNode('defaultArnoldFilter')

    driver = options.imageFormat.get()
    if driver:
        defaultDriver.aiTranslator.set(driver)

    filter = options.filterType.get()
    if filter:
        defaultFilter.aiTranslator.set(filter)

    data = [(aovNodes, 'aiAOVDriver', '.outputs[0].driver', 'imageFormat', defaultDriver),
            (aovNodes, 'aiAOVFilter', '.outputs[0].filter', 'filterType', defaultFilter)]

    for nodes, mayaNodeType, inputAttr, controlAttr, defaultNode in data:
#        attrSet = set([])
#        for transName, arnoldNode in listTranslators(mayaNodeType):
#            print "\t", arnoldNode
#            for paramName, attrName, label, annotation in getAttributeData(arnoldNode):
#                print "\t\t", paramName, attrName
#                attrSet.add(attrName)
        for node in nodes:
            at = node.name() + inputAttr
            inputs = pm.listConnections(at, source=True, destination=False)
            if not inputs:
                translator = node.attr(controlAttr).get()
                if translator in ['', '<Use Globals>']:
                    defaultNode.message.connect(at)
                    print "[mtoa] upgrading %s: connected to default node %s" % (node, defaultNode)
                else:
                    outputNode = pm.createNode(mayaNodeType, skipSelect=True)
                    print "[mtoa] upgrading %s: created new node %s and set translator to %r" % (node, outputNode, translator)
                    outputNode.message.connect(at)
                    outputNode.aiTranslator.set(translator)

#                for attr in attrSet:
#                    oldName = outputType + attr[0].upper() + attr[1:]
#                    try:
#                        value = aovNode.attr(oldName).get()
#                        print aovNode, oldName, value
#                    except AttributeError:
#                        pass
#                    outputNode.attr(attr)


def createOptions():
    """
    override this with your own function to set defaults
    """
    import mtoa.aovs as aovs
    import mtoa.hooks as hooks

    # the shared option ensures that it is only created if it does not exist
    options = pm.createNode('aiOptions', skipSelect=True, shared=True, name='defaultArnoldRenderOptions')
    filterNode = pm.createNode('aiAOVFilter', name='defaultArnoldFilter', skipSelect=True, shared=True)
    driverNode = pm.createNode('aiAOVDriver', name='defaultArnoldDriver', skipSelect=True, shared=True)
    displayDriverNode = pm.createNode('aiAOVDriver', name='defaultArnoldDisplayDriver', skipSelect=True, shared=True)

    if (filterNode or driverNode) and not options:
        options = pm.PyNode('defaultArnoldRenderOptions')
        # options previously existed, so we need to upgrade
        upgradeAOVOutput(options, filterNode, driverNode)

    # if we're just creating the options node, then be sure to connect up the driver and filter
    if filterNode:
        # newly created default filter
        hooks.setupFilter(filterNode)
    else:
        filterNode = pm.PyNode('defaultArnoldFilter')

    if driverNode:
        # newly created default driver
        hooks.setupDriver(driverNode)
    else:
        driverNode = pm.PyNode('defaultArnoldDriver')

    if options:
        # newly created options
        hooks.setupDefaultAOVs(aovs.AOVInterface(options))
        hooks.setupOptions(options)
        pm.setAttr('defaultArnoldRenderOptions.version', str(cmds.pluginInfo( 'mtoa', query=True, version=True)))
    else:
        options = pm.PyNode('defaultArnoldRenderOptions')
        if displayDriverNode:
            # options exist, but not display driver: upgrade from older version of mtoa
            hooks.setupDefaultAOVs(aovs.AOVInterface(options))

    if displayDriverNode:
        # newly created default driver
        displayDriverNode.aiTranslator.set('maya')
        # GUI only
        displayDriverNode.outputMode.set(0)
        hooks.setupDriver(displayDriverNode)
        displayDriverNode.message.connect(options.drivers, nextAvailable=True)
    elif not options.drivers.inputs():
        pm.connectAttr('defaultArnoldDisplayDriver.message', options.drivers, nextAvailable=True)
    try:
        pm.connectAttr('%s.message' % filterNode.name(), '%s.filter' % options.name(), force=True)
    except:
        pass
    try:
        pm.connectAttr('%s.message' % driverNode.name(), '%s.driver' % options.name(), force=True)
    except:
        pass
    

#-------------------------------------------------
# translator defaults
#-------------------------------------------------

_defaultTranslators = {}

def _doSetDefaultTranslator(obj):
    if not arnoldIsCurrentRenderer():
        return
    try:
        default = getDefaultTranslator(obj)
        pm.api.MFnDependencyNode(obj).findPlug('aiTranslator').setString(default)
    except RuntimeError:
        pm.warning("failed to set default translator for %s" % pm.api.MFnDependencyNode(obj).name())

def registerDefaultTranslator(nodeType, default):
    """
    Register the default translator for a node type. The second argument identifies the name of the
    translator.  Pass the translator name (as a string) if the default is always the same,
    or a function that takes the current node as a pymel PyNode and returns the translator name as a string.

    The default will automatically be set whenever a node of the given type is added to the scene.
    """

    global _defaultTranslators
    _defaultTranslators[nodeType] = default

    isFunc = callable(default)
    if not isFunc:
      cmds.arnoldPlugins(setDefaultTranslator=(nodeType, default))    
    if arnoldIsCurrentRenderer():
        it = pm.api.MItDependencyNodes()
        while not it.isDone():
            obj = it.item()
            if not obj.isNull():
                mfn = pm.api.MFnDependencyNode(obj)
                if mfn.typeName() == nodeType:
                    plug = mfn.findPlug("aiTranslator")
                    if not plug.isNull() and plug.asString() == "":
                        if isFunc:
                            val = default(obj)
                        else:
                            val = default
                        plug.setString(val)
            it.next()

    callbacks.addNodeAddedCallback(_doSetDefaultTranslator, nodeType,
                                   applyToExisting=False, apiArgs=True)

def getDefaultTranslator(obj):
    if isinstance(obj, basestring):
        obj = pm.api.toMObject(obj)
    mfn = pm.api.MFnDependencyNode(obj)
    global _defaultTranslators
    try:
        default = _defaultTranslators[mfn.typeName()]
        if callable(default):
            return default(obj)
        else:
            return default
    except KeyError:
        pass

def _rendererChanged(*args):
    if pm.getAttr('defaultRenderGlobals.currentRenderer') == 'arnold':
        global _defaultTranslators

        it = pm.api.MItDependencyNodes()
        while not it.isDone():
            obj = it.item()
            if not obj.isNull():
                mfn = pm.api.MFnDependencyNode(obj)
                nodeType = mfn.typeName()
                if nodeType in _defaultTranslators:
                    default = _defaultTranslators[nodeType]
                    assert default is not None
                    plug = mfn.findPlug("aiTranslator")
                    if not plug.isNull() and plug.asString() == "":
                        if callable(default):
                            val = default(obj)
                        else:
                            val = default
                        plug.setString(val)
            it.next()
            
def installCallbacks():
    """
    install all callbacks
    """
    # certain scenes fail to execute this callback:
    #callbacks.addAttributeChangedCallback(_rendererChanged, 'renderGlobals', 'currentRenderer')
    if pm.about(batch=True):
        callbacks.addAttributeChangedCallback(_rendererChanged, 'renderGlobals', 'currentRenderer')
    else:
        pm.scriptJob(attributeChange=['defaultRenderGlobals.currentRenderer', _rendererChanged] )
        pm.scriptJob(event =['SceneOpened', _rendererChanged] )

    import mtoa.aovs as aovs
    aovs.installCallbacks()

def uninstallCallbacks():
    #TODO: write uninstall code
    pass
