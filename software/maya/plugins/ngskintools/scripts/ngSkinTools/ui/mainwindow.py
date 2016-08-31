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
from ngSkinTools.version import Version
from ngSkinTools.ui.tabSkinRelax import TabSkinRelax
from ngSkinTools.ui.tabAssignWeights import TabAssignWeights
from ngSkinTools.ui.updateCheckWindow import UpdateCheckWindow
from ngSkinTools.utils import Utils
from ngSkinTools.ui.targetDataDisplay import TargetDataDisplay
from ngSkinTools.ui.uiWrappers import FormLayout
from ngSkinTools.ui.constants import Constants
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.tabMirror import TabMirror
from ngSkinTools.ui.tabPaint import TabPaint
from ngSkinTools.ui.dlgAbout import AboutDialog
from ngSkinTools.ui.actions import InfluenceFilterAction, NewLayerAction,\
    DeleteLayerAction, MoveLayerAction, LayerPropertiesAction,\
    ConvertMaskToTransparencyAction, ConvertTransparencyToMaskAction,\
    MirrorLayerWeightsAction, BaseAction, RemovePreferencesAction,\
    EnableDisableLayerAction, ExportAction, ImportAction, TransferWeightsAction,\
    MergeLayerDownAction, InvertPaintTargetAction
from ngSkinTools.ui.basetoolwindow import BaseToolWindow
from ngSkinTools.log import LoggerFactory
from ngSkinTools.importExport import Formats
from ngSkinTools.ui.utilities.importInfluencesUi import ImportInfluencesAction
from ngSkinTools.ui.utilities.duplicateLayerAction import DuplicateLayersAction
from ngSkinTools.ui.headlessDataHost import HeadlessDataHost
from ngSkinTools.doclink import SkinToolsDocs
from ngSkinTools.ui.utilities.weightsClipboardActions import CopyWeights,\
    CutWeights, PasteWeightsAdd, PasteWeightsReplace, PasteWeightsSubstract
from ngSkinTools.layerUtils import LayerUtils
from ngSkinTools.ui.tabSettings import TabSettings
from ngSkinTools.ui.options import PersistentValueModel
from ngSkinTools.ui.events import MayaEvents, MayaEventsHost, LayerEvents

log = LoggerFactory.getLogger("MainWindow")


