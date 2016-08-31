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
from maya import cmds,mel
from ngSkinTools.ui.events import Signal, LayerEvents, MayaEvents
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.dlgLayerProperties import LayerPropertiesDialog
from ngSkinTools.ui.basedialog import BaseDialog
from ngSkinTools.utils import Utils, MessageException
from ngSkinTools.ui.basetoolwindow import BaseToolWindow
from ngSkinTools.log import LoggerFactory
from ngSkinTools.ui.options import deleteCustomOptions
from ngSkinTools.mllInterface import MllInterface, MirrorDirection

log = LoggerFactory.getLogger("actions")


class BaseAction(object):
    def __init__(self,ownerUI):
        self.ownerUI = ownerUI
        self.onExecuted = Signal("action executed")
        self.updateControls = []

    def addUpdateControl(self,control,menu=False):
        self.updateControls.append((control,menu))
    
    def isEnabled(self):
        '''
        override this method to provide enabled/disabled state of this action
        '''
        return True;    
    
    def updateEnabled(self):
        '''
        triggers update on this action's enabled state, and updates controls with that state
        '''
        
        enabled = self.isEnabled()
        for i in self.updateControls:
            if i[1]:
                cmds.menuItem(i[0],e=True,enable=enabled)
            else:
                cmds.control(i[0],e=True,enable=enabled)
                
    def createUiCommand(self):
        cmd = lambda *args:self.execute()
        cmd.__name__ = "Action_"+self.__class__.__name__;
        cmd.__str__ = lambda: "Action_"+self.__class__.__name__;
        cmd.__repr__ = cmd.__str__
        cmd.__unicode__ = cmd.__str__
        
        return cmd
                
    def newMenuItem(self,label):
        menuItem = cmds.menuItem( label=label,command=self.createUiCommand())
        self.addUpdateControl(menuItem,True)
                
    def execute(self):
        pass

class BaseLayerAction(BaseAction):
    '''
    base for layer actions - 
    enables or disables controls based on layers availability
    '''
    
    def __init__(self,ownerUI):
        BaseAction.__init__(self,ownerUI)
        LayerEvents.layerAvailabilityChanged.addHandler(self.updateEnabled,self.ownerUI)

    def isEnabled(self):
        return LayerDataModel.getInstance().layerDataAvailable     
        
class InfluenceFilterAction(BaseLayerAction):
    
    def execute(self):
        from ngSkinTools.ui.mainwindow import MainWindow
        MainWindow.getInstance().targetUI.layersUI.filterUi.toggle() 
        self.onExecuted.emit(True)
        
        
class NewLayerAction(BaseLayerAction):
    def execute(self):
        defaultLayerName = "New Layer"
        dlg = LayerPropertiesDialog(newLayerMode=True)
        dlg.layerNameValue.set("")
        if dlg.execute()!=dlg.BUTTON_OK:
            return
        
        newLayerName = dlg.layerNameValue.get()
        if newLayerName.strip()=="":
            newLayerName = defaultLayerName
        LayerDataModel.getInstance().addLayer(newLayerName)
        self.onExecuted.emit()
        
class EnableDisableLayerAction(BaseLayerAction):
    def execute(self):
        layerData = LayerDataModel.getInstance()
        for layerId in layerData.layerListsUI.getSelectedLayers():
            layerData.toggleLayerEnabled(layerId)
        LayerEvents.layerListModified.emit()
        self.onExecuted.emit()

class LayerPropertiesAction(BaseLayerAction):
    def onOpacitySliderChange(self):
        '''
        emits when opacity slider in the dialog changes value
        '''
        currLayer = LayerDataModel.getInstance().getCurrentLayer()
        if currLayer is not None:
            cmds.ngSkinLayer(e=True,id=currLayer,opacity=self.dlg.layerOpacityValue.get())
        
        
    def execute(self):
        data = LayerDataModel.getInstance()

        currLayer = data.getCurrentLayer()
        if currLayer is None or currLayer==0:
            return;

        
        self.dlg = LayerPropertiesDialog(newLayerMode=False)
        
        self.dlg.layerNameValue.set("Layer Properties")
        self.dlg.layerNameValue.set(data.getLayerName(currLayer))

        initialOpacity = data.getLayerOpacity(currLayer)
        self.dlg.layerOpacityValue.set(initialOpacity)
        self.dlg.onOpacityChange.addHandler(self.onOpacitySliderChange)
        
        
        if self.dlg.execute()!=BaseDialog.BUTTON_OK:
            # dialog canceled: rollback changes and exit
            cmds.ngSkinLayer(e=True,id=currLayer,opacity=initialOpacity)
            return
        
        # dialog confirmed - apply changes
        data.setLayerName(currLayer,self.dlg.layerNameValue.get())
        self.onExecuted.emit()

class DeleteLayerAction(BaseLayerAction):
    @Utils.visualErrorHandling
    @Utils.undoable
    def execute(self):
        for layerId in LayerDataModel.getInstance().layerListsUI.getSelectedLayers():
            LayerDataModel.getInstance().removeLayer(layerId)
        
        self.onExecuted.emit()
            
