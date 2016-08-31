#
#    ngSkinTools
#    Copyright (c) 2009-2015 Viktoras Makauskas. 
#    All rights reserved.
#    
#    Get more information at 
#        http://www.ngskintools.com
#    
#    --------------------------------------------------------------------------
#
#    The coded instructions, statements, computer programs, and/or related
#    material (collectively the "Data") in these files are subject to the terms 
#    and conditions defined by
#    Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License:
#        http://creativecommons.org/licenses/by-nc-nd/3.0/
#        http://creativecommons.org/licenses/by-nc-nd/3.0/legalcode
#        http://creativecommons.org/licenses/by-nc-nd/3.0/legalcode.txt
#         
#    A copy of the license can be found in file 'LICENSE.txt', which is part 
#    of this source code package.
#    

from ngSkinTools.ui.basetoolwindow import BaseToolWindow
from maya import cmds
from ngSkinTools.ui.basetab import BaseTab
from ngSkinTools.doclink import SkinToolsDocs
from ngSkinTools.ui.events import LayerEvents, MayaEvents
from ngSkinTools.ui.uiWrappers import FloatField, StoredTextEdit,\
    DropDownField, CheckBoxField, RadioButtonField
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.constants import Constants
from ngSkinTools.utils import Utils
from ngSkinTools.ui.SelectHelper import SelectHelper
from ngSkinTools.log import LoggerFactory
from ngSkinTools.influenceMapping import InfluenceMapping
from ngSkinTools.mllInterface import MllInterface
from ngSkinTools.orderedDict import OrderedDict


log = LoggerFactory.getLogger("initTransferWindow")

class InfluencesListEntry:
    def __init__(self,source=None,destination=None,specialValue=None,automatic=True):
        self.source = source
        self.destination = destination
        self.bidirectional = False
        self.automatic = automatic
        self.targetAndDestinationIsSameMesh = False
        self.specialValue = specialValue
    
    @staticmethod    
    def shortName(longName):
        separator = longName.rfind("|")
        if separator>=0:
            return longName[separator+1:]
        return longName
    
    def asLabel(self):
        if self.specialValue is not None:
            return self.specialValue
        
        prefix = "[M] " if not self.automatic else ""
        
        if self.isSelfReference():
            return prefix+self.shortName(self.source.path)+": itself"
        
        if self.source is not None and self.destination is not None: 
            mask = "%s -> %s"
            if self.bidirectional:
                mask = "%s <-> %s"
            return prefix+mask % (self.shortName(self.source.path),self.shortName(self.destination.path))
        
        if self.source is not None:
            return prefix+self.shortName(self.source.path)
                
        if self.destination is not None:
            return prefix+self.shortName(self.destination.path)
                
        return "Could not format item" 
    
    def isSelfReference(self):
        return self.specialValue is None and self.targetAndDestinationIsSameMesh and self.source.path==self.destination.path
    
    def isConnectedElsewhere(self):
        return self.source!=None and self.destination!=None and self.source.path!=self.destination.path
    
    
    def highlight(self):
        SelectHelper.replaceHighlight([self.source.path,self.destination.path])
        
    def __repr__(self):
        return self.asLabel()
        

