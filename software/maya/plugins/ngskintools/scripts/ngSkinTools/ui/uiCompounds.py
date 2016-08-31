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
from ngSkinTools.ui.events import Signal
from ngSkinTools.ui.uiWrappers import FloatField

class FloatSliderField:
    '''
    Similar to float slider group, only without caption
    '''
    
    def __init__(self,range=[0.0,1.0]):
        assert(len(range)==2)
        
        self.model = None
        self.floatField = None
        self.slider = None
        self.onChange = Signal()
        self.onChanging = Signal()
        self.range = range
        self.flexibleRange=False
        
    def updateModel(self):
        if self.model is not None:
            self.model.set(self.getValue())
        
    def sliderChanging(self,*args):
        '''
        handler for when float slider value is dragged
        '''
        self.floatField.setValue(cmds.floatSlider(self.slider,q=True,value=True))
        self.updateModel()
        self.onChanging.emit()
        
    def sliderChanged(self,*args):
        self.updateModel()
        self.onChange.emit()
        
    def __updateSliderValue(self):
        value = self.floatField.getValue()
        minValue = cmds.floatSlider(self.slider,q=True,minValue=True)
        maxValue = cmds.floatSlider(self.slider,q=True,maxValue=True)
        if self.flexibleRange:
            #change min/max, if needed
            cmds.floatSlider(self.slider,e=True,minValue=min(value,minValue),maxValue=max(value,maxValue))
        else:
            #change value, if needed
            value = min(maxValue,max(value,minValue))
            
        cmds.floatSlider(self.slider,e=True,value=self.floatField.getValue())

    def fieldChanged(self):
        '''
        handler for when float field value changes
        '''
        self.__updateSliderValue()
        self.updateModel()
        self.onChange.emit()
    
    def create(self):
        result =self.mainLayout= cmds.rowLayout(nc=2,adjustableColumn=2)
        step = (self.range[1]-self.range[0])/100.0;
        
        self.floatField = FloatField(self.model,step=step)
        if not self.flexibleRange:
            self.floatField.editUI(minValue=self.range[0],maxValue=self.range[1])
            
        self.floatField.changeCommand.addHandler(self.fieldChanged)
        self.slider = cmds.floatSlider(value=self.floatField.getValue(),
                                       dragCommand=self.sliderChanging,changeCommand=self.sliderChanged,
                                       step=step,
                                       minValue=self.range[0],maxValue=self.range[1]
                                       )
        
        self.__updateSliderValue()
        return result
    
    def setModel(self,model):
        self.floatField.setModel(model)
        self.__updateSliderValue()
        
    def setValue(self,value):
        self.floatField.setValue(value)
        self.__updateSliderValue()
    
    def getValue(self):
        return self.floatField.getValue()
    
    def setEnabled(self,enabled):
        cmds.layout(self.mainLayout,e=True,enable=enabled)
