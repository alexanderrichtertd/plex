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

import maya.OpenMaya as om
from maya import cmds
from ngSkinTools.utils import Utils, MessageException
from ngSkinTools.ui.constants import Constants


class MeshSelectEntry:
    def __init__(self,dag):
        self.dag = dag;
        self.handle = om.MObjectHandle(dag.node())
        # list of component IDs
        self.components = []
        
    def isCurrentlyValid(self):
        '''
        returns true if selection on this mesh can be done with current state of the scene
        (object can be recently deleted)
        '''
        return self.handle.isValid()
    
    def getNodeName(self):
        dag =  om.MFnDagNode(self.handle.object())
        return dag.name()
    
    
    

class MeshSelectRow:
    def __init__(self,parentLayout,caption,annotation):
        self.parent = parentLayout
        self.title = caption
        self.annotation = annotation
        self.componentType = om.MFn.kMeshVertComponent
        
        # list of MeshSelectEntry
        self.selection = []
        
        # custom function can be set to be fired each time
        # control changes selection
        self.selectionChangedHandler = None
        
    def getSelectionAsSelList(self):
        '''
        constructs a selection list from self.selection
        '''
        result = om.MSelectionList()
        for i in self.selection:
            if not i.isCurrentlyValid():
                continue
            vertSelection = om.MFnSingleIndexedComponent();
            components = vertSelection.create(om.MFn.kMeshVertComponent);
            for c in i.components:
                vertSelection.addElement(c)
            
            
            result.add(i.dag,components,True)
        
        return result
    
    def getSelectionStrings(self):
        sel = []
        self.getSelectionAsSelList().getSelectionStrings(sel)
        return sel
        
            
    
    def parseSelectionList(self,selectionList):
        '''
        calculates compacted internal selection list from the MSelectionList
        '''
        selection = []
        if selectionList is None or selectionList.isEmpty():
            return selection
        
        #compact selection list first
        mergedList = om.MSelectionList()
        mergedList.merge(selectionList,om.MSelectionList.kMergeNormal)
                                 
        for i in Utils.mIter(om.MItSelectionList(mergedList)):
            # read selection item
            path = om.MDagPath()
            compSelection = om.MObject()
            i.getDagPath(path,compSelection)
            if not i.hasComponents() or not compSelection.hasFn(self.componentType):
                continue
            
            # create selection entry and fill it with components
            selEntry = MeshSelectEntry(path)
            for c in Utils.mIter(om.MItMeshVertex(path,compSelection)):
                selEntry.components.append(c.index())
            selection.append(selEntry)
        return selection
            
    def setSelection(self,selection):
        '''
            sets current selection, updates display and fires event
        '''
        self.selection = selection
        cmds.textField(self.lblSelectionInfo,e=True,text=self.getSelectionDisplay())
        if self.selectionChangedHandler is not None:
            self.selectionChangedHandler()
    
    def getSelectionDisplay(self):
        numComponents = 0
        numMeshes = 0
        for i in self.selection:
            if i.isCurrentlyValid():
                numMeshes += 1
                numComponents += len(i.components)
                
        if numMeshes==0:
            return ""
        
        # i don't know why am i doing this but i just don't like "1 verts selected" info string.
        componentName = "vertex"
        if numComponents % 10!=1 or numComponents%100==11:
            componentName = "vertexes"
            
        if numMeshes==1:
            return "%d %s in %s" % (numComponents,componentName,self.selection[0].getNodeName())
        
        return "%d %s in %d meshes" % (numComponents,componentName,numMeshes)
                    
    @Utils.visualErrorHandling
    def execSetCurrentSelection(self,*args):
        '''
        handler for "<<" button
        '''
        selList = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selList)
        sel = self.parseSelectionList(selList)
        if len(sel)<1:
            raise MessageException("No vertices selected")
        self.setSelection(sel)
        
    @Utils.visualErrorHandling
    def execPreview(self,*args):
        sel = self.getSelectionStrings()
        if len(sel)<1:
            raise MessageException("Nothing to select")
        
        cmds.select(sel)
        
    def execClear(self,*args):
        self.setSelection([])
        
        
    def create(self):
        row = cmds.rowLayout(parent=self.parent,nc=5,adjustableColumn=2,
                             columnWidth5=[Constants.MARGIN_COLUMN2,100,Constants.BUTTON_WIDTH_SMALL,Constants.BUTTON_WIDTH_SMALL,Constants.BUTTON_WIDTH_SMALL],
                             columnAttach5=["both"]*5, 
                             columnAlign5=["right","left","center","center","center"])
        cmds.text(self.title,annotation=self.annotation)
        self.lblSelectionInfo = cmds.textField("",enable=False,font="boldLabelFont",annotation=self.annotation)
        cmds.button("<<",command=self.execSetCurrentSelection, annotation="set current selection as value of this field")
        cmds.button("?",command=self.execPreview, annotation="preview what's set")
        cmds.button("X",command=self.execClear, annotation="clear")
        
        
        self.setSelection([])
        