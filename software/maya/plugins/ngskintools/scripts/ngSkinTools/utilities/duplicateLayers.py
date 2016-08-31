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
from ngSkinTools.mllInterface import MllInterface
import re

class DuplicateLayers:
    '''
    Layer duplication utility. Usage:
    
    .. code-block:: python
    
        mll = MllInterface()
        mll.setMesh('mesh1');
        
        u = DuplicateLayers()
        u.setMllInterface(mll)
        u.addLayer(1)
        u.addLayer(2)
        
        u.execute()
    
    '''
    
    def __init__(self):
        self.layerIds = []
        self.mll = MllInterface
        self.duplicateIds = []
        
    def setMllInterface(self,mll):
        self.mll = mll
        
    def addLayer(self,layerId):
        '''
        add layer to the list of layers to be duplicated
        '''
        
        self.layerIds.append(layerId)
        
    def sortLayerIds(self):
        '''
        sort added layers in order from bottom to top
        '''
        layerIndexes = [l[0] for l in self.mll.listLayers()]
        
        
        def comparator(id1,id2):
            return layerIndexes.index(id2)-layerIndexes.index(id1)
        
        self.layerIds = sorted(self.layerIds,comparator)
            
        
        
        
    def duplicateLayer(self,layerId):
        '''
        duplicates single layer
        '''
        oldName = self.mll.getLayerName(layerId)
        newLayer = self.mll.createLayer(self.createUniqueName(oldName))
        self.mll.setLayerEnabled(newLayer, self.mll.isLayerEnabled(layerId))
        self.mll.setLayerOpacity(newLayer, self.mll.getLayerOpacity(layerId))
        self.mll.setLayerMask(newLayer, self.mll.getLayerMask(layerId))
        self.mll.setDualQuaternionWeights(newLayer, self.mll.getDualQuaternionWeights(layerId))
        for _,influenceIndex in self.mll.listLayerInfluences(layerId):
            weights = self.mll.getInfluenceWeights(layerId, influenceIndex)
            self.mll.setInfluenceWeights(newLayer, influenceIndex, weights)
            
        self.duplicateIds.append(newLayer)
        
    def createLayerName(self,oldName):
        prefix=" copy"
        
        # copy already? add index
        if oldName.endswith(prefix):
            return oldName+"(2)"
        
        # indexing exists? increase value
        s=re.search('(.*)\\((\\d+)\\)$',oldName)
        if s!=None:
            return s.group(1)+"(%d)"%(int(s.group(2))+1,) 
        
        # nothing? just add default copy prefix then
        return oldName+prefix
    
    def createUniqueName(self,fromName):
        layerNames = [l[1] for l in self.mll.listLayers()]
        result = self.createLayerName(fromName)
        while result in layerNames:
            result = self.createLayerName(result)
            
        return result
        
        
    def execute(self):
        '''
        duplicate all layers that were added
        '''
        self.sortLayerIds()
        
        
        with self.mll.batchUpdateContext():
            for layerId in self.layerIds:
                self.duplicateLayer(layerId)
            
        