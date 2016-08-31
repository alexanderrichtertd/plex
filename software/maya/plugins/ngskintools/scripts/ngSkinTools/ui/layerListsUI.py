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

from __future__ import with_statement
from maya import cmds
from ngSkinTools.ui.uiWrappers import FormLayout, TextEdit, RadioButtonField
from ngSkinTools.ui.constants import Constants
from ngSkinTools.layerUtils import NamedPaintTarget
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.events import LayerEvents, Signal, MayaEvents
from ngSkinTools.utils import Utils
from ngSkinTools.ui.options import Options, PersistentValueModel
from ngSkinTools.log import LoggerFactory
from ngSkinTools.InfluenceNameTransforms import InfluenceNameTransform
from ngSkinTools.InfluenceNameFilter import InfluenceNameFilter
from ngSkinTools.ui import uiWrappers

log = LoggerFactory.getLogger("layerListsUI")


class IdToNameEntry(object):
    def __init__(self,itemId=None,name=None,displayName=None,suffix=None):
        if displayName is None:
            displayName = name
            
        self.internalId = None
        self.id = itemId
        
        self.name = name
        self.displayName = displayName
        self.suffix = suffix
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self,id):
        self.__id = id
        self.internalId = str(id)
        
    def __repr__(self):
        return "IdToNameEntry({0},{1})".format(self.internalId,self.name)

    
class TreeViewIDList(object):
    def __init__(self,allowMultiSelection=True):
        self.items = []
        selectCommand = self.selectionChanged
        editCommand = self.editLabelCommand
        
        if Utils.getMayaVersion()<Utils.MAYA2012:
            selectCommand = Utils.createMelProcedure(self.selectionChanged, [('int','item'),('int','state')],returnType="int")
            editCommand = Utils.createMelProcedure(self.editLabelCommand, [('string','item'),('string','newName')])
            
        self.control = cmds.treeView(numberOfButtons=0, height=100, selectCommand=selectCommand, editLabelCommand=editCommand,dragAndDropCommand=self.handleDragDropCommand)
        
        cmds.treeView(self.control,e=True,enableKeys=True)
        
        # list of selected IDs
        self.selectedItems = []
        self.onSelectionChanged = Signal()
        
        self.__selectionChanging = False
        self.__itemNameChanging = False
    
    def handleDragDropCommand(self,itemList,prevParents,prevIndexes,newParent,newIndexes,itemBefore,itemAfter):
        pass

    def setItems(self,newItems,selectedID):
        '''
        sets new items in the ID list;
        :param list newItems: list of IdToNameEntry
        :param selectedID: item to select in the list after setting the items 
        '''
        
        log.debug("set items: {0},selected id: {1}".format(newItems,selectedID))
            
        if self.items!=newItems:
            if self.__selectionChanging:
                raise Exception("cannot change items while selection is changing")
            if self.__itemNameChanging:
                # raise Exception("cannot change items while item name is changing")
                # silently exit: should be no harm ignoring new items as the only thing that changed
                # is label name, and we already reflect that in UI 
                return
            
            self.selectedItems = []
            
            cmds.treeView(self.control,e=True,clearSelection=True)
            cmds.treeView(self.control,e=True,removeAll=True)
            for i in newItems:
                cmds.treeView(self.control,e=True,addItem=(i.id,''))
                cmds.treeView(self.control,e=True,displayLabel=(i.id,i.displayName),displayLabelSuffix=(i.id,i.suffix))
            
        self.items = newItems
        self.selectByID(selectedID)
        
    def getIdByInternalId(self,internalId):
        '''
        given item ID (internal UI label), return actual item ID from the item.
        '''
        if internalId is None:
            return None
        
        for i in self.items:
            if i.internalId==internalId:
                return i.id
            
        raise Exception("invalid internal ID: {!r}".format(internalId))

    def selectionChanged(self,internalId,selected):
        '''
        UI event handler for when selection is changed
        there are events fired for items being unselected (``selected`` is 0)
        and for items being selected (``selected`` is 1)
        '''
        item = self.getIdByInternalId(internalId)
        
        self.__selectionChanging = True
        try:
            if selected:
                if item is not None and item not in self.selectedItems:
                    self.selectedItems.append(item)
                    self.onSelectionChanged.emit()
            else:
                if item in self.selectedItems:
                    self.selectedItems.remove(item)
                    self.onSelectionChanged.emit()
        finally:
            self.__selectionChanging = False
            
        return True
        
    
    def internalEditLabelCommand(self,item,newName):
        '''
        indirectly executed by treeview inplace editor;
        return non empty string to let treeView know that rename succeeded
        
        :return: True, if rename was successful; false otherwise. 
        '''
        return False
    
    def editLabelCommand(self,internalId,newName):
        '''
        UI event handler for when user edits item label;
        
        subclasses should override internalEditLabelCommand instead
        '''
        self.__itemNameChanging = True
        try:
            item = self.getIdByInternalId(internalId)
            renameSuccessful = self.internalEditLabelCommand(item, newName)
            if not renameSuccessful:
                return ''
            return internalId
        finally:
            self.__itemNameChanging = False
            

    def getSelectedNames(self):
        '''
        :return: names of all currently selected items 
        '''
        return [i.name for i in self.items if (i.id in self.selectedItems)]
    
    
    def getSelectedID(self):
        '''
        :return: ID of currently selected item
        '''
        return None if not self.selectedItems else self.selectedItems[-1]

    def getSelectedIDs(self):
        '''
        :return: IDs of selected items
        '''
        return self.selectedItems
        

    
    def selectByID(self,itemId):
        self.setSelectedIDs([itemId])
        
    def setSelectedIDs(self,ids):
        log.debug("selecting by ID: {0}".format(id))
        if self.__selectionChanging:
            return
        
        # remove any null items
        ids = [i for i in ids if i is not None]
        
        if self.selectedItems == ids:
            return

        self.selectedItems = ids
        
        for i in self.items:
            cmds.treeView(self.control,e=True,si=(i.internalId,int(i.id in ids)))
        
        
        