class MoveLayerAction(BaseLayerAction):
    '''
    UI action: moves layer up or down
    '''
    
    def __init__(self,directionUp,ownerUI):
        BaseLayerAction.__init__(self,ownerUI)
        self.isUp = directionUp
        LayerEvents.currentLayerChanged.addHandler(self.updateEnabled,self.ownerUI)
        LayerEvents.layerListModified.addHandler(self.updateEnabled,self.ownerUI)
        
    def execute(self):
        newIndex = cmds.ngSkinLayer(q=True,layerIndex=True)+(1 if self.isUp else -1)
        if newIndex<0:
            newIndex=0
        cmds.ngSkinLayer(layerIndex=newIndex)
        self.updateEnabled()
        LayerEvents.layerListModified.emit()
        self.onExecuted.emit()
        
    def isEnabled(self):
        '''
        disable if reorder in given direction cannot happen
        '''
        # do nothing if already disabled
        if not BaseLayerAction.isEnabled(self):
            return False
        
        try:
            currIndex = cmds.ngSkinLayer(q=True,layerIndex=True)
        except:
            return False 
        
        # for "down", index has to be above 0
        if not self.isUp:
            return currIndex>0
        
        # for "up", index has to be <parent.numChildren-1
        parent = cmds.ngSkinLayer(q=True,parent=True)
        # python does not support values with query params
        #numChildren = cmds.ngSkinLayer(id=parent,q=True,nch=True)
        numChildren = mel.eval("ngSkinLayer -id %d -q -nch" %parent)
        return currIndex<(numChildren-1)

        
class ConvertTransparencyToMaskAction(BaseLayerAction):
    @Utils.undoable
    def execute(self):
        cmds.ngSkinLayer(ttm=True)

class ConvertMaskToTransparencyAction(BaseLayerAction):
    @Utils.undoable
    def execute(self):
        cmds.ngSkinLayer(mtt=True)
        
class InvertPaintTargetAction(BaseLayerAction):
    @Utils.undoable
    def execute(self):
        layerData = LayerDataModel.getInstance()
        layerId = layerData.getCurrentLayer()
        influences = layerData.getSelectedInfluenceIds()
        
        zeroWeights = [0]*layerData.mll.getVertCount()
        prevWeights = {}
        
        if None in influences:
            raise Exception("fail")
        
        with layerData.mll.batchUpdateContext():
            for paintTarget in influences:
                prevWeights[paintTarget] = layerData.mll.getInfluenceWeights(layerId, paintTarget)
                if (prevWeights[paintTarget]):
                    layerData.mll.setInfluenceWeights(layerId, paintTarget, zeroWeights)
                    
            for paintTarget in influences:
                if not prevWeights[paintTarget]:
                    continue
                weights = [1-i for i in prevWeights[paintTarget]]
                layerData.mll.setInfluenceWeights(layerId, paintTarget, weights)
        
class MirrorLayerWeightsAction(BaseLayerAction):

    
    def __init__(self, ownerUI):
        BaseLayerAction.__init__(self, ownerUI)
        LayerEvents.mirrorCacheStatusChanged.addHandler(self.updateEnabled,self.ownerUI)
        
    def isEnabled(self):
        model = LayerDataModel.getInstance()
        if model is None:
            return False
        if not model.mirrorCache.isValid:
            return False
        return BaseLayerAction.isEnabled(self)
    
    def execute(self):
        '''
        button handler for "Mirror Skin Weights"
        '''
        from ngSkinTools.ui.mainwindow import MainWindow
        from ngSkinTools.ui.tabMirror import TabMirror
        

        # any problems? maybe cache is not initialized/outdated?
        layerData = LayerDataModel.getInstance() 
        layerData.updateMirrorCacheStatus()
        if not layerData.mirrorCache.isValid:
            Utils.displayError(layerData.mirrorCache.message)
            return False

        try:
            mirrorTab = MainWindow.getInstance().tabMirror
            
            mirrorDirection = MirrorDirection.DIRECTION_POSITIVETONEGATIVE
            if mirrorTab.controls.mirrorDirection.getValue()==0: # guess
                mirrorDirection = MirrorDirection.DIRECTION_GUESS;
            if mirrorTab.controls.mirrorDirection.getValue()==2: # negative to positive
                mirrorDirection = MirrorDirection.DIRECTION_NEGATIVETOPOSITIVE;
            if mirrorTab.controls.mirrorDirection.getSelectedText()==TabMirror.MIRROR_FLIP: 
                mirrorDirection = MirrorDirection.DIRECTION_FLIP;
            
            with LayerDataModel.getInstance().mll.batchUpdateContext():
                for layerId in LayerDataModel.getInstance().layerListsUI.getSelectedLayers():
                    LayerDataModel.getInstance().mll.mirrorLayerWeights(layerId,
                            mirrorWidth=mirrorTab.controls.mirrorWidth.getValue(),
                            mirrorLayerWeights=mirrorTab.controls.mirrorWeights.getValue(),
                            mirrorLayerMask=mirrorTab.controls.mirrorMask.getValue(),
                            mirrorDualQuaternion=mirrorTab.controls.mirrorDq.getValue(),
                            mirrorDirection=mirrorDirection
                        )

            # if layer list is filtered, might be handy to refresh influence list now - not that it costs much
            LayerEvents.influenceListChanged.emit()
            
            return True
        except:
            import traceback;traceback.print_exc();
            Utils.displayError("unknown error")
            # we're not sure what's wrong in this case, just re-raise
            raise        




