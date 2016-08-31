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
import os
from ngSkinTools.ui.basedialog import BaseDialog
from ngSkinTools.ui.uiWrappers import FormLayout
from ngSkinTools.version import Version



class AboutDialog(BaseDialog):
    def __init__(self):
        BaseDialog.__init__(self)
        self.title = "About ngSkinTools"
        self.buttons = [self.BUTTON_CLOSE]
        
        
    def createInnerUi(self,parent):
        layout = FormLayout(parent=parent,width=400,height=180)
        
        
        labelTitle = cmds.text(label=Version.getReleaseName(), font='boldLabelFont')
        
        logoFrame = cmds.tabLayout(parent=layout,tv=False,childResizable=True,scrollable=False,width=130,height=130,innerMarginWidth=10)
        cmds.image(image=os.path.join(os.path.dirname(__file__),'images','logo.png'))
        layout.attachForm(logoFrame,10,10,None,None)
        
        cmds.setParent(layout)
        labelCopyright = cmds.text(label=Version.COPYRIGHT)
        labelUrl = cmds.text(label=Version.PRODUCT_URL)
        
        
        layout.attachForm(labelTitle, 10, None, None, 10)
        
        layout.attachControl(labelCopyright, labelTitle, 25,None,None,None)
        layout.attachForm(labelCopyright,None,None,None,10)
        layout.attachControl(labelUrl, labelCopyright, 0,None,None,None)
        layout.attachForm(labelUrl,None,None,None,10)
        
        return layout