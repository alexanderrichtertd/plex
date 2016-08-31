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
from ngSkinTools.utils import Utils, MessageException
from ngSkinTools.ui.basetab import BaseTab
from ngSkinTools.ui.intensityslider import IntensitySlider
from ngSkinTools.doclink import SkinToolsDocs
from ngSkinTools.ui.uiWrappers import IntField, FloatField, CheckBoxField
from ngSkinTools.ui.softSelectionRow import SoftSelectionRow
from ngSkinTools.log import LoggerFactory

     


log = LoggerFactory.getLogger("tabSkinRelax")
    
    

class TabSkinRelax(BaseTab):
    '''
        Defines a UI function set for Weights Relax operations.
    '''
    
    # prefix for environment variables for this tab
    VAR_RELAX_PREFIX = 'ngSkinToolsRelaxTab_'
    
     

    def __init__(self):
        BaseTab.__init__(self)
    
    @Utils.visualErrorHandling
    def execRelax(self,*args):
        '''
            relax button click handler. this is where it actually 
            executes skin relax, whoop-tee-doo.
        '''
        try:

            args = {}
            args['numSteps']=self.controls.numSteps.getValue()
            args['stepSize']=self.controls.stepSize.getValue()
            
            # do we need soft selection?
            self.controls.softSelection.addToArgs(args)
            
                
            # do we need volume association?
            if self.controls.useVolumeAssociation.getValue():
                args['abv']=1
                args['avr']=self.controls.volumeAssociationRadius.getValue()

            # add selection+highlight as arguments
            # we need highlight as second argument because
            # other meshes for simulation might be included only through highlight.
            #
            # This will never be an empty list as we tested for vertex selection available earlier
            def makeList(listOrNull):
                if listOrNull is None:
                    return []
                return listOrNull
            
            objects = makeList(cmds.ls(sl=True))+makeList(cmds.ls(hl=True))
            
            if len(objects)==0:
                raise MessageException("Nothing is selected")
            
            # execute stuff  
            try:
                cmds.waitCursor(state=True)
                cmds.ngSkinRelax(objects,**args)
            finally:
                cmds.waitCursor(state=False)
                
            Utils.refreshPaintWeightsTool()
            
        except MessageException,err:
            raise err
        except Exception,err:
            
            log.error('unknown error: '+err.message)
            # remap error to a more meaningful
            Utils.testPluginLoaded()
            
            # unknown error,reraise it
            raise err
        
    def intensitySliderPreset(self):
        '''
        called from a slider change; set new numsteps and stepsize values
        '''
        intensity = self.controls.intensitySlider.getIntensity() 
        self.controls.numSteps.setValue(10+int(round(40*intensity)))
        self.controls.stepSize.setValue(0.3*intensity)
        
    
    def createPrecisionControlGroup(self,layout):
        group = self.createUIGroup(layout,"Intensity/Precision Control")

        self.createTitledRow(group, "Intensity preset")
        self.controls.intensitySlider = IntensitySlider(
                'Drag slider to quickly set "number of steps" and "step size" aproximatelly corresponding to low or high relax intensity values',
                self.VAR_RELAX_PREFIX+'relaxIntensity',0.5)
        self.controls.intensitySlider.changeCommand.addHandler(self.intensitySliderPreset)
        self.controls.intensitySlider.create()
        
        self.createFixedTitledRow(group, 'Number of steps')
        self.controls.numSteps = IntField(self.VAR_RELAX_PREFIX+'NumSteps', minValue=1,maxValue=1000,step=1,defaultValue=30,
                annotation='Defines amount of times to repeat relax procedure. Recommended: 20 - 50')
        
        self.createFixedTitledRow(group, 'Step size')
        self.controls.stepSize = FloatField(self.VAR_RELAX_PREFIX+'StepSize', minValue=0, maxValue=1,step=0.001,defaultValue=0.15, 
                annotation='Defines a slight amount of relax applied with each step (0 - 1.0). Recommended: 0.02 - 0.15')
        
        
    def createVolumeAssociationGroup(self,layout):
        group = self.createUIGroup(layout,"Surface and Volume Association Rules")

        self.controls.softSelection = SoftSelectionRow(self.VAR_RELAX_PREFIX+'softSelection')
        self.controls.softSelection.create(group)

        cmds.setParent(group)
        self.controls.useVolumeAssociation = CheckBoxField(self.VAR_RELAX_PREFIX+'associateByVolume',defaultValue=0,label="Associate by volume",
                annotation='when turned on, smoothing will extend across vertices that are not connected by edges (across shell borders, seams, close-by meshes, etc)')
        
        self.controls.useVolumeAssociation.changeCommand.addHandler(self.updateUIEnabled) 

        self.controls.volumeSearchRow = self.createFixedTitledRow(group, "Volume search radius")
        self.controls.volumeAssociationRadius = FloatField(self.VAR_RELAX_PREFIX+'associateByVolumeRadius',minValue=0, maxValue=10000,step=0.1, 
                defaultValue=10,
                annotation='search radius of volume association. set this to a fairly little value, just a little above distance of the gap you are trying to "close"')

        
    def updateUIEnabled(self):
        useVolumeSearch = self.controls.useVolumeAssociation.getValue()
        cmds.layout(self.controls.volumeSearchRow,e=True,enable=useVolumeSearch)
        
        
    def createUI(self,parent):
        self.setTitle('Relax')
        
        self.cmdLayout = self.createCommandLayout([('Relax', self.execRelax,'Executes relax on a current vertices selection.')], SkinToolsDocs.UI_TAB_RELAX)
        
        self.createPrecisionControlGroup(self.cmdLayout.innerLayout)
        self.createVolumeAssociationGroup(self.cmdLayout.innerLayout)
        
        self.updateUIEnabled()
        return self.cmdLayout.outerLayout