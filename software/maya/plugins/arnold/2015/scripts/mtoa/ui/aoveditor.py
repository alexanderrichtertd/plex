import pymel.core as pm
from mtoa.callbacks import *
import mtoa.aovs as aovs
import mtoa.utils as utils
import mtoa.ui.ae.shaderTemplate as shaderTemplate
import mtoa.ui.ae.templates as templates
import mtoa.core as core
import mtoa.callbacks as callbacks
import mtoa.hooks as hooks

from collections import defaultdict
import sys

import maya.OpenMaya as om

UI_NAME = 'ArnoldAOVUI'
AOV_ATTRS = ('name', 'type', 'prefix')
WIDTH = 402

AOV_ROW_WIDTHS = [18, 110, 74]
OUTPUT_ROW_WIDTHS = [60, 90]
    
def _uiName(tag):
    return '%s_%s' % (UI_NAME, tag)

global _updating
_updating = False

AOV_CALLBACK_ATTRS = ('type', 'defaultValue')

class AOVBrowser(object):
    '''
    A UI for browsing node types and their registered AOVs
    '''
    def __init__(self, renderOptions=None, nodeTypes=None, listAOVGroups=True, showGroupsColumn=True):
        '''
        renderOptions : an aovs.AOVInterface instance, or None to use the default
        
        nodeTypes : a list of node types to display in the available nodes column, 
            or None to display the complete list of nodes with AOVs
        '''
        self.allAOVs = set([])
        self.renderOptions = aovs.AOVInterface() if renderOptions is None else renderOptions
        self.allNodeTypes = set(aovs.getNodeTypesWithAOVs())
        if nodeTypes:
            self.setNodeTypes(nodeTypes)
        else:
            self.nodeTypes = sorted(self.allNodeTypes)

        self.doAOVGroups = listAOVGroups
        self.doGroups = showGroupsColumn

        self.form = pm.formLayout()
        if self.doGroups:
            groupsLbl = pm.text(_uiName('groupsLbl'), align='center', label='AOV Groups')
        availableLbl = pm.text(_uiName('availableLbl'), align='center', label='Available AOVs')
        activeLbl = pm.text(_uiName('activeLbl'), align='center', label='Active AOVs')

        if self.doGroups:
            self.groupLst = pm.textScrollList(_uiName('groupLst'), numberOfRows=10, allowMultiSelection=True,
                          selectCommand=self.updateActiveAOVs)
        self.availableLst = pm.textScrollList(_uiName('availableLst'), numberOfRows=10, allowMultiSelection=True,
                          doubleClickCommand=self.addAOVs)
        self.activeLst = pm.textScrollList(_uiName('activeLst'), numberOfRows=10, allowMultiSelection=True,
                          doubleClickCommand=self.removeAOVs)

        addBtn = pm.button(_uiName('addBtn'), label='>>', command=self.addAOVs)
        remBtn = pm.button(_uiName('remBtn'), label='<<', command=self.removeAOVs)

        pm.formLayout(self.form, edit=True, attachForm=[
                                    (groupsLbl, 'top', 1),
                                    (availableLbl, 'top', 1),
                                    (activeLbl, 'top', 1),
                                    
                                    (groupsLbl, 'left', 1),
                                    (self.groupLst, 'left', 1),
                                    
                                    (activeLbl, 'right', 1),
                                    (self.activeLst, 'right', 1),
                                    
                                    (remBtn, 'right', 1),
                                    (addBtn, 'bottom', 1),
                                    (remBtn, 'bottom', 1),
                               ])
        pm.formLayout(self.form, edit=True, attachControl=[
                                    #(availableLbl, 'left', 1, groupsLbl),
                                    
                                    (self.groupLst, 'top', 1, groupsLbl),
                                    (self.activeLst, 'top', 1, activeLbl),
                                    (self.availableLst, 'top', 1, availableLbl),
                                    
                                    (self.groupLst, 'bottom', 1, addBtn),
                                    (self.activeLst, 'bottom', 1, addBtn),
                                    (self.availableLst, 'bottom', 1, remBtn),
                                    
                                    (addBtn, 'right', 1, remBtn),
#                                    (addBtn, 'top', 1, self.activeLst),
#                                    (remBtn, 'top', 1, self.availableLst)
                                ])

        pm.formLayout(self.form, edit=True, attachPosition=[
                                    (groupsLbl, 'right', 1, 33),
                                    (availableLbl, 'left', 1, 33),
                                    (availableLbl, 'right', 1, 66),
                                    (activeLbl, 'left', 1, 66),
                                    
                                    (self.groupLst, 'right', 1, 33),
                                    (self.availableLst, 'left', 1, 33),
                                    (self.availableLst, 'right', 1, 66),
                                    (self.activeLst, 'left', 1, 66),
                                    
                                    (addBtn, 'left', 1, 33),
                                    (addBtn, 'right', 1, 66),
                                    (remBtn, 'left', 1, 66),
                                ])
 


    def setNodeTypes(self, nodeTypes):
        '''set the node types listed in the AOV Groups column'''
        self.nodeTypes = sorted(self.allNodeTypes.intersection(nodeTypes))
 
    def populate(self):
        '''
        update the contents of all scroll lists
        '''
        if self.doGroups:
            pm.textScrollList(self.groupLst, edit=True, removeAll=True)
            if self.doAOVGroups:
                for nodeType in aovs.getAOVGroups():
                    pm.textScrollList(self.groupLst, edit=True, append=nodeType)
            for nodeType in self.nodeTypes:
                # make sure we have at least one named aov
                # FIXME: what does an empty AOV mean? why are these nodes returned by getNodeTypesWithAOVs()?  
                #if any([x for x in aovs.getRegisteredAOVs(nodeType=nodeType) if x]):
                pm.textScrollList(self.groupLst, edit=True, append=nodeType)
        # populate available and active based on aovs provided by groups and nodes
        self.updateActiveAOVs()

    def addAOVs(self, *args):
        '''
        create the selected AOVs, and connect the new AOV nodes to their corresponding
        AOV attributes for any nodes in the scene.
        '''
        sel = pm.textScrollList(self.availableLst, query=True, selectItem=True)
        if sel:
            global _updating
            _updating = True
            try:
                for aovName in sel:
                    aov = self.renderOptions.addAOV(aovName)
            finally:
                _updating = False
            self.updateActiveAOVs()

    def removeAOVs(self, *args):
        '''
        delete the selected AOVs
        '''
        sel = pm.textScrollList(self.activeLst, query=True, selectItem=True)
        if sel:
            global _updating
            _updating = True
            try:
                self.renderOptions.removeAOVs(sel)
                for aov in sel:
                    pm.textScrollList(self.availableLst, edit=True, append=aov)
                    pm.textScrollList(self.activeLst, edit=True, removeItem=aov)
            finally:
                _updating = False
            self.updateActiveAOVs()

    def updateActiveAOVs(self):
        '''
        fill the active and inactive columns based on the nodeType/group selected
        '''
        if _updating:
            return
        
        if not self.doGroups or (not self.doAOVGroups and len(self.nodeTypes) == 1):
            groups = self.nodeTypes
        else:
            groups = pm.textScrollList(self.groupLst, query=True, selectItem=True)

        # first, find out what's selected, so we can reselect any persistent items
        availableSel = pm.textScrollList(self.availableLst, query=True, selectItem=True)
        activeSel = pm.textScrollList(self.activeLst, query=True, selectItem=True)
        availableList = []
        activeList = []

        # update the available list
        pm.textScrollList(self.availableLst, edit=True, removeAll=True)
        pm.textScrollList(self.activeLst, edit=True, removeAll=True)
        try:
            activeAOVs = self.renderOptions.getAOVs()
        except pm.MayaNodeError:
            activeAOVs = []
        self.allAOVs = set([])
        for group in groups:
            if group.startswith('<'):
                # it's an AOV group
                aovList = aovs.getGroupAOVs(group)
            else:
                aovList = [x for x in aovs.getRegisteredAOVs(nodeType=group) if x]
            self.allAOVs.update(aovList)
            for aovName in aovList:
                if aovName not in activeAOVs:
                    if aovName not in availableList:
                        availableList.append(aovName)
                else:
                    if aovName not in activeList:
                        activeList.append(aovName)
        # update sorted and not duplicated available AOVs
        availableList.sort()
        for aovName in availableList:
            pm.textScrollList(self.availableLst, edit=True, append=aovName)
            if aovName in availableSel:
                pm.textScrollList(self.availableLst, edit=True, selectItem=aovName)
        # update sorted and not duplicated active AOVs
        activeList.sort()
        for aovName in activeList:
            pm.textScrollList(self.activeLst, edit=True, append=aovName)
            if aovName in activeSel:
                pm.textScrollList(self.activeLst, edit=True, selectItem=aovName)