class TransferWeightsTab(BaseTab):
    log = LoggerFactory.getLogger("Transfer Weights Tab")
    VAR_PREFIX = 'ngSkinToolsTransferTab_'
    
    axisValues = ('X','Y','Z')
    
    def __init__(self):
        BaseTab.__init__(self)
        self.items = []
        self.dataModel = None
        self.currentSelection = None
        self.currentInfluencesSelection = []
        self.manualOverrides = {}
        self.mirrorMode = True
        
    def setDataModel(self,dataModel):
        self.dataModel = dataModel
        self.dataModel.parent = self
    
    def createUI(self, parent):
        buttons = []
        buttons.append(('Done', self.execContinue,''))
        buttons.append(('Cancel', self.closeWindow,''))
        
        self.cmdLayout = self.createCommandLayout(buttons,SkinToolsDocs.INITWEIGHTTRANSFER_INTERFACE)
        
        if self.mirrorMode:
            self.createMirrorOptionsGroup()
        
        if not self.mirrorMode:
            self.createTransferOptionsGroup()
        self.createInfluenceMappingGroup()

        LayerEvents.layerAvailabilityChanged.addHandler(self.updateLayoutEnabled,self.cmdLayout.outerLayout)
        LayerEvents.mirrorCacheStatusChanged.addHandler(self.updateUIValues,self.cmdLayout.outerLayout)
        MayaEvents.nodeSelectionChanged.addHandler(self.updateUIValues, self.cmdLayout.outerLayout)

        self.updateLayoutEnabled()
        self.updateUIValues()
        self.updatePreferedValues()
        
        
    def releaseUI(self):
        LayerEvents.layerAvailabilityChanged.removeHandler(self.updateLayoutEnabled)
        LayerEvents.mirrorCacheStatusChanged.removeHandler(self.updateUIValues)
        MayaEvents.nodeSelectionChanged.removeHandler(self.updateUIValues)
        
    def updatePreferedValues(self):
        if self.mirrorMode:
            preferedMirrorAxis = LayerDataModel.getInstance().mirrorCache.mirrorAxis
            if preferedMirrorAxis is None:
                preferedMirrorAxis = 'X'
            self.controls.mirrorAxis.setValue(TransferWeightsTab.axisValues.index(preferedMirrorAxis.upper()))
        
        if self.mirrorMode and LayerDataModel.getInstance().layerDataAvailable:
            self.manualOverrides = LayerDataModel.getInstance().mll.getManualMirrorInfluences()
        else:
            self.manualOverrides = {}
            
            
    def updateUIValues(self):
        # when selection changes between update UI calls, overwrite UI with preferred values in the mesh
        selection = cmds.ls(sl=True)
        if selection!=self.currentSelection:
            self.updatePreferedValues()
        self.currentSelection = selection
        self.previewInfluenceMapping()
        

    def createMirrorOptionsGroup(self):
        group = self.createUIGroup(self.cmdLayout.innerLayout, 'Mirror Options')


        self.createFixedTitledRow(group, 'Mirror Axis')
        cmds.columnLayout()
        self.controls.mirrorAxis = DropDownField(self.VAR_PREFIX+'mirrorAxis')
        self.controls.mirrorAxis.beginRebuildItems()
        
        
        for i in TransferWeightsTab.axisValues:
            self.controls.mirrorAxis.addOption(i);
        self.controls.mirrorAxis.endRebuildItems()
        self.controls.mirrorAxis.changeCommand.addHandler(self.previewInfluenceMapping, group)
        

        self.createTitledRow(parent=group, title="Vertex Mapping Mode")
        self.controls.transferMode = DropDownField(self.VAR_PREFIX+'vertexMirrorMappingMode')
        for opt in MirrorTransferModel.vertexTransferModes.keys():
            self.controls.transferMode.addOption(opt)
        

    def createTransferOptionsGroup(self):
        group = self.createUIGroup(self.cmdLayout.innerLayout, 'Transfer Options')
        self.createTitledRow(parent=group, title="Vertex Transfer Mode")
        self.controls.transferMode = DropDownField(self.VAR_PREFIX+'vertexTransferMode')
        
        for opt in CopyWeightsModel.vertexTransferModes.keys():
            self.controls.transferMode.addOption(opt)
        
        self.createTitledRow(parent=group, title=None)
        self.controls.keepExistingLayers = CheckBoxField(self.VAR_PREFIX+'KeepExistingLayers',label="Keep existing layers",
                annotation='when unselected, will delete existing layers in destination',defaultValue=1)
        
        

    def ignoreModeChanged(self):
        if not self.mirrorMode:
            return
                
        self.controls.prefixesGroup.setVisible(self.isPrefixIgnoreMode())
        self.controls.suffixesGroup.setVisible(not self.isPrefixIgnoreMode())
        self.previewInfluenceMapping()
        
    def isPrefixIgnoreMode(self):
        return self.controls.ignorePrefixes.getValue()==1

    def createInfluenceMappingGroup(self):
        group = self.createUIGroup(self.cmdLayout.innerLayout, 'Influence Mapping')
        
        self.createFixedTitledRow(group, 'Infl. Distance Error')
        self.controls.influenceDistanceError = FloatField(self.VAR_PREFIX+'distanceError', minValue=0, maxValue=None, step=0.01, defaultValue=0.001, 
                                    annotation='Defines maximum inaccuracy between left and right influence positions')
        self.controls.influenceDistanceError.changeCommand.addHandler(self.previewInfluenceMapping, group)
        
        if not self.mirrorMode:
            self.createTitledRow(parent=group, title="Namespaces")
            self.controls.ignoreNamespaces = CheckBoxField(self.VAR_PREFIX+'IgnoreNamespaces',label="Ignore",
                    annotation='ignore influence namespaces when matching by name',defaultValue=1)
            self.controls.ignoreNamespaces.changeCommand.addHandler(self.previewInfluenceMapping,ownerUI=group)
            

        if self.mirrorMode:
            self.createTitledRow(group, 'Ignore')
            cmds.radioCollection()
            for index,i in enumerate(['Prefixes','Suffixes']):
                ctrl = self.controls.__dict__['ignore'+i] = RadioButtonField(self.VAR_PREFIX+'ignoreMode'+i,defaultValue=1 if index==0 else 0,label=i)
                ctrl.changeCommand.addHandler(self.ignoreModeChanged,group)        


            self.controls.prefixesGroup = self.createTitledRow(group, 'Influence Prefixes')
            self.controls.influencePrefixes = StoredTextEdit(self.VAR_PREFIX+'inflPrefix', annotation='Specifies influence prefixes to be ignored when matching by name;\nUsually you would put your left/right influence prefixes here;\nseparate them with commas, e.g. "L_, R_"')
            self.controls.influencePrefixes.changeCommand.addHandler(self.previewInfluenceMapping, group)
            
            self.controls.suffixesGroup = self.createTitledRow(group, 'Influence Suffixes')
            self.controls.influenceSuffixes = StoredTextEdit(self.VAR_PREFIX+'inflSuffix', annotation='Specifies influence suffixes to be ignored when matching by name;\nUsually you would put your left/right influence suffixes here;\nseparate them with commas, e.g. "_Lf, _Rt"')
            self.controls.influenceSuffixes.changeCommand.addHandler(self.previewInfluenceMapping, group)
        
        
        
        influencesLayout = cmds.columnLayout(parent=group,adjustableColumn=1,rowSpacing=Constants.MARGIN_SPACING_VERTICAL)
        cmds.text(parent=influencesLayout,label="Influence mapping to be used:",align='left')
        self.controls.influencesList = cmds.textScrollList(parent=influencesLayout, height=200, numberOfRows=5, allowMultiSelection=True,
                                                           selectCommand=self.onInfluenceSelected,
                                                           deleteKeyCommand=lambda *args: self.removeSelectedManualMappings())
        
        manualGroup = self.createUIGroup(self.cmdLayout.innerLayout, 'Manual influence mapping')
        cmds.rowLayout(parent=manualGroup,nc=3) 
        
        
        buttonWidth = 110
        cmds.button('Disconnect link',width=buttonWidth,command=lambda *args: self.doDisconnectMapping(),annotation='Disconnect two associated influences, and make each influence point to itself')
        if self.mirrorMode:
            cmds.button('Link, both ways',width=buttonWidth,command=lambda *args: self.doConnectMapping(bidirectional=True),annotation='Connect two selected influences and link them both ways')
        cmds.button('Link, one way' if self.mirrorMode else "Link",width=buttonWidth,command=lambda *args: self.doConnectMapping(bidirectional=False),annotation='Connect two selected influences and link on source to destination')
        cmds.rowLayout(parent=manualGroup,nc=2) 
        cmds.button('Remove manual rule',width=buttonWidth,command=lambda *args: self.removeSelectedManualMappings(),annotation='Remove manual rule; influence will be a subject to automatic matching')

        self.ignoreModeChanged()
        
        cmds.setParent(group)
        
    def getSelectedPairs(self):
        selection = cmds.textScrollList(self.controls.influencesList,q=True,sii=True)

        if selection is not None:
            for i in selection:
                yield self.items[i-1]
    
        
    def closeWindow(self,*args):
        self.parentWindow.closeWindow()
        
    def buildInfluenceMappingEngine(self):
        '''
        :rtype: InfluenceMapping
        '''
        result = self.dataModel.buildInfluenceMappingEngine(self.controls)
        result.manualOverrides = self.manualOverrides
        return result
    
    
    def previewInfluenceMapping(self):
        if not self.dataModel.isEnabled():
            return
        engine = self.buildInfluenceMappingEngine()
        engine.calculate()
        self.contructInfluenceList()
        self.currentInfluencesSelection = []
        


    def execContinue(self,*args):
        self.previewInfluenceMapping()
        self.dataModel.execute()
        self.closeWindow()
        

    def onInfluenceSelected(self,*args):
        newSelection = list(self.getSelectedPairs())

        newHighlight = []
        for i in newSelection:
            if i.source is not None:
                newHighlight.append(i.source.path)
            if i.destination is not None:
                newHighlight.append(i.destination.path)
            
        SelectHelper.replaceHighlight(newHighlight)
        
        
        # the weird way of forming this currentInfluencesSelection like that
        # is because we want the items to be ordered in first to last selected order
        # when new selection happens, first all items that are not selected anymore 
        # are removed from the current selection cache,
        # then all new items that are selected are added at the end.
        for i in self.currentInfluencesSelection[:]:
            if i not in newSelection:
                self.currentInfluencesSelection.remove(i)
        for i in newSelection:
            if i not in self.currentInfluencesSelection:
                self.currentInfluencesSelection.append(i)
        
    @staticmethod
    def findAssociation(itemList,source,destination,automatic):
        for i in itemList:
            if i.automatic!=automatic:
                continue
            
            if i.source.path==source and i.destination.path==destination:
                return i
            if i.bidirectional and i.destination.path==source and i.source.path==destination:
                return i
            
        return None
    
    def influencesListSort(self,entry1,entry2):
        # priority for non-automatic entries
        if entry1.automatic!=entry2.automatic:
            return 1 if entry1.automatic else -1

        # priority for non-self references
        if entry1.isSelfReference()!=entry2.isSelfReference():
            return 1 if entry1.isSelfReference() else -1
            
        # priority for bidirectional entries
        if entry1.bidirectional!=entry2.bidirectional:
            return 1 if not entry1.bidirectional else -1
        
        if entry1.source is not None and entry2.source is not None:
            return cmp(entry1.source.path, entry2.source.path)
        
        if entry1.destination is not None and entry2.destination is not None:
            return cmp(entry1.destination.path, entry2.destination.path)
        
        return 0    
        
    def contructInfluenceList(self):
        self.items = []

        mapper = self.dataModel.mapper
        
        unmatchedSources = mapper.sourceInfluences[:]
        unmatchedDestinations = mapper.destinationInfluences[:]
        
        
        sourceInfluencesMap = dict((i.logicalIndex,i) for i in mapper.sourceInfluences)
        destinationInfluencesMap = dict((i.logicalIndex,i) for i in mapper.destinationInfluences)
        
        
        def isSourceAutomatic(source):
            return source.logicalIndex not in mapper.manualOverrides.keys()

        for source,destination in mapper.mapping.items():
            source = sourceInfluencesMap[source]
            destination = None if destination is None else destinationInfluencesMap[destination]
            
            if source is None or destination is None:
                continue

            if source in unmatchedSources:
                unmatchedSources.remove(source)

            if destination in unmatchedDestinations:
                unmatchedDestinations.remove(destination)

            
            
            automatic = isSourceAutomatic(source)
            item = None
            if self.mirrorMode and destination is not None:
                item=self.findAssociation(self.items, destination.path, source.path,automatic)
            if item is not None:
                item.bidirectional = True
            else:
                item = InfluencesListEntry()
                item.targetAndDestinationIsSameMesh = self.mirrorMode
                item.source = source
                item.destination = destination
                item.bidirectional = False
                self.items.append(item)
                item.automatic = automatic
        
        self.items = sorted(self.items,self.influencesListSort)
         
        if len(unmatchedSources)>0 and not self.mirrorMode:
            self.items.append(InfluencesListEntry(specialValue="Unmatched source influences:"))
            
            for source in unmatchedSources:
                self.items.append(InfluencesListEntry(source=source,automatic=isSourceAutomatic(source)))
                
        if len(unmatchedDestinations)>0 and not self.mirrorMode:
            self.items.append(InfluencesListEntry(specialValue="Unmatched destination influences:"))
            
            for destination in unmatchedDestinations:
                self.items.append(InfluencesListEntry(destination=destination))
                
        cmds.textScrollList(self.controls.influencesList,e=True,removeAll=True,
                            append=[i.asLabel() for i in self.items])
        
        

    def updateLayoutEnabled(self):
        '''
        updates UI enabled/disabled flag based on layer data availability
        '''
        enabled = self.dataModel.isEnabled()
        cmds.layout(self.cmdLayout.innerLayout,e=True,enable=enabled)
        cmds.layout(self.cmdLayout.buttonForm,e=True,enable=enabled)
    
    def addManualInfluenceMapping(self,source,destination):
        self.manualOverrides[source.logicalIndex] = None if destination is None else destination.logicalIndex    
    
    def doDisconnectMapping(self):
        for mapping in self.currentInfluencesSelection:
            if mapping.source is None:
                continue
            
            if mapping.destination is None:
                continue
            
            if mapping.source == mapping.destination:
                continue
            
            # for both source and destination, create a mapping for just itself
            self.addManualInfluenceMapping(mapping.source, mapping.source if mapping.targetAndDestinationIsSameMesh else None)
            if mapping.bidirectional:
                self.addManualInfluenceMapping(mapping.destination, mapping.destination)
                
        self.previewInfluenceMapping()
        
    def doConnectMapping(self,bidirectional=True):
        if len(self.currentInfluencesSelection)<2:
            return
        
        if bidirectional and len(self.currentInfluencesSelection)!=2:
            return

        validSources = []
        
        for item in self.currentInfluencesSelection[:-1]:
            if item.isConnectedElsewhere() or item.source is None:
                continue
            validSources.append(item)
        
        # second selected list item
        destinationItem = self.currentInfluencesSelection[-1]
        if destinationItem.isConnectedElsewhere():
            return
        
        destination = destinationItem.destination if destinationItem.destination is not None else destinationItem.source
        if destination is None:
            return
        
        destination = destination.logicalIndex
        for sourceItem in validSources:
            source = sourceItem.source.logicalIndex
            self.manualOverrides[source] = destination
            if bidirectional:
                self.manualOverrides[destination] = source
        
        self.previewInfluenceMapping()
             
    def removeSelectedManualMappings(self):
        for item in self.currentInfluencesSelection:
            if item.source.logicalIndex in self.manualOverrides:
                del self.manualOverrides[item.source.logicalIndex]
            if item.bidirectional and item.destination.logicalIndex in self.manualOverrides:
                del self.manualOverrides[item.destination.logicalIndex]
        self.previewInfluenceMapping() 
        
