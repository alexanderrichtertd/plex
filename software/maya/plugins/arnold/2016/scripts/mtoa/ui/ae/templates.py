"""
This module provides the functions necessary to register Attribute Editor templates written
in python.  The core class for writing templates is `AttributeTemplate`, which are then registered
using `registerAETemplate` or `registerTranslatorUI` depending on whether the template is for a node
or for an mtoa translator.
"""

import pymel
import pymel.core as pm
from maya.utils import executeDeferred
from mtoa.ui.ae.utils import aeCallback, AttrControlGrp
from mtoa.utils import prettify, toMayaStyle
import mtoa.core as core
from mtoa.core import registerDefaultTranslator, getDefaultTranslator
import arnold

from collections import defaultdict
import inspect

global _translatorTemplates
_translatorTemplates = defaultdict(dict)

global _templates
_templates = {}

showAllTranslators = False

#-------------------------------------------------
# Queries
#-------------------------------------------------

def getTranslators(nodeType):
    """
    Return a list of translator names for the given nodeType
    """
    return [x[0] for x in core.listTranslators(nodeType)]

def getTranslatorTemplates(nodeType):
    """
    Return a dictionary of {translatorName : [template instance]} for the given nodeType
    """
    # return a copy so it doesn't get messed with
    global _translatorTemplates
    return dict(_translatorTemplates[nodeType])

def getTranslatorTemplate(nodeType, translatorName):
    """
    Return an `AttributeTemplate` instance for the given nodeType and translator, or None if one has not been registered
    """
    try:
        cls = getTranslatorTemplates(nodeType)[translatorName]
        assert "translator UI must be AttributeTemplate sub class", issubclass(cls, AttributeTemplate)
        inst = cls(nodeType)
        
        # translator templates must be in child mode because multiple templates may reference the same attribute
        # something that editorTemplate (used by root mode) does not allow
        inst._setToChildMode()
        return inst
    except KeyError:
        pass

def getNodeTemplate(nodeType):
    """
    Return an `AttributeTemplate` instance for the given nodeType or None if one has not been registered.
    
    This is the root template for the node type. Unlike translator UIs, there can be only one template per node type.
    """
    global _templates
    try:
        # has one been explicitly registered?
        templateClass, nodeType, args, kwargs = _templates[nodeType]
    except KeyError:
        return
    else:
        return templateClass(nodeType, *args, **kwargs)

#-------------------------------------------------
# AE templates
#-------------------------------------------------

class BaseTemplate(object):
    """
    This class provides a simple framework for creating UIs.
    """
    def __init__(self, nodeType):
        self._nodeType = nodeType
        self._nodeName = None
        self._attr = None

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._nodeType)

    # queries
    @property
    def nodeName(self):
        "get the active node"
        # assert self._nodeName, "%r: nodeName should be set by now" % self
        return self._nodeName

    @property
    def attr(self):
        return self._attr

    def nodeType(self):
        if self._nodeType is None:
            self._nodeType = pm.objectType(self.nodeName)
        return self._nodeType

    def nodeAttr(self, attr=None):
        if attr is None:
            attr = self.attr
        return self.nodeName + '.' + attr

    def nodeAttrExists(self, attr):
        return pm.addAttr(self.nodeAttr(attr), q=True, ex=True)

def modeAttrMethod(func):
    def wrapped(self, attr, *args, **kwargs):
        assert isinstance(attr, basestring), "%r.%s: attr argument must be a string, got %s" % (self, func.__name__, type(attr).__name__)
        modefunc = getattr(self._mode, func.__name__)
        if self.convertToMayaStyle:
            attr = toMayaStyle(attr)
        if self._record:
            self._actions.append((modefunc, (attr,) + args, kwargs))
        else:
            modefunc(attr, *args, **kwargs)
        self._attributes.append(attr)
    wrapped.__doc__ = func.__doc__
    wrapped.__name__ = func.__name__
    wrapped._orig = func
    return wrapped