class LayersTreeView(TreeViewIDList):
    def internalEditLabelCommand(self, layerId, newName):
        '''
        implements layer in-place rename
        '''
        # do not allow empty layer names
        if newName.strip()=='':
            return False
        
        LayerDataModel.getInstance().setLayerName(layerId,newName)
        #cmds.treeView(self.control,e=True,displayLabel=(item,newName))
        return True

    def handleDragDropCommand(self, itemList, prevParents, prevIndexes, newParent, newIndexes, itemBefore, itemAfter):
        
        def asId(internalId):
            if internalId=='' or internalId is None:
                return None
            return self.getIdByInternalId(internalId)
        
        self.itemDropped([asId(internalId) for internalId in itemList], 
                         asId(newParent),
                         asId(itemBefore),
                         asId(itemAfter))
        LayerEvents.layerListModified.emit()

class InfluencesTreeView(TreeViewIDList):
    def internalEditLabelCommand(self, layerId, newName):
        return False # no rename for infl tree view

    def handleDragDropCommand(self, itemList, prevParents, prevIndexes, newParent, newIndexes, itemBefore, itemAfter):
        # force reload on influences list
        LayerEvents.influenceListChanged.emit()

class InfluenceFilterUi:
    VAR_PREFIX = 'ngSkinToolsInfluenceFilter_'

    def __init__(self,parent):
        self.parent = parent
        self.mainLayout = None
        self.filterChanged = Signal("Influence filter changed")
        self.isVisible = PersistentValueModel(Options.VAR_OPTION_PREFIX+"_InfluenceFilterVisible", False)
    
    def createUI(self,parent):
        result = group = self.mainLayout = uiWrappers.frameLayout(parent=parent,label="Influence Filter", marginWidth=Constants.MARGIN_SPACING_HORIZONTAL,marginHeight=Constants.MARGIN_SPACING_VERTICAL, collapsable=True,
                                 expandCommand=self.isVisible.save,collapseCommand=self.isVisible.save,
                                 borderStyle='etchedIn')
        cmds.frameLayout(group,e=True,collapse = self.isVisible.get())
        
        column = cmds.columnLayout(parent=group,adjustableColumn=1,rowSpacing=Constants.MARGIN_SPACING_VERTICAL)
        
        form = FormLayout(parent=column)
        
        label=cmds.text(label='Influence Filter:')
        textField = self.influenceNameFilter = TextEdit(annotation="Filter influence list by name")
        clearButton = cmds.button(label='clear',width=50,command=self.clearNameFilter)
        
        
        form.attachForm(label, 10, None, 0, Constants.MARGIN_SPACING_HORIZONTAL)
        form.attachForm(clearButton, 10, Constants.MARGIN_SPACING_HORIZONTAL, 0, None)
        form.attachForm(textField,10,None,0,None)
        form.attachControl(textField,label,None,None,None,Constants.MARGIN_SPACING_HORIZONTAL)
        form.attachControl(textField,clearButton,None,Constants.MARGIN_SPACING_HORIZONTAL,None,None)
        
        
        textField.changeCommand.addHandler(self.filterChanged.emit)
        
        cmds.setParent(result)
        cmds.radioCollection()
        
        
        form = FormLayout(parent=column)
        
        self.radioAllInfluences = RadioButtonField(self.VAR_PREFIX+"allInfluences",defaultValue=1,label='Show all influences')
        self.radioAllInfluences.changeCommand.addHandler(self.radioAllInfluencesChanged)
        self.radioActiveInfluences = RadioButtonField(self.VAR_PREFIX+"activeInfluences",defaultValue=0,label='Only influences with non-zero weights')
        form.attachForm(self.radioAllInfluences, 0, 0, None, 90)
        form.attachForm(self.radioActiveInfluences, None, 0, None, 90)
        form.attachControl(self.radioActiveInfluences, self.radioAllInfluences, 0, None, None, None)
        
        return result
    
    def clearNameFilter(self,*args):
        self.influenceNameFilter.setValue('')
        self.influenceNameFilter.changeCommand.emit()
        
    def radioAllInfluencesChanged(self):
        self.parent.updateInfluenceMenuValues()
        self.filterChanged.emit()

        

    def setVisible(self,visible):
        self.isVisible.set(visible)
        cmds.frameLayout(self.mainLayout,e=True,collapse = self.isVisible.get())
    
    def toggle(self):
        self.setVisible(not self.isVisible.get())
        
    def createNameFilter(self):
        '''
        returns name filter (InflFilterMatch instance) based on control values
        '''
        filter = InfluenceNameFilter()
        filter.setFilterString(self.influenceNameFilter.getValue())
        return filter
    

