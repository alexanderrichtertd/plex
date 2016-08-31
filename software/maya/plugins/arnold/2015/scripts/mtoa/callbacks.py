"""
a module for managing mtoa's callbacks
"""
 
import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMaya as om
from collections import defaultdict
import types

global _callbackIds
_callbackIds = om.MCallbackIdArray()

global _nodeAddedCallbacks
_nodeAddedCallbacks = defaultdict(list)

global _nodeRemovedCallbacks
_nodeRemovedCallbacks = defaultdict(list)

global _attrChangedCallbacks
_attrChangedCallbacks = {}

global _nameChangedCallbacks
_nameChangedCallbacks = defaultdict(list)

CONTEXTS = [om.MNodeMessage.kConnectionMade,
            om.MNodeMessage.kConnectionBroken,
            om.MNodeMessage.kAttributeEval,
            om.MNodeMessage.kAttributeSet,
            om.MNodeMessage.kAttributeLocked,
            om.MNodeMessage.kAttributeUnlocked,
            om.MNodeMessage.kAttributeAdded,
            om.MNodeMessage.kAttributeRemoved,
            om.MNodeMessage.kAttributeRenamed,
            om.MNodeMessage.kAttributeKeyable,
            om.MNodeMessage.kAttributeUnkeyable,
            om.MNodeMessage.kIncomingDirection,
            om.MNodeMessage.kAttributeArrayAdded,
            om.MNodeMessage.kAttributeArrayRemoved,
            om.MNodeMessage.kOtherPlugSet]

ANY_CHANGE = 0
for _msg in CONTEXTS:
    ANY_CHANGE |= _msg


def _removeCallbacks(*args):
    if args[0][0] != 'mtoa':
        return
    global _callbackIds
    om.MDGMessage.removeCallbacks(_callbackIds)

def manageCallback(callbackId):
    "track a callback id so that it can be automatically removed when mtoa is unloaded"
    global _callbackIds
    _callbackIds.append(callbackId)

def _makeNodeAddedCB(nodeType):
    def nodeAddedCB(obj, *args):
        # nodeAdded callback includes sub-types, but we want exact type only
        mfn = pm.api.MFnDependencyNode(obj)
        if mfn.typeName() != nodeType:
            return
        global _nodeAddedCallbacks
        for func, apiArgs in _nodeAddedCallbacks[nodeType]:
            if apiArgs:
                func(obj)
            else:
                node = pm.PyNode(obj)
                func(node)
    # no unicode allowed
    nodeAddedCB.__name__ = "nodeAddedCB_" + str(nodeType) 
    return nodeAddedCB
    
def _makeNodeRemovedCB(nodeType):
    def nodeRemovedCB(obj, *args):
        # nodeAdded callback includes sub-types, but we want exact type only
        mfn = pm.api.MFnDependencyNode(obj)
        if mfn.typeName() != nodeType:
            return
        global _nodeRemovedCallbacks
        for func, apiArgs in _nodeRemovedCallbacks[nodeType]:
            if apiArgs:
                func(obj)
            else:
                node = pm.PyNode(obj)
                func(node)
    # no unicode allowed
    nodeRemovedCB.__name__ = "nodeRemovedCB_" + str(nodeType) 
    return nodeRemovedCB

def addNodeAddedCallback(func, nodeType, applyToExisting=True, apiArgs=False):
    """
    creates and manages a node added callback

    Parameters
    ----------
    func : callback function
        should take a single argument. the type of the argument is controlled by the apiArgs flag
    nodeType : string
        type of node to install callbacks for
    applyToExisting : boolean
        whether to apply the function to existing nodes
    apiArgs : boolean
        if True, api objects (MObjects, MPlugs, etc) are left as is. If False, they're converted to string names
    """
    if nodeType not in _nodeAddedCallbacks:
        cb = _makeNodeAddedCB(nodeType)
        manageCallback(om.MDGMessage.addNodeAddedCallback(cb, nodeType))
    _nodeAddedCallbacks[nodeType].append((func, apiArgs))
    
    if applyToExisting and apiArgs:
        _updateExistingNodes(nodeType, func)
        