def modeMethod(func):
    def wrapped(self, *args, **kwargs):
        modefunc = getattr(self._mode, func.__name__)
        if self._record:
            self._actions.append((modefunc, args, kwargs))
        else:
            modefunc(*args, **kwargs)
    wrapped.__doc__ = func.__doc__
    wrapped.__name__ = func.__name__
    wrapped._orig = func
    return wrapped


class AttributeTemplate(BaseTemplate):
    """
    This class provides a framework for creating and managing Attribute Editor templates in python.

    When building Attribute Editor templates, there are major restrictions on what types of UI commands
    can be issued, depending on context:
        - editorTemplate commands may only be issued directly within the body of an Attribute Editor template
        - normal Maya UI commands may only be used in the context of the `editorTemplate -callCustom` callback
    The two types of commands must remain segregated.
    
    The goal of this class is to remove this complex distinction and provide a single unified, and 
    modular template class which may be used in either context, or even chained together. In most cases, the
    AE developer need not care what context their template class will be used in.

    The context-based functionality is implemented in AERootMode and AEChildMode.
    """
    convertToMayaStyle = False
    def __init__(self, nodeType):
        super(AttributeTemplate, self).__init__(nodeType)
        self._rootMode = AERootMode(self)
        self._childMode = AEChildMode(self)
        self._mode = self._rootMode
        self._actions = []
        self._attributes = []
        self._record = False

    def _setToRootMode(self):
        self._mode = self._rootMode

    def _isRootMode(self):
        return self._mode == self._rootMode

    def _setToChildMode(self):
        self._mode = self._childMode

    def _isChildMode(self):
        return self._mode == self._childMode

    def _setActiveNodeAttr(self, nodeName):
        "set the active node"
        parts = nodeName.split('.', 1)
        self._nodeName = parts[0]
        if len(parts) > 1:
            self._attr = parts[1]
            
    def _doSetup(self, nodeAttr):
        '''
        build the UI from the list of added attributes
        '''
        self._setActiveNodeAttr(nodeAttr)
        self._mode.preSetup()
        if self._record:
            for func, args, kwargs in self._actions:
                func(*args, **kwargs)
        else:
            self.setup()
        self._mode.postSetup()

    def _doUpdate(self, nodeAttr):
        self._setActiveNodeAttr(nodeAttr)
        self._mode.update()

    def setup(self):
        """
        this method should be overridden. it is called when the class is initialized. it is kept as a
        separate method to avoid the user coming into conflict with variables managed by this class
        """
        pass

    @modeMethod
    def update(self):
        pass

    @modeAttrMethod
    def addTemplate(self, attr, template):
        pass

    @modeAttrMethod
    def addChildTemplate(self, attr, template):
        pass

    @modeAttrMethod
    def addControl(self, attr, label=None, changeCommand=None, annotation=None,
                   preventOverride=False, dynamic=False, enumeratedItem=None):
        pass
        
            
    @modeMethod
    def suppress(self, attr):
        pass

    @modeMethod
    def addSeparator(self):
        pass

    @modeAttrMethod
    def addCustom(self, attr, createFunc, updateFunc):
        pass

    @modeMethod
    def beginLayout(self, label, **kwargs):
        '''
        begin a frameLayout.
        accepts any keyword args valid for creating a frameLayout
        '''
        pass

    @modeMethod
    def endLayout(self):
        '''
        end the current frameLayout
        '''
        pass

    @modeMethod
    def beginNoOptimize(self):
        pass

    @modeMethod
    def endNoOptimize(self):
        pass

    @modeMethod
    def beginScrollLayout(self):
        pass

    @modeMethod
    def endScrollLayout(self):
        pass

    @modeMethod
    def addExtraControls(self):
        pass

#-------------------------------------------------
# AE template Modes (internal)
#-------------------------------------------------

class BaseMode(object):
    def __init__(self, template):
        self.template = template