class TransferDataModel(object):
    def __init__(self):
        self.parent = None
        
    def isEnabled(self):
        return True
    
    def buildInfluenceMappingEngine(self,controls):
        self.controls = controls
        
        self.mapper = InfluenceMapping()
        
        def parseCommaValue(values):
            return [value.strip() for value in values.split(",")]
        
        if hasattr(self.controls, 'ignorePrefixes'):
            if self.controls.ignorePrefixes.getValue()==1:
                self.mapper.nameMatchRule.setPrefixes(*parseCommaValue(controls.influencePrefixes.getValue()))
            else:
                self.mapper.nameMatchRule.setSuffixes(*parseCommaValue(controls.influenceSuffixes.getValue()))

        if hasattr(self.controls, 'mirrorAxis'):
            self.mapper.distanceMatchRule.mirrorAxis = TransferWeightsTab.axisValues.index(controls.mirrorAxis.getSelectedText())
        self.mapper.distanceMatchRule.maxThreshold = float(controls.influenceDistanceError.getValue());
        return self.mapper
    
    
class MirrorTransferModel(TransferDataModel):
    vertexTransferModes = OrderedDict((
                    ("Closest point on surface","closestPoint"),
                    ("UV space","uvSpace"),
                    ))    
    
    def isEnabled(self):
        return LayerDataModel.getInstance().layerDataAvailable==True

    def buildInfluenceMappingEngine(self,controls):
        '''
        builds influence transfer mapping, using parameters from UI
        '''
        mapping = TransferDataModel.buildInfluenceMappingEngine(self,controls)
        mapping.sourceInfluences = LayerDataModel.getInstance().mll.listInfluenceInfo();
            
        mapping.mirrorMode = True
        
        mapping.manualOverrides = LayerDataModel.getInstance().mll.getManualMirrorInfluences()
        
        return mapping

    def execute(self):
        influencesMapping = MllInterface.influencesMapToList(self.mapper.mapping)
        mirrorAxis = TransferWeightsTab.axisValues[self.mapper.distanceMatchRule.mirrorAxis]
        vertexTransferMode = self.vertexTransferModes[self.parent.controls.transferMode.getSelectedText()]
        
        cmds.ngSkinLayer(initMirrorData=True, influencesMapping=influencesMapping, mirrorAxis=mirrorAxis, vertexTransferMode=vertexTransferMode)
        
        LayerDataModel.getInstance().mll.setManualMirrorInfluences(self.mapper.manualOverrides)
        
        LayerDataModel.getInstance().updateMirrorCacheStatus()
                
        




