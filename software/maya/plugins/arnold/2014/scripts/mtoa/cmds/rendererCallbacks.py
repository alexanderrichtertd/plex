import maya.cmds as cmds
import maya.mel as mel
import mtoa.utils as utils
from mtoa.ui.nodeTreeLister import aiHyperShadeCreateMenu_BuildMenu, createArnoldNodesTreeLister_Content
import mtoa.ui.ae.templates as templates
import ctypes
import types

def aiHyperShadePanelBuildCreateMenuCallback() :
    if cmds.pluginInfo('mtoa', query=True, loaded=True) :
        aiHyperShadeCreateMenu_BuildMenu()
        cmds.menuItem(divider=True)

def aiHyperShadePanelBuildCreateSubMenuCallback() :  
    return "rendernode/arnold"

def aiRenderNodeClassificationCallback() :
    return "rendernode/arnold"

def aiCreateRenderNodePluginChangeCallback(classification) :
    return classification.startswith("rendernode/arnold")

def aiCreateRenderNodeSelectNodeCategoriesCallback(nodeTypesFlag, renderNodeTreeLister) :
    if (nodeTypesFlag == "allWithArnoldUp") :
        cmds.treeLister(renderNodeTreeLister, edit=True, selectPath="arnold")

def aiBuildRenderNodeTreeListerContentCallback(renderNodeTreeLister, postCommand, filterString) :
    filterClassArray = filterString
    createArnoldNodesTreeLister_Content(renderNodeTreeLister, postCommand, filterClassArray)

def aiProvideClassificationStringsForFilteredTreeListerCallback(classification) :
    return "rendernode/arnold/shader/surface"

def aiNodeCanBeUsedAsMaterialCallback(nodeId, nodeOwner ) :
    if nodeOwner == "Arnold":
        return 1
    else:
        return 0
   
def castSelf(selfid):
    # Can't pass self as an object.
    # It's cast to id(self) by the caller
    # and we convert it back to a python object here
    if isinstance(selfid,str):
        return ctypes.cast( int(selfid), ctypes.py_object ).value
    else:
        return selfid
      
def aiExportFrame( self, frame, objFilename ):
    # Export a single mental ray archive frame.
    cmds.currentTime( frame )

    cmds.arnoldExportAss(f=objFilename+".ass.gz", s=True, c=True, bb=True, mask=56)
    #cmds.Mayatomr( 	mi=True, exportFilter=7020488, 
    #            active=True, binary=True, compression=9, 
    #            fragmentExport=True, fragmentChildDag =True, passContributionMaps =True, 
    #            assembly=True, assemblyRootName="obj", exportPathNames="n", 
    #            file=objFilename + ".mi" )
    self.log( "assExport " + objFilename + ".ass.gz")

def aiExportAppendFile( self, assFilename, material, obj, lod ):
    lodList = self.tweakLodAppend( self.curFiles, lod  )
    for l in lodList:
        self.addArchiveFile( "ass", assFilename, material, "", l, 3 )
        
def aiExport( self, objs, filename, lod, materialNS ):
    filename = self.nestFilenameInDirectory( filename, "ass" )
    
    lastProgress = self.progress
    self.splitProgress( len(objs) )
    
    self.log( "assExport " + filename + lod )
    
    # force units to centimeters when exporting mi.
    #prevUnits = cmds.currentUnit( query=True, linear=True, fullName=True )
    #cmds.currentUnit( linear="centimeter" )
    
    prevTime = cmds.currentTime( query=True )

    for obj in objs:
        objFilename = filename + "_" + obj.replace("|", "_").replace(":", "_") + lod
        cmds.select( obj, r=True )

        filenames = []
        # Choose to export single file or a sequence.
        frameToken = ""
        if self.startFrame != self.endFrame:
            frameToken =".${FRAME}"

            dummyFrameFile = open( objFilename + frameToken + ".ass.gz", "wt" )
            dummyFrameFile.write( "STARTFRAME=%4.4d\nENDFRAME=%4.4d\n" % (int( self.startFrame), int(self.endFrame) ) )
            dummyFrameFile.close()

            for curFrame in range( int(self.startFrame), int(self.endFrame)+ 1 ):
                aiExportFrame( self, curFrame, objFilename + ".%4.4d" % int(curFrame) )
        else:
            aiExportFrame( self, self.startFrame, objFilename )
        
        if self.curFiles != None:
            materials = self.getSGsFromObj( obj )
            if materials and len(materials)>0 :
                assFilename = objFilename + frameToken + ".ass.gz"
                aiExportAppendFile( self, assFilename, materialNS+materials[0], obj, lod )
        self.incProgress()
    
    #cmds.currentUnit( linear=prevUnits )
    cmds.currentTime( prevTime )
    
    self.progress = lastProgress
        
