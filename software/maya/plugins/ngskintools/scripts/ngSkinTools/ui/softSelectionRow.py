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
from ngSkinTools.ui.uiWrappers import CheckBoxField, FloatField
from ngSkinTools.ui.constants import Constants
from ngSkinTools.ui.basetab import BaseTab

class SoftSelectionRow:

    
    def __init__(self,uiName):
        self.name = uiName
        
    def checkUiEnabled(self):
        '''
        update UI enabled/disabled values
        '''
        self.nativeSoftSelect.editUI(enable=self.useSoftSelect.getValue())
        self.softSelectRadius.editUI(enable=self.useSoftSelect.getValue() and not self.nativeSoftSelect.getValue())

    def uiChanged(self):
        '''
        called when controls change value
        '''
        self.checkUiEnabled()
        
    def create(self,parent):
        cmds.rowLayout(parent=parent,nc=2,adjustableColumn=2,columnWidth2=[Constants.MARGIN_COLUMN2,50])
        self.useSoftSelect = CheckBoxField(self.name+'On',label='Use soft selection',defaultValue=0,annotation='extend effect outside selection with a fade out by defined distance') 
        self.useSoftSelect.changeCommand.addHandler(self.uiChanged)

        self.nativeSoftSelect = CheckBoxField(self.name+'Native',label='Native soft selection',defaultValue=0,annotation='use maya\'s soft selection instead of soft selection radius') 
        self.nativeSoftSelect.changeCommand.addHandler(self.uiChanged)
        
        BaseTab.createFixedTitledRow(parent, "Selection radius")
        self.softSelectRadius = FloatField(self.name+'Radius', minValue=0,defaultValue=1,step=0.1,annotation='soft selection radius is defined in world units') 
        
        self.checkUiEnabled()
        
    
    def addToArgs(self,args):
        if self.useSoftSelect.getValue():
            args['softSelectionRadius'] = self.softSelectRadius.getValue()
            
        if self.nativeSoftSelect.getValue():
            args['nativeSoftSelection'] = 1;