class InitTransferWindow(BaseToolWindow):
    def __init__(self,windowName):
        BaseToolWindow.__init__(self,windowName)
        self.useUserPrefSize = False
        self.windowTitle = 'Init Skin Transfer'
        self.sizeable = True
        self.defaultHeight = 600
        self.defaultWidth = 450
        self.content = TransferWeightsTab()
        self.content.parentWindow = self
        
    @staticmethod
    def getInstance():
        return BaseToolWindow.getWindowInstance('InitTransferWindow', InitTransferWindow)
        
    def createWindow(self):
        BaseToolWindow.createWindow(self)
        
        self.content.createUI(self.windowName)
        
    def onWindowDeleted(self):
        self.content.releaseUI()
        return BaseToolWindow.onWindowDeleted(self)
    
class MirrorWeightsWindow(InitTransferWindow):
    def __init__(self, windowName):
        InitTransferWindow.__init__(self, windowName)
        self.windowTitle = 'Init Weights Mirror'
        self.content.setDataModel(MirrorTransferModel())
    
    @staticmethod
    def getInstance():
        return BaseToolWindow.rebuildWindow('MirrorWeightsWindow', MirrorWeightsWindow)
    

class CopyWeightsModel(TransferDataModel):
    vertexTransferModes = OrderedDict((
                    ("Closest point on surface","closestPoint"),
                    ("UV space","uvSpace"),
                    ("By Vertex ID","vertexId"),
                    ))    
    
    def __init__(self):
        TransferDataModel.__init__(self)
        self.sourceModel = None
        self.sourceMesh = None
        self.targetMesh = None
    
    def isEnabled(self):
        return (self.sourceModel is not None or self.sourceMesh is not None) and (self.targetMesh is not None)

    def buildInfluenceMappingEngine(self,controls):
        '''
        builds influence transfer mapping, using parameters from UI
        '''
        
        mapping = TransferDataModel.buildInfluenceMappingEngine(self,controls)
        
        mapping.nameMatchRule.ignoreNamespaces = self.parent.controls.ignoreNamespaces.getValue()==1
        
        mapping.rules = [mapping.distanceMatchRule,mapping.nameMatchRule]
        if self.sourceModel is not None:
            mapping.sourceInfluences = self.sourceModel.influences;
        else:
            mapping.sourceInfluences = MllInterface(mesh=self.sourceMesh).listInfluenceInfo();
        
        mapping.destinationInfluences = MllInterface(mesh=self.targetMesh).listInfluenceInfo()
            
        mapping.mirrorMode = False
        return mapping
    
    @Utils.undoable
    def execute(self):
        targetMll = MllInterface(mesh=self.targetMesh)

        self.ensureTargetMeshLayers()
        
        previousLayerIds = [layerId for layerId, _  in targetMll.listLayers()]

        sourceMesh = self.sourceMesh        
        if self.sourceModel is not None:
            self.sourceModel.saveTo(MllInterface.TARGET_REFERENCE_MESH)
            sourceMesh = MllInterface.TARGET_REFERENCE_MESH
        
        vertexTransferMode = self.vertexTransferModes[self.parent.controls.transferMode.getSelectedText()]

        
        sourceMll = MllInterface(mesh=sourceMesh)
        
        with targetMll.batchUpdateContext():
            sourceMll.transferWeights(self.targetMesh,influencesMapping=self.mapper.mapping,vertexTransferMode=vertexTransferMode)

            if self.parent.controls.keepExistingLayers.getValue()!=1:
                for layerId in previousLayerIds:
                    targetMll.deleteLayer(layerId)

        LayerDataModel.getInstance().updateLayerAvailability()
        LayerEvents.layerListModified.emit()
        

    def inputValuesChanged(self):
        self.parent.updateLayoutEnabled()
        self.parent.previewInfluenceMapping()
        
    def setSourceData(self,model):
        '''
        use LayerData model as source 
        '''
        self.sourceModel = model
        self.inputValuesChanged()
        
    def setSourceMesh(self,mesh):
        self.sourceMesh = mesh
        self.inputValuesChanged()
        
    def ensureTargetMeshLayers(self):
        targetMll = MllInterface(mesh=self.targetMesh)
        if not targetMll.getLayersAvailable():
            targetMll.initLayers()
            #targetMll.createLayer("weights before import")
        
    def setDestinationMesh(self,mesh):
        self.targetMesh = mesh
        self.ensureTargetMeshLayers()
        
        self.inputValuesChanged()
        
class TransferWeightsWindow(InitTransferWindow):
    def __init__(self, windowName):
        InitTransferWindow.__init__(self, windowName)
        self.windowTitle = 'Transfer Weights'
        self.content.setDataModel(CopyWeightsModel())
        self.content.mirrorMode = False

    @staticmethod
    def getInstance():
        return BaseToolWindow.rebuildWindow('TransferWeightsWindow', TransferWeightsWindow)
    