#    def __repr__(self):
#        return '%s(%r)' % (self.__class__.__name__, self.nodeType())

    # queries
    @property
    def nodeName(self):
        # get the active node
        # assert self._nodeName, "%r: nodeName should be set by now" % self
        return self.template.nodeName

    @property
    def attr(self):
        return self.template.attr

    def nodeType(self):
        self.template.nodeType()

    def nodeAttr(self, attr):
        return self.template.nodeAttr(attr)

    def nodeAttrExists(self, attr):
        return self.template.nodeAttrExists(attr)

class AEChildMode(BaseMode):
    """
    Interprets `AttributeEditor` actions as custom Maya UI code
    
    This mode is used for:
        - Partial AE Templates that are used with callCustom
    """
    def __init__(self, template):
        super(AEChildMode, self).__init__(template)
        self._controls = []
        self._layoutStack = []

    def preSetup(self):
        pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
        self._layoutStack = [pm.setParent(query=True)]

    def postSetup(self):        
        pm.setUITemplate(popTemplate=True)

    def update(self):
        pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)
        try:
            for attr, updateFunc, parent in self._controls:
                pm.setParent(parent)
                updateFunc(self.nodeAttr(attr))
        except:
            # print some useful info
            print("[mtoa] Template %r failed to update attribute '%s'" % (self.template, attr))
            # re-raise the last exception
            raise
        finally:
            pm.setUITemplate(popTemplate=True)

    def addTemplate(self, attr, template):
        self.addChildTemplate(attr, template)

    def addChildTemplate(self, attr, template):
        template._setToChildMode()
        template._record = True
        template.setup()
        for attr in template._attributes:
            try:
                pm.cmds.editorTemplate(suppress=attr)
            except RuntimeError:
                pass
        self.addCustom(attr, template._doSetup, template._doUpdate)

    def addControl(self, attr, label=None, changeCommand=None, annotation=None,
                   preventOverride=False, dynamic=False, enumeratedItem=None):
        # TODO: lookup label and descr from metadata
        if not label:
            label = prettify(attr)
            if label.startswith('Ai '):
                label = label[3:]
        kwargs = {}
        kwargs['label'] = label
        kwargs['attribute'] = self.nodeAttr(attr)
        if annotation:
            kwargs['annotation'] = annotation
        if changeCommand:
            kwargs['changeCommand'] = changeCommand
        if enumeratedItem:
            kwargs['enumeratedItem'] = enumeratedItem
        parent = self._layoutStack[-1]
        pm.setParent(parent)
        control = AttrControlGrp(**kwargs)
        self._controls.append((attr, control.setAttribute, parent))

    def addCustom(self, attr, createFunc, updateFunc):
        parent = self._layoutStack[-1]
        pm.setParent(parent)
        col = pm.cmds.columnLayout(adj=True)
        if not hasattr(createFunc, '__call__'):
            createFunc = getattr(pm.mel, createFunc)
        if not hasattr(updateFunc, '__call__'):
            updateFunc = getattr(pm.mel, updateFunc)
        createFunc(self.nodeAttr(attr))
        pm.setParent(parent)
        self._controls.append((attr, updateFunc, col))

    def addSeparator(self):
        pm.separator()

    def beginLayout(self, label, **kwargs):
        '''
        begin a frameLayout.
        accepts any keyword args valid for creating a frameLayout
        '''
        kwargs['label'] = label
        pm.setParent(self._layoutStack[-1])
        pm.frameLayout(**kwargs)
        self._layoutStack.append(pm.columnLayout(adjustableColumn=True))

    def endLayout(self):
        '''
        end the current frameLayout
        '''
        self._layoutStack.pop()
        pm.setParent(self._layoutStack[-1])

    # for compatibility with pymel.core.uitypes.AETemplate
    def beginNoOptimize(self):
        pass

    # for compatibility with pymel.core.uitypes.AETemplate
    def endNoOptimize(self):
        pass

    # for compatibility with pymel.core.uitypes.AETemplate
    def beginScrollLayout(self):
        pass

    # for compatibility with pymel.core.uitypes.AETemplate
    def endScrollLayout(self):
        pass

    # for compatibility with pymel.core.uitypes.AETemplate
    def addExtraControls(self):
        pass