def addNodeRemovedCallback(func, nodeType, applyToExisting=True, apiArgs=False):
    """
    creates and manages a node removed callback

    Parameters
    ----------
    func : callback function
        should take a single argument. the type of the argument is controlled by the apiArgs flag
    nodeType : string
        type of node to install callbacks for
    applyToExisting : boolean
        whether to apply the function to existing nodes
    apiArgs : boolean
        if True, api objects (MObjects, MPlugs, etc) are left as is. If False, they're converted to string names
    """
    if nodeType not in _nodeRemovedCallbacks:
        cb = _makeNodeRemovedCB(nodeType)
        manageCallback(om.MDGMessage.addNodeRemovedCallback(cb, nodeType))
    _nodeRemovedCallbacks[nodeType].append((func, apiArgs))
    
    if applyToExisting and apiArgs:
        _updateExistingNodes(nodeType, func)

def _getHandle(obj):
    handle = om.MObjectHandle(obj)
    handle.__hash__ = handle.hashCode
    return handle

def _makeInstallAttributeChangedCallback(nodeType):
    """
    make a function to be used with a nodeAdded callback which
    installs attributeChanged callbacks for the passed attribute
    """
    def installAttrChangeCallback(obj):
        fnNode = om.MFnDependencyNode(obj)
        # nodeAdded callback includes sub-types, but we want exact type only
        if fnNode.typeName() != nodeType:
            return
        # scriptJob does not receive an arg, but we want ours to
        def attrChanged(msg, plug, otherPlug, *args):
            global _attrChangedCallbacks
            try:
                funcMap = _attrChangedCallbacks[nodeType]
            except KeyError:
                pass
            else:
                plugName = plug.partialName(False, False, True, False, True, True)
                # functions which should execute on any attribute change have a key of None
                funcList = funcMap.get(plugName, []) + funcMap.get(None, [])

                #if funcList: print "attr changed", plugName, msg
                for func, context in funcList:
                    if context & msg:
                        func(plug, otherPlug, *args)
                    #else: print "skipping %s %s based on context %s %s" % (plugName, func, msg, context)
#        _attrChangedCallbacks[_getHandle(node)]
        manageCallback(om.MNodeMessage.addAttributeChangedCallback(obj, attrChanged))
    return installAttrChangeCallback
    
def _makeInstallNameChangedCallback(nodeType):
    """
    make a function to be used with a nodeAdded callback which
    installs nameChanged callbacks
    """
    def installNameChangeCallback(obj):
        fnNode = om.MFnDependencyNode(obj)
        # nodeAdded callback includes sub-types, but we want exact type only
        if fnNode.typeName() != nodeType:
            return
        # scriptJob does not receive an arg, but we want ours to
        def nameChanged(obj, name, *args):
            global _nameChangedCallbacks
            for func, apiArgs in _nameChangedCallbacks[nodeType]:
                func(obj, name, *args)
            
        manageCallback(om.MNodeMessage.addNameChangedCallback(obj, nameChanged))
    return installNameChangeCallback


def _updateExistingNodes(nodeType, func):
    fnNode = om.MFnDependencyNode()
    nodeIt = om.MItDependencyNodes()
    while 1:
        if nodeIt.isDone():
            break
        node = nodeIt.item()
        if node.isNull():
            continue
        fnNode.setObject(node)
        if fnNode.typeName() == nodeType:
            func(node)
        nodeIt.next()

