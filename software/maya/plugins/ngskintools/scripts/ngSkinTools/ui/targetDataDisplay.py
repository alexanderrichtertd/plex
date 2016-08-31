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

from maya import cmds
from ngSkinTools.ui.layerListsUI import LayerListsUI
from ngSkinTools.ui.noLayersUI import NoLayersUI
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.events import LayerEvents
from ngSkinTools.ui.uiWrappers import FormLayout

class TargetDataDisplay:
    '''
    Manages UI for either layer lists or "no layers available" UI
    '''
    
    def __init__(self):
        self.layersUI = LayerListsUI()
        self.noLayersUI = NoLayersUI()
        self.data = LayerDataModel.getInstance() 
        

    def updateUiVisibility(self):
        cmds.layout(self.noLayersUI.baseLayout,e=True,visible=self.data.layerDataAvailable==False) # 3rd option is none, hence weird compares
        cmds.layout(self.layersUI.baseLayout,e=True,visible=self.data.layerDataAvailable==True)
    
    def create(self,parent):
        LayerEvents.layerAvailabilityChanged.addHandler(self.updateUiVisibility,parent)
        result = self.uiSwitchLayout = FormLayout(parent=parent)

        self.noLayersUI.createUI(self.uiSwitchLayout)
        result.attachForm(self.noLayersUI.baseLayout, 0, 0, 0, 0)
        self.layersUI.createUI(self.uiSwitchLayout)
        result.attachForm(self.layersUI.baseLayout, 0, 0, 0, 0)
        
        self.noLayersUI.update()
        self.layersUI.update()
        self.updateUiVisibility()
        
        
        return result
        
    def getSelectedInfluences(self):
        if self.data.layerDataAvailable:
            return self.layersUI.getSelectedInfluences()
        
        return []
    