class AERootMode(BaseMode):
    """
    Interprets `AttributeEditor` actions as editorTemplate commands.

    This mode is used for:
        - Full AE Node Templates
        - Partial AE Templates that are used inline (cannot be used with callCustom)
    """

    def __init__(self, template):
        super(AERootMode, self).__init__(template)
        self._attr = None
        # argument is a node type
        self._nodeName = None
        self._nodeType = self.template.nodeType()

    def _updateCallback(self, nodeAttr):
        self.template._doUpdate(nodeAttr.split('.')[0])

    def preSetup(self):
        self.addCustom('message', self._updateCallback, self._updateCallback)

    def postSetup(self):
        pass

    def update(self):
        pass

    def addTemplate(self, attr, template):
        if template._isRootMode():
            template._doSetup(self.nodeAttr(attr))
        else:
            self.addChildTemplate(attr, template)

    def addChildTemplate(self, attr, template):
        template._setToChildMode()
        template._record = True
        template.setup()
        for attr in template._attributes:
            try:
                pm.cmds.editorTemplate(suppress=attr)
            except RuntimeError:
                pass
        pm.cmds.editorTemplate(aeCallback(template._doSetup),
                          aeCallback(template._doUpdate),
                          attr,
                          callCustom=True)

    def addControl(self, attr, label=None, changeCommand=None, annotation=None,
                   preventOverride=False, dynamic=False, enumeratedItem=None):
        if not label:
            label = prettify(attr)
            if label.startswith('Ai '):
                label = label[3:]
        args = [attr]
        kwargs = {}
#        kwargs['preventOverride'] = preventOverride
        if dynamic:
            kwargs['addDynamicControl'] = True
        else:
            kwargs['addControl'] = True        
        if changeCommand:
            if hasattr(changeCommand, '__call__'):
                changeCommand = aeCallback(changeCommand)
            args.append(changeCommand)
        if label:
            kwargs['label'] = label
        if annotation:
            kwargs['annotation'] = annotation
        pm.cmds.editorTemplate(*args, **kwargs)
        
    def suppress(self, attr):
        pm.cmds.editorTemplate(suppress=attr)

    def addCustom(self, attr, newFunc, replaceFunc):
        # TODO: support multiple attributes passed
        if hasattr(newFunc, '__call__'):
            newFunc = aeCallback(newFunc)
        if hasattr(replaceFunc, '__call__'):
            replaceFunc = aeCallback(replaceFunc)
        args = (newFunc, replaceFunc, attr) 
        pm.cmds.editorTemplate(callCustom=1, *args)

    def addSeparator(self):
        pm.cmds.editorTemplate(addSeparator=True)

    def suppress(self, control):
        pm.cmds.editorTemplate(suppress=control)

    def dimControl(self, nodeName, control, state):
        pm.cmds.editorTemplate(dimControl=(nodeName, control, state))

    def beginLayout(self, name, collapse=True):
        pm.cmds.editorTemplate(beginLayout=name, collapse=collapse)

    def endLayout(self):
        pm.cmds.editorTemplate(endLayout=True)

    def beginScrollLayout(self):
        pm.cmds.editorTemplate(beginScrollLayout=True)

    def endScrollLayout(self):
        pm.cmds.editorTemplate(endScrollLayout=True)

    def beginNoOptimize(self):
        pm.cmds.editorTemplate(beginNoOptimize=True)

    def endNoOptimize(self):
        pm.cmds.editorTemplate(endNoOptimize=True)

    def interruptOptimize(self):
        pm.cmds.editorTemplate(interruptOptimize=True)

    def addComponents(self):
        pm.cmds.editorTemplate(addComponents=True)

    def addExtraControls(self, label=None):
        kwargs = {}
        if label:
            kwargs['extraControlsLabel'] = label
        pm.cmds.editorTemplate(addExtraControls=True, **kwargs)

