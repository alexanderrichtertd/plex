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
from ngSkinTools.ui.headlessDataHost import HeadlessDataHost
from ngSkinTools.log import LoggerFactory
from ngSkinTools.ui.events import scriptJobs

class BaseToolWindow(object):
    log = LoggerFactory.getLogger("BaseToolWindow")
    
    windowInstances = {}
    
    def __init__(self,windowName):
        self.updateAvailable = False
        self.windowTitle = ''
        self.windowName = windowName
        self.sizeable = False
        self.menuBar = True
        
        self.defaultWidth = 300
        self.defaultHeight = 300
        self.useUserPrefSize = True
        
        BaseToolWindow.windowInstances[self.windowName]=self
        
    @staticmethod
    def closeAll():
        for _, window in BaseToolWindow.windowInstances.items():
            window.closeWindow()
        
    
    @staticmethod
    def getWindowInstance(windowName,windowClass=None):
        if BaseToolWindow.windowInstances.has_key(windowName):
            return BaseToolWindow.windowInstances[windowName]
        
        if windowClass is None:
            return None
        
        return BaseToolWindow.rebuildWindow(windowName, windowClass)
        
    @staticmethod
    def rebuildWindow(windowName,windowClass):
        BaseToolWindow.destroyWindow(windowName);
        instance = windowClass(windowName)
        instance.createWindow()
        return instance        
    
    def createWindow(self):
        self.log.debug("creating window "+self.windowName)
        if self.windowExists(self.windowName):
            raise Exception("window %s already opened" % self.windowName)
        if not self.useUserPrefSize:
            try:
                cmds.windowPref(self.windowName,remove=True)
                cmds.windowPref(self.windowName,width=self.defaultWidth,height=self.defaultHeight)
            except:
                pass

        cmds.window(self.windowName,
                                   title=self.windowTitle,
                                   maximizeButton=False,
                                   minimizeButton=False,
                                   width=self.defaultWidth,
                                   height=self.defaultHeight,
                                   sizeable=self.sizeable,
                                   menuBar=self.menuBar)
        
        
        scriptJobs.scriptJob(uiDeleted=[self.windowName,self.onWindowDeleted])
        
        HeadlessDataHost.HANDLE.addReference(self)
        
    def onWindowDeleted(self):
        if not HeadlessDataHost.HANDLE.removeReference(self):
            return

        BaseToolWindow.windowInstances.pop(self.windowName)
        
        
    def showWindow(self):
        if self.windowExists(self.windowName):
            cmds.showWindow(self.windowName)

    def closeWindow(self):
        if self.windowExists(self.windowName):
            self.onWindowDeleted()
            cmds.window(self.windowName,e=True,visible=False)

    @staticmethod        
    def windowExists(windowName):
        return cmds.window(windowName, exists=True)

    @staticmethod
    def destroyWindow(windowName):
        if BaseToolWindow.windowExists(windowName):
            instance = BaseToolWindow.getWindowInstance(windowName)
            if instance is not None:
                instance.onWindowDeleted();
            cmds.deleteUI(windowName, window=True)
            
    @staticmethod
    def closeAllWindows():
        for i in BaseToolWindow.windowInstances.values():
            i.closeWindow()
        
