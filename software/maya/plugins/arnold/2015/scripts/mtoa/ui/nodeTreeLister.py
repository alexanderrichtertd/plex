"""
add arnold nodes to maya's node tree lister

Before 2013 there are several options for getting callbacks for adding our own nodes, but because autodesk gives Mayatomr specail
treatment it is very hard for 3rd party renderers to properly integrate.
 
options:
  - use the renderNodeTreeInitializeUserProc optionVar: could be displaced at any time by a custom script or another renderer.
  - override buildRenderNodeTreeListerContent: difficult to maintain as it changes between versions
  - override the functions that call buildRenderNodeTreeListerContent: best option

"""
import mtoa.utils as utils
import pymel.core as pm
from mtoa.core import _processClass, createArnoldNode, isSubClassification
from mtoa.callbacks import *
from collections import namedtuple


# known categories: used for ordering in the UI
# define a named tuple class, which acts like a struct, with index or attribute access
NodeClassInfo = namedtuple('NodeClassInfo',
                           ['staticClassification',
                            'runtimeClassification',
                            'nodePath',
                            'nodeTypes'])
CATEGORIES = ('shader', 'texture', 'light', 'utility')

global _typeInfoMap
_typeInfoMap = ()

def isClassified(node, klass):
    nodeType = pm.nodeType(node)
    return klass in pm.getClassification(nodeType)

def getTypeInfo():
    '''
    return a tuple of NodeClassInfo namedtuples containing 
    (staticClassification, runtimeClassifciation, nodePath, nodeTypes)
    '''
    global _typeInfoMap
    if not _typeInfoMap :
        # use a dictionary to get groupings
        tmpmap = {}
        nodeTypes = []
        for cat in CATEGORIES:
            catTypes = pm.listNodeTypes('rendernode/arnold/' + cat)
            if catTypes :
                nodeTypes.extend(catTypes)
        if nodeTypes:
            for nodeType in nodeTypes:
                (staticClass, runtimeClass, nodePath) = _processClass(nodeType)
                if staticClass is not None :
                    if staticClass not in tmpmap:
                        tmpmap[staticClass] = [runtimeClass, nodePath, [nodeType]]
                    else:
                        tmpmap[staticClass][2].append(nodeType)
        # consistent order is important for UIs. build a reliably ordered list. 
        tmplist = []
        # known types first.
        for cat in CATEGORIES:
            cat = 'rendernode/arnold/' + cat
            if cat in tmpmap:
                values = tmpmap.pop(cat)
                tmplist.append(NodeClassInfo(*([cat] + values)))
        # custom types in alphabetical order
        for custom in sorted(tmpmap.keys()):
            tmplist.append(NodeClassInfo(*([custom] + tmpmap[custom])))
        _typeInfoMap = tuple(tmplist)
    return _typeInfoMap

def createArnoldNodesTreeLister_Content(renderNodeTreeLister, postCommand, filterString):
    filters = filterString.split()
    for (staticClass, runtimeClass, nodePath, nodeTypes) in getTypeInfo():
        if not filters or any([isSubClassification(staticClass, filter) for filter in filters]):
            for nodeType in nodeTypes:
                command = Callback(createNodeCallback, runtimeClass, postCommand, nodeType)
                import maya.app.general.tlfavorites as _fav
                _fav.addPath(nodePath + '/' + nodeType, nodeType)
                pm.nodeTreeLister(renderNodeTreeLister, e=True, add=[nodePath + '/' + nodeType, "render_%s.png" % nodeType, command])
                del _fav


def aiHyperShadeCreateMenu_BuildMenu():
    """
    Function:   aiHyperShadeCreateMenu_BuildMenu()
    Purpose:    Builds menu items for creating arnold nodes, organized
                into submenus by category.

    Notes:  When this function is invoked, it is inside of the Create menu.
            This function mimics the buildCreateSubmenu() function in 
            hyperShadePanel.mel, and in fact calls that function with a slightly
            different set of arguments than the other Maya node types.  For 
            arnold nodes, the menu items are set up to call back to the
            aiCreateCustomNode() function for node creation.
    """

    # build a submenu for each node category
    #
    for (staticClass, runtimeClass, nodePath, nodeTypes) in getTypeInfo():
        # skip unclassified
        if staticClass == 'rendernode/arnold' or staticClass == 'rendernode/arnold/shader':
            continue
        pm.menuItem(label = nodePath.replace('/', ' '), 
                      tearOff = True, subMenu = True)
        
        # call buildCreateSubMenu() to create the menu entries.  The specified 
        # creation command is aiCreateCustomNode runtimeClassification.  The
        # buildCreateSubMenu will append to that argument list the name of the
        # node type, thereby completing the correct argument list for the 
        # creation routine.
        #
        pm.mel.buildCreateSubMenu(staticClass, '%s %s ""' % (_createNodeCallbackProc,
                                                             runtimeClass) )
        pm.setParent('..', menu=True)

def createNodeCallback(runtimeClassification, postCommand, nodeType):

    node = unicode(createArnoldNode(nodeType, runtimeClassification=runtimeClassification))
    if postCommand:
        postCommand = postCommand.replace('%node', node).replace('%type', nodeType).replace(r'\"','"')
        pm.mel.eval(postCommand)
    return node

_createNodeCallbackProc = utils.pyToMelProc(createNodeCallback, 
                                            [('string', 'runtimeClassification'),
                                             ('string', 'postCommand'),
                                             ('string', 'nodeType')],
                                             returnType='string')

# names of the following procs mirror mental ray naming convention, so the inconsistency is not ours

# make the global proc available for the renderCReateBarUI.mel override
utils.pyToMelProc(createArnoldNodesTreeLister_Content,
                                       [('string', 'renderNodeTreeLister'),
                                        ('string', 'postCommand'),
                                        ('string', 'filterString')], useName=True)

# make the global proc available for the hyperShadePanel.mel override
utils.pyToMelProc(aiHyperShadeCreateMenu_BuildMenu, useName=True)