def addAttributeChangedCallback(func, nodeType, attribute, context=ANY_CHANGE, applyToExisting=True):
    """
    add an attribute changed callback for all current and future nodes of the given type

    Parameters
    ----------
    func : function
        should take a single string arg for the node of the attribute that changed
    nodeType : string
        type of node to install attribute changed callbacks for 
    attribute : string, list, or None
        name of attribute without leading period ('.').
        If a list, func will be registered for all of the passed attributes.
        If None, func will execute on any attribute change for the given node. 
    context : int mask
        an AttributeMessage enum from maya.OpenMaya.MNodeMessage describing what type of attribute
        change triggers the callback. defaults to any
    applyToExisting : boolean
        whether to apply the function to existing nodes
    """
    assert callable(func), "please pass a function as the first argument"
    global _attrChangedCallbacks
    nodeAddedCallback = _makeInstallAttributeChangedCallback(nodeType)
    if nodeType not in _attrChangedCallbacks:
        # add a callback which creates the scriptJob that calls our function
        addNodeAddedCallback(nodeAddedCallback, nodeType, applyToExisting=False, apiArgs=True)
        _attrChangedCallbacks[nodeType] = defaultdict(list)
    if isinstance(attribute, (list, tuple)):
        for at in attribute:
            _attrChangedCallbacks[nodeType][at].append((func, context))
    else:
        _attrChangedCallbacks[nodeType][attribute].append((func, context))

    # setup callback for existing nodes
    if applyToExisting and not om.MFileIO.isOpeningFile():
        _updateExistingNodes(nodeType, nodeAddedCallback)

def addAttributeChangedCallbacks(nodeType, attrFuncs, context=ANY_CHANGE):
    """
    add multiple attribute changed callbacks for all current and future nodes of the given type.
    
    this is more efficient at installing multiple attribute changed callbacks than repeatedly
    calling `addAttributeChangedCallback`
    
    Parameters
    ----------
    nodeType : string
        type of node to install attribute changed callbacks for 
    attrFuncs : list of (attribute name, functions) pairs
        function should take a single string arg for the node of the attribute that changed
        attributes should be names of attribute without leading period ('.')
    context : int mask
        an AttributeMessage enum from maya.OpenMaya.MNodeMessage describing what type of attribute
        change triggers the callback. defaults to any
    """
    global _attrChangedCallbacks
    nodeAddedCallback = _makeInstallAttributeChangedCallback(nodeType)
    if nodeType not in _attrChangedCallbacks:
        # add a callback which creates the scriptJob that calls our function
        addNodeAddedCallback(nodeAddedCallback, nodeType, apiArgs=True)
        _attrChangedCallbacks[nodeType] = defaultdict(list)

    for attr, func in attrFuncs:
        # TODO: support more than one callback per nodeType/attribute
        _attrChangedCallbacks[nodeType][attr].append((func, context))

    # setup callback for existing nodes
    if not om.MFileIO.isOpeningFile():
        _updateExistingNodes(nodeType, nodeAddedCallback)

def removeAttributeChangedCallbacks(nodeType, attribute):
    return _attrChangedCallbacks[nodeType].pop(attribute)
    
    
def addNameChangedCallback(func, nodeType, context=ANY_CHANGE, applyToExisting=True):
    """
    creates and manages a name changed callback

    Parameters
    ----------
    func : function
        should take a single string arg for the node of the attribute that changed
    nodeType : string
        type of node to install attribute changed callbacks for 
    applyToExisting : boolean
        whether to apply the function to existing nodes
    """
    assert callable(func), "please pass a function as the first argument"
    global _nameChangedCallbacks
    nodeAddedCallback = _makeInstallNameChangedCallback(nodeType)
    if nodeType not in _nameChangedCallbacks:
        # add a callback which creates the scriptJob that calls our function
        addNodeAddedCallback(nodeAddedCallback, nodeType, applyToExisting=False, apiArgs=True)
        _nameChangedCallbacks[nodeType].append((func, context))

    # setup callback for existing nodes
    if applyToExisting and not om.MFileIO.isOpeningFile():
        _updateExistingNodes(nodeType, nodeAddedCallback)

