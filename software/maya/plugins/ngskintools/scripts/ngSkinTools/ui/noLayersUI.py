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

from maya import cmds,OpenMaya as om
from ngSkinTools.ui.uiWrappers import FormLayout, TextLabel
from ngSkinTools.ui.constants import Constants
from ngSkinTools.layerUtils import LayerUtils
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.events import MayaEvents, LayerEvents
from ngSkinTools.utils import Utils

class NoLayersUI:
    def __init__(self):
        self.data = LayerDataModel.getInstance()
        class Controls:
            pass
        self.controls = Controls()

    def execAttachLayerData(self,*args):
        self.data.attachLayerData()


    def createUI(self,parent):
        self.baseLayout = form = FormLayout(parent=parent)
        t1 = self.controls.label1 = TextLabel('',align=TextLabel.ALIGN_LEFT)
        t2 = self.controls.label2 = TextLabel('',align=TextLabel.ALIGN_LEFT)
        t2.setBold()
        b = self.controls.addLayerDataButton = cmds.button("Initialize Skinning Layers",command=self.execAttachLayerData)
        
        for i in (t1,t2,b):
            form.attachForm(i,None,Constants.MARGIN_SPACING_HORIZONTAL,None,Constants.MARGIN_SPACING_HORIZONTAL)
        form.attachForm(t1,Constants.MARGIN_SPACING_VERTICAL,None,None,None)
        form.attachControl(t2,t1,0,None,None,None)
        form.attachControl(b,t2,Constants.MARGIN_SPACING_VERTICAL,None,None,None)

        LayerEvents.layerAvailabilityChanged.addHandler(self.update,parent)
        MayaEvents.nodeSelectionChanged.addHandler(self.update,parent)
        MayaEvents.undoRedoExecuted.addHandler(self.update,parent)
        
    def update(self):
        if self.data.layerDataAvailable:
            return
        
        attachPoint = self.data.getLayersCandidateFromSelection()
        
        attachPossible = bool(attachPoint)
        selection = cmds.ls(sl=True,o=True)
        selectionAvailable = selection is not None and len(selection)>0
        
        if attachPossible:
            self.controls.label1.setLabel('Skin selected:')
            self.controls.label2.setLabel("%s (%s)" % tuple(map(Utils.shortName,tuple(attachPoint))))
        elif selectionAvailable:
            self.controls.label1.setLabel("Layer data cannot be attached to:")
            self.controls.label2.setLabel(Utils.shortName(selection[0]))
        else:
            self.controls.label1.setLabel("Nothing is selected")
            self.controls.label2.setLabel('')
        
        self.controls.label1.setEnabled(selectionAvailable)
        self.controls.label2.setEnabled(selectionAvailable)
        
        cmds.button(self.controls.addLayerDataButton,e=True,enable=attachPossible)
        