class AOVItem(object):
    '''
    Builds the UI for a single AOV control, which may contain multiple outputs (Driver + Filter combo)
    '''

    def __init__(self, parent, aovObject, lockName=False):
        self.outputsChanged = True
        self.parent = parent
        self.aov = aovObject
        DARK_BLUE = [.16, .17, .2]
        aovNode = self.aov.node

        self.baseWidget = pm.cmds.columnLayout(adj=True)

        pm.cmds.rowLayout(nc=3,
                     rowAttach=([1, 'top', 2],
                                [3, 'top', 2]),
                     columnWidth3=[sum(AOV_ROW_WIDTHS)+8, sum(OUTPUT_ROW_WIDTHS)+8, 20],
                     columnAttach3=['right', 'both', 'both'])

        # AOV UI --------
        pm.cmds.rowLayout(nc=3,
                     
                     columnWidth3=AOV_ROW_WIDTHS,
                     columnAttach3=['right', 'both', 'both'])

        self.enabledCtrl = pm.cmds.checkBox(label='')
        pm.connectControl(self.enabledCtrl, aovNode.attr('enabled'))

        nameAttr = aovNode.attr('name')
        # use evalDeferred to ensure that the update happens after the aov node attribute is set
        self.nameCtrl = pm.textField(editable=not lockName,
                                # we save out the current aov name for the replaceShadingGroupDummyAttrs callback
                                changeCommand=lambda new, old=nameAttr.get(): self.aov.rename(new, old)
                                )
        pm.connectControl(self.nameCtrl, nameAttr)
        # must set editability after connecting control
        self.nameCtrl.setEditable(not lockName)
        if aovNode.isReferenced():
            # orange
            self.nameCtrl.setBackgroundColor(DARK_BLUE)

        #pm.text(label='name')
        # attrEnumOptionMenu does not work with multi-attrs and optionMenu does not work with connectControl,
        # so, unfortunately, our best option is attrEnumOptionMenuGrp
        self.channelsMenu = pm.cmds.attrEnumOptionMenuGrp(attribute=str(aovNode.attr('type')), columnWidth2=[1, 50])

        pm.setParent('..')

        pm.cmds.frameLayout(labelVisible=False)
        self.outputColumn = pm.cmds.columnLayout(adj=True, rowSpacing=2)

        # cache the list of outputs
        self.outputs = []
        for outputAttr in aovNode.attr('outputs'):
            try:
                outputRow = AOVOutputItem(self.outputColumn, outputAttr, self)
            except IndexError:
                continue
            else:
                self.outputs.append(outputRow)
                #pm.symbolButton(image="navButtonConnected.png")
                #pm.symbolButton(image="smallTrash.png")
                pm.setParent('..')

        pm.setParent('..')
        pm.setParent('..')


        aovMenuButton = pm.cmds.symbolButton(image="arrowDown.png")
