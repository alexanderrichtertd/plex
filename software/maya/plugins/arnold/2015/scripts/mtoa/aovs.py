import pymel.core as pm
import mtoa.utils as utils
import mtoa.callbacks as callbacks
from collections import namedtuple
from itertools import groupby
import arnold.ai_params

BUILTIN_AOVS = (
                ('P',                   'point'),
                ('Z',                   'float'),
                ('N',                   'vector'),
                ('opacity',             'rgb'),
                ('motionvector',        'rgb'),
                ('Pref',                'rgb'),
                ('raycount',            'float'),
                ('cputime',             'float'),
                ('beauty',              'rgba'),
                ('ID',                  'int'),
                ('mesh_light_beauty',   'rgb'),
                ('volume',              'rgb'),
                ('volume_opacity',      'rgb'),
                ('volume_direct',       'rgb'),
                ('volume_indirect',     'rgb'),
#                ('A',       'float'),
#                ('OBJECT',  'node'),
#                ('SHADER',  'node'),
                )

TYPES = (
    ("int",    arnold.ai_params.AI_TYPE_INT),
    ("bool",   arnold.ai_params.AI_TYPE_BOOLEAN),
    ("float",  arnold.ai_params.AI_TYPE_FLOAT),
    ("rgb",    arnold.ai_params.AI_TYPE_RGB),
    ("rgba",   arnold.ai_params.AI_TYPE_RGBA),
    ("vector", arnold.ai_params.AI_TYPE_VECTOR),
    ("point",  arnold.ai_params.AI_TYPE_POINT),
    ("point2", arnold.ai_params.AI_TYPE_POINT2),
    ("pointer",arnold.ai_params.AI_TYPE_POINTER))

defaultFiltersByName = {'Z' : 'closest', 'motion_vector' : 'closest', 'P' : 'closest', 'N' : 'closest', 'Pref' : 'closest', 'ID' : 'closest'}

GlobalAOVData = namedtuple('GlobalAOVData', ['name', 'attribute', 'type'])

SceneAOVData = namedtuple('SceneAOVData', ['name', 'type', 'index', 'node'])

def nextAvailableIndex(attr):
    lastIndex = -1
    for at in attr:
        currIndex = at.index()
        if currIndex > (lastIndex +1):
            return lastIndex +1
        lastIndex = currIndex
    return lastIndex +1

def getShadingGroupAOVMap(nodeAttr):
    '''
    return a mapping from aov name to element 'aovName' plug on aiCustomAOVs, and the next available index
    '''
    lastIndex = -1
    nextIndex = None
    nameToAttr = {}
    for at in nodeAttr:
        currIndex = at.index()
        if nextIndex is None and currIndex > (lastIndex +1):
            nextIndex = lastIndex +1
        name = at.aovName.get()
        if name:
            nameToAttr[name] = at
        lastIndex = currIndex
    if nextIndex is None:
        nextIndex = lastIndex +1
    return nameToAttr, nextIndex

def removeAliases(aovs):
    for sg in pm.ls(type='shadingEngine'):
        for aov in aovs:
            try:
                pm.removeMultiInstance(sg + '.ai_aov_' + aov.name)
            except RuntimeError, err:
                pass #print err

def addAliases(aovs):
    for sg in pm.ls(type='shadingEngine'):
        sgAttr = sg.aiCustomAOVs
        nameMapping, nextIndex = getShadingGroupAOVMap(sgAttr)
        for aov in aovs:
            try:
                plug = nameMapping[aov.name]
            except KeyError:
                plug = sgAttr[nextIndex]
                plug.aovName.set(aov.name)
            try:
                pm.aliasAttr('ai_aov_' + aov.name, plug)
            except RuntimeError as err:
                pm.aliasAttr(sg + '.ai_aov_' + aov.name, remove=True)
                pm.aliasAttr('ai_aov_' + aov.name, plug)

def refreshAliases():
    aovList = getAOVs()
    removeAliases(aovList)
    addAliases(aovList)

