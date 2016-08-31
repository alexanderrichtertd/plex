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

import threading
from ngSkinTools.utils import Utils
from maya import cmds
from ngSkinTools.ui.uiWrappers import CheckBoxField
from ngSkinTools.ui.options import Options
from ngSkinTools.ui.constants import Constants
from ngSkinTools.ui.basetoolwindow import BaseToolWindow
from datetime import datetime
from ngSkinTools.log import LoggerFactory
from ngSkinTools.context import applicationContext
import logging
import maya


log = LoggerFactory.getLogger("updateCheckWindow")


class UpdateCheckWindow(BaseToolWindow):
    '''
    An interface for Check-For-Updates feature.
    '''
    
    UPDATE_THREAD = None
    
    def __init__(self,windowName):
        BaseToolWindow.__init__(self,windowName)
        self.updateAvailable = False
        self.windowTitle = 'NgSkinTools Update'
        self.defaultWidth = 500
        self.defaultHeight = 400
        self.sizeable = True
        self.useUserPrefSize = False
    
    def createWindow(self):
        BaseToolWindow.createWindow(self)
        margin1 = 5 
        margin2 = 10

        form = cmds.formLayout(parent=self.windowName)
        self.topLabel = cmds.text(label='',font='boldLabelFont')
        self.customUIContainer = cmds.columnLayout(adjustableColumn=1,rowSpacing=margin2)
        cmds.separator()
        cmds.setParent('..')
        
        lowerRow = cmds.formLayout(height=Constants.BUTTON_HEIGHT)
        checkBox = CheckBoxField(Options.OPTION_CHECKFORUPDATES,label='Automatically check for updates',
                      annotation='Check for updates automatically when ngSkinTools window is opened (once per Maya application session)')
        closeButton = cmds.button(label='Close',align='center',width=80,command=lambda *args:self.closeWindow())

        cmds.formLayout(lowerRow,e=True,attachForm=[(closeButton,'top',0)])
        cmds.formLayout(lowerRow,e=True,attachNone=[(closeButton,'left')])
        cmds.formLayout(lowerRow,e=True,attachForm=[(closeButton,'right',margin1)])
        cmds.formLayout(lowerRow,e=True,attachForm=[(closeButton,'bottom',0)])

        cmds.formLayout(lowerRow,e=True,attachForm=[(checkBox.field,'top',0)])
        cmds.formLayout(lowerRow,e=True,attachForm=[(checkBox.field,'left',margin1)])
        cmds.formLayout(lowerRow,e=True,attachControl=[(checkBox.field,'right',margin1,closeButton)])
        cmds.formLayout(lowerRow,e=True,attachForm=[(checkBox.field,'bottom',0)])

        
        
        cmds.formLayout(form,e=True,attachForm=[(self.topLabel,'top',margin2)])
        cmds.formLayout(form,e=True,attachForm=[(self.topLabel,'left',margin1)])
        cmds.formLayout(form,e=True,attachNone=[(self.topLabel,'right')])
        cmds.formLayout(form,e=True,attachNone=[(self.topLabel,'bottom')])

        cmds.formLayout(form,e=True,attachNone=[(lowerRow,'top')])
        cmds.formLayout(form,e=True,attachForm=[(lowerRow,'left',margin1)])
        cmds.formLayout(form,e=True,attachForm=[(lowerRow,'right',margin1)])
        cmds.formLayout(form,e=True,attachForm=[(lowerRow,'bottom',margin1)])
        
        cmds.formLayout(form,e=True,attachControl=[(self.customUIContainer,'top',margin2,self.topLabel)])
        cmds.formLayout(form,e=True,attachForm=[(self.customUIContainer,'left',margin1)])
        cmds.formLayout(form,e=True,attachForm=[(self.customUIContainer,'right',margin1)])
        cmds.formLayout(form,e=True,attachControl=[(self.customUIContainer,'bottom',margin2,lowerRow)])
        
    def setTopLabel(self,message):
        cmds.text(self.topLabel,e=True, label=message)
        
    def addMessage(self,message):
        cmds.text(label=message,parent=self.customUIContainer,wordWrap=True,width=300,align='left')
        
    def addButton(self,title,command):
        cmds.button(label=title,parent=self.customUIContainer,command=lambda *args:command())
    
        
    @staticmethod
    def execute(silent=False):
        '''
        executes update. when silent is true, only "update available" window will be shown,
        no "loading" or "no update available"
        
        this is a non-blocking method, returning immediately 
        after update thread is initiated.
        
        this method also ensures that two concurent threads can't be launched, as first 
        launched has to complete before second one can be created
        '''
        
        if Utils.DEBUG_MODE:
            return
        
        if UpdateCheckWindow.UPDATE_THREAD is None or not UpdateCheckWindow.UPDATE_THREAD.isAlive():
            UpdateCheckWindow.UPDATE_THREAD = UpdateCheckThread(silent)
            UpdateCheckWindow.UPDATE_THREAD.start();
        else:
            from maya import OpenMaya as om
            om.MGlobal.displayWarning('update check is already running')
            

