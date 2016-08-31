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

from maya import cmds,mel
from ngSkinTools.layerUtils import LayerUtils
from ngSkinTools.ui.events import LayerEvents, MayaEvents
from ngSkinTools.log import LoggerFactory
from ngSkinTools.mllInterface import MllInterface
from ngSkinTools.utilities.weightsClipboard import WeightsClipboard


class LayerDataModel:
    log = LoggerFactory.getLogger("layerDataModel")

    class MirrorCacheStatus:
        def __init__(self):
            self.isValid = None
            self.message = None
            self.mirrorAxis = None
    
    
    # holds instance of singleton object
    __instance = None
    
    @staticmethod
    def getInstance():
        '''
        returns singleton instance of LayerDataModel
        
        :rtype: LayerDataModel
        '''
        if LayerDataModel.__instance is None:
            LayerDataModel.__instance = LayerDataModel()
        
        return LayerDataModel.__instance
    
    @staticmethod
    def reset():
        LayerDataModel.__instance = None
    
    def __init__(self):
        self.layerListsUI = None # :type: LayerListsUI
        self.layerDataAvailable = None
        self.mirrorCache = self.MirrorCacheStatus()
        self.mll = MllInterface()
        self.clipboard = WeightsClipboard(self.mll)
        
        MayaEvents.undoRedoExecuted.addHandler(self.updateLayerAvailability)
        MayaEvents.nodeSelectionChanged.addHandler(self.updateLayerAvailability)
        
        self.updateLayerAvailability()
        
    def setLayerListsUI(self,ui):
        self.layerListsUI = ui
        
    def getSelectedLayer(self):
        if self.layerListsUI is None:
            return None
        return self.layerListsUI.getLayersList().getSelectedID()
    
    def getSelectedLayers(self):
        if self.layerListsUI is None:
            return []
        return self.layerListsUI.getSelectedLayers()
    
    def getSelectedInfluenceIds(self):
        if self.layerListsUI is None:
            return []
        return self.layerListsUI.getSelectedInfluenceIds()
    
    def updateLayerAvailability(self):
        '''
        checks if availability of skin layers changed with the 
        current scene selection 
        '''
        self.log.info("updating layer availability")
        

        oldValue = self.layerDataAvailable
        self.layerDataAvailable = self.mll.getLayersAvailable()
        if self.layerDataAvailable!=oldValue:
            LayerEvents.layerAvailabilityChanged.emit()
        self.updateMirrorCacheStatus()
        
    def updateMirrorCacheStatus(self):
        def setStatus(newStatus,message,axis=None):
            change = newStatus != self.mirrorCache.isValid or self.mirrorCache.message != message or self.mirrorCache.mirrorAxis != axis
              
            self.mirrorCache.message = message
            self.mirrorCache.isValid = newStatus
            self.mirrorCache.mirrorAxis = axis

            if change:
                self.log.info("mirror cache status changed to %s." % self.mirrorCache.message)
                LayerEvents.mirrorCacheStatusChanged.emit()        

        self.log.info("updating mirror cache status")
        if not self.layerDataAvailable:
            setStatus(False,"Layer Data is not available")
            return
        
        try:
            cacheInfo = cmds.ngSkinLayer(q=True,mirrorCacheInfo=True)
            if cacheInfo[0]=='ok':
                setStatus(True,'Mirror Data Initialized',cmds.ngSkinLayer(q=True,mirrorAxis=True))
            else:
                setStatus(False,cacheInfo[1])
        except :
            setStatus(False,'Cache check failed')
            #log.error("error: "+str(err))
        
            
    def addLayer(self,name):
        layerId = self.mll.createLayer(name)
        
        if layerId is None:
            return
        LayerEvents.layerListModified.emit()
        
        self.setCurrentLayer(layerId)
        
    def removeLayer(self,layerId):
        self.mll.deleteLayer(layerId)
        LayerEvents.layerListModified.emit()
        LayerEvents.currentLayerChanged.emit()
        
        
    def setCurrentLayer(self,layerId):
        self.mll.setCurrentLayer(layerId)
        LayerEvents.currentLayerChanged.emit()
        
    def getCurrentLayer(self):
        return self.mll.getCurrentLayer()
        
    def attachLayerData(self):
        self.mll.initLayers()
        self.addLayer('Base Weights')

        
        self.updateLayerAvailability() 

        
        
    def cleanCustomNodes(self):
        '''
        removes all custom nodes from current scene
        '''
        LayerUtils.deleteCustomNodes()
        
        self.updateLayerAvailability()
        
    def getLayerName(self,layerId):
        return mel.eval('ngSkinLayer -id %d -q -name' % layerId)       
    
    def setLayerName(self,layerId,name):
        self.mll.setLayerName(layerId,name)
        LayerEvents.nameChanged.emit()   

    def getLayerOpacity(self,layerId):
        return mel.eval('ngSkinLayer -id %d -q -opacity' % layerId)

    def getLayerEnabled(self,layerId):
        return mel.eval('ngSkinLayer -id %d -q -enabled' % layerId)
    
    def setLayerEnabled(self,layerId,enabled):
        cmds.ngSkinLayer(e=True,id=layerId,enabled=1 if enabled else 0)
        
    def toggleLayerEnabled(self,layerId):
        self.setLayerEnabled(layerId, not self.getLayerEnabled(layerId))
            
    def getLayersCandidateFromSelection(self):
        '''
        for given selection, returns mesh and skin cluster node names where skinLayer data
        is (or can be) attached. 
        '''
        return self.mll.getTargetInfo()

    
    def getLayersAvailable(self):
        self.updateLayerAvailability()
        return self.layerDataAvailable
    
    def isDqMode(self):
        '''
        returns True if current skin cluster is operating in dual quaternion mode
        '''
        target = self.mll.getTargetInfo()
        if not target:
            return False   
        skinCluster = target[1]     
        return cmds.skinCluster(skinCluster,q=True,skinMethod=True)==2    
        