class SceneAOV(object):
    def __init__(self, node, destAttr):
        self.destAttr = destAttr
        self._node = node
        self._index = None
        self._name = None
        self._type = None

    def __repr__(self):
        return '%s(%r, %d)' % (self.__class__.__name__, self.node, self.index)

    def __eq__(self, other):
        if isinstance(other, basestring):
            return self.name == other
        else:
            return self.name == other.name

    def __lt__(self, other):
        if isinstance(other, basestring):
            if other == "beauty":
                return False
            if self.name == "beauty":
                return True
            else:
                return self.name < other
        else:
            if other.name == "beauty":
                return False
            if self.name == "beauty":
                return True
            else:
                return self.name < other.name

    def __gt__(self, other):
        if isinstance(other, basestring):
            if self.name == "beauty":
                return False
            if other == "beauty":
                return True
            else:
                return self.name > other
        else:
            if self.name == "beauty":
                return False
            if other.name == "beauty":
                return True
            else:
                return self.name > other.name

    @property
    def index(self):
        if self._index is None:
            self._index = self.destAttr.index()
        return self._index

    @property
    def name(self):
        '''
        Note that this value is cached on first access and for the sake of speed it
        is not requeried.  To update the instance to reflect the current state of
        the aiAOV node that it wraps, call update()
        '''
        if self._name is None:
            self._name = self._node.attr('name').get()
        return self._name

    @property
    def type(self):
        '''
        Note that this value is cached on first access and for the sake of speed it
        is not requeried.  To update the instance to reflect the current state of
        the aiAOV node that it wraps, call update()
        '''
        if self._type is None:
            self._type = self._node.attr('type').get()
        return self._type

    @property
    def node(self):
        return self._node

    def rename(self, newName, oldName=None):
        '''
        rename an AOV in the active list.
        
        provide oldName if the attribute has already been renamed and you just need
        to perform the proper bookkeeping 
        '''
        if oldName is None:
            oldName = self.name
            self.node.attr('name').set(newName)

        for sg in pm.ls(type='shadingEngine'):
            try:
                pm.aliasAttr(sg + '.ai_aov_' + oldName, remove=True)
            except RuntimeError, err:
                pass #print err

            sgAttr = sg.aiCustomAOVs
            try:
                pm.aliasAttr('ai_aov_' + newName, sgAttr[self.index])
            except RuntimeError, err:
                pass #print err

    def update(self):
        '''
        update the cached name from the AOV node
        '''
        self._name = self._node.attr('name').get()
        self._name = self._node.attr('name').get()

#------------------------------------------------------------
# scene queries
#------------------------------------------------------------