class MainMenu:
    def __init__(self):
        pass
    
    def execCheckForUpdates(self,*args):
        UpdateCheckWindow.execute(silent=False)
        
    @Utils.undoable
    def execCleanNodes(self,*args):
        if not LayerUtils.hasCustomNodes():
            Utils.confirmDialog(icon='information', title='Info', message='Scene does not contain any custom ngSkinTools nodes.', button=['Ok']);
            return
        
        message = 'This command deletes all custom nodes from ngSkinTools plugin. Skin weights will be preserved, but all layer data will be lost. Do you want to continue?'
        if Utils.confirmDialog(
                icon='warning',
                title='Warning', 
                message=message, 
                button=['Yes','No'], defaultButton='No')!='Yes':
            return
        
        LayerDataModel.getInstance().cleanCustomNodes()
        
    def execAbout(self,*args):
        AboutDialog().execute()
        
    def createFileMenu(self,actions):
        cmds.menu( label='File',mnemonic='F' )
        actions.exportWeights.newMenuItem("Export Layers/Weights...")
        actions.importWeights.newMenuItem("Import Layers/Weights...")

    def createLayersMenu(self,actions):
        cmds.menu( label='Layers',mnemonic='L' )
        actions.newLayer.newMenuItem("New Layer...")
        actions.duplicateLayer.newMenuItem("Duplicate Selected Layer(s)")
        actions.deleteLayer.newMenuItem("Delete Selected Layer(s)")
        self.createDivider()
        actions.mergeLayerDown.newMenuItem("Merge Layer Down")
        self.createDivider()
        actions.moveLayerUp.newMenuItem("Move Current Layer Up")
        actions.moveLayerDown.newMenuItem("Move Current Layer Down")

        self.createDivider()
        actions.layerProperties.newMenuItem("Properties...")
        
    def createEditMenu(self,actions):
        cmds.menu( label='Edit',mnemonic='E' )
        actions.copyWeights.newMenuItem('Copy Influence Weights')
        actions.cutWeights.newMenuItem('Cut Influence Weights')
        actions.pasteWeightsAdd.newMenuItem('Paste Weights (Add)')
        actions.pasteWeightsSubstract.newMenuItem('Paste Weights (Substract)')
        actions.pasteWeightsReplace.newMenuItem('Paste Weights (Replace)')
        self.createDivider()
        actions.convertMaskToTransparency.newMenuItem('Convert Mask to Transparency')
        actions.convertTransparencyToMask.newMenuItem('Convert Transparency to Mask')
        self.createDivider()
        actions.invertPaintTarget.newMenuItem('Invert')
        self.createDivider()
        cmds.menuItem( label='Delete Custom Nodes',command=self.execCleanNodes)
        actions.removePreferences.newMenuItem('Reset to Default Preferences')

    def createToolsMenu(self,actions):
        cmds.menu( label='Tools',mnemonic='T' )
        actions.importInfluences.newMenuItem("Import Influences...")
        actions.transferWeights.newMenuItem("Transfer Weights...")
        
    def viewManual(self,*args):
        documentation = HeadlessDataHost.get().documentation
        documentation.openLink(SkinToolsDocs.DOCUMENTATION_ROOT)
        
    def openLocation(self,url):
        import webbrowser
        webbrowser.open_new(url)
    
    def openIssueTracker(self,*args):
        self.openLocation("http://www.ngskintools.com/issue-tracker")

    def openContactForm(self,*args):
        self.openLocation("http://ngskintools.com/contact/")
        
    def openDonationsPage(self,*args):
        self.openLocation("http://ngskintools.com/donate/")
        

    def createHelpMenu(self,actions):
        cmds.menu( label='Help',mnemonic='H' )
        cmds.menuItem( label='View Manual Online',command=self.viewManual )
        cmds.menuItem( label='Contact Author directly',command=self.openContactForm )
        cmds.menuItem( label='Check for Updates',command=self.execCheckForUpdates )
        self.createDivider()
        cmds.menuItem( label='Donate!',command=self.openDonationsPage )
        self.createDivider()
        cmds.menuItem( label='Planned Features and Known Issues',command=self.openIssueTracker)
        cmds.menuItem( label='About ngSkinTools',mnemonic='A',command=self.execAbout )
        
    def createDivider(self):
        cmds.menuItem( divider=True)
        
        
    def create(self):
        actions = MainWindow.getInstance().actions
        
        self.createFileMenu(actions)
        self.createLayersMenu(actions)
        self.createEditMenu(actions)
        self.createToolsMenu(actions)
        self.createHelpMenu(actions)



        
    