#        pm.symbolButton(image="smallTrash.png",
#                        command=lambda *args: self.parent.removeAOV(aovNode))

        self.popupMenu = pm.cmds.popupMenu(parent=aovMenuButton, button=1, postMenuCommand=self.buildPopupMenu)

        pm.setParent('..')
        pm.setParent('..')

    def aovName(self):
        return self.aov.node.attr('name').get()

    def getMenus(self):
        '''
        Get a list of all of the menus in this AOVItem
        '''
        # flatten the menus
        return [row.filterMenu for row in self.outputs]

    def fixOptionMenus(self):
        for menu in self.getMenus():
            pm.optionMenu(menu, edit=True, visible=False)
            pm.optionMenu(menu, edit=True, visible=True)

    def delete(self):
        '''
        Delete the control and all of its children
        '''
        pm.deleteUI(self.baseWidget)

    def addOutput(self):
        '''
        Connect the defaultArnoldDriver and defaultArnoldFilter to the next available
        output on the aiAOV node for this AOVItem, then build a sub-UI for it
        '''
        # all new output starts with the default driver/filter nodes
        driverNode = pm.PyNode('defaultArnoldDriver')
        filterNode = pm.PyNode('defaultArnoldFilter')
        outputAttr = self.aov.node.attr('outputs')
        outputAttr = outputAttr.elementByLogicalIndex(outputAttr.numElements())
 
        driverNode.message.connect(outputAttr.driver)
        filterNode.message.connect(outputAttr.filter)
        outputRow = AOVOutputItem(self.outputColumn, outputAttr, self)
        self.outputs.append(outputRow)
        self.outputsChanged = True

    def removeOutput(self, index):
        '''
        Disconnect the driver and filter nodes at the given index from the aiAOV node for this AOVItem.
        Delete the driver and filter nodes if they are no longer used by any AOVs. Delete the UI
        for this output.
        '''
        outputRow = self.outputs.pop(index)
        outputRow.delete()
        self.outputsChanged = True
        #pm.evalDeferred(self.fixOptionMenus)

    def buildPopupMenu(self, menu, parent):
        if self.outputsChanged:
            pm.popupMenu(self.popupMenu, edit=True, deleteAllItems=True)
            pm.cmds.menuItem(parent=menu, label='Select AOV Node', c=lambda *args: pm.select(self.aov.node))
            pm.cmds.menuItem(parent=menu, label='Remove AOV', c=lambda *args: self.parent.removeAOV(self.aov))
            pm.cmds.menuItem(parent=menu, label='Add New Output Driver', c=lambda *args: self.addOutput())
            pm.cmds.menuItem(parent=menu, divider=True)
            if len(self.outputs) > 1:
                for i, outputRow in enumerate(self.outputs):
                    subMenu = pm.cmds.menuItem(parent=menu, label='Output Driver %d' % (i+1), subMenu=True)
                    pm.cmds.menuItem(parent=subMenu, label='Select Driver',
                                     c=pm.Callback(pm.select, outputRow.driverNode))
                    pm.cmds.menuItem(parent=subMenu, label='Select Filter',
                                     c=pm.Callback(pm.select, outputRow.filterNode))
                    pm.cmds.menuItem(parent=subMenu, divider=True)
                    pm.cmds.menuItem(parent=subMenu, label='Remove',
                                     c=pm.Callback(self.removeOutput, i))
            elif len(self.outputs) == 1:
                outputRow = self.outputs[0]
                pm.cmds.menuItem(parent=menu, label='Select Driver',
                                 c=pm.Callback(pm.select, outputRow.driverNode))
                pm.cmds.menuItem(parent=menu, label='Select Filter',
                                 c=pm.Callback(pm.select, outputRow.filterNode))
            self.outputsChanged = False
        return menu

