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
from ngSkinTools.utils import Utils
from ngSkinTools.ui.options import PersistentValueModel, ValueModel
from ngSkinTools.ui.constants import Constants
from ngSkinTools.ui.events import Signal

class BaseUIWrapper(object):
    '''
    base class for wrapping Maya's UI commands 
    '''
    
    def __init__(self,uiCommand,annotation=''):
        self.uiCommand = uiCommand
        self.annotation=annotation
        pass
    
    def editUI(self,**kargs):
        self.uiCommand(self.field,e=True,**kargs)

    def queryUI(self,**kargs):
        return self.uiCommand(self.field,q=True,**kargs)
        
    def __str__(self):
        return self.field
    
    @property
    def enabled(self):
        return self.queryUI(enable=True)
        
    def setEnabled(self,enabled):
        self.editUI(enable=enabled)
        
    def createUI(self,**kargs):
        kargs['annotation'] = self.annotation
        self.field = self.uiCommand(**kargs)
        
    def focus(self):
        cmds.setFocus(self.field)
        
        
class ValueUIWrapper(BaseUIWrapper):
    '''
    UI wrapper for controls that have a settable/gettable value (like float field)
    '''
    
    def __init__(self,uiCommand=None,annotation=''):
        BaseUIWrapper.__init__(self,uiCommand,annotation)
        self.valueKeyName = 'value'
        self.changeCommand = Signal()
        
    def getValue(self):
        return self.uiCommand(self.field,q=True,**{self.valueKeyName:True})
    
    def setValue(self,value):
        args = {self.valueKeyName:value}
        self.uiCommand(self.field,e=True,**args)
        
    def createUI(self,**kargs):
        kargs['changeCommand'] = self.fieldChanged
        BaseUIWrapper.createUI(self,**kargs)

    def fieldChanged(self,*args):
        self.changeCommand.emit()
        
class ModelUIWrapper(ValueUIWrapper):
    '''
    value wrapper that uses persistent value storage (model) to store it's value
    '''
    
    def __init__(self,model=None,uiCommand=None,defaultValue=None,annotation=''):
        ValueUIWrapper.__init__(self,uiCommand=uiCommand,annotation=annotation)
        
        if (isinstance(model, ValueModel)):
            self.model = model
        elif model is not None:
            self.model = PersistentValueModel(model, defaultValue=defaultValue)
        else:
            self.model = None
        
    def createUI(self,**kargs):
        ValueUIWrapper.createUI(self,**kargs)
        self.updateUI()
        
    def updateModel(self):
        '''
        updates model with current control value
        '''
        if self.model is not None:
            self.model.set(self.getValue())
            
    def updateUI(self):
        '''
        updates UI to current model value
        '''
        if self.model is not None:
            try:
                self.editUI(**{self.valueKeyName:self.model.get()})
            except:
                pass
        
        
    def setValue(self,value):
        '''
        saves value after setting it through code
        '''
        ValueUIWrapper.setValue(self, value)
        self.updateModel();
        
    def getModelValue(self):
        if self.model is not None:
            return self.model.get()
        
        return self.getValue()
        
    def setModel(self,pValue):
        if self.model==pValue:
            return
        
        assert (isinstance(pValue,ValueModel))
        self.model = pValue
        ValueUIWrapper.setValue(self, pValue.get())

    def fieldChanged(self,*args):
        '''
        updates data storage when field changes
        '''
        
        self.updateModel();
        ValueUIWrapper.fieldChanged(self,*args)
            

class IntField(ModelUIWrapper):
    def __init__(self,model,minValue=1,maxValue=1000,step=1,defaultValue=1,annotation=''):
        '''
        minValue/maxValue accept none as "no-limit" value
        '''
        
        ModelUIWrapper.__init__(self,model, cmds.intField,defaultValue,annotation)
        self.createUI(minValue=minValue,value=defaultValue,maxValue=maxValue,step=step)
        
    def createUI(self,**kargs):
        kargs['width'] = Constants.NUMBER_FIELD_WIDTH
        for key in ('minValue','maxValue'):
            if kargs[key] is None:
                del kargs[key]
        ModelUIWrapper.createUI(self,**kargs)
        
    
class FloatField(ModelUIWrapper):
    def __init__(self,model,minValue=None,maxValue=None,step=1,defaultValue=1,annotation=''):
        ModelUIWrapper.__init__(self,model, cmds.floatField,defaultValue,annotation)
        args = {}
        if maxValue is not None:
            args['maxValue'] = maxValue
        if minValue is not None:
            args['minValue'] = minValue
        if minValue is not None:
            args['value'] = defaultValue
        if step is not None:
            args['step'] = step 
        self.createUI(**args)

    def createUI(self,**kargs):
        kargs['width'] = Constants.NUMBER_FIELD_WIDTH
        ModelUIWrapper.createUI(self,**kargs)
        
    
class CheckBoxField(ModelUIWrapper):
    def __init__(self,model=None,label='',defaultValue=1,annotation=''):
        ModelUIWrapper.__init__(self,model, cmds.checkBox,defaultValue,annotation)
        self.createUI(label=label,align='left')
        
    def isChecked(self):
        '''
        just a more readable alias to getModelValue()
        '''
        return self.getModelValue()
        
    
        