class MainUiActions:
    def __init__(self,ownerUI):
        self.influenceFilter = InfluenceFilterAction(ownerUI) 
        self.newLayer = NewLayerAction(ownerUI)
        self.deleteLayer = DeleteLayerAction(ownerUI)
        self.moveLayerUp = MoveLayerAction(True,ownerUI)
        self.moveLayerDown = MoveLayerAction(False,ownerUI)
        self.layerProperties = LayerPropertiesAction(ownerUI)
        self.removePreferences = RemovePreferencesAction(ownerUI)
        
        self.convertMaskToTransparency = ConvertMaskToTransparencyAction(ownerUI)
        self.convertTransparencyToMask = ConvertTransparencyToMaskAction(ownerUI)
        
        self.invertPaintTarget = InvertPaintTargetAction(ownerUI)
        
        self.mirrorWeights = MirrorLayerWeightsAction(ownerUI)
        self.enableDisableLayer = EnableDisableLayerAction(ownerUI)
        
        self.importInfluences = ImportInfluencesAction(ownerUI)
        self.transferWeights = TransferWeightsAction(ownerUI)
        
        self.duplicateLayer = DuplicateLayersAction(ownerUI)
        
        self.mergeLayerDown = MergeLayerDownAction(ownerUI)
        
        self.copyWeights = CopyWeights(ownerUI)
        self.cutWeights = CutWeights(ownerUI)
        self.pasteWeightsAdd = PasteWeightsAdd(ownerUI)
        self.pasteWeightsReplace = PasteWeightsReplace(ownerUI)
        self.pasteWeightsSubstract = PasteWeightsSubstract(ownerUI)
        

                
        self.importWeights = ImportAction(ownerUI,ioFormat=Formats.getJsonFormat())
        self.exportWeights = ExportAction(ownerUI,ioFormat=Formats.getJsonFormat())
        
    def updateEnabledAll(self):
        '''
        updates all actions hosted in this instance
        '''
        
        # update all field-based actions
        for i in dir(self):
            field = getattr(self,i)
            if isinstance(field,BaseAction):
                field.updateEnabled()
                

