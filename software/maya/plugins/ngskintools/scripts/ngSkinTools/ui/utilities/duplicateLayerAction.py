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

class DuplicateLayersAction(BaseLayerAction):
    
    
    @Utils.visualErrorHandling
    @Utils.undoable
    @Utils.preserveSelection
    def execute(self):
        layerListsUi = LayerDataModel.getInstance().layerListsUI
        
        setup = DuplicateLayers()
        setup.setMllInterface(LayerDataModel.getInstance().mll)
        
        layers = layerListsUi.getSelectedLayers()
        if len(layers)==0:
            raise MessageException('No layers selected')
        
        for layer in reversed(layers):
            setup.addLayer(layer)
        setup.execute()
        
        LayerDataModel.getInstance().mll.setCurrentLayer(setup.duplicateIds[-1])
        
        LayerEvents.layerListModified.emit()
        
        
        
        