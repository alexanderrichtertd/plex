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
from ngSkinTools.utils import Utils, MessageException
from ngSkinTools.ui.basetab import BaseTab
from ngSkinTools.doclink import SkinToolsDocs
from ngSkinTools.ui.intensityslider import IntensitySlider
from ngSkinTools.ui.uiWrappers import IntField, CheckBoxField, \
    RadioButtonField, FormLayout, Layout, FloatField
from ngSkinTools.ui.constants import Constants
from ngSkinTools.ui.softSelectionRow import SoftSelectionRow
from ngSkinTools.importExport import LayerData
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.events import LayerEvents, MayaEvents

     

class TabSettings(BaseTab):
    '''
    '''
    
    # prefix for preset variables for this tab
    SETTINGS_PREFIX = 'ngSkinToolsSettingsTab_'
    
    def __init__(self):
        BaseTab.__init__(self)
        
    def updateUIEnabled(self):
        layersAvailable = LayerDataModel.getInstance().getLayersAvailable()
        
        Layout.setEnabled(self.controls.selectedSkinSettingsGroup,layersAvailable)
        if not layersAvailable:
            return
        
        self.controls.influenceLimitRow.setEnabled(self.controls.useInfluenceLimit.getModelValue())
        self.controls.pruneFilterRow.setEnabled(self.controls.usePruneFilter.getModelValue())
        
    def applyCurrentSkinSettings(self):
        limit = 0 if not self.controls.useInfluenceLimit.isChecked() else self.controls.numMaxInfluences.getModelValue()
        LayerDataModel.getInstance().mll.setInfluenceLimitPerVertex(limit)

        pruneFilter = 0.00 if not self.controls.usePruneFilter.isChecked() else self.controls.pruneFilterValue.getModelValue()
        LayerDataModel.getInstance().mll.setPruneWeightsFilter(threshold=pruneFilter)
        
        self.updateUIEnabled()
        
    def refreshSettingsFromSelection(self):
        layersAvailable = LayerDataModel.getInstance().getLayersAvailable()

        currentLimit = 0 if not layersAvailable else LayerDataModel.getInstance().mll.getInfluenceLimitPerVertex()
        self.controls.numMaxInfluences.setValue(max(3,currentLimit))
        self.controls.useInfluenceLimit.setValue(currentLimit!=0)
        
        pruneFilterValue = 0 if not layersAvailable else LayerDataModel.getInstance().mll.getPruneWeightsFilter()
        self.controls.pruneFilterValue.setValue(max(0.01,min(1,pruneFilterValue)))
        self.controls.usePruneFilter.setValue(pruneFilterValue!=0)
        
        self.updateUIEnabled()

    def createUI(self, parent):
        self.setTitle('Settings')
        self.outerLayout = FormLayout()
        scrollLayout = BaseTab.createScrollLayout(self.outerLayout)
        self.baseLayout = cmds.columnLayout(adjustableColumn=1)
        self.outerLayout.attachForm(scrollLayout, 0, 0, 0, 0)
        
        
        self.controls.selectedSkinSettingsGroup = group = self.createUIGroup(self.baseLayout, 'Selected Skin Settings')

        self.controls.useInfluenceLimit = CheckBoxField(None,defaultValue=0,label="Use maximum influences per vertex limit",
                annotation='Turn this on to enforce a max influences per vertex limit')
        self.controls.useInfluenceLimit.changeCommand.addHandler(self.updateUIEnabled, ownerUI=parent)
        self.controls.influenceLimitRow = self.createFixedTitledRow(group, 'Influence limit')
        self.controls.numMaxInfluences = IntField(None,minValue=1,maxValue=None,annotation="Number of max influences per vertex")

        cmds.setParent(group)
        self.controls.usePruneFilter = CheckBoxField(None,defaultValue=0,label="Prune small weights before writing to skin cluster")
        self.controls.usePruneFilter.changeCommand.addHandler(self.updateUIEnabled, ownerUI=parent)
        self.controls.pruneFilterRow = self.createFixedTitledRow(group, 'Prune below')
        self.controls.pruneFilterValue = FloatField(None,minValue=0.0,defaultValue=.01,maxValue=1.0,step=0.01, annotation="Influence values lower than this limit will be set to zero")

        
        cmds.setParent(group)
        cmds.rowLayout(nc=2,adjustableColumn=2,columnWidth2=[Constants.BUTTON_WIDTH_SMALL,50], columnAttach2=["both","both"],columnAlign2=["center","center"])
        BaseTab.createHelpButton(SkinToolsDocs.CURRENTSKINSETTINGS_INTERFACE)
        cmds.button(height=Constants.BUTTON_HEIGHT,label='Apply',command=lambda *args:self.applyCurrentSkinSettings())        
        
        LayerEvents.layerAvailabilityChanged.addHandler(self.refreshSettingsFromSelection, parent)
        MayaEvents.nodeSelectionChanged.addHandler(self.refreshSettingsFromSelection,parent)
        MayaEvents.undoRedoExecuted.addHandler(self.refreshSettingsFromSelection,parent)
        
        self.refreshSettingsFromSelection()
        
        cmds.setParent(parent)
        
        return self.outerLayout