class ShapeMixin(object):
    def renderStatsAttributes(self):
        self.addControl("castsShadows")
        self.addControl("receiveShadows")
        self.addControl("primaryVisibility")
        self.addControl("visibleInReflections")
        self.addControl("visibleInRefractions")

    def commonShapeAttributes(self):
        self.addControl("aiSelfShadows", label="Self Shadows")
        self.addControl("aiOpaque", label="Opaque")
        self.addControl("aiVisibleInDiffuse", label="Visible In Diffuse")
        self.addControl("aiVisibleInGlossy", label="Visible In Glossy")
        self.addControl("aiMatte", label="Matte")
        self.addControl("aiTraceSets", label="Trace Sets")

class ShapeTranslatorTemplate(AttributeTemplate, ShapeMixin):
    pass

class AutoTranslatorTemplate(AttributeTemplate):
    '''
    A translator template which automatically builds itself based on data queried from
    an arnold node type
    
    It is highly recommended that you use the utility function `registerAutoTranslatorUI()`
    to create a template of this type
    '''
    _arnoldNodeType = None
    _attribData = None
    def setup(self):
        """
        default setup automatically builds a UI based on metadata
        """
        if self.__class__._attribData is None:
            self.__class__._attribData = core.getAttributeData(self._arnoldNodeType)
        for paramName, attrName, label, annotation in self._attribData:
            self.addControl(attrName,
                            label if label else prettify(paramName),
                            annotation)