class AOVOutputItem(object):
    '''
    Builds the UI for an output row belonging to an AOVItem
    '''
    def __init__(self, parent, outputAttr, aovItem):
        self.parent = parent
        self.aovItem = aovItem # required to set .outputsChanged
        self.outputAttr = outputAttr
        self.row = None
        self.driverMenu = None
        self.filterMenu = None
        self.driverNode = outputAttr.driver.inputs()[0]
        self.filterNode = outputAttr.filter.inputs()[0]
        self.buildOutputRow()

    def buildOutputRow(self):
        '''
        Add a new Driver and Filter row within the AOVItem row
        '''
        pm.setParent(self.parent)
        

        # DRIVER UI ----------
        self.row = pm.cmds.rowLayout(nc=2,
                     columnWidth2=OUTPUT_ROW_WIDTHS,
                     columnAttach2=['both', 'both'])

        self.driverMenu = pm.cmds.optionMenu(label='', w=50,
                                             changeCommand=lambda newDriver, at=self.outputAttr.driver: \
                                             self.driverMenuChanged(at, newDriver))

        defaultDriver = '<%s>' % pm.getAttr('defaultArnoldDriver.aiTranslator')
        pm.cmds.menuItem(label=defaultDriver)
        for tran in templates.getTranslators('aiAOVDriver'):
            pm.cmds.menuItem(label=tran)
        if self.driverNode.name() == 'defaultArnoldDriver':
            driver = defaultDriver
            isDefaultDriver=True
        else:
            driver = self.driverNode.attr('aiTranslator').get()
            isDefaultDriver=False
        try:
            pm.cmds.optionMenu(self.driverMenu, e=True, value=driver)
            #driverMenu.setValue(driver)
        except RuntimeError:
            pm.warning("[mtoa] %s: Unknown driver %r" % (self.driverNode, driver))
        else:
            if not isDefaultDriver:
                drivTransAttr = self.driverNode.attr('aiTranslator')
                self.driverJobId = pm.scriptJob(attributeChange=[drivTransAttr,
                                              lambda: self.translatorChanged(drivTransAttr, self.driverMenu)],
                             parent=self.driverMenu)
            # rebuild the menu when the default driver changes
            pm.scriptJob(attributeChange=['defaultArnoldDriver.aiTranslator',
                                          lambda: self.defaultTranslatorChanged('defaultArnoldDriver', self.driverMenu, 'aiAOVDriver')],
                                          parent=self.parent)
            
        # FILTER UI ----------
        self.filterMenu = pm.cmds.optionMenu(label='', w=60,
                                             changeCommand=lambda newFilter, at=self.outputAttr.filter: \
                                             self.filterMenuChanged(at, newFilter))
        
        defaultFilter = '<%s>' % pm.getAttr('defaultArnoldFilter.aiTranslator')
        pm.cmds.menuItem(label=defaultFilter)
        for tran in templates.getTranslators('aiAOVFilter'):
            pm.cmds.menuItem(label=tran)
        if self.filterNode.name() == 'defaultArnoldFilter':
            filter = defaultFilter
            isDefaultFilter=True
        else:
            filter = self.filterNode.attr('aiTranslator').get()
            isDefaultFilter=False
        try:
            pm.cmds.optionMenu(self.filterMenu, e=True, value=filter)
            #filterMenu.setValue(filter)
        except RuntimeError:
            pm.warning("[mtoa] %s: Unknown filter %r" % (self.filterNode, filter))
        else:
            if not isDefaultFilter:
                filtTransAttr = self.filterNode.attr('aiTranslator')
                self.filterJobId = pm.scriptJob(attributeChange=[filtTransAttr,
                                              lambda: self.translatorChanged(filtTransAttr, self.filterMenu, isDefaultFilter, 'aiAOVFilter')],
                             parent=self.filterMenu)
            # rebuild the menu when the default filter changes
            pm.scriptJob(attributeChange=['defaultArnoldFilter.aiTranslator',
                                          lambda: self.defaultTranslatorChanged('defaultArnoldFilter', self.filterMenu, 'aiAOVFilter')],
                                          parent=self.parent)

        callbacks.DelayedIdleCallbackQueue(self.fixOptionMenus)

    def delete(self):
        if self.driverNode.message.outputs() > 1:
            self.outputAttr.driver.disconnect()
        else:
            utils.safeDelete(self.driverNode)

        if self.filterNode.message.outputs() > 1:
            self.outputAttr.filter.disconnect()
        else:
            utils.safeDelete(self.filterNode)
        self.outputAttr.remove()
        pm.deleteUI(self.row)

    def translatorChanged(self, translatorAttr, menu):
        '''
        called when the aiTranslator attribute of a driver/filter node changes
        so that we can update the corresponding menu
        '''
        value = translatorAttr.get()
        pm.cmds.optionMenu(menu, e=True, value=value)

    def defaultTranslatorChanged(self, defaultNode, menu, outputType):
        '''
        rebuilds the menu, updating the value for the default driver/filter and
        restoring the selected item to the proper value
        '''
        # clear menu
        value = pm.optionMenu(menu, query=True, value=True)
        for item in pm.optionMenu(menu, query=True, itemListLong=True) or []:
            pm.deleteUI(item)
        default = '<%s>' % pm.getAttr(defaultNode + '.aiTranslator')
        pm.cmds.menuItem(parent=menu, label=default)
        for tran in templates.getTranslators(outputType):
            pm.cmds.menuItem(parent=menu, label=tran)
        callbacks.DelayedIdleCallbackQueue(self.fixOptionMenus)
        if value.startswith('<'):
            value = default
        pm.cmds.optionMenu(menu, e=True, value=value)

    def dummy(self, *args):
        pass

    def driverMenuChanged(self, aovOutputAttr, newValue):
        self.outputChangedCallback(aovOutputAttr, newValue, 'aiAOVDriver', 'defaultArnoldDriver')

    def filterMenuChanged(self, aovOutputAttr, newValue):
        self.outputChangedCallback(aovOutputAttr, newValue, 'aiAOVFilter', 'defaultArnoldFilter')

    def outputChangedCallback(self, aovOutputAttr, newValue, outputType, defaultNode):
        """
        change callback for both filter and driver menus
        
        outputType: either 'aiAOVDriver' or 'aiAOVFilter'
        """
        conn = aovOutputAttr.inputs()
        if newValue.startswith('<'):
            isDefault=True
            pm.connectAttr(defaultNode + '.message', aovOutputAttr, force=True)
            outputNode = pm.PyNode(defaultNode)
            pm.select(outputNode)
            if conn and not conn[0].outputs():
                utils.safeDelete(conn[0])
        else:
            isDefault=False
            if conn and conn[0].outputs():
                # other AOVs are dependent on existing filter/driver. create and connect a new one
                outputNode = pm.createNode(outputType)
                pm.connectAttr(outputNode.message, aovOutputAttr, force=True)
            else:
                outputNode = conn[0]
            newValue = newValue.strip('<>')
            outputNode.aiTranslator.set(newValue)

        if outputType == 'aiAOVFilter':
            self.filterNode = outputNode
            hooks.setupFilter(outputNode, self.aovItem.aovName())
            menu = self.filterMenu
        else:
            self.driverNode = outputNode
            hooks.setupDriver(outputNode, self.aovItem.aovName())
            menu = self.driverMenu

        transAttr = outputNode.attr('aiTranslator')
        if not isDefault:
            # change the selected menu item when the translator attribute changes for our driver/filter
            pm.scriptJob(attributeChange=[transAttr, lambda: self.translatorChanged(transAttr, menu)],
                         replacePrevious=True,
                         parent=menu)
        else:
            # delete pre-existing scriptJob
            pm.scriptJob(attributeChange=[transAttr, lambda: self.dummy()],
                         replacePrevious=True,
                         parent=menu)

        self.aovItem.outputsChanged = True

    def fixOptionMenus(self):
        pm.optionMenu(self.filterMenu, edit=True, visible=False)
        pm.optionMenu(self.filterMenu, edit=True, visible=True)

