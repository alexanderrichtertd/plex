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
from ngSkinTools.ui.options import Options
from ngSkinTools.ui.constants import Constants
from ngSkinTools.ui.uiWrappers import FormLayout
from ngSkinTools.ui.events import Signal

class IntensitySlider:
    def __init__(self,annotation,name,value=None):
        self.annotation = annotation
        self.name = name
        self.intensityTexts = {0.0:"low",0.33:"medium",0.7:"high"}
        self.changeCommand = Signal()
        self.__value = Options.loadOption(name, 1.0 if value is None else value);
    
    def create(self):
        form = FormLayout(width=100)

        self.intensityIndicator = cmds.textField(width=Constants.NUMBER_FIELD_WIDTH,editable=False,annotation=self.annotation);
        self.sliderIntensity = cmds.floatSlider(min=0, max=1, step=0.05, value=self.__value,cc=self.sliderChange,annotation=self.annotation )

        form.attachForm(self.intensityIndicator,0,None,0,0)
        form.attachForm(self.sliderIntensity,2,0,None,None)
        form.attachControl(self.sliderIntensity,self.intensityIndicator,None,None,None,0)

        self.updateIntensityDisplay()
        return form
        
    def getIntensity(self):
        return cmds.floatSlider(self.sliderIntensity,q=True,value=True)
    
    
    def sliderChange(self,*args):
        self.updateIntensityDisplay()
        Options.saveOption(self.name, self.getIntensity())
        self.changeCommand.emit()
    
    def updateIntensityDisplay(self):
        currIntensity = self.getIntensity()

        displayText = None
        displayedValue = -1
        for currValue,currText in self.intensityTexts.items():
            if currValue<=currIntensity and currValue>displayedValue:
                displayText = currText
                displayedValue = currValue

        cmds.textField(self.intensityIndicator,e=True,text=displayText);
        