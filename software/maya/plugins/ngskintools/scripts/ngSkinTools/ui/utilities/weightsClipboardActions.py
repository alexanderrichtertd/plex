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

from ngSkinTools.ui.actions import BaseLayerAction
from ngSkinTools.utils import Utils, MessageException
from ngSkinTools.utilities.duplicateLayers import DuplicateLayers
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.events import LayerEvents
from ngSkinTools.ui.layerListsUI import LayerListsUI

class CopyWeights(BaseLayerAction):
    @Utils.visualErrorHandling
    @Utils.undoable
    @Utils.preserveSelection
    def execute(self):
        LayerDataModel.getInstance().clipboard.withCurrentLayerAndInfluence().copy()


class CutWeights(BaseLayerAction):
    
    @Utils.visualErrorHandling
    @Utils.undoable
    @Utils.preserveSelection
    def execute(self):
        LayerDataModel.getInstance().clipboard.withCurrentLayerAndInfluence().cut()

class PasteWeightsAdd(BaseLayerAction):
    
    @Utils.visualErrorHandling
    @Utils.undoable
    @Utils.preserveSelection
    def execute(self):
        LayerDataModel.getInstance().clipboard.withCurrentLayerAndInfluence().pasteAdd()

class PasteWeightsSubstract(BaseLayerAction):
    
    @Utils.visualErrorHandling
    @Utils.undoable
    @Utils.preserveSelection
    def execute(self):
        LayerDataModel.getInstance().clipboard.withCurrentLayerAndInfluence().pasteSubstract()

class PasteWeightsReplace(BaseLayerAction):
    
    @Utils.visualErrorHandling
    @Utils.undoable
    @Utils.preserveSelection
    def execute(self):
        LayerDataModel.getInstance().clipboard.withCurrentLayerAndInfluence().pasteReplace()