class ArnoldAOVEditor(object):

    def __init__(self, aovNode=None):
        self.waitingToRefresh = False
        self.aovControls = []
        self.optionMenus = []
        self.aovRows = {}
        self.renderOptions = aovs.AOVInterface() if aovNode is None else aovNode

        self.mainCol = pm.cmds.columnLayout('arnoldAOVMainColumn')

        # global drivers
        pm.cmds.frameLayout('arnoldDisplayDriverFrame', label='Default Drivers',
                            width=WIDTH, collapsable=True, collapse=True)
        pm.cmds.columnLayout(adj=True)
        for attr in self.renderOptions.node.drivers:
            driver = attr.inputs()
            if driver:
                pm.cmds.rowLayout(nc=2, columnAttach2=['both', 'right'], adjustableColumn=1, rowAttach=[2, 'top', 5])
                pm.cmds.columnLayout(adj=True)
                templates.createTranslatorMenu(driver[0], 
                                     label=utils.prettify(driver[0].name()),
                                     nodeType='aiAOVDriver')
                pm.cmds.setParent('..')
                pm.cmds.symbolButton(image="navButtonConnected.png",
                                      command=Callback(pm.select, driver))
        pm.cmds.setParent('..')

        pm.setParent(self.mainCol)

        pm.cmds.frameLayout('arnoldAOVBrowserFrame', label='AOV Browser', width=WIDTH,
                            collapsable=True, collapse=False, height=200)

        self.browser = AOVBrowser(self.renderOptions)
        pm.setParent(self.mainCol)

        pm.cmds.frameLayout('arnoldAOVPrimaryFrame', label='AOVs', width=WIDTH,
                            collapsable=True, collapse=False)
        self.aovCol = pm.cmds.columnLayout('arnoldAOVListColumn', adj=True)

        pm.cmds.rowLayout('arnoldAOVButtonRow', nc=3, columnWidth3=[140, 100, 100], columnAttach3=['right', 'both', 'both'])
        pm.cmds.text(label='')
        pm.cmds.button(label='Add Custom', c=lambda *args: shaderTemplate.newAOVPrompt())
        pm.cmds.button(label='Delete All', c=lambda *args: (self.renderOptions.removeAOVs(self.aovRows.keys()), \
                                                            hooks.setupDefaultAOVs(self.renderOptions)))
        pm.setParent('..') # rowLayout

        pm.cmds.separator(style='in')
        pm.rowLayout(nc=4,
                     columnWidth4=[130, 66, 80, 40],
                     columnAttach4=['both', 'both', 'both', 'both'])
        pm.cmds.text(label='name')
        pm.cmds.text(label='data')
        pm.cmds.text(label='driver')
        pm.cmds.text(label='filter')

        pm.cmds.setParent('..') # rowLayout
        
        pm.cmds.separator(style='in')

    #    pm.text(_uiName('prefixLbl'), align='center', label='Prefix', parent=form)
    #    pm.textField(_uiName('prefixFld'), enable=False, text='', parent=form, changeCommand=Callback(setAOVPrefix, aovnode))

        self.browser.populate()

        # add all control rows
        self.addRows()

        aovs.addAOVChangedCallback(self.refresh, 'aoveditor')
        
        # update AOV imageFormat of all rows when the default imageFormat changes.  a scriptJob will suffice here 
        pm.scriptJob(parent=self.aovCol,
                     attributeChange=[self.renderOptions.node.imageFormat.name(),
                                      lambda *args: pm.evalDeferred(self.refresh)])

    def removeAOVCallbacks(self, *args):
        for attr in AOV_CALLBACK_ATTRS:
            try:
                callbacks.removeAttributeChangedCallbacks('aiAOV', attr)
            except KeyError:
                print "AOV callback no longer exists", attr

    def addRows(self):
        for aovName, aovList in self.renderOptions.getAOVs(group=True):
            frame = pm.frameLayout(collapsable=False, labelVisible=False)
            col = pm.columnLayout(adj=True)
            rows = []
            for aov in aovList:
                row = AOVItem(self, aov)
                rows.append(row)
                self.optionMenus.extend(row.getMenus())
            self.aovRows[aov.name] = rows
            self.aovControls.append(frame)
            pm.setParent('..')
            pm.setParent('..')

    def refresh(self):
        '''
        Delete and rebuild the AOV control rows
        '''
        self.waitingToRefresh = False
        pm.setParent(self.aovCol)
        pm.cmds.columnLayout(self.aovCol, edit=True, visible=False)
        numDeleted = len(self.optionMenus)
        for ctrl in self.aovControls:
            ctrl.delete()
        self.aovControls = []
        self.optionMenus = []
        self.aovRows = {}

        # add all control rows
        if self.renderOptions.node.exists():
            self.addRows()

        self.browser.updateActiveAOVs()

        pm.cmds.columnLayout(self.aovCol, edit=True, visible=True)

        # a maya bug causes menus to ignore their specified width
        #print "refresh", numDeleted, len(self.optionMenus)
        if numDeleted != len(self.optionMenus):
            #print "creating script job"
            callbacks.DelayedIdleCallbackQueue(self.fixOptionMenus)
            #pm.scriptJob(runOnce=True, idleEvent=self.fixOptionMenus)
            #pm.evalDeferred(self.fixOptionMenus)

    def removeAOV(self, aov):
        self.renderOptions.removeAOV(aov)

    def setEnabledState(self):
        mode = self.renderOptions.node.attr('aovMode').get()
        state = mode > 0
        pm.cmds.columnLayout(self.mainCol, edit=True, enable=state)


    def fixOptionMenus(self):
        '''
        Callback to fix an annoying bug where option menus do not respect their set width.
        ''' 
        # The only thing I've found that will make the option menu's return to their proper width
        # is hiding and then unhiding them.  However, this must be delayed until after the window they're in
        # is shown. Even an idle event scriptJob (set to run-once) is not 100% successful as sometimes it
        # is trigger too soon.  This technique relies on an idle callback where we skip the first coule fires
        # before calling fixOptionMenus() callback and removing the idle callback. -CHAD
        #print self.idle_id, self.idle_ticker
        for menu in self.optionMenus:
            #print "fixing", menu
            pm.optionMenu(menu, edit=True, visible=False)
            pm.optionMenu(menu, edit=True, visible=True)


        
