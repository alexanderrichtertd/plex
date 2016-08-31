import pymel.core as pm
import mtoa.utils as utils
import mtoa.ui.ae

import os
import pkgutil
import re
import sys
import inspect

def arnoldGetDimValue(node, attr):

    fullAttr = '%s.%s'%(node, attr)
    value = pm.getAttr(fullAttr)
    return value

# Dims target control if source attribute is true.
def arnoldDimControlIfTrue(node, target, source):
    dim = arnoldGetDimValue(node, source)
    pm.editorTemplate(dimControl=(node, target, dim))

# Dims target control if source attribute is false.
def arnoldDimControlIfFalse(node, target, source):
    dim = not arnoldGetDimValue(node, source)
    pm.editorTemplate(dimControl=(node, target, dim))

def getNodeType(name):
    nodeType = pm.nodeType(name)
    lights = ["directionalLight",
                "pointLight",
                "spotLight",
                "areaLight"]

    if nodeType in lights:
        nodeType = 'light'

    return nodeType

def attributeExists(attribute, nodeName):
    return pm.attributeQuery(attribute, node=nodeName, exists=True)


def loadAETemplates():
    templates = []
    customTemplatePaths = []
    
    if (os.getenv('MTOA_TEMPLATES_PATH')):
        import sys
        customTemplatePaths = os.getenv('MTOA_TEMPLATES_PATH').split(os.pathsep)
        sys.path += customTemplatePaths
        
    pathsList = mtoa.ui.ae.__path__ + customTemplatePaths
    
    for importer, modname, ispkg in pkgutil.iter_modules(pathsList):
        # module name must end in "Template"
        if modname.endswith('Template') and modname not in templates:
            # TODO: use importer?
            try:
                mod = __import__(modname, globals(), locals(), [], -1)
            
                procName = 'AE%s' % modname
                if hasattr(mod, modname):
                    # a function named after the module
                    templates.append(modname)
                    _makeAEProc(modname, modname, procName)
                elif hasattr(mod, procName):
                    # a class named AEmodname
                    templates.append(modname)
                    _makeAEProc(modname, procName, procName)
            except:
                print '[MtoA] Error parsing AETemplate file %s' % str(modname)
                import traceback
                print traceback.format_exc()

def aeCallback(func):
    return utils.pyToMelProc(func, [('string', 'nodeName')], procPrefix='AEArnoldCallback')

def _makeAEProc(modname, objname, procname):
    contents = '''global proc %(procname)s( string $nodeName ){
    python("import %(__name__)s;%(__name__)s._aeLoader('%(modname)s','%(objname)s','" + $nodeName + "')");}'''
    d = locals().copy()
    d['__name__'] = __name__
    pm.mel.eval( contents % d )

def _aeLoader(modname, objname, nodename):
    mod = __import__(modname, globals(), locals(), [objname], -1)
    try:
        f = getattr(mod, objname)
        if inspect.isfunction(f):
            f(nodename)
        elif inspect.isclass(f):
            inst = f(pm.nodeType(nodename))
            inst._doSetup(nodename)
        else:
            print "AE object %s has invalid type %s" % (f, type(f))
    except Exception:
        print "failed to load python attribute editor template '%s.%s'" % (modname, objname)
        import traceback
        traceback.print_exc()

def interToUI(label):
    label = re.sub('([a-z])([A-Z])', r'\1 \2', label.replace('_', ' '))
    label = re.sub('(\s[a-z])|(^[a-z])', lambda m: m.group().upper(), label)
    return label

def attrType(attr):
    type = pm.getAttr(attr, type=True)
    if type == 'float3':
        node, at = attr.split('.', 1)
        if pm.attributeQuery(at, node=node, usedAsColor=1):
            type = 'color'
    return type

def rebuildAE():
    "completely rebuild the attribute editor"
    edForm = pm.melGlobals['gAttributeEditorForm']
    if pm.layout(edForm, q=True, exists=True):
        children = pm.layout(edForm, q=True, childArray=True)
        if children:
            pm.deleteUI(children[0])
            pm.mel.attributeEditorVisibilityStateChange(1, "")