class AOVInterface(object):
    def __init__(self, node=None):
        self._node = node if node else pm.PyNode('defaultArnoldRenderOptions')
        self._aovAttr = self._node.aovs

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._node)

    @property
    def node(self):
        if not self._node.exists():
            raise TypeError("node doesn't exist")
        return self._node

    def nextAvailableAttr(self):
        return self._aovAttr.elementByLogicalIndex(self._aovAttr.numElements())

    def getAOVs(self, group=False, sort=True, enabled=None, include=None, exclude=None):
        '''
        return a list of SceneAOV classes for all AOVs in the scene
        if group is True, the SceneAOVs are grouped by name: (aovName, [SceneAOV1, SceneAOV2, ...])
        
        enabled: the enabled state of the AOV. ignored if None (default)
        include: a list of AOV names to include
        exclude: a list of AOV names to exclude
        '''
        result = [SceneAOV(fromAttr.node(), toAttr) for toAttr, fromAttr in self._aovAttr.inputs(plugs=True, connections=True)]
        if sort:
            result = sorted(result)
        if enabled is not None:
            result = [aov for aov in result if aov.node.attr('enabled').get() == enabled]
        if group:
            result = [(aovName, list(aovs)) for aovName, aovs in groupby(result, lambda x: x.name)]
        if include:
            result = [a for a in result if a.name in include]
        if exclude:
            result = [a for a in result if a.name not in exclude]
        return result

    def getAOVNodes(self, names=False):
        '''
        sorted by aovName
        @param names: if True, returns pairs of (aovName, aovNode). if False, returns a list of aovNodes
        '''
        if names:
            result = [(x.attr('name').get(), x) for x in self._aovAttr.inputs()]
            return sorted(result, key = lambda x: x[0])
        else:
            result = self._aovAttr.inputs()
            return sorted(result, key = lambda x: x.attr('name').get())

    def getAOVNode(self, aovName):
        '''
        given the name of an AOV, return the corresponding aov node
        
        raises an error if there is more than one match.
        returns None if there are no matches.
        '''
        matches = self.getAOVs(include=[aovName])
        if len(matches) > 1:
            raise ValueError("More than one AOV matches name %r" % aovName)
        elif matches:
            return matches[0].node

    def addAOV(self, aovName, aovType=None):
        '''
        add an AOV to the active list for this AOV node

        returns the created AOV node
        '''
        if aovType is None:
            aovType = getAOVTypeMap().get(aovName, 'rgba')
        if not isinstance(aovType, int):
            aovType = dict(TYPES)[aovType]
        aovNode = pm.createNode('aiAOV', name='aiAOV_' + aovName, skipSelect=True)
        out = aovNode.attr('outputs')[0]

        pm.connectAttr('defaultArnoldDriver.message', out.driver)
        filter = defaultFiltersByName.get(aovName, None)
        if filter:
            node = pm.createNode('aiAOVFilter', skipSelect=True)
            node.aiTranslator.set(filter)
            filterAttr = node.attr('message')
            import mtoa.hooks as hooks
            hooks.setupFilter(filter, aovName)
        else:
            filterAttr = 'defaultArnoldFilter.message'
        pm.connectAttr(filterAttr, out.filter)

        aovNode.attr('name').set(aovName)
        aovNode.attr('type').set(aovType)
        nextPlug = self.nextAvailableAttr()
        aovNode.message.connect(nextPlug)
        aov = SceneAOV(aovNode, nextPlug)
        addAliases([aov])
        return aov

    def removeAOV(self, aov):
        '''
        remove an AOV from the active list for this AOV node

        raises an error if there is more than one match
        returns True if the node was found and removed, False otherwise
        '''
        if isinstance(aov, basestring):
            matches = self.getAOVs(include=[aov])
            if not matches:
                return False
            assert len(matches) == 1
            aov = matches[0]

        self._removeAOVNode(aov.node)
        removeAliases([aov])

    def removeAOVs(self, aovNames):
        '''
        remove AOVs matching names in aovNames from the active list

        returns True if any nodes were removed
        '''
        matches = self.getAOVs(include=aovNames)
        if matches:
            for aov in matches:
                self._removeAOVNode(aov.node)
            removeAliases(matches)
            return True
        return False

    def _removeAOVNode(self, aovNode):
        '''
        Note this does not remove aliases. You must call removeAliases() manually
        '''
        inputs = aovNode.inputs(type=['aiAOVDriver', 'aiAOVFilter'])
        utils.safeDelete(aovNode)
        for input in inputs:
            # callback may have deleted it
            if input.exists() and not input.message.outputs():
                print "deleting", input

    def renameAOVs(self, oldName, newName):
        '''
        rename an AOV in the active list
        '''
        matches = self.getAOVs(include=[oldName])
        if matches:
            for aov in matches:
                aov.node.attr('name').set(newName)

            # we can only use one
            matches[0].rename(newName, oldName)
        else:
            raise NameError('Scene does not contain any AOVs with name %r' % oldName)

def getAOVs(group=False, sort=True, enabled=None, include=None, exclude=None):
    try:
        return AOVInterface().getAOVs(group, sort, enabled, include, exclude)
    except pm.MayaNodeError:
        return []

def getAOVNodes(names=False):
    try:
        return AOVInterface().getAOVNodes(names)
    except pm.MayaNodeError:
        return []

#------------------------------------------------------------
# global queries
#------------------------------------------------------------

