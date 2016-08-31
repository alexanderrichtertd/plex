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

import sys
from maya import OpenMaya as om
from maya import cmds
from maya import mel
from ngSkinTools.log import LoggerFactory
from functools import wraps

class MessageException(Exception):
    def __init__(self,message):
        self.message = message
        
    def __str__(self, *args, **kwargs):
        return self.message
        
log = LoggerFactory.getLogger("utils")

class Utils:
    '''
        various utility methods that didn't fit into any specific category
    '''
    
    ERROR_PLUGINNOTAVAILABLE = 'Skin tools plugin is not loaded.'
    ERROR_NO_MESH_VERT_SELECTED = 'No mesh vertices are selected'
    
    # constants for maya version
    # earlier maya versions have smaller constant value, so comparisions can be made (e.g. getMayaVersion()<MAYA2011)
    # (new constants must follow this pattern, e.g., "2008 release 2" should be 2008.2 instead of 200802)
    MAYA_UNKNOWN_VERSION = 0 # /// special constant for unknown version. assumed earlier version in code
    MAYA2011 = 2011
    MAYA2012 = 2012
    MAYA2013 = 2013
    MAYA2014 = 2014
    MAYA2014_5 = 2014.5
    MAYA2015 = 2015
    MAYA2016 = 2016
    CURRENT_MAYA_VERSION = None
    
    DEBUG_MODE = False # /// set to true to enable debug output
    

    # check for updates once per session
    # will be set to true after first silent update check
    # user can still manually issue update checks
    UPDATECHECKED = False
    
    
    # plugin binary name
    PLUGIN_BINARY = 'ngSkinTools'
    
    @staticmethod
    def confirmDialog(**kwargs):
        '''
        used to be a pre-2011 Maya compatibility wrapper 
        of cmds.confirmDialog. Keeping for now
        '''
        
        return cmds.confirmDialog(**kwargs)
        
        
    
    @staticmethod
    def displayError(message):
        '''
        displays error in script editor and in a dialog box
        '''
        
        message = str(message)
        om.MGlobal.displayError('[NgSkinTools] '+message)
        Utils.confirmDialog( title='NgSkinTools: Error', message=str(message), button=['Ok'], defaultButton='Ok')
        
        
    @staticmethod
    def visualErrorHandling(function):
        '''
            decorator for function;
            executes proc in a try..except block, displaying errors 
            in a dialog box and script editor with MGlobal.displayError
        '''
        
        @wraps(function)
        def result(*args,**kargs):
            try:
                return function(*args,**kargs)
            except MessageException, err:
                Utils.displayError(err.message)
            except Exception, err:
                import traceback;traceback.print_exc()
                Utils.displayError(str(err))

        return result
    
    @staticmethod
    def preserveSelection(function):
        '''
            decorator for function;
            saves selection prior to execution and restores it 
            after function finishes
        '''
        @wraps(function)
        def result(*args,**kargs):
            selection = cmds.ls(sl=True,fl=True)
            highlight = cmds.ls(hl=True,fl=True)
            try:
                result = function(*args,**kargs)
            finally:
                if selection:
                    cmds.select(selection)
                else:
                    cmds.select(clear=True)
                if highlight:
                    cmds.hilite(highlight)
        return result
    
    @staticmethod
    def isVertexSelectionAvailable():
        '''
        returns False, if no vert selection is available;
        
        '''
        selList = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selList)
        it = om.MItSelectionList(selList)
        while not it.isDone():
            path = om.MDagPath()
            compSelection = om.MObject()
            if it.itemType()==om.MItSelectionList.kDagSelectionItem:
                it.getDagPath(path,compSelection)
                if not compSelection.isNull() and compSelection.hasFn(om.MFn.kMeshVertComponent):
                    return True
            
            it.next()
            
        return None    
    
    @staticmethod
    def testVertexSelectionAvailable():
        '''
        throws exception if vertex selection is not available
        '''
        if not Utils.isVertexSelectionAvailable():
            raise MessageException(Utils.ERROR_NO_MESH_VERT_SELECTED)
        
    
    
    @staticmethod
    def testPluginLoaded():
        '''
        throws exception if plugin is not loaded
        '''
        if not Utils.isPluginLoaded():
            raise MessageException(Utils.ERROR_PLUGINNOTAVAILABLE)
        
        
        
    @staticmethod
    def createMelProcedure(pythonMethod,args=[],returnType=''):
        '''
        creates a valid mel procedure to be called that invokes pythonMethod
        two procedures with a temporary name are created in global MEL and Python spaces for this reason
        no parameter passing is supported
        '''
        
        # generate procedure name
        procName = "ngSkinToolsProc%i%s" % (id(pythonMethod),pythonMethod.__name__)
        
        # create link to method in global python space
        sys.modules['__main__'].__dict__[procName] = pythonMethod
        
        # create mel procedure
        melArgs = ",".join(map(lambda a:"%s $%s" % (a[0],a[1]),args))
        pythonArgs = ','.join(map(lambda a: '\'"+$%s+"\'' %a[1],args))
        returnStmt = 'return' if returnType!='' else ''
        melCode = 'global proc %s %s(%s) { %s python ("%s(%s)");  }' % (returnType,procName,melArgs,returnStmt,procName,pythonArgs)
        mel.eval(melCode)
        
        return procName
    
    @staticmethod
    def getMayaVersion():
        '''
        returns maya version (use Utils.MAYA* constants for comparision of a returned result)
        currently uses "about -v" string parsing
        '''
        
        if Utils.CURRENT_MAYA_VERSION is None:
            version = cmds.about(v=True)
            
            Utils.CURRENT_MAYA_VERSION = Utils.MAYA_UNKNOWN_VERSION
            
            
            def testVersion(search,result):
                if search in version:
                    Utils.CURRENT_MAYA_VERSION = result
                    return True
                return False

                        
            testVersion('2011', Utils.MAYA2011) or \
            testVersion('2012', Utils.MAYA2012) or \
            testVersion('2013', Utils.MAYA2013) or \
            testVersion('2014', Utils.MAYA2014) or \
            testVersion('2015', Utils.MAYA2015) or \
            testVersion('2016', Utils.MAYA2016)
            
        return Utils.CURRENT_MAYA_VERSION
    
    @staticmethod
    def mel(melSource):
        '''
        little wrapper around mel.eval to debug/print source on error
        '''
        
        log.info("[MEL] "+melSource);
            
        try:
            return mel.eval(melSource)
        except Exception,err:
            raise err
        
    @staticmethod
    def isCurrentlyPaintingWeights():
        '''
        returns true if paint skin weights is the current context in Maya
        '''
        return cmds.currentCtx()=='artAttrSkinContext'

    @staticmethod
    def refreshPaintWeightsTool():
        '''
        checks if "paint skin weights" is currently open,
        and attempts to update its view and internal data
        (otherwise next skin paint operation messes up with new skin weights)
        
        current implementation is rather ugly which is based on 
        restarting paint weights tool completely
        '''
        
        if not Utils.isCurrentlyPaintingWeights():
            return
        
        # TODO: redo this by selecting first influence and then back to current influence
        Utils.preserveSelection(cmds.ArtPaintSkinWeightsTool)()
        
    @staticmethod
    def silentCheckForUpdates():
        from ngSkinTools.ui.options import Options
        from ngSkinTools.ui.updateCheckWindow import UpdateCheckWindow
        
        if Options.OPTION_CHECKFORUPDATES.get() and not Utils.UPDATECHECKED:
            Utils.UPDATECHECKED = True
            UpdateCheckWindow.execute(silent=True)

    @staticmethod
    def isPluginLoaded():
        '''
        returns true if ngSkinTools plugin is loaded
        '''
        return cmds.pluginInfo(Utils.PLUGIN_BINARY,q=True,loaded=True)
    
    @staticmethod
    def getPluginVersion():
        return cmds.pluginInfo(Utils.PLUGIN_BINARY,q=True,version=True)

    @staticmethod
    def loadPlugin():
        '''
        makes sure that plugin is loaded
        '''
        
        from ngSkinTools.version import Version
        
        if not Utils.isPluginLoaded():
            cmds.loadPlugin(Utils.PLUGIN_BINARY,quiet=True)
            
        if not Utils.DEBUG_MODE:
            if Utils.getPluginVersion()!=Version.pluginVersion():
                Utils.displayError("Invalid plugin version detected: required '%s', but was '%s'. Clean reinstall recommended." % (Version.pluginVersion(), Utils.getPluginVersion()))
            
            
    @staticmethod
    def mIter(mayaIterator):
        '''
            shortcut method to iterate maya iterators and lists with foreach
        '''
        
        # iterator?
        if hasattr(mayaIterator, "isDone"):
            while not mayaIterator.isDone():
                yield mayaIterator
                mayaIterator.next()
        # array?
        elif hasattr(mayaIterator, "length"):
            for i in xrange(mayaIterator.length()):
                yield mayaIterator[i]
            
        

    @staticmethod
    def convertArgsToCommandLine(args):
        '''
        converts pythnon dictionary into MEL command arguments
        '''
        result = ""
        for key,value in args.items():
            if result!="":
                result += " "
            result += "-%s "%str(key)
            
            if isinstance(value, float):
                result += "%f"%value
            else:
                result += "%s"%str(value)
                
        return result
    
    
    @staticmethod
    def undoable(function):
        '''
        function decorator, makes function contents undoable in one go
        '''
        @wraps(function)
        def result(*args,**kargs):
            cmds.undoInfo(openChunk=True)
            try:
                function(*args,**kargs)
            finally:
                cmds.undoInfo(closeChunk=True)
        
        return result

    @staticmethod
    def getMObjectForNode(nodeName):
        sel = om.MSelectionList();
        sel.add(nodeName)
        obj = om.MObject()
        sel.getDependNode(0,obj)
        return obj            

    @staticmethod
    def getDagPathForNode(nodeName):
        sel = om.MSelectionList();
        sel.add(nodeName)
        result = om.MDagPath()
        sel.getDagPath(0,result)
        
        if not result.isValid():
            raise MessageException("node %s does not exist" % nodeName) 
        return result
        
    @staticmethod
    def shortName(nodeName):
        if not isinstance(nodeName,basestring):
            return nodeName
        
        try:
            return nodeName[nodeName.rfind("|")+1:]
        except:
            return nodeName
        
