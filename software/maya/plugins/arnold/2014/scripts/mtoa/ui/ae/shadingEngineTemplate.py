import pymel.core as pm
import maya.cmds as cmds
import mtoa.aovs as aovs
import mtoa.ui.ae.templates as templates
import mtoa.ui.ae.shaderTemplate as shaderTemplate
import mtoa.ui.aoveditor as aoveditor
from collections import defaultdict

#------------------------------------------
# Shading Group
#------------------------------------------

def getAOVsInNetwork(rootNode):
    '''
    returns a map from PyNode to aovs
    
    the aov list contains all registered aovs for that node type, regardless of whether
    they are currently enabled in the globals 
    '''
    results = {}
    for node in pm.listHistory(rootNode, pruneDagObjects=True):
        # TODO: Create a general method to assign AOVs of hidden nodes
        # lambert shader has only translator registered so this is a Lambert Maya node and does not have an AOV tab
        if pm.nodeType(node) == "lambert":
            results[node] = [u'direct_diffuse', u'indirect_diffuse']
        else:
            # TODO: cache this result
            results[node] = [node.attr(at).get() for (aov, at, type) in aovs.getNodeGlobalAOVData(node.type())]
    return results

class ShadingEngineTemplate(templates.AttributeTemplate):
    def __init__(self, nodeType):
        self._msgCtrls = []
        aovs.addAOVChangedCallback(self.update, 'ShadingEngineTemplate')
        self.networkCol = None
        self.otherCol = None

        # populated by updateNetworkData()
        self.networkData = {} # mapping from node -> aov list
        self.networkAOVs = set([]) # set of all possible aovs in network, regardless of whether they are active
        self.networkNodeTypes = set([]) # set of node types in the shading network 
        self.aovNodes = {} # reverse lookup to networkData:  aovName -> node list
        
        # populated by updateCustomArrayData()
        self.nameToAttr = {} # mapping from aov name to element plug on aiCustomAOVs 
        self.arrayIndices = set([])  # set of all indices used by aiCustomAOVs
        self.orphanedAOVs = set([]) # set of aov names that appear in aiCustomAOVs that are not in the globals

        super(ShadingEngineTemplate, self).__init__(nodeType)
        
    def surfaceShaderCreate(self, attrName):
        cmds.columnLayout()
        cmds.attrNavigationControlGrp("ShadingEngineSurfaceShader", label = "Surface Shader",
                            attribute=attrName)
        cmds.setParent('..')
        
    def surfaceShaderUpdate(self, attrName):
        cmds.attrNavigationControlGrp("ShadingEngineSurfaceShader", edit=True, attribute=attrName)

    def volumeShaderCreate(self, attrName):
        cmds.columnLayout()
        cmds.attrNavigationControlGrp('ShadingEngineVolumeShader', label = 'Volume Shader',
                                     attribute=attrName)
        cmds.setParent('..')

    def volumeShaderUpdate(self, attrName):
        cmds.attrNavigationControlGrp('ShadingEngineVolumeShader', edit=True, attribute=attrName)

    def setup(self):
        self.addCustom("aiSurfaceShader", self.surfaceShaderCreate, self.surfaceShaderUpdate)
        self.addCustom("aiVolumeShader", self.volumeShaderCreate, self.volumeShaderUpdate)
        self.addCustom("aiCustomAOVs", self.buildAOVFrame, self.updateAOVFrame)

    def update(self):
        if self.nodeName is None or not pm.objExists(self.nodeName) \
            or self.networkCol is None or not pm.layout(self.networkCol, exists=True):
            return

        nodeAttr = pm.Attribute(self.nodeAttr('aiCustomAOVs'))
        self.updateAOVFrame(nodeAttr)

    def getAOVAttr(self, nodeAttr, aovName):
        '''
        given an aov name, return the corresponding attribute in the aiCustomAOVs array,
        or make a new one if it does not yet exist
        '''

        try:
            return self.nameToAttr[aovName]
        except KeyError:
            i = 0
            while i in self.arrayIndices:
                i+=1
            at = nodeAttr[i]
            at.aovName.set(aovName)
            self.nameToAttr[aovName] = at
            self.arrayIndices.add(i)
            return at

    def updateCustomArrayData(self, nodeAttr, aovList):
        '''
        set three data structures regarding the shadingEngine aiCustomAOVs attribute:
            - mapping from aov name to element plug on aiCustomAOVs 
            - set of all indices used by aiCustomAOVs
            - set of aov names that appear in aiCustomAOVs that are not in the globals
        '''
        self.nameToAttr, nextIndex = aovs.getShadingGroupAOVMap(nodeAttr)
        self.arrayIndices = set([at.index() for at in self.nameToAttr.values()])
        self.orphanedAOVs = set(self.nameToAttr.keys()).difference([aov.name for aov in aovList])

    def updateNetworkData(self):
        self.networkData = getAOVsInNetwork(self.nodeAttr('surfaceShader'))
        self.networkAOVs = set(aovs.getBuiltinAOVs()) # builtins are always in network
        self.networkNodeTypes = set([])
        self.aovNodes = defaultdict(list)
        for node, aovList in self.networkData.iteritems():
            self.networkAOVs.update(aovList)
            self.networkNodeTypes.add(node.type())
            for aov in aovList:
                self.aovNodes[aov].append(node)

    def buildAOVFrame(self, nodeAttr):
        # TODO: move this into AttributeEditorTemplate
        self._setActiveNodeAttr(nodeAttr)
        nodeAttr = pm.Attribute(nodeAttr)

        aovList = aovs.getAOVs()
        self.updateNetworkData()
        self.updateCustomArrayData(nodeAttr, aovList)

        pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)

        pm.cmds.frameLayout(label='AOVs', collapse=False)
        pm.cmds.columnLayout(adjustableColumn=True)

        pm.cmds.frameLayout(label='Surface Shader AOVs', collapse=False)
        pm.cmds.columnLayout(adjustableColumn=True)
        
        pm.cmds.rowLayout(nc=2)
        pm.cmds.text(label='')
        pm.cmds.button(label='AOV Browser',
                       c=lambda *args: aoveditor.arnoldAOVBrowser(listAOVGroups=True,
                                                                  nodeTypes=self.networkNodeTypes))
        pm.setParent('..') # rowLayout

        pm.cmds.frameLayout(labelVisible=False, collapsable=False)
        self.networkCol = pm.cmds.columnLayout(adjustableColumn=True)
        self.buildNetworkAOVs(nodeAttr, aovList)
        pm.setParent('..') # columnLayout
        pm.setParent('..') # frameLayout

        pm.setParent('..') # columnLayout
        pm.setParent('..') # frameLayout

        pm.cmds.frameLayout(label='Other AOVs', collapse=False)
        pm.cmds.columnLayout(adjustableColumn=True)

        pm.cmds.rowLayout(nc=2)
        pm.cmds.text(label='')
        pm.cmds.button(label='Add Custom', c=lambda *args: shaderTemplate.newAOVPrompt())
        pm.setParent('..') # rowLayout

        pm.cmds.frameLayout(labelVisible=False, collapsable=False)
        self.otherCol = pm.cmds.columnLayout(adjustableColumn=True)
        self.buildOtherAOVs(nodeAttr, aovList)
        pm.setParent('..') # columnLayout
        pm.setParent('..') # frameLayout

        pm.setParent('..') # columnLayout
        pm.setParent('..') # frameLayout
        
        pm.setParent('..') # columnLayout
        pm.setParent('..') # frameLayout
        pm.setUITemplate('attributeEditorTemplate', popTemplate=True)

    def updateAOVFrame(self, nodeAttr):
        # TODO: move this into AttributeEditorTemplate
        self._setActiveNodeAttr(nodeAttr)
        nodeAttr = pm.Attribute(nodeAttr)

        self.updateNetworkData()
        for ctrl in self._msgCtrls:
            pm.deleteUI(ctrl)
        self._msgCtrls = []

        pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)

        aovList = aovs.getAOVs()
        self.updateCustomArrayData(nodeAttr, aovList)

        pm.setParent(self.networkCol)
        self.buildNetworkAOVs(nodeAttr, aovList)

        pm.setParent(self.otherCol)
        self.buildOtherAOVs(nodeAttr, aovList)

        pm.setUITemplate('attributeEditorTemplate', popTemplate=True)

    def buildNetworkAOVs(self, nodeAttr, aovList):
        '''
        Populate the UI with an attrNavigationControlGrp for each AOV in the network
        '''
        for aov in aovList:
            if aov.name in self.networkAOVs:
                at = self.getAOVAttr(nodeAttr, aov.name)
                #at = nodeAttr[aov.index]
                #at.aovName.set(aov.name)
                ctrl = pm.cmds.attrNavigationControlGrp(at=at.aovInput.name(),
                                                   label=aov.name)
                self._msgCtrls.append(ctrl)
                pm.popupMenu(parent=ctrl);
                pm.menuItem(subMenu=True, label="Goto Node")
                for node in self.aovNodes[aov.name]:
                    pm.cmds.menuItem(label=node.name(), command=lambda arg, node=node: pm.select(node))

    def buildOtherAOVs(self, nodeAttr, aovList):
        '''
        Populate the UI with an attrNavigationControlGrp for each AOV not in the network
        '''
        for aov in aovList:
            if aov.name not in self.networkAOVs:
                at = self.getAOVAttr(nodeAttr, aov.name)
                ctrl = pm.cmds.attrNavigationControlGrp(at=at.aovInput.name(),
                                                        label=aov.name)
                self._msgCtrls.append(ctrl)


templates.registerAETemplate(ShadingEngineTemplate, "shadingEngine")