def arnoldAOVEditor(*args):
    if pm.window(UI_NAME, exists=True):
        pm.deleteUI(UI_NAME)
    win = pm.window(UI_NAME, title='AOV setup', width=640, height=300)
    import time
    s = time.time()
    ed = ArnoldAOVEditor()
    print time.time() - s
    win.show()
    pm.evalDeferred(ed.fixOptionMenus)
    return ed

def arnoldAOVBrowser(**kwargs):
    core.createOptions()
    win = pm.window(title='AOV Browser', width=640, height=300)
    browser = AOVBrowser(**kwargs)
    browser.populate()
    win.show()
    return browser


_aovDisplayCtrl= None

def createArnoldAOVTab():
    parentForm = cmds.setParent(query=True)

    aovNode = aovs.AOVInterface()
    pm.columnLayout('enableAOVs', adjustableColumn=True)
    
    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)

    pm.attrControlGrp(attribute=aovNode.node.aovMode, label='Mode')

    # the tab gets recreated from scratch each time rather than updated and each
    # time the AOVOptionMenuGrp adds itself to the AOVChanged callback list. 
    # we must remove it or we'll leave behind invalid copies
    global _aovDisplayCtrl
    if _aovDisplayCtrl is not None:
        aovs.removeAOVChangedCallback(_aovDisplayCtrl.update)

    _aovDisplayCtrl = shaderTemplate.AOVOptionMenuGrp('aiOptions', 'displayAOV', label='Render View AOV',
                                           allowCreation=False,
                                           includeBeauty=True,
                                           allowEmpty=False,
                                           allowDisable=False)
    _aovDisplayCtrl._setToChildMode()
    _aovDisplayCtrl._doSetup(aovNode.node.name() + '.displayAOV')
    
    pm.setParent(parentForm)

    cmds.scrollLayout('arnoldAOVsScrollLayout', horizontalScrollBarThickness=0)

    cmds.columnLayout('arnoldTabColumn', adjustableColumn=True)

    ed = ArnoldAOVEditor(aovNode)

    cmds.formLayout(parentForm,
               edit=True,
                    af=[('enableAOVs',"top", 5),
                        ('enableAOVs', "left", 0),
                        ('enableAOVs', "right", 0),
                        ('arnoldAOVsScrollLayout', "bottom", 0),
                        ('arnoldAOVsScrollLayout', "left", 0),
                        ('arnoldAOVsScrollLayout', "right", 0)],
                    an=[('enableAOVs', "bottom")],
                    ac=[('arnoldAOVsScrollLayout', "top", 5, 'enableAOVs')])

    pm.setUITemplate('attributeEditorTemplate', popTemplate=True)

    cmds.setParent(parentForm)
    pm.evalDeferred(ed.fixOptionMenus)
    ed.setEnabledState()
    pm.scriptJob(attributeChange = (aovNode.node.aovMode, ed.setEnabledState), parent=ed.mainCol)

    #cmds.setUITemplate(popTemplate=True)

def updateArnoldAOVTab():
    pass