class MainWindow(BaseToolWindow):
    WINDOW_NAME = 'ngSkinToolsMainWindow'
    DOCK_NAME = 'ngSkinToolsMainWindow_dock'
    
    @staticmethod
    @Utils.visualErrorHandling
    def open():
        '''
        just a shortcut method to construct and display main window
        '''

        window = MainWindow.getInstance()
        
        if cmds.control(MainWindow.DOCK_NAME,q=True,exists=True):
            cmds.control(MainWindow.DOCK_NAME,e=True,visible=True)
        else:
            cmds.dockControl(MainWindow.DOCK_NAME,l=window.createWindowTitle(),content=MainWindow.WINDOW_NAME,
                             area='right',allowedArea=['right', 'left'],
                             width=window.preferedWidth.get(),
                             floating=window.preferedFloating.get(),
                             visibleChangeCommand=window.visibilityChanged)
            
            if window.preferedFloating.get():
                cmds.window(MainWindow.DOCK_NAME,e=True,
                            topEdge=window.preferedTop.get(),leftEdge=window.preferedLeft.get(),
                            w=window.preferedWidth.get(),h=window.preferedHeight.get())
        
            Utils.silentCheckForUpdates()
        
        # bring tab to front; evaluate lazily as sometimes UI can show other errors and this command somehow fails
        cmds.evalDeferred(lambda *args: cmds.dockControl(MainWindow.DOCK_NAME,e=True,r=True));
        
        # a bit of a fake, but can't find a better place for an infrequent save
        LayerEvents.layerAvailabilityChanged.addHandler(window.savePrefs, MainWindow.DOCK_NAME)
        
        return window
    
    def visibilityChanged(self,*args):
        hidden = cmds.control(MainWindow.DOCK_NAME,q=True,isObscured=1)
            
        if hidden:
            self.savePrefs()

    def savePrefs(self):
        if cmds.dockControl(MainWindow.DOCK_NAME,exists=True):
            self.preferedFloating.set(cmds.dockControl(MainWindow.DOCK_NAME,q=True,floating=True))
            self.preferedWidth.set(cmds.dockControl(MainWindow.DOCK_NAME,q=True,w=True))

        if cmds.window(MainWindow.DOCK_NAME,exists=True):
            self.preferedWidth.set(cmds.window(MainWindow.DOCK_NAME,q=True,w=True))
            self.preferedHeight.set(cmds.window(MainWindow.DOCK_NAME,q=True,h=True))
            self.preferedTop.set(cmds.window(MainWindow.DOCK_NAME,q=True,topEdge=True))
            self.preferedLeft.set(cmds.window(MainWindow.DOCK_NAME,q=True,leftEdge=True))
        
        
    @staticmethod
    def getInstance():
        '''
        returns instance of a main window; returned value is only valid while window is opened.
        
        :rtype: MainWindow
        '''
        
        return BaseToolWindow.getWindowInstance(MainWindow.WINDOW_NAME,MainWindow)
        
        
    def __init__(self,windowName):
        log.debug("creating main window")
        
        BaseToolWindow.__init__(self,windowName)
        
        self.windowTitle = self.createWindowTitle()
        
        self.mainTabLayout = None
        self.tabs = []
        
        
        # layer target UI - compound for layers list/no layer data ui
        self.targetUI = None
        
        self.actions = None
        
        self.preferedWidth = PersistentValueModel('ngSkinToolsMainWindow_preferedWidth', 400);
        self.preferedHeight = PersistentValueModel('ngSkinToolsMainWindow_preferedHeight',400);
        self.preferedTop = PersistentValueModel('ngSkinToolsMainWindow_preferedTop');
        self.preferedLeft = PersistentValueModel('ngSkinToolsMainWindow_preferedLeft');
        self.preferedFloating = PersistentValueModel('ngSkinToolsMainWindow_preferedFloating',False)
        
        self.useUserPrefSize = False
        
        self.defaultWidth = self.preferedWidth.get()
        self.defaultHeight = self.preferedHeight.get()
        
        self.sizeable = True
        


    def createWindowTitle(self):
        '''
        creates main window title
        '''
        return Version.getReleaseName()
    
    def createWindow(self):
        '''
            creates main GUI window and it's contents
        '''
        
    
        BaseToolWindow.createWindow(self)
        
        self.targetUI = TargetDataDisplay()
        self.actions = MainUiActions(self.windowName)
        
        self.mainMenu = MainMenu()
        self.mainMenu.create();
        
        
        

        # putting tabs in a from targetUiLayout is needed to workaround maya2011 
        # bug with an additional empty tab appearing otherwise
        
        
        self.splitPosition = PersistentValueModel(name="ngSkinTools_mainWindow_splitPosition", defaultValue=50)
        def updateSplitPosition(*args):
            size = cmds.paneLayout(horizontalSplit,q=True,paneSize=True)
            # returns (widht, height, width, height)
            self.splitPosition.set(int(size[1]))
        horizontalSplit = cmds.paneLayout(configuration="horizontal2",width=100,height=200,separatorMovedCommand=updateSplitPosition)
        cmds.paneLayout(horizontalSplit,e=True,staticHeightPane=2)
        cmds.paneLayout(horizontalSplit,e=True,paneSize=(1,100,self.splitPosition.get()))
        cmds.paneLayout(horizontalSplit,e=True,paneSize=(2,100,100-self.splitPosition.get()))
        
        
        
        targetUiLayout = self.targetUI.create(horizontalSplit)
        self.mainTabLayout = cmds.tabLayout(childResizable=True,parent=horizontalSplit,scrollable=False,innerMarginWidth=3)        
        
        
        
        self.tabPaint = self.addTab(TabPaint())
        self.tabMirror = self.addTab(TabMirror())
        self.tabRelax = self.addTab(TabSkinRelax())
        self.tabAssignWeights = self.addTab(TabAssignWeights())
        self.tabSettings = self.addTab(TabSettings())
        
        self.actions.updateEnabledAll()
        
        
        
    def addTab(self,tab):
        '''
        adds tab object to tab UI, creating it's ui and attaching to main window
        '''
        cmds.setParent(self.mainTabLayout)
        layout = tab.createUI(self.mainTabLayout)
        cmds.tabLayout( self.mainTabLayout, edit=True, tabLabel=((layout, tab.getTitle())));
        tab.parentWindow = self
        self.tabs.append(tab)
        
        return tab
        

        
    def findTab(self,tabClass):
        for i in self.tabs:
            if isinstance(i,tabClass):
                return i
            
        return None    