class LinkOpener:
    '''
    proxy callable object to open links (serves as "command" object for link buttons)
    '''
    def __init__(self,link):
        self.link = link
    
    def __call__(self,*args):
        import webbrowser
        webbrowser.open(self.link)


class MainThreadResultsDisplay:
    def __init__(self,display):
        self.resultsDisplay = display
        
    def showInfoWindow(self,title,message):
        maya.utils.executeInMainThreadWithResult(self.resultsDisplay.showInfoWindow,title,message)
        
    def showResultsWindow(self,checker):
        maya.utils.executeInMainThreadWithResult(self.resultsDisplay.showResultsWindow,checker)

class ResultsDisplay:        
    WINDOW_NAME='ngSkinToolsUpdateCheckWindow'
    
    def showInfoWindow(self,title,message):
        BaseToolWindow.destroyWindow(self.WINDOW_NAME)
        w = BaseToolWindow.getWindowInstance(self.WINDOW_NAME, UpdateCheckWindow)
        w.setTopLabel(title)
        w.addMessage(message)
        w.showWindow()

    def showResultsWindow(self,checker):
        BaseToolWindow.destroyWindow(self.WINDOW_NAME)
        w = BaseToolWindow.getWindowInstance(self.WINDOW_NAME, UpdateCheckWindow)
        w.setTopLabel('Update Available' if checker.updateAvailable else 'No Updates Found')
        
        if checker.updateAvailable:
            w.addMessage("New plugin version available: %s"%checker.updateTitle)
        else:
            w.addMessage("Plugin is up to date")

        time = datetime.strptime(checker.updateDate,"%Y-%m-%dT%H:%M:%S+00:00")
        w.addMessage("Released date: %s"%time.strftime("%d %B, %Y"))
        
        for i in checker.links:
            w.addButton(i.title,LinkOpener(i.url))
        
        w.showWindow()

        
    
class UpdateCheckThread(threading.Thread):
    
    
    '''
    This thread enables the non-blocking load of update information from the server,
    showing "loading.." window while it's working, then switching to "finished.." window when done
    '''
    def __init__(self,silent):
        threading.Thread.__init__(self)
        self.silent=silent
        self.updateResultsDisplay = MainThreadResultsDisplay(ResultsDisplay())
        self.checker = applicationContext.createVersionChecker()
        
    def run(self):
        log.info('update check started')
        if not self.silent:
            self.updateResultsDisplay.showInfoWindow('Please wait...','Information is being retrieved from ngSkinTools server.')
        
        try:   
            self.checker.execute()
            
            if not self.silent or self.checker.isUpdateAvailable():
                self.updateResultsDisplay.showResultsWindow(self.checker)
                
            log.info('update check finished')
        except Exception,err:
            if not self.silent:
                self.updateResultsDisplay.showInfoWindow('Error occurred','Error occurred while getting information from the server:'+str(err))
            if log.isEnabledFor(logging.DEBUG):
                import traceback;log.debug(traceback.format_exc())
            log.error('update encountered an error')
        
        
            