class TranslatorControl(AttributeTemplate):
    '''
    Allows multiple AttributeTemplates, each representing an arnold translator, to be controlled via
    one optionMenu, such that only the active template is visible.
    
    A default `TranslatorControl` is automatically created for each node that registers an arnold
    translator UIs via `registerTranslatorUI`. Manually creating a `TranslatorControl` is only necessary if you
    need to customize the default controller behavior.
    
    Note that changing the visibility of an AE control is not possible with a normal AE template, but considering
    the number of translators that may be available on one node, it is a requirement for mtoa to avoid unruly
    AE templates.  Additionally, translators may share attributes, but AE templates do not allow the same control
    to be repeated. This class performs some UI wizardry to pull off these features.
    '''
    def __init__(self, nodeType, label='Arnold Translator', optionMenuName=None):
        super(TranslatorControl, self).__init__(nodeType)
        self._optionMenu = optionMenuName if optionMenuName is not None else (nodeType + '_aiTranslatorOMG')
        self._translators = None
        self._label = label

    #---- translator methods

    def nodeType(self):
        return self._nodeType

    def getCurrentTranslator(self, nodeName):
        """
        get the current translator for this node, querying and setting the default if not yet set
        """
        try :
            # asString allows for enum attributes as well
            transName = pm.getAttr(nodeName + ".aiTranslator", asString=True)
        except :
            transName = None
        translators = self.getTranslators()
        if not transName or transName not in translators:
            # set default
            transName = getDefaultTranslator(nodeName)
            if transName is None:
                if not translators:
                    pm.warning("cannot find default translator for %s" % nodeName)
                    return
                transName = translators[0]
            try :
                pm.setAttr(nodeName + ".aiTranslator", transName)
            except:
                pm.warning("cannot set default translator for %s" % nodeName)
                import traceback
                traceback.print_exc()
        return transName

    def updateChildrenCallback(self, attr):
        """
        this function is assigned to an AE refresh callback. this allows us to call updateChildren
        to set things up.
        """
        # attr should be aiTranslator. do we need to split?
        nodeName = attr.split('.')[0]
        self.updateChildren(nodeName, pm.getAttr(nodeName + ".aiTranslator", asString=True))

    def updateChildren(self, nodeName, currentTranslator):
        """
        update the translator UI, which consists of an optionMenuGrp and a frameLayout per translator,
        so that only the frameLayout corresponding to the currently selected translator is visible
        """
        if not pm.layout(self._optionMenu, exists=True):
            # not built yet
            return
        fullpath = pm.layout(self._optionMenu, query=True, fullPathName=True)
        # get the grand-parent columnLayout
        gparent = fullpath.rsplit('|', 2)[0]
        # get the great-grand parent frame layout
        frame = fullpath.rsplit('|', 3)[0]
        try:
            pm.frameLayout(frame, edit=True, collapsable=False, labelVisible=False, borderVisible=False)
        except RuntimeError:
            # this is a little dirty: it will only succeed when attaching to AE
            pass

        children = pm.layout(gparent, query=True, childArray=True)
        # hide all frameLayouts but ours
        assert currentTranslator, "we should have a translator set by now"

        for child in children:
            # is it a frame layout?
            objType = pm.objectTypeUI(child)
            if objType == 'frameLayout':
                label = pm.frameLayout(child, query=True, label=True)
                # turn collapsable and label off
                if showAllTranslators:
                    pm.frameLayout(child, edit=True, collapsable=False, labelVisible=True,
                                     visible=True)
                else:
                    pm.frameLayout(child, edit=True, collapsable=False, labelVisible=False,
                                     visible=(label == currentTranslator))
        # FIXME: this needs a check for read-only nodes from referenced files. also, not sure
        # changing attribute properties is the best approach
        #AttributeTemplate.syncChannelBox(nodeName, nodeType, currentTranslator)

    def attributeChanged(self, nodeName, attr, *args):
        """
        called when the translator attribute is changed
        """
        transName = pm.getAttr(attr)
        pm.optionMenuGrp(self._optionMenu, edit=True, value=transName)
        self.updateChildren(nodeName, transName)

    def menuChanged(self, nodeName, currentTranslator):
        """
        called when the translator optionMenuGrp (aiTranslatorOMG) changes
        """
        # this setAttr triggers attributeChanged to call updateChildren
        pm.setAttr(nodeName + ".aiTranslator", currentTranslator)

    def createMenu(self, nodeName):
        """
        called to create an optionMenuGrp for choosing between multiple translator options for a given node
        """
        self._optionMenu = pm.optionMenuGrp(self._optionMenu, label=self._label,
                                             cc=lambda *args: self.menuChanged(nodeName, args[0]))
        # create menu items
        for tran in self.getTranslators():
            pm.menuItem(label=tran)
        pm.setParent(menu=True)

        transName = self.getCurrentTranslator(nodeName)
        pm.optionMenuGrp(self._optionMenu, edit=True, value=transName)

        transAttr = nodeName + ".aiTranslator"
        pm.scriptJob(attributeChange=[transAttr, lambda *args: self.attributeChanged(nodeName, transAttr, *args)],
                     replacePrevious=True,
                     parent=self._optionMenu)

    def updateMenu(self, nodeName):
        """
        called to update an optionMenuGrp for choosing between multiple translator options for a given node
        """
        # delete current options
        translators = pm.optionMenuGrp(self._optionMenu, q=True, itemListLong=True)
        for tran in translators:
            pm.deleteUI(tran, menuItem=True)

        # populate with a fresh list
        parent = pm.setParent(self._optionMenu)
        for tran in self._translators:
            pm.menuItem(label=tran, parent=parent + '|OptionMenu')

        transName = self.getCurrentTranslator(nodeName)
        pm.optionMenuGrp(self._optionMenu, edit=True, value=transName,
                           cc=lambda *args: self.menuChanged(nodeName, args[0]))
        self.updateChildren(nodeName, transName)

        transAttr = nodeName + ".aiTranslator"
        pm.scriptJob(attributeChange=[transAttr, lambda *args: self.attributeChanged(nodeName, transAttr, *args)],
                     replacePrevious=True,
                     parent=self._optionMenu)

    def getTranslators(self):
        if self._translators is None:
            self._translators = getTranslators(self.nodeType())
        return self._translators

    def getTranslatorTemplates(self):
        return filter(lambda x: bool(x[1]),
                      [(translator, getTranslatorTemplate(self.nodeType(), translator)) \
                        for translator in self.getTranslators()])

    def setup(self):
        translators = self.getTranslators()
        if translators:
            if len(translators) > 1:
                self.beginLayout('hide', collapse=False)
                # if there is more than one translator, we group each in its own layout
                # create the menu for selecting the translator
                self.addCustom("aiTranslator",
                               aeCallback(lambda attr: self.createMenu(attr.split('.')[0])),
                               aeCallback(lambda attr: self.updateMenu(attr.split('.')[0])))

                for translator, template in self.getTranslatorTemplates():
                    # we always create a layout, even if it's empty
                    self.beginLayout(translator, collapse=False)
                    self.addChildTemplate('message', template)
                    self.endLayout()
                self.endLayout()
                # timing on AE's is difficult: the frameLayouts are not created at this point even though
                # the `editorTemplate -beginLayout` calls have been made. this is a little hack
                # to ensure we get a callback after the AE ui elements have been built: normal controls can get
                # an update callback, but we don't have any normal controls around, so we'll have to make one and
                # hide it
                self.addCustom('message',
                               aeCallback(self.updateChildrenCallback),
                               aeCallback(self.updateChildrenCallback))
            else:
                translator, template = self.getTranslatorTemplates()[0]
                self.addChildTemplate('message', template)

