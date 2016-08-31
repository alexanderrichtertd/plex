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
from ngSkinTools.ui.uiWrappers import FormLayout
from ngSkinTools.ui.constants import Constants
from ngSkinTools.log import LoggerFactory

log = LoggerFactory.getLogger("base dialog")

class BaseDialog:
    currentDialog = None
    
    BUTTON_OK = "ok"
    BUTTON_CANCEL = "cancel"
    BUTTON_CLOSE = "close"
    
    BUTTON_LABELS = {BUTTON_OK:"Ok",BUTTON_CANCEL:"Cancel",BUTTON_CLOSE:"Close"}
    
    def __init__(self):
        self.title = "Untitled"
        self.buttons = []
        class Controls:
            pass
        self.controls = Controls()
        
    def createInnerUi(self,parent):
        pass
    
    
    def closeDialogWithResult(self,buttonID):
        '''
        called when button is clicked. buttonID is one of BUTTON_* constants,
        representing which dialog button was clicked
        '''
        cmds.layoutDialog(dismiss=buttonID)
        
    
    def createUi(self):
        def getButtonClickHandler(buttonId):
            'helper function to create separate instances of button click handler for each button'
            def handler(*args):
                self.closeDialogWithResult(buttonId)
                
            return handler

        form = FormLayout(useExisting=cmds.setParent(q=True))
        
        
        innerUi = self.createInnerUi(form)
        buttonsForm = FormLayout(parent=form,height=Constants.BUTTON_HEIGHT+Constants.MARGIN_SPACING_VERTICAL*2)
        prevBtn = None
        for i in reversed(self.buttons):
            
            btn = cmds.button(label=self.BUTTON_LABELS[i],height=Constants.BUTTON_HEIGHT,width=Constants.BUTTON_WIDTH,
                              command=getButtonClickHandler(i));
            
            buttonsForm.attachForm(btn, 0, None if prevBtn is not None else Constants.MARGIN_SPACING_HORIZONTAL*2, None, None)
            if prevBtn is not None:
                buttonsForm.attachControl(btn, prevBtn, None, Constants.MARGIN_SPACING_HORIZONTAL, None, None)
            prevBtn = btn
            
            
        form.attachForm(innerUi, Constants.MARGIN_SPACING_VERTICAL, Constants.MARGIN_SPACING_HORIZONTAL, None, Constants.MARGIN_SPACING_HORIZONTAL)
        form.attachForm(buttonsForm, None, True, True, True)
        form.attachControl(innerUi, buttonsForm, None, None, Constants.MARGIN_SPACING_VERTICAL, None)
        
        
    def execute(self,parentWindow=None):
        BaseDialog.currentDialog = self
        log.debug("executing a dialog")
        
        options = {'ui':self.createUi,'title':self.title}
        if parentWindow is not None:
            options["parent"] = parentWindow
        result = cmds.layoutDialog(**options)
        BaseDialog.currentDialog = None
        log.debug("dialog ended")
        return result
        