# cleanup callbacks once the mtoa plugin unloads
manageCallback(om.MSceneMessage.addStringArrayCallback(om.MSceneMessage.kAfterPluginUnload, _removeCallbacks, None))


class CallbackError(Exception): pass

class Callback(object):
    """
    Enables deferred function evaluation with 'baked' arguments.
    Useful where lambdas won't work...

    It also ensures that the entire callback will be be represented by one
    undo entry.

    Example:

    .. python::

        import pymel as pm
        def addRigger(rigger, **kwargs):
            print "adding rigger", rigger

        for rigger in riggers:
            pm.menuItem(
                label = "Add " + str(rigger),
                c = Callback(addRigger,rigger,p=1))   # will run: addRigger(rigger,p=1)
    """

    def __init__(self,func,*args,**kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self,*args):
        cmds.undoInfo(openChunk=1)
        try:
            try:
                return self.func(*self.args, **self.kwargs)
            except Exception, e:
                raise CallbackError('Error during callback: %s' % e)
        finally:
            cmds.undoInfo(closeChunk=1)

class CallbackWithArgs(Callback):
    def __call__(self,*args,**kwargs):
        # not sure when kwargs would get passed to __call__,
        # but best not to remove support now
        kwargsFinal = self.kwargs.copy()
        kwargsFinal.update(kwargs)
        cmds.undoInfo(openChunk=1)
        try:
            return self.func(*self.args + args, **kwargsFinal)
        finally:
            cmds.undoInfo(closeChunk=1)

class CallbackQueue(object):
    '''
    A basic queue of callback functions.
    
    It is comprised of 3 parts: 
      - entryCallback():  should be passed to the function that will be triggering the callback chain
                          (e.g. MNodeMessage.addAttributeChangedCallback)
      - deferredCallback(): passed by entryCallback to evalDeferred
      - the callback queue: custom functions added via addCallback() which are executed by deferredCallback()

    '''
    def __init__(self, callbacks=None):
        self._callbackQueue = {}
        if isinstance(callbacks, (list, tuple)):
            for item in callbacks:
                try:
                    size = len(item)
                except TypeError:
                    size = 1
                if size == 1:
                    self.addCallback(item)
                elif size == 2:
                    self.addCallback(item[1], item[0])
                elif size == 3:
                    self.addCallback(item[1], item[0], item[2])
                else:
                    raise TypeError("If passing a list or tuple, must be a list of functions or of key, function pairs")
        elif isinstance(callbacks, dict):
            for key, func in callbacks.iteritems():
                self.addCallback(func, key)
        elif hasattr(callbacks, '__call__'):
            self.addCallback(callbacks)
        elif callbacks is not None:
            raise TypeError("Please pass a list, tuple, dictionary, or function")

    def __call__(self, *args, **kwargs):
        self.entryCallback(*args, **kwargs)

    def addCallback(self, func, key=None, passArgs=False):
        if key is None:
            key = func
        self._callbackQueue[key] = (func, passArgs)

    def removeCallback(self, key):
        self._callbackQueue.pop(key)

    def clearCallbacks(self):
        self._callbackQueue = {}

    def deferredCallback(self, *args, **kwargs):
        for func, passArgs in self._callbackQueue.values():
            try:
                if passArgs:
                    func(*args, **kwargs)
                else:
                    func()
            except:
                import traceback
                traceback.print_exc()

    def entryCallback(self, *args, **kwargs):
        '''
        the public callback function
        '''
        self.deferredCallback(*args, **kwargs)