#-------------------------------------------------
# Registration
#-------------------------------------------------

def registerAETemplate(templateClass, nodeType, *args, **kwargs):
    """
    Register an `AttributeTemplate` class to be used with the given nodeType.
    
    This is the root template for the node type. Unlike translator UIs, there can be only one template per node type.
    """
    assert inspect.isclass(templateClass) and issubclass(templateClass, AttributeTemplate), \
        "you must pass a subclass of AttributeTemplate"
    global _templates
    if nodeType not in _templates:
        try:
            _templates[nodeType] = (templateClass, nodeType, args, kwargs)
            arnold.AiMsgDebug("registered attribute template for %s" % nodeType)
        except:
            arnold.AiMsgError("Failed to instantiate AE Template %s" % templateClass)
            import traceback
            traceback.print_exc()

def aeTemplate(nodeType, baseClass=AttributeTemplate):
    """
    decorator to convert a simple UI function into an AttributeTemplate class.
    """
    def registerUIDecorator(func):
        cls = type(nodeType + "Template", (baseClass,), dict(setup=func))
        registerAETemplate(cls, nodeType)
        # return function unchanged
        return func
    return registerUIDecorator

def registerTranslatorUI(templateClass, mayaNodeType, translatorName='<built-in>'):
    """
    A translator UI is a specialized `AttributeTemplate` subclass that is associated with a specific mtoa translator. 
    
    Every node type can have multiple translators. Each translator UI class is responsible for creating the UI for
    a single translator. For example, the camera node registers a separate `AttributeTemplate`
    for each of its various translators:  perspective, orthographic, spherical, fisheye, etc.
    """
    global _translatorTemplates
    translators = getTranslators(mayaNodeType)
    if translatorName not in translators:
        if translators:
            pm.warning('[mtoa] Registering UI for unknown translator "%s" for Maya node %s. Valid choices are: %s' % \
                   (translatorName, mayaNodeType, ', '.join(['"%s"' % x for x in translators])))
        else:
            pm.warning('[mtoa] Registering UI for translator "%s" for Maya node %s, but node has no translators. Did you mean to call registerAETemplate?' % \
                   (translatorName, mayaNodeType))
    assert inspect.isclass(templateClass) and issubclass(templateClass, AttributeTemplate),\
        "you must pass a subclass of AttributeTemplate"
    _translatorTemplates[mayaNodeType][translatorName] = templateClass

    registerAETemplate(TranslatorControl, mayaNodeType)