def xgaiArchiveExport(selfid) :
    self = castSelf(selfid)
    aiExport( self, self.invokeArgs[0], self.invokeArgs[1], self.invokeArgs[2], self.invokeArgs[3] )
    
def xgaiArchiveExportInfo(selfid) :
    self = castSelf(selfid)
    self.archiveDirs.append( "ass" )
    self.archiveLODBeforeExt.append( ".${FRAME}.ass" )
    self.archiveLODBeforeExt.append( ".${FRAME}.ass.gz" )
    self.archiveLODBeforeExt.append( ".ass" )
    self.archiveLODBeforeExt.append( ".ass.gz" )
    
#def xgaiArchiveExportInit(selfid) :
#    print "##### xgaiArchiveExportInit ",selfid
 

try:
    import xgenm as xg
    xg.registerCallback( "ArchiveExport", "mtoa.cmds.rendererCallbacks.xgaiArchiveExport" )
    xg.registerCallback( "ArchiveExportInfo", "mtoa.cmds.rendererCallbacks.xgaiArchiveExportInfo" )
    #xg.registerCallback( "ArchiveExportInit", "mtoa.cmds.rendererCallbacks.xgaiArchiveExportInit" )
except:
    pass
 

# Add the callbacks
def registerCallbacks():
    if cmds.about(batch=True):
        return
        
    
        
    cmds.callbacks(addCallback=aiHyperShadePanelBuildCreateMenuCallback,
                   hook="hyperShadePanelBuildCreateMenu",
                   owner="arnold")

    cmds.callbacks(addCallback=aiHyperShadePanelBuildCreateSubMenuCallback,
                   hook="hyperShadePanelBuildCreateSubMenu",
                   owner="arnold")

    cmds.callbacks(addCallback=aiCreateRenderNodeSelectNodeCategoriesCallback,
                   hook="createRenderNodeSelectNodeCategories",
                   owner="arnold")
               

    # FIXME: Maya doc is wrong
    #cmds.callbacks(addCallback=aiRenderNodeClassificationCallback,
    #               hook="addToRenderNodeTreeLister",
    #              owner="arnold")
    # Should be this instead

    cmds.callbacks(addCallback=aiRenderNodeClassificationCallback,
                   hook="renderNodeClassification",
                   owner="arnold")

    cmds.callbacks(addCallback=aiBuildRenderNodeTreeListerContentCallback,
                   hook="buildRenderNodeTreeListerContent",
                   owner="arnold")

    cmds.callbacks(addCallback=aiCreateRenderNodePluginChangeCallback,
                   hook="createRenderNodePluginChange",
                   owner="arnold")

    cmds.callbacks(addCallback=templates.loadArnoldTemplate,
                   hook="AETemplateCustomContent",
                   owner="arnold")

    cmds.callbacks(addCallback=aiProvideClassificationStringsForFilteredTreeListerCallback,
                   hook="provideClassificationStringsForFilteredTreeLister",
                   owner="arnold")

    cmds.callbacks(addCallback=aiNodeCanBeUsedAsMaterialCallback,
                   hook="nodeCanBeUsedAsMaterial",
                   owner="arnold")

def clearCallbacks():
    if cmds.about(batch=True):
        return
    try:
        cmds.callbacks(clearAllCallbacks=True, owner="arnold")
    except:
        pass