class DeferredCallbackQueue(CallbackQueue):
    """
    This class is used to execute one or many callbacks in a deferred fashion. It is intended to
    resolve the problem of accumulating many deferred callbacks when just one will do.  For example,
    when a scene is opened or a reference is created many attributeChanged callbacks may be triggered,
    but instead of running a function for each of these, you may wish a function to only run once, when
    the file is finished loading.

    Once the class's entryCallback() is triggered, any additional callback requests will be ignored until the
    deferredCallback() executes the callback queue.
    
    A single instance of the class can be used as a callback in multiple places (more than one attribute changed
    callback, for example), and it will run only once, even if both attributes trigger the callback.
    """
    def __init__(self, callbacks=None):
        super(DeferredCallbackQueue, self).__init__(callbacks)
        self._updating = False

    def deferredCallback(self, *args, **kwargs):
        try:
            super(DeferredCallbackQueue, self).deferredCallback(*args, **kwargs)
        finally:
            self._updating = False
    
    def entryCallback(self, *args):
        '''
        the public callback function
        '''
        if not self._updating:
            #print pm.api.MFileIO.isOpeningFile(), pm.api.MFileIO.isReadingFile()
            if not pm.api.MFileIO.isOpeningFile():
                self._updating = True
                #print self, "evalDeferred"
                pm.evalDeferred(self.deferredCallback)
        #else:print self, "skipping"

class SceneLoadCallbackQueue(CallbackQueue):
    '''
    This callback queue delays any callbacks received while opening or referencing a scene
    until after the operation has completed. Unlike DeferredCallbackQueue, which executes
    only the first callback it receives, SceneLoadCallbackQueue will execute every
    callback that it receives.
    '''
    def __init__(self, callbacks=None):
        super(SceneLoadCallbackQueue, self).__init__(callbacks)
        self._id = None
        self._args = []

    def __del__(self):
        if self._id:
            pm.api.MMessage.removeCallback(self._id)

    def deferredCallback(self, *trash):
        # arguments are intentionally unexpanded (i.e. they don't have * and **)
        # trash is an argument pass by MSceneMessage that we don't want to keep
        # print "SceneLoadCallbackQueue.deferredCallback", args
        cb = super(SceneLoadCallbackQueue, self).deferredCallback
        try:
            for args, kwargs in self._args:
                cb(*args, **kwargs)
        finally:
            self._args = []
            if self._id:
                pm.api.MMessage.removeCallback(self._id)
                self._id = None

    def entryCallback(self, *args, **kwargs):
        '''
        the public callback function
        '''
        
        if not self._id:
            #print self, "evalDeferred"
            if pm.api.MFileIO.isOpeningFile():
                self._args.append((args, kwargs))
                #print "setting up scene open callback", args, kwargs
                self._id = pm.api.MSceneMessage.addCallback(pm.api.MSceneMessage.kAfterOpen, self.deferredCallback)
            elif pm.api.MFileIO.isReadingFile():
                self._args.append((args, kwargs))
                #print "setting up reference load callback", args, kwargs
                self._id = pm.api.MSceneMessage.addCallback(pm.api.MSceneMessage.kAfterCreateReference, self.deferredCallback)
            else:
                #print "eval"
                # execute immediately
                super(SceneLoadCallbackQueue, self).deferredCallback(*args, **kwargs)
        else:
            # accumulate
            self._args.append((args, kwargs))

        #else:print self, "skipping"

class DelayedIdleCallbackQueue(DeferredCallbackQueue):
    '''
    This callback queue runs once on idle, much like `scriptJob -runOnce -idleEvent`,
    but with the key difference that an idleDelay can be specified such that the first n
    idle events will be skipped before finally executing the callbacks.
    
    Unlike the other callback queues, this one sets up its own MEventMessage callback on init. 
    '''
    def __init__(self, callbacks=None, idleDelay=5):
        super(DelayedIdleCallbackQueue, self).__init__(callbacks)
        self._id = None
        self._ticker = 0
        self._delay = idleDelay
        self._id = pm.api.MEventMessage.addEventCallback("idle", self.entryCallback)

    def __del__(self):
        if self._id:
            pm.api.MMessage.removeCallback(self._id)

    def entryCallback(self, *args):
        if self._ticker == self._delay:
            self._ticker = 0
            pm.api.MMessage.removeCallback(self._id)
            self._id = None
            self.deferredCallback()
        else:
            self._ticker+=1 