def getRegisteredAOVs(builtin=False, nodeType=None):
    '''
    returns a list of all registered aov names.

    @param builtin: set to True to include built-in AOVs
    @param nodeType: a node name or list of node names to restrict result to AOVs for only those nodes
    '''
    if nodeType:
        if isinstance(nodeType, (list, tuple)):
            result = [x[0] for x in getNodeGlobalAOVData(nt) for nt in nodeType]
        else:
            result = [x[0] for x in getNodeGlobalAOVData(nodeType)]
    else:
        result = pm.cmds.arnoldPlugins(listAOVs=True)
    if builtin:
        result = getBuiltinAOVs() + result
    return result

def getBuiltinAOVs():
    return [x[0] for x in BUILTIN_AOVS]

def getNodeGlobalAOVData(nodeType):
    "returns a list of registered (name, attribute, data type) pairs for the given node type"
    # convert to a 2d array
    result = [GlobalAOVData(*x) for x in utils.groupn(pm.cmds.arnoldPlugins(listAOVs=True, nodeType=nodeType), 3)]
    return sorted(result, key=lambda x: x.name)

def getNodeTypesWithAOVs():
    return sorted(pm.cmds.arnoldPlugins(listAOVNodeTypes=True))

_aovTypeMap = None
def getAOVTypeMap():
    "return a dictionary of AOV name to AOV type"
    # TODO: update this cached result when new nodes are added
    global _aovTypeMap
    if _aovTypeMap is None:
        _aovTypeMap = {}
        for nodeType in getNodeTypesWithAOVs():
            for aovName, attr, type in getNodeGlobalAOVData(nodeType):
                _aovTypeMap[aovName] = type
        _aovTypeMap.update(dict(BUILTIN_AOVS))
    return _aovTypeMap

#- groups

def getAOVGroups():
    return ['<builtin>']

def getGroupAOVs(groupName):
    if groupName == '<builtin>':
        return getBuiltinAOVs()
    raise


#------------------------------------------------------------
# callbacks
#------------------------------------------------------------
_aovOptionsChangedCallbacks = callbacks.DeferredCallbackQueue()
# a public function for adding AOV callbacks
def addAOVChangedCallback(func, key=None):
    _aovOptionsChangedCallbacks.addCallback(func, key)

def removeAOVChangedCallback(key):
    _aovOptionsChangedCallbacks.removeCallback(key)

def createAliases(sg):
    # This will run on scene startup but the list of AOVs will be unknown
    if not sg:
        return
    if sg.name() == "swatchShadingGroup":
        return
        
    if pm.hasAttr(sg, "attributeAliasList"):
        alias_list = sg.attributeAliasList
        if alias_list.exists() and not sg.listAliases() :
            print "Shading Group %s with bad Attribute Alias list detected. Fixing!" % sg.name()
            alias_list.delete()
        
    aovList = getAOVs()
    sgAttr = sg.aiCustomAOVs
    for aov in aovList:
        exists = False
        for at in sgAttr:
            if at.aovName.get() == aov.name:
                exists = True
        if not exists:
            i = nextAvailableIndex(sgAttr)
            at = sgAttr[i]
            at.aovName.set(aov.name)
       
    if pm.referenceQuery(sg.name(), isNodeReferenced=True):
        return
    for at in sgAttr:
        name = at.aovName.get()
        try:
            pm.aliasAttr('ai_aov_' + name, at)
        except RuntimeError as err:
            pm.aliasAttr(sg + '.ai_aov_' + name, remove=True)
            pm.aliasAttr('ai_aov_' + name, at)


def installCallbacks():
    _sgAliasesCallbacks = callbacks.SceneLoadCallbackQueue()
    _sgAliasesCallbacks.addCallback(createAliases, passArgs=True)
    callbacks.addNodeAddedCallback(_sgAliasesCallbacks, 'shadingEngine',
                                   applyToExisting=True, apiArgs=False)
    
    if not pm.about(batch=True):
        callbacks.addAttributeChangedCallback(_aovOptionsChangedCallbacks, 'aiOptions', 'aovList',
                                  context=pm.api.MNodeMessage.kConnectionMade | pm.api.MNodeMessage.kConnectionBroken,
                                  applyToExisting=True)
    #callbacks.addAttributeChangedCallback(_aovOptionsChangedCallbacks.entryCallback, 'aiAOV', None, applyToExisting=True)

