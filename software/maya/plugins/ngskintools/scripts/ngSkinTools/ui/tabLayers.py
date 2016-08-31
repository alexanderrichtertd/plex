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

from maya import cmds, mel,OpenMaya as om
from ngSkinTools.ui.basetab import BaseTab
from ngSkinTools.utils import Utils
from ngSkinTools.ui.uiWrappers import FloatField, FormLayout, CheckBoxField,\
    TextLabel, TextEdit
from ngSkinTools.ui.constants import Constants
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.events import LayerEvents, MayaEvents


class LayerProperties:
    def __init__(self,data):
        self.data = data
        class Controls:
            pass
        self.controls = Controls()
        
    
    def layerNameChanged(self):
        currLayer = self.data.getCurrentLayer()
        if currLayer is not None:
            name = self.controls.layerName.getValue().strip()
            cmds.ngSkinLayer(e=True,id=currLayer,name=name)
            LayerEvents.nameChanged.emit()


    def layerOpacityChanged(self):
        currLayer = self.data.getCurrentLayer()
        if currLayer is not None:
            value = self.controls.layerOpacity.getValue()
            cmds.ngSkinLayer(e=True,id=currLayer,opacity=value)
            cmds.floatSlider(self.controls.sliderIntensity,e=True,value=value)
        
    def layerOpacitySliderChanged(self,*args):
        self.controls.layerOpacity.setValue(cmds.floatSlider(self.controls.sliderIntensity,q=True,value=True))
        self.layerOpacityChanged()
        
    def createUI(self,tab,parent):
        LayerEvents.currentLayerChanged.addHandler(self.update,parent)
        LayerEvents.layerListUIUpdated.addHandler(self.update,parent)
        MayaEvents.undoRedoExecuted.addHandler(self.update,parent)

        group = tab.createUIGroup(parent, "Layer Properties")
        cmds.setParent(group)
        
        cmds.rowLayout(parent=group,nc=2,adjustableColumn=2,columnWidth2=[Constants.MARGIN_COLUMN2,50], columnAttach2=["both","left"],columnAlign2=["right","left"])
        TextLabel('Layer name:')
        self.controls.layerName = TextEdit()
        self.controls.layerName.changeCommand.addHandler(self.layerNameChanged)

        cmds.rowLayout(parent=group,adjustableColumn=3,nc=3,columnWidth3=[Constants.MARGIN_COLUMN2,50,100], columnAttach3=["both","left","both"],columnAlign3=["right","left","center"])
        TextLabel('Opacity:')
        self.controls.layerOpacity = FloatField(None, minValue=0.0, maxValue=1.0, step=0.1, defaultValue=1.0, annotation="overall intensity of this layer")
        self.controls.layerOpacity.changeCommand.addHandler(self.layerOpacityChanged)
        self.controls.sliderIntensity = cmds.floatSlider(min=0, max=1, step=0.05, value=1.0,cc=self.layerOpacitySliderChanged,dc=self.layerOpacitySliderChanged,annotation='Drag slider to change layer opacity' )
        
    def update(self):
        if not self.data.layerDataAvailable:
            return
        
        currLayer = self.data.getCurrentLayer()
        if currLayer is not None and currLayer>0:
            # looks like python version of command does not supply querying with parameters
            name = mel.eval('ngSkinLayer -id %d -q -name' % currLayer)
            self.controls.layerName.setValue(name)
            opacity = mel.eval('ngSkinLayer -id %d -q -opacity' % currLayer)
            self.controls.layerOpacity.setValue(opacity)
            cmds.floatSlider(self.controls.sliderIntensity,e=True,value=opacity)
        
        
class TabLayers(BaseTab):
    # prefix for environment variables for this tab
    VAR_LAYERS_PREFIX = 'ngSkinToolsLayersTab_'
    
    def __init__(self):
        BaseTab.__init__(self)
        self.layerDataModel = LayerDataModel.getInstance()
    


        
        
    def execAddWeightsLayer(self,*args):
        self.layerDataModel.addLayer('New Layer')

        
    def execRemoveLayer(self,*params):
        id = self.layerDataModel.getCurrentLayer()
        if id is None:
            return
        self.layerDataModel.removeLayer(id)
        
        
        
    def createManageLayersGroup(self,parent):
        group = self.createUIGroup(parent, "Manager Layers")
        buttonForm = FormLayout(parent=group,numberOfDivisions=100,height=Constants.BUTTON_HEIGHT)
        buttons = []
        buttons.append(cmds.button(label="Add Layer",command=self.execAddWeightsLayer))
        buttons.append(cmds.button(label="Del Layer",command=self.execRemoveLayer))
        self.layoutButtonForm(buttonForm, buttons)
        
    def createLayerOrderGroup(self,parent):
        group = self.createUIGroup(parent, "Layer Ordering")
        buttonForm = FormLayout(parent=group,numberOfDivisions=100,height=Constants.BUTTON_HEIGHT)
        buttons = []
        buttons.append(cmds.button(label="Move Up",command=self.moveLayerUp))
        buttons.append(cmds.button(label="Move Down",command=self.moveLayerDown))
        self.layoutButtonForm(buttonForm, buttons)
        


    def layersAvailableHandler(self):
        cmds.layout(self.baseLayout,e=True,enable=LayerDataModel.getInstance().layerDataAvailable)
        
        
    def moveLayer(self,up=True):
        newIndex = cmds.ngSkinLayer(q=True,layerIndex=True)+(1 if up else -1)
        if newIndex<0:
            newIndex=0
        cmds.ngSkinLayer(layerIndex=newIndex)
        LayerEvents.layerListModified.emit()
        
    def moveLayerUp(self,*args):
        self.moveLayer(True)
        
    def moveLayerDown(self,*args):
        self.moveLayer(False)
    
    def createUI(self,parent):
        self.setTitle('Layers')
        
        LayerEvents.layerAvailabilityChanged.addHandler(self.layersAvailableHandler,parent)
        
        result = self.baseLayout = self.createScrollLayout(parent)
        layout = cmds.columnLayout(adjustableColumn=1)
        
        #self.createManageLayersGroup(layout)
        
        self.layerPropertiesUI = LayerProperties(self.layerDataModel)
        self.layerPropertiesUI.createUI(self,layout)
        
        #self.createLayerOrderGroup(layout)
        
        
        

        self.layerPropertiesUI.update()
        return result
        