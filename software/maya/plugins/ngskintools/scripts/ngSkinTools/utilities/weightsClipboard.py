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

from ngSkinTools.utils import MessageException
from ngSkinTools.log import LoggerFactory
from ngSkinTools.layerUtils import NamedPaintTarget

log = LoggerFactory.getLogger("WeightsClipboard")
class WeightsClipboard:
    def __init__(self,mllInterface):
        '''
        :param MllInterface mllInterface: 
        '''
        self.copiedWeights = None
        self.mll = mllInterface
        self.layer = None
        self.influence = None
        
    

    def withCurrentLayerAndInfluence(self):
        '''
        :rtype: WeightsClipboard
        '''
        self.layer = self.mll.getCurrentLayer()
        log.debug("weights clipboard setting current layer to %r" % self.layer)
        self.influence = self.mll.getCurrentPaintTarget()
        log.debug("weights clipboard setting current influence to %r" % self.influence)
        return self
    
    def getPaintTargetWeights(self,paintTarget):
        if paintTarget==NamedPaintTarget.MASK:
            return self.mll.getLayerMask(self.layer)
        elif paintTarget==NamedPaintTarget.DUAL_QUATERNION:
            return self.mll.getDualQuaternionWeights(self.layer)
        else:
            return self.mll.getInfluenceWeights(self.layer,paintTarget)

    def copy(self):
        self.copiedWeights = self.getPaintTargetWeights(self.influence)
        
        log.debug("copied weights: %r" % self.copiedWeights)
        if len(self.copiedWeights)==0:
            self.copiedWeights = None
            raise MessageException("Nothing copied")
    
    def cut(self):
        self.copy()
        
        vertexSelection = self.mll.getVertexSelectionWeights()
        if vertexSelection is None:
            newWeights = [0.0]*len(self.copiedWeights)
        else:
            newWeights = [(1-v)*w for v,w in zip(vertexSelection,self.copiedWeights)]
        self.mll.setInfluenceWeights(self.layer, self.influence, newWeights)
        
    def __paste__(self,weightsCalculator):
        if self.copiedWeights == None:
            raise MessageException("Nothing to paste")
        
        if self.mll.getVertCount()!=len(self.copiedWeights):
            raise MessageException("Could not paste weights - vertex count does not match")
        
        prevWeights = self.getPaintTargetWeights(self.influence)
        vertSelection = self.mll.getVertexSelectionWeights()        
        newWeights = weightsCalculator(prevWeights)
        if newWeights is None:
            return 
        if vertSelection is not None:
            for i in range(len(vertSelection)):
                newWeights[i] = newWeights[i]*vertSelection[i]+prevWeights[i]*(1-vertSelection[i])
                
        
        if self.influence==NamedPaintTarget.MASK:
            self.mll.setLayerMask(self.layer, newWeights)
        if self.influence==NamedPaintTarget.DUAL_QUATERNION:
            self.mll.setDualQuaternionWeights(self.layer, newWeights)
        else:
            self.mll.setInfluenceWeights(self.layer, self.influence, newWeights)
        
    def pasteReplace(self):
        def calc(prevWeights):
            return self.copiedWeights
        self.__paste__(calc)

    def pasteAdd(self):
        def calc(prevWeights):
            if not prevWeights: # only sum if previous weights existed
                return self.copiedWeights
            return [a+b for a,b in zip(self.copiedWeights,prevWeights)]
            
        self.__paste__(calc)

    def pasteSubstract(self):
        def calc(prevWeights):
            if not prevWeights:
                return None
            return [max(0,b-a) for a,b in zip(self.copiedWeights,prevWeights)]
            
        self.__paste__(calc)

        