def attrTextFieldGrp(*args, **kwargs):
    """
    There is a bug with attrControlGrp and string attributes where it ignores
    any attempt to edit the current attribute.  So, we have to write our own
    replacement
    """
    attribute = kwargs.pop('attribute', kwargs.pop('a', None))
    assert attribute is not None, "You must passed an attribute"
    changeCommand = kwargs.pop('changeCommand', kwargs.pop('cc', None))
    if changeCommand:
        def cc(newVal):
            pm.setAttr(attribute, newVal)
            changeCommand(newVal)
    else:
        cc = lambda newVal: pm.setAttr(attribute, newVal)

    if kwargs.pop('edit', kwargs.pop('e', False)):
        ctrl = args[0]
        pm.textFieldGrp(ctrl, edit=True,
                    text=pm.getAttr(attribute),
                    changeCommand=cc)
        pm.scriptJob(parent=ctrl,
                     replacePrevious=True,
                     attributeChange=[attribute,
                                      lambda: pm.textFieldGrp(ctrl, edit=True,
                                                              text=pm.getAttr(attribute))])
    elif kwargs.pop('query', kwargs.pop('q', False)):
        # query
        pass
    else:
        # create
        labelText = kwargs.pop('label', None)
        if not labelText:
            labelText = pm.mel.interToUI(attribute.split('.')[-1])
        ctrl = None
        if len(args) > 0:
            ctrl = args[0]
            pm.textFieldGrp(ctrl,
                            label=labelText,
                            text=pm.getAttr(attribute),
                            changeCommand=cc)
        else:
            ctrl = pm.textFieldGrp(label=labelText,
                                   text=pm.getAttr(attribute),
                                   changeCommand=cc)
        pm.scriptJob(parent=ctrl,
                     attributeChange=[attribute,
                                      lambda: pm.textFieldGrp(ctrl, edit=True,
                                                              text=pm.getAttr(attribute))])
        return ctrl

def attrBoolControlGrp(*args, **kwargs):
    attribute = kwargs.pop('attribute', kwargs.pop('a', None))
    assert attribute is not None, "You must passed an attribute"
    changeCommand = kwargs.pop('changeCommand', kwargs.pop('cc', None))
    if changeCommand:
        def cc(newVal):
            pm.setAttr(attribute, newVal)
            changeCommand(newVal)
    else:
        cc = lambda newVal: pm.setAttr(attribute, newVal)

    if kwargs.pop('edit', kwargs.pop('e', False)):
        ctrl = args[0]
        pm.checkBox(ctrl, edit=True,
                    value=pm.getAttr(attribute),
                    changeCommand=cc)
        pm.scriptJob(parent=ctrl,
                     replacePrevious=True,
                     attributeChange=[attribute,
                                      lambda: pm.checkBox(ctrl, edit=True, value=pm.getAttr(attribute))])
    elif kwargs.pop('query', kwargs.pop('q', False)):
        # query
        pass
    else:
        # create
        labelText = kwargs.pop('label', None)
        if not labelText:
            labelText = pm.mel.interToUI(attribute.split('.')[-1])
        ctrl = args[0]
        pm.rowLayout(numberOfColumns=1, columnWidth1=285, columnAttach1='right')
        pm.checkBox(ctrl, label=labelText,
                    value=pm.getAttr(attribute),
                    changeCommand=cc)
        pm.setParent('..')
        pm.scriptJob(parent=ctrl,
                     attributeChange=[attribute,
                     lambda: pm.checkBox(ctrl, edit=True, value=pm.getAttr(attribute))])
        return ctrl

class AttrControlGrp(object):
    UI_TYPES = {
        'float':  pm.cmds.attrFieldSliderGrp,
        'float2': pm.cmds.attrFieldGrp,
        'float3': pm.cmds.attrFieldGrp,
        'color':  pm.cmds.attrColorSliderGrp,
        'bool':   pm.cmds.attrControlGrp,
        'long':   pm.cmds.attrFieldSliderGrp,
        'byte':   pm.cmds.attrFieldSliderGrp,
        'long2':  pm.cmds.attrFieldGrp,
        'long3':  pm.cmds.attrFieldGrp,
        'short':  pm.cmds.attrFieldSliderGrp,
        'short2': pm.cmds.attrFieldGrp,
        'short3': pm.cmds.attrFieldGrp,
        'enum':   pm.cmds.attrEnumOptionMenuGrp,
        'double': pm.cmds.attrFieldSliderGrp,
        'double2':pm.cmds.attrFieldGrp,
        'double3':pm.cmds.attrFieldGrp,
        'string': attrTextFieldGrp,
        'message':pm.cmds.attrNavigationControlGrp
    }
    def __init__(self, attribute, *args, **kwargs):
        self.attribute = attribute
        self.type = kwargs.pop('type', kwargs.pop('typ', None))
        if not self.type:
            self.type = attrType(self.attribute)

        if self.type in ['color', 'enum', 'message']:
            self.callback = kwargs.pop('changeCommand', None)
        else:
            self.callback = None
        kwargs['attribute'] = self.attribute
        if self.type not in self.UI_TYPES:
            return
        cmd = self.UI_TYPES[self.type]
        try:
            self.control = cmd(*args, **kwargs)
        except RuntimeError:
            print "Error creating %s:" % cmd.__name__
            raise
        if self.callback:
            pm.scriptJob(attributeChange=[self.attribute, self.callback],
                         replacePrevious=True, parent=self.control)

    def edit(self, **kwargs):
        kwargs['edit'] = True
        if self.type not in self.UI_TYPES:
            return
        self.UI_TYPES[self.type](self.control, **kwargs)

    def setAttribute(self, attribute):
        self.attribute = attribute
        if self.type not in self.UI_TYPES:
            return
        self.UI_TYPES[self.type](self.control, edit=True, attribute=self.attribute)
        if self.callback:
            pm.scriptJob(attributeChange=[self.attribute, self.callback],
                         replacePrevious=True, parent=self.control)