def registerAutoTranslatorUI(arnoldNode, mayaNodeType, translatorName='<built-in>', skipEmpty=False):
    """
    Utility function for automatically creating a translator UI template based on an arnold
    node type.
    """
    translatorName = str(translatorName) # doesn't like unicode
    # we query the attribute data up front instead of when the translator is initialized or setup
    # so that it is done when mtoa.cmds.registerArnoldRenderer is first  called and the Arnold
    # universe is already active. otherwise, successive calls to core.getAttributeData later on cause
    # the Arnold universe to repeatedly begin and end.
    attribs = core.getAttributeData(arnoldNode)
    if skipEmpty and not attribs:
        return
    cls = type('%s_%sTemplate' % (mayaNodeType, translatorName),
               (AutoTranslatorTemplate,),
               dict(_arnoldNodeType=arnoldNode,
                    _attribData = attribs))
    registerTranslatorUI(cls, mayaNodeType, translatorName)

# FIXME: should we just get rid of this?
def translatorUI(nodeType, translatorName='<built-in>', baseClass=AttributeTemplate):
    """
    Decorator for registering a function for creating a simple translator UI. 
    
    Normally an AttributeTemplate sub-class
    would be created manually, but for simple UIs that require only one function, this decorator can reduce the boiler-plate
    class code.  The function that it is applied to should be written to receive an AttributeTemplate instance, which it should
    use to make calls to addControl, addSeparator, addCustom, etc.
    """
    def registerUIDecorator(func):
        cls = type(nodeType + "_TransTemplate", (baseClass,), dict(setup=func))
        registerTranslatorUI(cls, nodeType, translatorName)
        # return function unchanged
        return func
    return registerUIDecorator

def createTranslatorMenu(node, label=None, nodeType=None, default=None, optionMenuName=None):
    '''
    convenience function for creating a TranslatorControl and attaching it to a non-AE UI
    '''
    if nodeType is None:
        nodeType = pm.nodeType(node)
    kwargs = {}
    if label is not None:
        kwargs['label'] = label
    if optionMenuName:
        kwargs['optionMenuName'] = optionMenuName
    if default:
        registerDefaultTranslator(nodeType, default)
    trans = TranslatorControl(nodeType, **kwargs)
    trans._setToChildMode()
    trans._doSetup(node + '.aiTranslator')
    return trans

#----------------------------------------------------------------
# functions used internally for loading templates
#----------------------------------------------------------------

def shapeTemplate(nodeName):
    """
    override for the builtin maya shapeTemplate procedure
    """
    # Run the hooks.
    # see mtoa.registerArnoldRenderer._addAEHooks for where loadArnoldTemplate gets added to AEshapeHooks.
    # note that this is not called in 2013: loadArnoldTemplate is called for both depend and DAG nodes 
    for hook in pm.melGlobals['AEshapeHooks']:
        pm.mel.eval(hook + ' "' + nodeName + '"')

    pm.cmds.editorTemplate(beginLayout=pm.mel.uiRes("m_AEshapeTemplate.kObjectDisplay"))

    # include/call base class/node attributes
    pm.mel.AEdagNodeCommon(nodeName)
    pm.cmds.editorTemplate(endLayout=True)

    # include/call base class/node attributes
    pm.mel.AEdagNodeInclude(nodeName)

def loadArnoldTemplate(nodeName):
    """
    Create the "Arnold" AE template for the passed node
    """
    global _templates
    nodeType = pm.objectType(nodeName)

    # skip nodes that were created by mtoa, these should not generate an "Arnold" section.
    # this is here mostly for versions > 2013, because the new hook system causes this function to be
    # called for every AE
    if core.isMtoaNode(nodeType):
        return

    template = getNodeTemplate(nodeType)
    if template:
        pm.cmds.editorTemplate(beginLayout='Arnold', collapse=True)
        template._doSetup(nodeName)
        if hasattr(template, '_attributes'):
            for attr in template._attributes:
                pm.cmds.editorTemplate(suppress=attr)
        pm.cmds.editorTemplate(endLayout=True)