class RadioButtonField(ModelUIWrapper):
    def __init__(self,model,label='',defaultValue=1,annotation=''):
        ModelUIWrapper.__init__(self,model, cmds.radioButton,defaultValue,annotation)
        self.valueKeyName = 'select'
        self.createUI(label=label)
    
class TextLabel(BaseUIWrapper):
    ALIGN_LEFT='left'
    
    def __init__(self,label='',annotation='',align=None):
        BaseUIWrapper.__init__(self,cmds.text,annotation)
        self.createUI(label=label)
        if align is not None:
            self.setAlign(align)
    
    def setAlign(self,align):
        self.editUI(align=align)
    
    def setBold(self):
        self.editUI(font='boldLabelFont')
        
    def setLabel(self,label):
        self.editUI(label=label)   
    
    def getLabel(self):
        return self.queryUI(label=True) 
        
class TextEdit(ValueUIWrapper):
    def __init__(self,annotation=''):
        ValueUIWrapper.__init__(self,uiCommand=cmds.textField,annotation=annotation)
        self.valueKeyName = 'text'
        self.createUI()

class StoredTextEdit(ModelUIWrapper):
    def __init__(self,model,defaultValue='',annotation=''):
        ModelUIWrapper.__init__(self,model=model, uiCommand=cmds.textField,defaultValue=defaultValue,annotation=annotation)
        self.valueKeyName = 'text'
        self.createUI()


class DropDownField(ModelUIWrapper):
    
    
    def __init__(self,model,defaultValue=0,annotation=''):
        ModelUIWrapper.__init__(self,model=model, uiCommand=cmds.optionMenu,defaultValue=defaultValue,annotation=annotation)
        self.menuItems = []
        self.texts = []
        self.beginRebuildItems()
        
        self.createUI()
        self.editUI(changeCommand=self.menuSelected)
        
        self.indexModel = model
        
        
        self.updatingItems = False
        
    def addOption(self,optionName):
        item = cmds.menuItem(parent=self.field,label=optionName)
        self.menuItems.append(item)
        self.texts.append(optionName)
        
        if not self.updatingItems:
            self.updateUI()
        
        
    def clear(self):
        for i in self.menuItems:
            cmds.deleteUI(i,menuItem=True)
            
        self.menuItems = []
        self.texts = []
        
        
        
    def getValue(self):
        return cmds.optionMenu(self.field,q=True,select=True)-1
    
    def getSelectedText(self):
        return self.texts[self.getValue()]

    def setValue(self, value):
        if isinstance(value, basestring):
            value = self.texts.index(value)
        ModelUIWrapper.setValue(self, self.texts[value])
        
    def menuSelected(self,item):
        self.updateModel()
        self.changeCommand.emit()
        
    def beginRebuildItems(self):
        self.clear()
        self.updatingItems = True
    
    def endRebuildItems(self):
        self.updatingItems = False
        
        cmds.optionMenu(self.field,e=True,select=self.model.getInt()+1)
        self.updateModel()
        
    
    
class Layout():
    @staticmethod
    def setEnabled(layout,enabled):        
        cmds.layout(layout,e=True,enable=enabled)

    @staticmethod        
    def setVisible(layout,visible):        
        cmds.layout(layout,e=True,visible=visible)
        
class FormLayout:
    def __init__(self,useExisting=None,**kargs):
        if useExisting is None:
            self.layout = cmds.formLayout(**kargs)
        else:
            self.layout = useExisting
            
    def setEnabled(self,enabled):
        Layout.setEnabled(self.layout, enabled)

    def setVisible(self,enabled):
        Layout.setVisible(self.layout, enabled)
        
    def repeatTBLR(self,function,top,right,bottom,left):
        '''
        repeats the same function for top, right, bottom and left sides, if value of each is not None
        '''
        for value,name in ((top,'top'),(bottom,'bottom'),(left,'left'),(right,'right')):
            if value is not None:
                function(value,name)
                
    def attachForm(self,control,top,right,bottom,left):
        def a(value,name):
            cmds.formLayout(self.layout,e=True,af=(control,name,value))
        
        self.repeatTBLR(a, top, right, bottom, left)

    def attachOppositeForm(self,control,top,right,bottom,left):
        def a(value,name):
            cmds.formLayout(self.layout,e=True,attachOppositeForm=(control,name,value))
        
        self.repeatTBLR(a, top, right, bottom, left)

    def attachControl(self,control,targetControl,top,right,bottom,left):
        def a(value,name):
            cmds.formLayout(self.layout,e=True,ac=(control,name,value,targetControl))
        self.repeatTBLR(a, top, right, bottom, left)

    def attachPosition(self,control,targetControl,top,right,bottom,left):
        def a(value,name):
            cmds.formLayout(self.layout,e=True,attachPosition=(control,name,value,targetControl))
        self.repeatTBLR(a, top, right, bottom, left)
            
    def __str__(self):
        return self.layout

def frameLayout(*args,**kwargs):
    if Utils.CURRENT_MAYA_VERSION>=Utils.MAYA2016:
        kwargs.pop("bs",None)
        kwargs.pop("borderStyle",None)
    return cmds.frameLayout(*args,**kwargs)