class LayerListsUI:
    '''
    UI piece that defines layers&influences lists
    '''
    
    def __init__(self):
        class Controls:
            pass
        self.controls = Controls()
        self.data = LayerDataModel.getInstance()
        self.data.setLayerListsUI(self)
        
    def getMll(self):
        '''
        :rtype: MllInterface
        '''
        return self.data.mll;
        
        
    def layerSelectionChanged(self,*args):
        '''
        even hander for changed layer selection
        '''
        layerId = self.controls.layerDisplay.getSelectedID();
        if layerId is not None:
            self.getMll().setCurrentLayer(layerId)
            #self.updateLayerList()
            self.updateInfluenceList()

            LayerEvents.layerSelectionChanged.emit()
            LayerEvents.currentLayerChanged.emit()
        
    def currentLayerChangedHandler(self):
        self.controls.layerDisplay.selectByID(self.data.getCurrentLayer())
        self.updateInfluenceList()
          
    def update(self):
        self.updateLayerList()
        self.updateInfluenceList()
        self.updateInfluenceMenuValues()
        
    
            
    def updateLayerList(self):
        
        if not self.data.layerDataAvailable:
            return
        
        layers = self.data.mll.listLayers()
        currLayer = self.data.getCurrentLayer()
            
        newItems = []
        for layerId,layerName in layers:
            entry = IdToNameEntry()
            entry.id = layerId
            entry.name = layerName
            entry.displayName = layerName
            entry.suffix = "" if self.data.getLayerEnabled(layerId) else " [OFF]"
            newItems.append(entry)

        
        self.controls.layerDisplay.setItems(newItems,currLayer)
        LayerEvents.layerListUIUpdated.emit()
        

        
    def updateInfluenceList(self):
        if not self.data.layerDataAvailable:
            return

        showAllInfluences = self.filterUi.radioAllInfluences.getValue()
        influences = self.data.mll.listLayerInfluences(activeInfluences=not showAllInfluences)
        
        filter = self.filterUi.createNameFilter()
        
        newItems = []

        # append named targets
        if self.data.getCurrentLayer()>0:
            newItems.append(IdToNameEntry(NamedPaintTarget.MASK, "[Layer Mask]"))
            if self.data.isDqMode():
                newItems.append(IdToNameEntry(NamedPaintTarget.DUAL_QUATERNION, "[Dual Quaternion Weights]"))
        
        names = [name for name,_ in influences]
        displayNames = InfluenceNameTransform().appendingOriginalName().transform(names)
        ids = [inflId for _,inflId in influences]
        
        for name,displayName,influenceId in zip(names,displayNames,ids):
            if filter.isMatch(displayName):
                newItems.append(IdToNameEntry(influenceId,name=name,displayName=displayName))
                
            
            
        self.controls.influenceDisplay.setItems(newItems,self.data.mll.getCurrentPaintTarget())
            
                
    def execInfluenceSelected(self,*args):
        '''
        selection change handler for .influenceDisplay
        '''
        targetId = self.controls.influenceDisplay.getSelectedID();
        
        if targetId is None:
            return
        
        LayerDataModel.getInstance().mll.setCurrentPaintTarget(targetId)

        LayerEvents.currentInfluenceChanged.emit()
        
        log.info("selected logical influence {0}".format(targetId))
        
        
    def createLayersListRMBMenu(self):
        from ngSkinTools.ui.mainwindow import MainWindow
        self.controls.layerListMenu = cmds.popupMenu( parent=self.controls.layerDisplay.control )
        
        actions = MainWindow.getInstance().actions
        actions.newLayer.newMenuItem("New Layer...")
        actions.duplicateLayer.newMenuItem("Duplicate Selected Layer(s)")
        actions.deleteLayer.newMenuItem("Delete Selected Layer(s)")
        cmds.menuItem( divider=True)
        actions.mergeLayerDown.newMenuItem("Merge Layer Down")
        cmds.menuItem( divider=True)
        actions.moveLayerUp.newMenuItem("Move Current Layer Up")
        actions.moveLayerDown.newMenuItem("Move Current Layer Down")
        actions.enableDisableLayer.newMenuItem("Toggle Layer On/Off")
        cmds.menuItem( divider=True)
        actions.layerProperties.newMenuItem("Properties...")

    def influenceMenuChangeCommand(self,*args):
        '''
        right mouse button menu handler for "all influences/active influences"
        '''
        all = cmds.menuItem(self.controls.menuAllInfluences,q=True,radioButton=True)
        # update filter
        self.filterUi.radioAllInfluences.setValue(all)
        self.filterUi.radioActiveInfluences.setValue(not all)
        self.updateInfluenceList()
        
    def updateInfluenceMenuValues(self):
        '''
        updates right mouse button menu values with filter values
        '''
        cmds.menuItem(self.controls.menuAllInfluences,e=True,radioButton=self.filterUi.radioAllInfluences.getValue())
        cmds.menuItem(self.controls.menuActiveInfluences,e=True,radioButton=self.filterUi.radioActiveInfluences.getValue())
        
    def createInfluenceListRMBMenu(self):
        from ngSkinTools.ui.mainwindow import MainWindow
        actions = MainWindow.getInstance().actions
        
        self.controls.inflListMenu = cmds.popupMenu( parent=self.controls.influenceDisplay.control )
        actions.copyWeights.newMenuItem('Copy Influence Weights')
        actions.cutWeights.newMenuItem('Cut Influence Weights')
        actions.pasteWeightsAdd.newMenuItem('Paste Weights (Add)')
        actions.pasteWeightsSubstract.newMenuItem('Paste Weights (Substract)')
        actions.pasteWeightsReplace.newMenuItem('Paste Weights (Replace)')
        cmds.menuItem( divider=True)
        
        
        cmds.radioMenuItemCollection()
        self.controls.menuAllInfluences = cmds.menuItem(label='List All Influences',
                enable=True, radioButton=True,command=self.influenceMenuChangeCommand )
        self.controls.menuActiveInfluences = cmds.menuItem(label='List Only Active Influences',
                enable=True, 
                radioButton=False,command=self.influenceMenuChangeCommand )
        
        cmds.menuItem( divider=True)
        
        actions.convertMaskToTransparency.newMenuItem('Convert Mask to Transparency')
        actions.convertTransparencyToMask.newMenuItem('Convert Transparency to Mask')

        cmds.menuItem( divider=True)
        actions.invertPaintTarget.newMenuItem('Invert')
        cmds.menuItem( divider=True)
        
        
        actions.influenceFilter.newMenuItem('Show/Hide Influence Filter')
        
    def layerDropped(self,layers,newParent,itemBefore,itemAfter):
        '''
        final handler of drag-drop action in layers list
        '''
        
        mll = LayerDataModel.getInstance().mll
        
        with mll.batchUpdateContext():
            # first, order layers by index, and start the "drop" with lowest index
            layers = sorted(layers,key=lambda layer:mll.getLayerIndex(layer),reverse=True)
            
            if newParent:
                itemAfter = None
                itemBefore = newParent
    
            for layer in layers:
                # as layers are shifted, indexes change for target layers
                currentIndex = mll.getLayerIndex(layer)
                
                targetIndex = 0
                if itemAfter:
                    targetIndex = mll.getLayerIndex(itemAfter)+1
                elif itemBefore:
                    targetIndex = mll.getLayerIndex(itemBefore)
    
                # fix index when moving up            
                if targetIndex>currentIndex:
                    targetIndex -= 1
                    
                mll.setLayerIndex(layer,targetIndex)
                
                # for subsequent layers, drop after this layer
                itemBefore = layer
                itemAfter = None


    def createLayerListsUI(self,parent):
        cmds.setParent(parent)
        #self.outerFrame = cmds.frameLayout(label='Skinning Layers',collapsable=False,borderVisible=True,borderStyle="etchedIn",labelAlign="center")

        paneLayout = cmds.paneLayout(configuration="vertical2",width=100,height=200)
            
        

        leftForm = form = FormLayout()
        label = cmds.text("Layers:",align="left",font='boldLabelFont')
        list = self.controls.layerDisplay = LayersTreeView()
        list.onSelectionChanged.addHandler(self.layerSelectionChanged)
        list.itemDropped = self.layerDropped
        
        form.attachForm(label,10,0,None,Constants.MARGIN_SPACING_HORIZONTAL)
        form.attachForm(list.control,None,0,0,Constants.MARGIN_SPACING_HORIZONTAL)
        form.attachControl(list.control,label,3,None,None,None)
        
        cmds.setParent("..")
        rightForm = form = FormLayout()
        label = cmds.text("Influences:",align="left",font='boldLabelFont')
        

        list = self.controls.influenceDisplay = InfluencesTreeView(allowMultiSelection=True)
        list.onSelectionChanged.addHandler(self.execInfluenceSelected)
        
        self.createLayersListRMBMenu()
        self.createInfluenceListRMBMenu()

        form.attachForm(label,10,Constants.MARGIN_SPACING_HORIZONTAL,None,0)
        form.attachForm(list.control,None,Constants.MARGIN_SPACING_HORIZONTAL,0,0)
        form.attachControl(list.control,label,3,None,None,None)

        return paneLayout
    
    


    def createUI(self,parent):
        baseForm = FormLayout(parent=parent)
        self.baseLayout = baseForm
        self.controls.layerListsUI = self.createLayerListsUI(baseForm)

        
        self.filterUi = InfluenceFilterUi(self)
        self.filterUi.filterChanged.addHandler(self.updateInfluenceList)
        filterLayout = self.filterUi.createUI(baseForm)
        baseForm.attachForm(self.controls.layerListsUI, 0, 0, None, 0)
        baseForm.attachForm(filterLayout,None,0,0,0)
        baseForm.attachControl(self.controls.layerListsUI, filterLayout, None, None, Constants.MARGIN_SPACING_VERTICAL, None)

        LayerEvents.nameChanged.addHandler(self.updateLayerList,parent)
        LayerEvents.layerAvailabilityChanged.addHandler(self.update,parent)
        LayerEvents.layerListModified.addHandler(self.update,parent)
        LayerEvents.influenceListChanged.addHandler(self.updateInfluenceList,parent)
        MayaEvents.undoRedoExecuted.addHandler(self.update,parent)
        LayerEvents.currentLayerChanged.addHandler(self.currentLayerChangedHandler,parent)
        MayaEvents.nodeSelectionChanged.addHandler(self.update,parent)


        self.update()
        

    def getLayersList(self):
        return self.controls.layerDisplay
    
    def getSelectedInfluences(self):
        return self.controls.influenceDisplay.getSelectedNames()

    def getSelectedInfluenceIds(self):
        return self.controls.influenceDisplay.getSelectedIDs()
    
    def getSelectedLayers(self):
        '''
        returns IDs for selected layers
        '''
        return [int(i) for i in self.controls.layerDisplay.getSelectedIDs()]