class RemovePreferencesAction(BaseAction):
    def execute(self):
        from maya import utils as mu
        from ngSkinTools.ui.mainwindow import MainWindow
        
        BaseToolWindow.closeAllWindows()
        
        deleteCustomOptions()
        
        mu.executeDeferred(MainWindow.open)
        

class BaseImportExportAction(BaseLayerAction):
    def __init__(self,ownerUI,ioFormat):
        BaseLayerAction.__init__(self, ownerUI)
        MayaEvents.nodeSelectionChanged.addHandler(self.updateEnabled, self.ownerUI)
        self.ioFormat = ioFormat


    def selectFile(self,forSave):
        '''
        shows UI for file selection; returns file name or None 
        '''
        extensionList = " ".join(map(lambda a: "*.%s" % a,self.ioFormat.recommendedExtensions))
        caption = ('Export as %s' if forSave else 'Import from %s') %self.ioFormat.title
        fileFilter = 'Layer data in %s format (%s);;All Files (*.*)' % (self.ioFormat.title,extensionList)
        
        result = cmds.fileDialog2(dialogStyle=1,caption=caption,fileFilter=fileFilter,fileMode=0 if forSave else 1,returnFilter=True)
        if result is None:
            return None
        return result[0]
            
    def getTargetMesh(self):            
        return LayerDataModel.getInstance().getLayersCandidateFromSelection()[0]
    
    def getDataModel(self):
        return LayerDataModel.getInstance()
    
    def getMll(self):
        return self.getDataModel().mll
            
class ExportAction(BaseImportExportAction):
    
    def execute(self):
        if not LayerDataModel.getInstance().getLayersAvailable():
            raise Exception("layers data not available")
        
        fileName = self.selectFile(forSave=True)
        if fileName is None:
            return

        import ngSkinTools.importExport as ie 
        model = ie.LayerData()
        
        model.loadFrom(self.getTargetMesh())
        
        exporter = self.ioFormat.exporterClass()
        
        f = open(fileName,'w')
        try:
            f.write(exporter.process(model))
        finally:
            f.close();
            
class ImportAction(BaseImportExportAction):
    
    def isEnabled(self):
        self.targetInfo = self.getMll().getTargetInfo() 
        return self.targetInfo !=None
    
    def getFileContents(self,fileName):
        f = open(fileName,'r')
        try:
            contents = ''.join(f.readlines())
        finally:
            f.close();
            
        return contents
    
    def doImport(self,fileName,destinationMesh):
        '''
        initiates import and returns import (TransferWeightsWindow) dialog instance
        '''
        log.info("importing from '%s' on to %s" % (fileName,destinationMesh))
        
        importer = self.ioFormat.importerClass()
        model = importer.process(self.getFileContents(fileName))
        
        from ngSkinTools.ui.initTransferWindow import TransferWeightsWindow
        window = TransferWeightsWindow.getInstance()
        window.showWindow()
        window.content.dataModel.setSourceData(model)
        window.content.dataModel.setDestinationMesh(destinationMesh)
        return window
        
    @Utils.undoable
    def execute(self):
        if not self.isEnabled():
            raise Exception("Import not possible for current selection")
        
        fileName = self.selectFile(forSave=False)
        if fileName is None:
            return
        
        self.doImport(fileName,self.targetInfo[0])
        
        
class TransferWeightsAction(BaseAction):
    
    def isEnabled(self):
        return True
    
    @Utils.visualErrorHandling
    @Utils.undoable
    def execute(self):
        meshes = cmds.ls(sl=True)
        if meshes==None or len(meshes)!=2:
            raise MessageException("select two skinned meshes with layers initialized to perform this operation")
        
        for mesh in meshes:
            if not MllInterface(mesh=meshes[0]).getLayersAvailable():
                raise MessageException("'%s' is not a valid selection (no skin layers available)" % mesh)

        from ngSkinTools.ui.initTransferWindow import TransferWeightsWindow
        window = TransferWeightsWindow.getInstance()
        window.showWindow()
        window.content.dataModel.setSourceMesh(meshes[0])
        window.content.dataModel.setDestinationMesh(meshes[1])
                    
        
class MergeLayerDownAction(BaseLayerAction):
    
    @Utils.visualErrorHandling
    @Utils.undoable
    def execute(self):
        ldm = LayerDataModel.getInstance()
        for layerId in ldm.layerListsUI.getSelectedLayers():
            if ldm.mll.getLayerIndex(layerId)==0:
                Utils.displayError("Cannot merge lowest layer")
                return
            
            ldm.mll.layerMergeDown(layerId)
            
            
        
            
        LayerEvents.layerListModified.emit()
        self.onExecuted.emit()