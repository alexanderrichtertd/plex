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

from ngSkinTools.ui.basedialog import BaseDialog
from maya import cmds
from ngSkinTools.ui.basetab import BaseTab
from ngSkinTools.ui.constants import Constants
from ngSkinTools.ui.actions import BaseAction
from ngSkinTools.utilities.importInfluences import ImportInfluences
from ngSkinTools.utils import Utils

class ImportInfluencesDialog(BaseDialog):
    CTRL_PREFIX = 'ngSkinToolsImportInfluences_'
    
    def __init__(self):
        BaseDialog.__init__(self)
        self.title = "Import influences from another skin cluster"
        self.buttons = [self.BUTTON_OK,self.BUTTON_CANCEL]
        self.importer = None
        self.selectedInfluences = []
        
    
    def remapToShorterNames(self,dagPathList):
        return map(lambda a:cmds.ls(a)[0],dagPathList)
        
    def updateSelectedItems(self,*args):
        self.selectedInfluences = cmds.textScrollList(self.influencesList,q=True,selectItem=True)
    
    def createInnerUi(self, parent):
        rows=cmds.columnLayout(parent=parent,
            adjustableColumn=1,rowSpacing=Constants.MARGIN_SPACING_VERTICAL,
            width=400)
        

        BaseTab.createFixedTitledRow(rows, "Source")
        cmds.text(label=self.importer.sourceSkinCluster)
        BaseTab.createFixedTitledRow(rows, "Destination")
        cmds.text(label=self.importer.destinationSkinCluster)
        
        cmds.setParent(rows)
        
        cmds.text(label="Select influences to add to %s:" % self.importer.destinationSkinCluster,font='boldLabelFont',align='left')
        influences = self.remapToShorterNames(self.importer.listInfluencesDiff())
        self.influencesList = cmds.textScrollList(numberOfRows=8,allowMultiSelection=True,append=influences,sc=self.updateSelectedItems)
        
        return rows


class ImportInfluencesAction(BaseAction):
    
    @Utils.visualErrorHandling
    @Utils.undoable
    @Utils.preserveSelection
    def execute(self):
        setup = ImportInfluences()
        setup.initFromSelection()
        
        dlg = ImportInfluencesDialog()
        dlg.importer = setup
        result = dlg.execute(parentWindow=self.ownerUI)
        
        if result!=ImportInfluencesDialog.BUTTON_OK:
            return
        
        for influence in dlg.selectedInfluences:
            setup.addInfluence(influence)
        
        
        
        