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
from ngSkinTools.ui.basetab import BaseTab
from ngSkinTools.ui.uiWrappers import FloatField, CheckBoxField, DropDownField
from ngSkinTools.doclink import SkinToolsDocs
from ngSkinTools.ui.initTransferWindow import InitTransferWindow,\
    MirrorWeightsWindow
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.events import LayerEvents, MayaEvents
from ngSkinTools.log import LoggerFactory

log = LoggerFactory.getLogger("mirror UI")

class TabMirror(BaseTab):
    TOOL_PAINT = 'ngSkinToolsLayerPaintCtx'

    # prefix for environment variables for this tab
    VAR_PREFIX = 'ngSkinToolsMirrorTab_'
    
    
    MIRROR_TEXTS = {'x':("Left to right (+X to -X)", "Right to left (-X to +X)"),
                    'y':("Top to bottom (+Y to -Y)", "Bottom to top (-Y to +Y)"),
                    'z':("Front to back (+Z to -Z)", "Back to front (-Z to +Z)"),
                    }
    
    MIRROR_GUESS = 'Guess from stroke'
    MIRROR_FLIP = 'Flip'
    
    def __init__(self):
        BaseTab.__init__(self)
        
        
    def getMirrorSideTexts(self):
        dataModel = LayerDataModel.getInstance();
        if dataModel.layerDataAvailable:
            mirrorAxis = dataModel.mirrorCache.mirrorAxis
            
            if self.MIRROR_TEXTS.has_key(mirrorAxis):
                return self.MIRROR_TEXTS[mirrorAxis]
        
        return self.MIRROR_TEXTS['x']
        
    def execInitMirror(self,*args):
        '''
        Show init transfer window
        '''
        t = MirrorWeightsWindow.getInstance()
        t.showWindow()
        return t
        
    def rebuildMirrorDirectionDropDown(self):
        self.controls.mirrorDirection.beginRebuildItems()
        self.controls.mirrorDirection.addOption(self.MIRROR_GUESS)
        for mirrorText in self.getMirrorSideTexts():
            self.controls.mirrorDirection.addOption(mirrorText)
        self.controls.mirrorDirection.addOption(self.MIRROR_FLIP)
        
        self.controls.mirrorDirection.endRebuildItems()
        
                
    def createUI(self,parent):
        from mainwindow import MainWindow
        
        mainActions = MainWindow.getInstance().actions
        self.setTitle('Mirror')
        
        # base layout
        self.cmdLayout = self.createCommandLayout([
                    ('Initialize', self.execInitMirror,''),
                    ('Mirror Weights', mainActions.mirrorWeights,'')
                    ], SkinToolsDocs.UI_TAB_MIRROR)
        
        mainActions.mirrorWeights.addUpdateControl(self.cmdLayout.innerLayout)
        
        # mirror options group

        group = self.controls.mirrorOptionsGroup = self.createUIGroup(self.cmdLayout.innerLayout, 'Mirroring Options')

        self.createFixedTitledRow(group, 'Mirror direction')
        self.controls.mirrorDirection = DropDownField(self.VAR_PREFIX+'mirrorDirection')
        self.rebuildMirrorDirectionDropDown()
        LayerEvents.mirrorCacheStatusChanged.addHandler(self.rebuildMirrorDirectionDropDown,parent)

        self.createFixedTitledRow(group, 'Mirror Seam Width')
        self.controls.mirrorWidth = FloatField(self.VAR_PREFIX+'mirrorWidth', minValue=0, maxValue=None, step=1.0, defaultValue=0.1, annotation='Defines width of the interpolation from left to right side on the model center line.')
        cmds.setParent(group)
        self.createTitledRow(group, 'Elements')
        self.controls.mirrorWeights = CheckBoxField(self.VAR_PREFIX+'MirrorWeights',label="Mirror weights",
                annotation='Check this if mirror operation should be mirroring weights',defaultValue=1)
        self.controls.mirrorMask = CheckBoxField(self.VAR_PREFIX+'MirrorMask',label="Mirror mask",
                annotation='Check this if mirror operation should be mirroring layer mask',defaultValue=1)
        self.controls.mirrorDq = CheckBoxField(self.VAR_PREFIX+'MirrorDualQuaternion',label="Mirror dual quaternion weights",
                annotation='Check this if mirror operation should be mirroring dual quaternion weights',defaultValue=1)
        
        MayaEvents.nodeSelectionChanged.addHandler(self.updateUIEnabled, self.cmdLayout.outerLayout.layout)
        
        self.updateUIEnabled()
        return self.cmdLayout.outerLayout.layout
    
    def updateUIEnabled(self):
        data = LayerDataModel.getInstance()
        
        self.controls.mirrorDq.setEnabled(data.layerDataAvailable and data.isDqMode())
        
