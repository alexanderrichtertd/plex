'''
########################################################################
#             prSelectionUi.py                                         #
#             Copyright (C) 2012  Parzival Roethlein                   #
#             Email: pa.roethlein@gmail.com                            #
#                                                                      #
# This program is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
# This program is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         #
# GNU General Public License for more details.                         #
# See http://www.gnu.org/licenses/gpl.html for a copy of the GNU       #
# General Public License.                                              #
########################################################################

D E S C R I P T I O N:
This is an open source Maya script written in Python (PyMEL).
It is a dynamic and flexible UserInterface (UI) to manage selections and poses,
which can be useful during animation.

L I N K S:
- Demo video with link to latest version
http://vimeo.com/37670989
- Background information on my blog
http://pazrot3d.blogspot.com/2012/03/prselectionui.html
- This was written in my spare time. If you found it useful for animation or coding, consider supporting the author:
https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=7X4EJ8Z7NUSQW

F E A T U R E S:
- User can create and edit sets/selections/poses/members at any time
- All information is stored in the scene (works when referenced)
- Export/Import sets between shots/scenes
- There are a few pop-up menus (RMC=Right-mouse-click, MMC=Middle-mouse-click):
-- RMC on set-menu (top row): Create/Edit Sets and adjust UI (dockable, hide bar)
-- RMC on empty set-area: Create Selection/Pose
--- RMC on Selection/Pose: Create/Edit Selection/Pose/Members
---- MMC on Selection/Pose for extra commands (keyframe, reset, ..)

U S A G E:
Put the file prSelectionUi.py in your Maya scripts folder and execute:
- Python:
import prSelectionUi
reload(prSelectionUi)
prSelectionUi.UI()
- MEL (for marking menu, ...):
python("import prSelectionUi");
python("reload(prSelectionUi)");
python("prSelectionUi.UI()");

V E R S I O N S:
2012-12-25 / 0.9.8: Pose % items added to Pose middle mouse click menu // Autofocus on panel (tool shortcuts keep working) 
2012-12-15 / 0.9.7: added option "UI: toggle tablayout" to switch display between tablayout and drop down menu
2012-12-12 / 0.9.6: bugfix (maya crashed for some users) // does not work with older sets
2012-12-11 / 0.9.5: loads faster, no crashes // changed mouse-click menus // new members UI // tabs are now called sets and in optionMenu
2012-04-20 / 0.9.3: pose support added // tweaks (button ordering,..) // can't read sets from old version
2012-04-15 / 0.9.2: tweaks (no popup when changing member status, show/hide shape visible in button,..)
2012-04-13 / 0.9.1: removed limitations // new features // can't read sets from old version
2012-03-01 / 0.9.0: first version

T O D O:
- member window close scriptJob for warning when there are unsaved changes
- search and replace for members (give user string output, input field, they can edit in editor of their choice)
- (maybe) popup when leftclicking empty set-optionMenu
- (maybe) shift/ctrl+mouse click on selection center button with maya viewport functionality
- (maybe) save set to shelf
- (fix?) when adding nucleus to selection: api error...
- (code) store pose nodes in dictionary with attr and values for faster 'pose selected nodes' cmd

F E E D B A C K:
Bugs, questions and suggestions to pa.roethlein@gmail.com

T E S T:
# #########################
import sys
sys.path.append(r'E:\eclipseworkspace\prScripts\animation')
#sys.path.append( r'C:\Users\prothlein\Documents\eclipseworkspace\svn\prRS\animation' )
import prSelectionUi
reload( prSelectionUi )
prSelectionUi.UI()
# #########################
'''

import pymel.core as pm
import maya.mel as mm

class UI(pm.uitypes.Window):
    '''
    window of prSelectionUi.
    Maya-UI-Hierarchy:
    (UI:)      window > formLayout > horizontalLayout > optionMenu, tabLayout
    (Set:)     verticalLayout >
    (Element:) horizontalLayout > buttons (+,select,- OR pose)
    '''
    # constants
    _TITLE = 'prSelectionUi_098'# dots or space will break pm.window(cls._TITLE)
    _FORMLAYOUT = 'prSelForm'
    _TABLAYOUT = 'prSelTab'
    _DOCKCONTROL = 'prSelectionUiDoc'
    # variables
    sets = None
    setsOptionMenu = None
    setsTabLayout = None
    cbConfirmDialogs = None
    dockControl = None
    
    def __new__(cls):
        ''' delete possible old window and create new instance '''
        if pm.window(cls._TITLE, exists=True):
            pm.deleteUI( cls._TITLE )
        if( pm.dockControl( cls._DOCKCONTROL, ex=1 )):
            pm.deleteUI( cls._DOCKCONTROL, control=1 )
        self = pm.window(cls._TITLE, title=cls._TITLE)
        return pm.uitypes.Window.__new__(cls, self)
    
    def __init__(self):
        '''
        create UI elements (layouts, buttons)
        show window
        try to load from scene, else create default
        '''
        # initialize variables
        self.sets = []
        
        # formLayout base
        form = pm.formLayout( self._FORMLAYOUT )
        with form:
            # optionMenu
            self.setsOptionMenu = pm.optionMenu( cc=pm.Callback( self.setsMenu_cmd ))
            pm.popupMenu( parent=form, button=3 )
            pm.menuItem( 'Create Set', c=pm.Callback( self.set_new ) )
            pm.menuItem( 'Delete Set', c=pm.Callback( self.set_deleteActive ) )
            pm.menuItem( divider=1 )
            pm.menuItem( 'Edit Set Name', c=pm.Callback( self.set_editName ) )
            pm.menuItem( 'Edit Set Index', c=pm.Callback( self.set_editIndex ) )
            pm.menuItem( divider=1 )
            pm.menuItem( 'Reload Sets', c=pm.Callback( self.set_load ) )
            pm.menuItem( divider=1 )
            pm.menuItem( l='UI: Toggle title bar', c=pm.Callback( self.ui_toggleTitleBar ) )
            pm.menuItem( l='UI: Make dockable', c=pm.Callback( self.ui_makeDockable ) )
            pm.menuItem( l='UI: Toggle tablayout', c=pm.Callback( self.ui_toggleTablayout ) )
            self.cbConfirmDialogs = pm.menuItem( l='UI: Confirm dialogs', cb=1 )
            self.cbFocusPanel = pm.menuItem( l='UI: Autofocus panel', cb=1 )
            # tabLayout
            self.setsTabLayout = pm.tabLayout( self._TABLAYOUT, tabsVisible=0 )
        #form.redistribute(0,1)
        # no redistribute, because optionMenu width will resize to minimum when editing members and only refresh when UI gets modified again
        form.attachForm( self.setsOptionMenu, 'top', 0)# unnecessary? 
        form.attachForm( self.setsOptionMenu, 'left', 0)
        form.attachControl( self.setsTabLayout, 'top', 0, self.setsOptionMenu )
        form.attachForm( self.setsTabLayout, 'left', 0)
        form.attachForm( self.setsTabLayout, 'right', 0)
        form.attachForm( self.setsTabLayout, 'bottom', 0)
        
        # miConfirm.setCommand(..)# maya 2012+ only (pymel version ...?)
        
        # load tabs from scene
        self.set_load( 1 )
        # show window
        self.show()
    
    def createWarning( self, msg ):
        ''' create a warning for the user '''
        import maya.mel as mm
        mm.eval( 'warning "%s"' % msg )
    
    def setsMenu_cmd(self):
        ''' command to execute when set optionMenu items get selected '''
        count = self.setsOptionMenu.getNumberOfItems()
        selected = self.setsOptionMenu.getSelect()
        self.setsTabLayout.setSelectTabIndex( selected )
        self.setsMenu_updateSelected()
    
    def setsMenu_updateSelected(self):
        ''' select proper menuItem '''
        selectIndex = self.setsTabLayout.getSelectTabIndex()
        if( selectIndex == 0 ):
            return
        self.setsOptionMenu.setSelect( selectIndex )
    
    def tryConfirmDialog(self, msg, forced=False):
        ''' create confirm dialog if option is enabled '''
        # get confirmDialog checkBox value
        confirmDialogsValue = pm.menuItem( self.cbConfirmDialogs, q=1, checkBox=1 )
        # create pop-up if required
        if( confirmDialogsValue or forced ):
            result = pm.confirmDialog( title='Confirm ', message=msg, button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            if( result == 'Yes' ):
                return True
            else:
                return False
        else:
            return True
    
    def tryFocusPanel(self):
        ''' set focus on panel under cursor, if the option is enabled. So shortcuts for move-tool,... still work '''
        focusPanelValue = pm.menuItem( self.cbFocusPanel, q=1, checkBox=1 )
        if( focusPanelValue ):
            # The next line makes little sense, but is required for shortcuts to work in the panel below 
            pm.setFocus( self )
            # set focus on panel under prSelectionUi
            pm.setFocus( pm.getPanel( up=1 ) )
    
    def ui_toggleTitleBar(self):
        ''' toggle the UI title bar on/off, to reduce size of UI '''
        # error catching
        if( self.dockControl ):
            mm.eval( 'warning "Can\'t remove title bar of a window that is dockable."' )
            return
        # save height and width, else it changes to default
        height = self.getHeight()
        width = self.getWidth()
        # toggle title bar
        if( self.getTitleBar() ):
            self.setTitleBar(0)
        else:
            self.setTitleBar(1)
        # set height/width
        self.setHeight( height )
        self.setWidth( width )
    
    def ui_toggleTablayout(self):
        ''' toggle tablayout visibility / optionMenu visibility '''
        if( self.setsTabLayout.getTabsVisible() ):
            self.setsTabLayout.setTabsVisible(0)
            # select proper optionMenu item
            self.setsOptionMenu.setManage( 1 )
            self.setsOptionMenu.setSelect( self.setsTabLayout.getSelectTabIndex() )
            
        else:
            self.setsTabLayout.setTabsVisible(1)
            self.setsOptionMenu.setManage( 0 )
    
    def ui_makeDockable(self ):
        ''' make the window dockable '''
        # skip if already dockable
        if( self.dockControl ):
            mm.eval( 'warning "The window is dockable already."' )
            return
        # warning for user
        if(not self.tryConfirmDialog( 'Make UI dockable?\n', 1 )):
            return
        # create dockControl
        self.dockControl = pm.dockControl( self._DOCKCONTROL, l=self, content=self, area='left', allowedArea=['left', 'right'] )
    
    # #########################
    # SETS
    # #########################
    
    def set_load(self, forced=0):
        ''' load tabs (sets) from scene '''
        # warning
        if( not forced ):
            if( not self.tryConfirmDialog( 'Load tabs from sets/scene?' ) ):
                return
        
        # delete old UI elements
        for x in range( len(self.sets) ):
            self.sets[0].delete(1,1)
        if( self.sets != [] ):
            raise NameError( 'self.sets should be empty error' )
        
        # create UI
        tabSets = Set.findSets()
        if( tabSets ):
            # loading feedback for user
            print '\n######   start loading sets    ######'
            # load
            for x, eachSet in enumerate( tabSets ):
                self.set_new( eachSet )
            # loading feedback for user
            print '######  finished loading sets  ######\n'
    
    def set_sort(self):
        ''' order tabs by index and name '''
        # create index dictionary with tab-dictionary
        dic = {}
        for each in self.sets:
            if( dic.has_key(each.tabIndex) ):
                dic[each.tabIndex][each.referencePrefix+each.tabName+each.shortName()] = each
            else:
                dic[each.tabIndex] = {each.referencePrefix+each.tabName+each.shortName(): each}
        ordered = []
        for eachIndexKey in sorted( dic.iterkeys() ):
            for eachTabKey in sorted( dic[eachIndexKey].iterkeys() ):
                ordered.append( dic[eachIndexKey][eachTabKey] )
        self.sets = ordered
    
    def set_getActive( self, noReferenceMessage=None ):
        ''' return the currently active tab, optional error if active tab is reference '''
        # error check
        if( not self.sets ):
            self.setsMenu_updateSelected()
            raise NameError( '\n\n\n ------- \nYou have to create a set first (right click on drop down menu at top)' )
        # return selected tab
        selectedLayout = self.setsTabLayout.getSelectTab()
        for each in self.sets:
            if( each.shortName() == selectedLayout ):
                # found active tab
                if( noReferenceMessage and each.referencePrefix ):
                    import maya.mel as mm
                    raise NameError( noReferenceMessage )
                return each
    
    def set_new(self, fromSet=None):
        ''' create new tab, either with user input, or from given set '''
        # get tab name
        tabName = Set.getName( fromSet )
        if( not tabName ):
            return
        with self.setsTabLayout:
            # create tab: instance / UI element
            newSet = Set( tabName, self, fromSet )
    
    def set_deleteActive(self):
        ''' delete active tab '''
        self.set_getActive( 'Can\'t delete referenced tab!' ).delete()
    
    def set_editName(self):
        ''' rename the currently active tab '''
        self.set_getActive( 'Can\'t rename referenced tab!' ).rename()
    
    def set_editIndex(self):
        ''' change index/position of active tab '''
        self.set_getActive().changeIndex()
    
    def set_newElement(self, elementType):
        ''' create element of given type '''
        self.set_getActive( 'Can\'t add %s to referenced tab!'%elementType ).element_create( elementType )
    
    def set_toShelf(self):
        ''' save set to, so pressing shelf will create set '''
        print 'save to shelf'

class Set(pm.uitypes.FormLayout):# scroll layout?
    ''' class for each tab in the UI window '''
    # constants
    _SET_PREFIX = 'set_tab_'
    _ATTR_TABNAME = 'prSel_TabName'
    _ATTR_SELECTION = 'prSel_TabSelection'
    _ATTR_INDEX = 'prSel_TabIndex'
    # variables
    asMenuItem = None
    parentUi = None
    referencePrefix = None
    elements = None
    #     maya nodes / attributes
    set = None
    tabName = None
    tabIndex = None
    
    @staticmethod
    def getName( fromSet=None ):
        '''
        get name from given set or user input
        extra function because it should be known before instance is created
        '''
        if( fromSet ):
            # get tab name from set
            tabName = fromSet.attr( Set._ATTR_TABNAME ).get()
            Set.checkName( tabName )
        else:
            # get tab name from user
            result = pm.promptDialog(title='New Set', message='Name for new Set:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
            if( result != 'OK' ):
                return None
            tabName = str( pm.promptDialog(q=1, text=1) )
            Set.checkName( tabName )
        return tabName
    
    @staticmethod
    def checkName(name):
        ''' check if given name is valid for a tab '''
        if( name == '' ):
            raise NameError( 'Invalid name: "" (nothing)' )
    
    @staticmethod
    def findSets():
        ''' return all tab sets from scene '''
        sceneSets = []
        # find sets
        for eachSet in ( pm.ls( type='objectSet' ) ):
            if( eachSet.hasAttr( Set._ATTR_TABNAME ) ):
                sceneSets.append( eachSet )
        # return
        return sceneSets
    
    def __new__(cls, name, parentUi, fromSet=None ):
        ''' get name from user or read from set. then create instance '''
        self = pm.formLayout( nd=100 )
        return pm.uitypes.FormLayout.__new__(cls, self)
    
    def __init__(self, name, parentUi, fromSet=None ):
        ''' initialize variables '''
        if( fromSet ):
            print ('- set: %s // %s' % (name, fromSet) )
        # parent init for _reverse,... variables
        super( Set, self ).__init__()
        
        # variables
        self.tabName = name
        self.parentUi = parentUi
        
        # right click menu to create the first selection/pose
        pm.popupMenu( button=3 )
        pm.menuItem( label='New selection', c=pm.Callback( self.parentUi.set_newElement, Selection._TYPE ) )
        pm.menuItem( label='New pose', c=pm.Callback( self.parentUi.set_newElement, Pose._TYPE ) )
        
        # get/create set
        if( fromSet ):
            self.set = fromSet
        else:
            self.createSet()
        
        # read values from set
        self.tabIndex = self.set.attr( Set._ATTR_INDEX ).get()
        if( self.set.referenceFile() ):
            self.referencePrefix = self.set.referenceFile().fullNamespace+':'
        else:
            self.referencePrefix = ''
        #     elements
        self.elements = []
        for each in self.set.dnSetMembers.inputs():#pm.sets( self.set, q=1 ):# for propper order
            if( each.hasAttr( Selection._ATTR_TYPE ) ):
                self.element_create( Selection._TYPE, each )
            elif( each.hasAttr( Pose._ATTR_TYPE ) ):
                self.element_create( Pose._TYPE, each )
        
        # store in parentUi
        self.parentUi.sets.append( self )
        # set name in UI
        self.parentUi.setsTabLayout.setTabLabel( [self, self.getUiName()] )
        # select new tab
        self.parentUi.setsTabLayout.setSelectTab( self.shortName() )
        # position tab
        self.setPosition()
    
    def delete( self, forced=0, uiOnly=0 ):
        ''' delete tab UI element and set '''
        # skip reference tabs
        if( self.referencePrefix and not uiOnly ):
            return
        
        # pop-up
        if( not forced ):
            if( not self.parentUi.tryConfirmDialog( 'Delete tab: "%s" ?' % self.getUiName() ) ):
                return
        
        # parent delete
        super(Set, self).delete()
        # delete in parent
        self.parentUi.sets.remove( self )
        # delete set
        if( not uiOnly ):
            pm.delete( self.set )
        # delete menuItem
        pm.deleteUI( self.asMenuItem )
        self.parentUi.setsMenu_updateSelected()
    
    def setPosition(self):
        ''' calculate and set position of given set (by index and alphabet) '''
        # order self.sets variable
        self.parentUi.set_sort()
        # get index
        tabPosition = self.parentUi.sets.index( self )
        # adjust UI
        self.parentUi.setsTabLayout.moveTab( [self.parentUi.setsTabLayout.getSelectTabIndex(), tabPosition+1] )
        # select with new position
        self.parentUi.setsTabLayout.setSelectTab( self.shortName() )
        # delete possible old menuItem
        if( self.asMenuItem ):
            pm.deleteUI( self.asMenuItem )
        # create menuItem
        #with self.parentUi.setsOptionMenu:# parent flag because of maya 2012
        insertAfterIndex = self.parentUi.setsTabLayout.getSelectTabIndex()-1
        allMenuItems = pm.optionMenu(self.parentUi.setsOptionMenu, q=1, itemListLong=1)
        if( insertAfterIndex == 0 ):
            insertAfter = ''
        else:
            insertAfter = allMenuItems[ insertAfterIndex-1 ]# .getItemListLong() # maya(pymel) 2012+ 
        # shorten long reference-names/namespaces
        uiName = self.getUiName()
        if( uiName.find( ':' ) != -1 ):
            shortName = uiName[uiName.rfind(':')+1:]
            if( len(uiName) - len(shortName) > 20 ):
                uiIndex = uiName[:uiName.find(' ')+1]
                uiName = uiName[uiName.find(' ')+1:]
                splitList = uiName.split( ':' )[:-1]
                splitList.reverse()
                for eachPart in splitList:
                    if( len(eachPart) > 10 ):
                        eachPart = eachPart[:10]+'..'
                    shortName = eachPart+':'+shortName
                uiName = uiIndex+shortName
        
        # menuItem
        #if( len( self.parentUi.setsOptionMenu.getItemListLong() ) == 0 ):# only maya(pymel) 2012+
        if( not insertAfter ):
            if( allMenuItems ):
                self.asMenuItem = pm.menuItem( uiName, label=uiName, p=self.parentUi.setsOptionMenu, ia="" )
            else:
                self.asMenuItem = pm.menuItem( uiName, label=uiName, p=self.parentUi.setsOptionMenu )
        else:
            '''
            # changed from following line, because of maya 2011 bug/crash when using -ia flag (flag works for simple case thou?!)
            #self.asMenuItem = pm.menuItem( uiName, label=uiName, p=self.parentUi.setsOptionMenu, ia=insertAfter )
            '''
            # rebuild menuItems
            #     create new label list
            allLabels = []
            for eachItem in allMenuItems:
                allLabels.append( pm.menuItem( eachItem, q=1, label=1 ) )
            allLabels.insert(insertAfterIndex, uiName)
            #     delete old menuItems
            for eachItem in allMenuItems:
                pm.deleteUI( eachItem )
            #     create menuItems
            for x, each in enumerate(allLabels):
                eachItem = pm.menuItem( each, label=each, p=self.parentUi.setsOptionMenu )
                if( x == insertAfterIndex ):
                    self.asMenuItem = eachItem
        
        # update selection
        self.parentUi.setsMenu_updateSelected()
    
    def changeIndex( self ):
        ''' change index '''
        # create message to show user list of all tabs with indices
        strMessage = ('Change index of tab "%s"\n') % ( self.getUiName() )
        for eachSet in self.parentUi.sets:
            strMessage += '\n'+eachSet.getUiName()
            if( eachSet == self ):
                strMessage += '   <-----   (active)'
        # get input from user
        result = pm.promptDialog( title='Move tab', message=strMessage, tx=self.tabIndex,
                                  button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
        if( result != 'OK' ):
            return
        # get value
        newIndex = int( pm.promptDialog(q=1, text=1) )
        # change index
        self.tabIndex = newIndex
        self.set.attr( self._ATTR_INDEX ).set( newIndex )
        # set UI position
        self.setPosition()
        # set name
        self.parentUi.setsTabLayout.setTabLabel( [self, self.getUiName()] )
    
    def createSet(self):
        ''' create set of this tab '''
        # create set
        newSet = pm.sets( empty=1, name=self._SET_PREFIX+self.tabName )
        
        # add attributes
        newSet.setAttr( self._ATTR_TABNAME, self.tabName, force=1 )
        newSet.setAttr( self._ATTR_INDEX, 1, force=1 )
        
        # store set
        self.set = newSet
    
    def getUiName(self):
        ''' return name for UI display (tab name) '''
        return ( str(self.tabIndex)+' '+self.referencePrefix+self.tabName )
    
    def rename(self):
        ''' rename this tab (overwrote default rename()) '''
        # get name from user
        result = pm.promptDialog(title='Rename tab', 
                                 message='Rename tab: "%s" '%self.getUiName(), 
                                 tx=self.tabName,
                                 button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
        if( result == 'OK' ):
            text = pm.promptDialog(q=1, text=1)
            self.checkName( text )
            self.tabName = text
            self.set.attr( self._ATTR_TABNAME ).set( text )
            self.set.rename( self._SET_PREFIX+text )
            # adjust UI
            #     rename UI
            self.parentUi.setsTabLayout.setTabLabel( [self, self.getUiName()] )
            #     set UI position
            self.setPosition()
    
    # #########################
    # ELEMENT
    # #########################
    
    def element_orderUi(self):
        ''' set position (order) of elements in tab '''
        if( len( self.elements ) == 0 ):
            return
        # order elements from set children order
        oldSetOrder = []
        for each in self.elements:
            oldSetOrder.append( each.set )
        newSetOrder = self.set.dnSetMembers.inputs() #pm.sets( self.set, q=1 ) not correct order# self.set.members() / asSelectionSet # MPlug error..
        newElementList = []
        for x, each in enumerate( newSetOrder ):
            newElementList.append( self.elements[oldSetOrder.index(each)] )
        self.elements = newElementList
        #
        self.element_uiDistribute()
    
    def element_uiDistribute(self):
        ''' attach each elements top/bottom '''
        if( not self.elements ):
            return
        positionUnit = 100.0/len(self.elements)
        for x, each in enumerate( self.elements ):
            pm.formLayout( self, e=1, ap=[(each, 'top', 0, x*positionUnit), (each, 'bottom', 0, (x+1)*positionUnit)])
    
    def element_orderUiDeferred(self):
        '''  order tab-elements deferred to avoid crash when called from element popUpMenu '''
        import maya.utils as mu
        mu.executeDeferred( self.element_orderUi )
    
    def element_create(self, elementType, fromSet=0):
        ''' create element of given type "pose" or "selection" '''
        # get name
        elementName = SetElement.getName( elementType, fromSet )
        if( not elementName ):
            return
        # create element
        with self:
            if( elementType == Selection._TYPE ):
                Selection( elementName, self, fromSet )
            elif( elementType == Pose._TYPE ):
                Pose( elementName, self, fromSet )

class SetElement(pm.uitypes.FormLayout):
    ''' base class for tab elements: selections and poses '''
    # constants
    _DEFAULTCOLOR = [0.4,0.4,0.4]
    _ATTR_NAME = 'prSel_name'
    _ATTR_COLOR = 'prSel_color'
    #     has to be overwritten
    _SET_PREFIX = None # 'set_sel_' / 'set_pose_'
    _ATTR_TYPE = None # 'prSel_selection' / 'prSel_pose'
    _TYPE = None # 'selection' / 'pose'
    # variables
    parentUi = None
    referencePrefix = None
    set = None
    name = None
    color = None
    rightClickMenu = None
    middleClickMenu = None
    horizontal = None
    #     has to be set in child class
    button = None
    
    @staticmethod
    def checkName(name):
        ''' check if the given name string is a valid '''
        if( name == '' ):
            raise NameError( 'Invalid name: "" (nothing)' )
    
    @staticmethod
    def getName( elementType, fromSet=None ):
        ''' get name from user or given set '''
        # from set
        if( fromSet ):
            return fromSet.attr( SetElement._ATTR_NAME ).get()
        # get name from user
        result = pm.promptDialog( title=('New %s'%elementType), message=('Name for new %s:'%elementType), button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
        if( result == 'OK' ):
            text = pm.promptDialog(q=1, text=1)
            SetElement.checkName( text )
            return text
        else:
            return None
    
    def __new__(cls, name, parentUi, fromSet=None):
        ''' create new instance '''
        self = pm.formLayout()
        return pm.uitypes.FormLayout.__new__(cls, self)
    
    def __init__(self, name, parentUi, fromSet=None ):
        ''' initialize variables '''
        if( fromSet ):
            print ('-- element: %s (%s)' % (name, self._TYPE))
        
        # parent init for _reverse,... variables
        super( SetElement, self ).__init__()
        
        # variables
        self.name = name
        self.parentUi = parentUi
        
        # assign/create set
        if( fromSet ):
            self.set = fromSet
        else:
            # create set
            self.set = pm.sets( empty=1, name=self._SET_PREFIX+self.name )
            # attach to tab set
            pm.sets( self.parentUi.set, e=1, add=self.set )
            # add attributes with default values
            self.set.addAttr( self._ATTR_NAME, dt='string' ) # self.set.setAttr( self._ATTR_NAME, self.name, force=1 ) # problem with some signs (umlaute),..
            self.set.attr( self._ATTR_NAME ).set( self.name )
            self.set.addAttr( self._ATTR_COLOR, dt='float3' )
            self.set.attr( self._ATTR_COLOR ).set( self._DEFAULTCOLOR )
            self.set.addAttr( self._ATTR_TYPE, at='bool', dv=1 )
        
        # read set variables
        self.color = self.set.attr( self._ATTR_COLOR ).get()
        if( self.set.referenceFile() ):
            self.referencePrefix = self.set.referenceFile().fullNamespace+':'
        else:
            self.referencePrefix = ''
        
        # set color
        self.setColor()
        
        # attach left and right side to parent layout
        pm.formLayout( self.parentUi, e=1, attachForm=[(self, 'left', 0), (self, 'right', 0)] )
        
        # right click menu
        if self.referencePrefix:
            dynamicSel = 0
        else:
            dynamicSel = 1
        with self:
            self.rightClickMenu = pm.popupMenu( button=3 )
            pm.menuItem( l='New %s'%Selection._TYPE, c=pm.Callback( self.parentUi.element_create, Selection._TYPE ), en=dynamicSel )
            pm.menuItem( l='New %s'%Pose._TYPE, c=pm.Callback( self.parentUi.element_create, Pose._TYPE ), en=dynamicSel )
            pm.menuItem( l='Delete %s'%self._TYPE, c=pm.Callback( self.delete ), en=dynamicSel )
            pm.menuItem( divider=1 )
            pm.menuItem( l='Edit Name', c=pm.Callback( self.cmd_rename ), en=dynamicSel )
            pm.menuItem( l='Edit Position', c=pm.Callback( self.cmd_changePosition ) )
            pm.menuItem( l='Edit Color', c=pm.Callback( self.cmd_changeColor ) )
        
        # middle click menu
        with self:
            self.middleClickMenu = pm.popupMenu( button=2 )
        
        # store in tab
        self.parentUi.elements.append( self )
        # order UI
        self.parentUi.element_uiDistribute()
    
    def delete(self):
        ''' delete UI elements, sets, instance '''
        # warning
        if( not self.parentUi.parentUi.tryConfirmDialog( 'Delete %s: "%s" ?'%(self._TYPE, self.getUiName()) ) ):
            return
        # remove from tab selection list
        self.parentUi.elements.remove( self )
        # delete set (remove member first, else parent set will get deleted if last member gets deleted)
        pm.sets( self.parentUi.set, remove=self.set )
        pm.delete( self.set )
        # reconnect sets, to keep steady input attribute counting
        allSets = self.parentUi.set.dnSetMembers.inputs()
        self.parentUi.set.dnSetMembers.disconnect()
        for each in allSets:
            pm.sets( self.parentUi.set, add=each )
        # delete from UI
        import maya.utils as mu
        mu.executeDeferred( self.deleteUi )
    
    def deleteUi(self):
        ''' delete from UI '''
        pm.deleteUI( self )
        # reorder selections
        self.parentUi.element_uiDistribute()
    
    def setColor(self):
        ''' set color of selection and store in attr '''
        # attr
        self.set.attr( self._ATTR_COLOR ).set( self.color )
        # UI
        pm.formLayout( self, e=1, bgc=self.color )
    
    def getUiName(self):
        ''' return name for UI display (tab name) '''
        return self.name
    
    def cmd_rename(self):
        ''' rename variable, button label and set '''
        # get name from user
        result = pm.promptDialog(title=('Rename %s'%self._TYPE), message='Rename %s: "%s"'%(self._TYPE, self.name), text=self.name, button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
        if( result == 'OK' ):
            text = pm.promptDialog(q=1, text=1)
            self.checkName( text )
            # store
            self.name = text
            # update button label
            self.button.setLabel( self.getUiName() )
            # rename set
            self.set.attr( self._ATTR_NAME ).set( text )
            self.set.rename( self._SET_PREFIX+text )
    
    def cmd_changePosition(self):
        ''' change element position '''
        # create pop-up message with all selections for user
        strMessage = ('Enter new position index for %s "%s"\n') % ( self._TYPE, self.getUiName() )
        for x, eachSel in enumerate( self.parentUi.elements ):
            strMessage += '\n%s: %s' % (x, eachSel.getUiName() )
            if( eachSel == self ):
                strMessage += '   <-----   (active)'
        # get input from user
        result = pm.promptDialog( title='Move %s'%self._TYPE, message=strMessage, tx=self.parentUi.elements.index( self ),
                                  button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
        if( result == 'OK' ):
            # get value
            newIndex = pm.promptDialog(q=1, text=1)
            if( not newIndex.isdigit() ):
                raise NameError( 'Given value is not a digit: ', newIndex )
            newIndex = int(newIndex)
            # create setList with new order
            #     get sets
            allSets = self.parentUi.set.dnSetMembers.inputs()# pm.sets( self.parentUi.set, q=1 ) # self.parentUi.set.members() # .members() error in maya 2011
            #     remove from hierarchy
            self.parentUi.set.removeMembers( allSets )
            #     change order
            allSets.insert( newIndex, allSets.pop( allSets.index(self.set) ) )
            #     re-parent
            #self.parentUi.set.resetTo( allSets ) # ignores order // messes up order (not same in input array attr as hierarchy)
            #self.parentUi.set.addMembers( allSets ) # makes correct connections in array attr, but in maya hierarchy order is wrong (script should work anyways)
            #pm.sets( self.parentUi.set, add=allSets ) # ignores order - not sure, definitely something was wrong
            for each in allSets:
                #self.parentUi.set.add( each )# creates history in scriptEditor for each
                pm.sets( self.parentUi.set, add=each )
            # update UI positions
            self.parentUi.element_orderUiDeferred()
    
    def cmd_changeColor(self ):
        ''' edit color of selection '''
        # color UI for user
        pm.colorEditor( rgb=self.color )
        if( pm.colorEditor( q=1, result=1) ):
            self.color = pm.colorEditor( q=1, rgb=1)
            self.setColor()
    
    def object_getSceneName(self, objectName):
        ''' return scene name of given object. Fixed for referenced files '''
        return self.parentUi.referencePrefix+objectName.replace('|', '|'+self.parentUi.referencePrefix)

class Pose(SetElement):
    ''' class to apply and store a pose within a tab '''
    # constants to overwrite
    _SET_PREFIX = 'set_pose_'
    _ATTR_TYPE = 'prSel_pose'
    _TYPE = 'pose'
    # constants custom
    _ATTR_POSEVALUES = 'prSel_poseValues'
    # variables custom
    poseValues = None
    
    def __init__(self, name, parentUi, fromSet=None ):
        ''' create/read pose specific attributes, create button and menuItems '''
        super( Pose, self ).__init__( name, parentUi, fromSet )
        
        # modify new set
        if( not fromSet ):
            # create pose attribute
            self.set.addAttr( self._ATTR_POSEVALUES, dt='stringArray' )
            # read pose attributes and values
            poseAttrs = []
            for each in  pm.ls(sl=1):
                for eachAttr in each.listAttr( k=1, unlocked=1 ):
                    poseAttrs.append( str(eachAttr)+' '+str(eachAttr.get()) )
                for eachAttr in each.listAttr( cb=1, unlocked=1 ):
                    poseAttrs.append( str(eachAttr)+' '+str(eachAttr.get()) )
            # store pose
            self.set.attr( self._ATTR_POSEVALUES ).set( poseAttrs )
        
        # initialize pose variable
        self.poseValues = {}
        for each in self.set.attr( self._ATTR_POSEVALUES ).get():
            eachNode = each[:each.find('.')]
            eachNode = self.object_getSceneName(eachNode)
            if( not self.poseValues.has_key(eachNode) ):
                self.poseValues[eachNode] = []
            self.poseValues[eachNode].append( each )
        
        # UI
        horizontal = pm.horizontalLayout( self, spacing=0 )
        with horizontal:
            self.button = pm.button( l=self.getUiName(), c=pm.Callback( self.cmd_setPose ) )
        horizontal.redistribute()
        
        # menuItems
        with self.rightClickMenu:
            pm.menuItem( divider=1 )
            pm.menuItem( l='Print pose', c=pm.Callback( self.cmd_printPose ) )
        with self.middleClickMenu:
            pm.menuItem( l='Select nodes', c=pm.Callback( self.cmd_selectNodes ) )
            pm.menuItem( divider=1 )
            pm.menuItem( l='Pose selected', c=pm.Callback( self.cmd_setPoseOnSelected ) )
            pm.menuItem( l='Pose selected - XY%', c=pm.Callback( self.ui_poseCustomPercent, True ) )
            pm.menuItem( divider=1 )
            pm.menuItem( l='Pose - 20%', c=pm.Callback( self.cmd_setPose, 20 ) )
            pm.menuItem( l='Pose - 40%', c=pm.Callback( self.cmd_setPose, 40 ) )
            pm.menuItem( l='Pose - 60%', c=pm.Callback( self.cmd_setPose, 60 ) )
            pm.menuItem( l='Pose - 80%', c=pm.Callback( self.cmd_setPose, 80 ) )
            pm.menuItem( l='Pose - XY%', c=pm.Callback( self.ui_poseCustomPercent ) )
    
    def ui_poseCustomPercent(self, poseSelected=False ):
        ''' UI to let user set pose from 1-100% '''
        # create UI
        windowTitle = self.name+' - Pose'
        if( poseSelected ):
            windowTitle += ' selected'
        win = pm.window( title=windowTitle, h=40, w=250 )
        form = pm.horizontalLayout( ratios=[4,1], spacing=5 )
        with form:
            igPosePercent = pm.intSliderGrp( l='Pose __%', cw3=[50,30,10], ad2=1, field=1, min=1, max=100, value=50, step=1 )
            pm.button( l='Apply', c=pm.Callback( self.ui_poseCustomPercentCmd, igPosePercent, poseSelected ) )
        form.redistribute(5,1)
        pm.showWindow(win)
    
    def ui_poseCustomPercentCmd(self, intSliderGrp_percent, poseSelected ):
        ''' get int slider group value and call pose function '''
        percent = pm.intSliderGrp( intSliderGrp_percent, q=1, value=1 )
        if( poseSelected ):
            self.cmd_setPoseOnSelected( percent )
        else:
            self.cmd_setPose( percent )
    
    def setGivenPose(self, poseAttr, percent=100):
        ''' set pose of given string '''
        eachAttr, eachValue = poseAttr.split(' ')
        eachAttr = self.object_getSceneName( eachAttr )
        # check for boolean
        if( eachValue == 'True' ):
            eachValue = 1
        elif( eachValue == 'False' ):
            eachValue = 0
        else:
            eachValue = float(eachValue)
        # percent
        if( percent < 100 ):
            oldValue = pm.getAttr( eachAttr )
            # check for boolean
            if( type(oldValue) is bool ):
                if( oldValue ):
                    oldValue = 1
                else:
                    oldValue = 0
            # calculate new value # float casting because of Python integer rounding (80/100 = 0) for bool attrs
            eachValue = (eachValue*percent + oldValue*(100-percent)) / 100.0
        # set attr
        try:
            pm.setAttr( eachAttr, eachValue )
        except:
            self.parentUi.parentUi.createWarning( 'Invalid objects in pose: ' )
            print eachAttr
    
    def cmd_setPose( self, percent=100 ):
        ''' apply stored pose '''
        for eachPoseAttr in self.set.attr( self._ATTR_POSEVALUES ).get():
            self.setGivenPose( eachPoseAttr, percent )
    
    def cmd_setPoseOnSelected(self, percent=100):
        ''' set pose on selected objects '''
        sel = pm.ls(sl=1)
        for each in sel:
            each = str(each)
            if( self.poseValues.has_key(each) ):
                for eachAttr in self.poseValues[each]:
                    self.setGivenPose( eachAttr, percent )
    
    def cmd_printPose(self):
        ''' print out attributes and vales of pose '''
        print self.set.attr( self._ATTR_POSEVALUES ).get()
    
    def cmd_selectNodes(self):
        ''' select nodes that are part of pose '''
        pm.select( self.poseValues.keys() )

class Selection(SetElement):
    ''' class for each selection button group inside of a tab '''
    # parent-constants to overwrite
    _SET_PREFIX = 'set_selection_'
    _ATTR_TYPE = 'prSel_selection'
    _TYPE = 'selection'
    # constants
    #_ATTR_MEMBER = 'prSel_SelMember'# stringArray 
    _ATTR_MEMBER = 'prSel_SelMember'
    _ATTR_SHAPEVIS = 'prSel_shapeVisibility'
    # variables
    selShapevis = None
    members = None
    
    def __init__(self, name, parentUi, fromSet=None ):
        ''' initialize variables '''
        super( Selection, self ).__init__( name, parentUi, fromSet )
        
        # modify new set
        if( not fromSet ):
            # create custom attributes
            self.set.addAttr( self._ATTR_SHAPEVIS, at='bool', dv=1 )
            #self.set.addAttr( self._ATTR_MEMBER, dt='stringArray' )# stringArray - buggy? causes maya crashes
            self.set.addAttr( self._ATTR_MEMBER, dt='string' )
        
        # read set values
        self.selShapevis = self.set.attr( self._ATTR_SHAPEVIS ).get()
        self.members = []
        
        # right click menu
        if self.referencePrefix:
            dynamicSel = 0
        else:
            dynamicSel = 1
        with self.rightClickMenu:
            pm.menuItem( divider=1 )
            pm.menuItem( l='Add selected', en=dynamicSel, c=pm.Callback( self.member_addSelected ) )
            pm.menuItem( l='Remove selected', en=dynamicSel, c=pm.Callback( self.member_removeSelected ) )
            pm.menuItem( l='Remove disabled', en=dynamicSel, c=pm.Callback( self.member_removeDisabled ) )
            pm.menuItem( divider=1 )
            pm.menuItem( l='Edit Active Members', c=pm.Callback( self.members_window ) )
            pm.menuItem( divider=1 )
            pm.menuItem( l='Print members', c=pm.Callback( self.member_print ) )
        
        # middle click menu
        with self.middleClickMenu:
            pm.menuItem( l='Set keyframe', c=pm.Callback( self.cmd_setKeyframe ) )
            pm.menuItem( l='Delete keyframe', c=pm.Callback( self.cmd_deleteKeyframe ) )
            pm.menuItem( divider=1 )
            pm.menuItem( l='Reset attributes', c=pm.Callback( self.cmd_resetAttributes ) )
            pm.menuItem( divider=1 )
            pm.menuItem( l='Hide shapes', c=pm.Callback( self.cmd_shapeVisibiility, 0 ) )
            pm.menuItem( l='Show shapes', c=pm.Callback( self.cmd_shapeVisibiility, 1 ) )
        
        # make horizontal
        horizontal = pm.horizontalLayout( self, ratios=[1,3,1], spacing=0 )
        with horizontal:
            pm.button( l='-', h=1, w=1, c=pm.Callback( self.cmd_select, 'minus' ) )
            self.button = pm.button( l=self.getUiName(), h=1, w=1, c=pm.Callback( self.cmd_select, 'only' ) )
            pm.button( l='+', h=1, w=1, c=pm.Callback( self.cmd_select, 'plus' ) )
        horizontal.redistribute()
        
        # Members
        if( not fromSet ):
            self.memberAttr_set(1)
        self.members_set()
    
    def getUiName(self):
        ''' return name for UI (popUps, buttonLabel) '''
        prefixShapeVis = ''
        if( not self.selShapevis ):
            prefixShapeVis = '*'
        return ( prefixShapeVis + super(Selection, self).getUiName() )
    
    # #########################
    # MEMBER
    # #########################
    
    def memberAttr_get(self):
        ''' return member attribute as list '''
        #return self.set.attr( self._ATTR_MEMBER ).get()# stringArray 
        fullString = self.set.attr( self._ATTR_MEMBER ).get()
        returnList = []
        if( fullString ):
            for eachAttr in fullString.split(';'):
                eachName, eachStat = eachAttr.split(' ')
                returnList.append( [eachName, int(eachStat)] )
        return returnList
    
    def memberAttr_set(self, useSelection=0):
        ''' set member attribute from variable or selection '''
        '''# stringArray
        memberStringArray = []
        if( useSelection ):
            for each in pm.ls(sl=1):
                memberStringArray.append( '%s 1' % each )
        else:
            for eachName, eachStat in self.members:
                memberStringArray.append( str(eachName)+' '+str(eachStat) )
        self.set.attr( self._ATTR_MEMBER ).set( memberStringArray )
        '''
        memberString = ''
        if( useSelection ):
            for each in pm.ls(sl=1):
                prefix = ''
                if( memberString ):
                    prefix = ';'
                memberString += (prefix+'%s 1' % each)
        else:
            for eachName, eachStat in self.members:
                prefix = ''
                if( memberString ):
                    prefix = ';'
                memberString += prefix+eachName+' '+str(eachStat)
        self.set.attr( self._ATTR_MEMBER ).set( memberString )
    
    def members_set(self):
        ''' set members variable from memberAttribute '''
        self.members = self.memberAttr_get()
        #for eachMemberString in self.set.attr( self._ATTR_MEMBER ).get():# stringArray
        #    self.members.append( eachMemberString.split( ' ' ) )
    
    def members_recreate(self, newMembers):
        ''' set members variable from given list '''
        self.members = []
        for eachMember, eachStat in newMembers:
            self.members.append( [eachMember, eachStat] )
        # update attr
        self.memberAttr_set()
    
    def members_add(self, memberArg ):
        ''' add given string or string array to member variable '''
        if( type(memberArg) == type('') ):
            memberArg = [memberArg, 1]
        for each in memberArg:
            self.members.append( [each, 1] )
    
    def members_window(self):
        ''' open member UI '''
        MemberWindow( self )
    
    def member_getSceneObjects( self, value=None, returnIndices=False ):
        ''' return list of members with optional reference prefix (value None=all, 1=active, 0=inactive '''
        returnList = []
        invalidList = []
        indexList = []
        for x, [eachName, eachStat] in enumerate(self.members):
            if( int(eachStat) == value or value == None ):
                fullName = self.object_getSceneName(eachName)
                if( pm.objExists( fullName )):
                    returnList.append( fullName )
                    indexList.append( x )
                else:
                    invalidList.append( fullName )
        # check
        if( invalidList ):
            self.parentUi.parentUi.createWarning( 'Invalid objects in selection:' )
            print invalidList
        # finish
        if( not returnIndices ):
            return returnList
        else:
            return returnList, indexList
    
    def member_print(self):
        ''' print list of: members, active members, inactive members '''
        print '--- members of selection "%s"' % self.getUiName()
        # all members
        allMembers = self.member_getSceneObjects()
        print 'all      (%d): %s' % (len(allMembers), allMembers)
        # active
        activeMembers = self.member_getSceneObjects(1)
        print 'active   (%d): %s' % (len(activeMembers), activeMembers)
        # inactive
        inactiveMembers = self.member_getSceneObjects(0)
        print 'inactive (%d): %s' % (len(inactiveMembers), inactiveMembers)
    
    def member_addSelected(self):
        ''' add selected objects to selection members '''
        # get selection
        sel = pm.ls(sl=1)
        #     check
        if( not sel ):
            self.parentUi.parentUi.createWarning( 'Could not add selected objects, because nothing is selected.' )
            return
        # create list of objects that are not yet in the selection
        oldMembers = self.member_getSceneObjects()
        newMembers = []
        for each in sel:
            if( not each in oldMembers ):
                newMembers.append( each )
        #     check
        if( not newMembers ):
            self.parentUi.parentUi.createWarning( 'Could not add selected objects, because all selected objects are already part of selection.' )
            return
        # confirm dialog
        popupmsg = 'Add selected objects to "%s":\n' % self.getUiName()
        for each in newMembers:
            popupmsg += '\n'+each
        if( not self.parentUi.parentUi.tryConfirmDialog( popupmsg ) ):
            return
        # save in members variable
        self.members_add( newMembers )
        # update membersAttr
        self.memberAttr_set()
    
    def member_removeSelected(self):
        ''' remove selected objects from selection members '''
        # get selection
        sel = pm.ls(sl=1)
        #     check
        if( not sel ):
            self.parentUi.parentUi.createWarning( 'Could not remove selected objects, because nothing is selected.' )
            return
        # create list of matches between selection and stored members
        oldMembers = self.member_getSceneObjects()
        matchingMembers = []
        matchingIndices = []
        for each in sel:
            if( each in oldMembers ):
                matchingMembers.append( each )
                matchingIndices.append( oldMembers.index(each) )
        #     check
        if( not matchingMembers ):
            self.parentUi.parentUi.createWarning( 'Could not remove selected objects, because none of the selected objects are members.' )
            return
        # pop-up
        popupmsg = 'Remove selected objects from "%s":\n' % self.getUiName()
        for eachName in matchingMembers:
            popupmsg += '\n'+eachName
        if( not self.parentUi.parentUi.tryConfirmDialog( popupmsg ) ):
            return
        # delete members
        matchingIndices.sort()
        matchingIndices.reverse()
        for eachIndex in matchingIndices:
            self.members.pop(eachIndex)
        # update membersAttr
        self.memberAttr_set()
    
    def member_removeDisabled(self):
        ''' remove disabled objects from selection members '''
        # find disabled members
        disabledMembers, disabledIndices = self.member_getSceneObjects( 0, True )
        #     check
        if( not disabledMembers ):
            self.parentUi.parentUi.createWarning( 'Found no disabled members.' )
            return
        # pop-up
        popupmsg = 'Remove disabled members from "%s":\n' % self.getUiName()
        for each in disabledMembers:
            popupmsg += '\n'+each
        if( not self.parentUi.parentUi.tryConfirmDialog( popupmsg ) ):
            return
        # delete members
        disabledIndices.reverse()
        for eachIndex in disabledIndices:
            self.members.pop(eachIndex)
        # update membersAttr
        self.memberAttr_set()
    
    # #########################
    # COMMANDS
    # #########################
    
    def cmd_select(self, flag):
        ''' select command '''
        objects = self.member_getSceneObjects(1)
        # select
        if( flag == 'only' ):
            pm.select( objects )
        elif( flag == 'plus' ):
            pm.select( objects, add=1 )
        elif( flag == 'minus' ):
            pm.select( objects, deselect=1 )
        # focus on panel (so shortcuts work [move-tool,...])
        self.parentUi.parentUi.tryFocusPanel()
    
    def cmd_getKeyableAttrs( self ):
        ''' return all keyable attributes of given object list. use only channelBox if attrs are selected there '''
        # get all active objects
        objects = self.member_getSceneObjects(1)
        
        # find keyable attributes
        keyableAttrs = []
        cbAttrs = pm.channelBox( 'mainChannelBox', q=1, sma=1 )
        if( cbAttrs ):
            # if channelBox attributes are selected use them
            for eachAttr in pm.channelBox( 'mainChannelBox', q=1, sma=1 ):
                for eachObj in objects:
                    eachAttrFull = eachObj+'.'+eachAttr
                    if( pm.getAttr( eachAttrFull, k=1) and not pm.getAttr( eachAttrFull, lock=1) ):
                        keyableAttrs.append( eachAttrFull )
        else:
            # else use all keyable attributes
            for eachObj in objects:
                for eachAttr in pm.PyNode(eachObj).listAttr( k=1, unlocked=1 ):
                    keyableAttrs.append( eachAttr )
        return keyableAttrs
    
    def cmd_getTimeRange(self):
        ''' return current timerange (1,10) '''
        import maya.mel as mm
        aPlayBackSliderPython = mm.eval('$tmpVar=$gPlayBackSlider')
        sr = pm.timeControl( aPlayBackSliderPython, q=1, range=1 )
        rangeStart = int(sr[1:sr.find(':')])
        rangeEnd   = int(sr[sr.find(':')+1:-1])-1
        return (rangeStart, rangeEnd)
    
    def cmd_setKeyframe(self):
        ''' set keyframe on selection '''
        attributes = self.cmd_getKeyableAttrs()
        if( not attributes ):
            return
        # maybe: for performance increase in case of channelBox selection use: maya.mel.eval( 'channelBoxCommand -key' )
        pm.setKeyframe( attributes )
    
    def cmd_deleteKeyframe(self):
        ''' delete keyframes of selection '''
        # get keyable attributes
        attributes = self.cmd_getKeyableAttrs()
        if( not attributes ):
            return
        
        # get time range
        timeRange = self.cmd_getTimeRange()
        
        # maybe: for performance increase (in case of channelBox selection) use: maya.mel.eval( 'channelBoxCommand -cut' )
        # delete keys
        for eachAttr in attributes:
            pm.cutKey( eachAttr, cl=1, t=timeRange )
    
    def cmd_resetAttributes(self):
        ''' reset attribute values of selection '''
        for eachAttr in self.cmd_getKeyableAttrs():
            eachAttrStr = str(eachAttr)
            defaultValue = pm.attributeQuery( eachAttrStr[eachAttr.find('.')+1:], n=eachAttrStr[:eachAttrStr.find('.')], listDefault=1 )[0]
            pm.setAttr( eachAttr, defaultValue )
            #eachAttr.set( defaultValue )# maya 2012+
            #pm.setAttr( eachAttr, defaultValue )
    
    def cmd_shapeVisibiility(self, value):
        ''' show/hide member shapes '''
        # set attr
        self.set.attr( self._ATTR_SHAPEVIS ).set( value )
        self.selShapevis = value
        self.button.setLabel( self.getUiName() )
        
        # set visibility on member shapes
        for eachObject in self.member_getSceneObjects( 1 ):
            for eachShape in pm.PyNode(eachObject).getChildren(s=1):
                try:
                    eachShape.v.set(value)
                except:
                    pass
               
class MemberWindow(pm.uitypes.Window):
    ''' window to edit active members '''
    # constants
    _windowName = 'members_prSelectionUi'
    _BACKGROUND_UNSAVED = [0.5, 0, 0]
    _BACKGROUND_DEFAULT = [0.3, 0.3, 0.3]
    # variables
    memberTSL = None# textScrollList
    formsButton = []
    unsavedChanges = False
    
    def __new__(cls, parentUi):
        ''' delete possible old window and create new instance '''
        if pm.window(cls._windowName, exists=True):
            if( not parentUi.parentUi.parentUi.tryConfirmDialog( 'Close existing "'+cls._windowName+'"?' ) ):
                return
            pm.deleteUI( cls._windowName )
        self = pm.window( cls._windowName, title=parentUi.name )
        return pm.uitypes.Window.__new__(cls, self)
    
    def __init__(self, parentUi):
        ''' create layouts, buttons, show window '''
        # variables
        self.parentUi = parentUi
        # layout
        formRoot = pm.formLayout()
        with formRoot:
            formMembers = pm.formLayout()
            with formMembers:
                # member list
                self.memberTSL = pm.textScrollList( allowMultiSelection=1, sc=pm.Callback( self.cmd_TSL_selection ) )
                # UP / DOWN buttons
                formUpDown = pm.formLayout(w=20)
                #self.formsButton.append( formUpDown )
                with formUpDown:
                    pm.button( ebg=0,l='UP', c=pm.Callback( self.cmd_UP ) )#, nbg=0)# maya 2013+
                    pm.button( ebg=1,l='DN', c=pm.Callback( self.cmd_DN ) )
                formUpDown.vDistribute()
            formMembers.hDistribute(5,1)
            # active buttons
            formActiveBtns = pm.formLayout(h=20, ebg=0)
            #self.formsButton.append( formActiveBtns )
            with formActiveBtns:
                pm.button( l='Select All', c=pm.Callback( self.cmd_select_all ) )
                pm.button( l='Select None', c=pm.Callback( self.cmd_select_none ) )
                pm.button( l='Toggle', c=pm.Callback( self.cmd_select_toggle ) )
            formActiveBtns.hDistribute()
            # storage buttons
            formStorage = pm.formLayout(h=20, ebg=1)
            self.formsButton.append( formStorage )
            with formStorage:
                saveBtn = pm.button( l='Save', c=pm.Callback( self.cmd_save ) )
                reloadBtn = pm.button( l='Reload', c=pm.Callback( self.cmd_load ) )
                closeBtn = pm.button( l='Close', c=pm.Callback( self.cmd_close ) )
            formStorage.hDistribute()
        formRoot.redistribute(7,1,1)
        # color / status
        self.ui_showChanges(0)
        # load members
        self.createTSL()
        # show window
        self.show()
    
    def createTSL(self):
        ''' read members from selection class '''
        self.memberTSL.removeAll()
        for x, [each, status] in enumerate(self.parentUi.members):
            self.memberTSL.append( each )
            if( status == 1 ):
                self.memberTSL.setSelectIndexedItem( x+1 )
    
    def ui_showChanges(self, value):
        '''
        show/hide unsaved changes by coloring button backgrounds
        could not use for formRoot, because of automated textScrollList background color changes,...
        '''
        if( value ):
            backgroundColor = self._BACKGROUND_UNSAVED
        else:
            backgroundColor = self._BACKGROUND_DEFAULT
        for eachForm in self.formsButton:
            try:
                eachForm.setBackgroundColor( backgroundColor )
            except:
                pass
        self.unsavedChanges = value
    
    def cmd_save(self):
        ''' save changes '''
        newMemberAttr = []
        selectedIndices = self.memberTSL.getSelectIndexedItem()
        if( selectedIndices == None ):
            # .getSelectIndexedItem returns None when it should []
            selectedIndices = []
        for x, each in enumerate( self.memberTSL.getAllItems() ):
            if( (x+1) in selectedIndices ):
                newMemberAttr.append( [each, 1] )
            else:
                newMemberAttr.append( [each, 0] )
        # update selection
        self.parentUi.members_recreate( newMemberAttr )
        # update UI color
        self.ui_showChanges( 0 )
    
    def cmd_load(self):
        ''' save changes '''
        self.ui_showChanges( False )
        self.createTSL()
    
    def cmd_close(self):
        ''' close window. popup when there are unsaved changes '''
        if( not self.unsavedChanges ):
            pm.deleteUI( self._windowName )
            return
        if( self.parentUi.parentUi.parentUi.tryConfirmDialog( 'Close and lose unsaved changes?' ) ):
            pm.deleteUI( self._windowName )

    def cmd_TSL_selection(self):
        ''' executed whenever item in textScrollList gets selected '''
        self.ui_showChanges(1)
    
    def cmd_UP(self):
        ''' move selected members one index up '''
        allItems = self.memberTSL.getAllItems()
        newSelection = []
        lastUp = 1
        change = False
        # get selected indices
        selectedIndices = self.memberTSL.getSelectIndexedItem()
        if( selectedIndices == None ):
            # .getSelectIndexedItem returns None when it should []
            selectedIndices = []
        for index in selectedIndices:
            if( index > lastUp ):
                self.memberTSL.removeIndexedItem( index )
                self.memberTSL.appendPosition( [index-1, allItems[index-1]] )
                newSelection.append( index-1 )
                change = True
            else:
                newSelection.append( index )
            lastUp += 1
        # recreate selection
        for index in newSelection:
            self.memberTSL.setSelectIndexedItem( index )
        # update UI
        if( change ):
            self.ui_showChanges(1)
    
    def cmd_DN(self):
        ''' move selected members one index down '''
        # TODO?: merge function with cmd_UP?
        allItems = self.memberTSL.getAllItems()
        newSelection = []
        lastUp = len(allItems)
        change = False
        # get selected indices
        selectedIndices = self.memberTSL.getSelectIndexedItem()
        if( selectedIndices == None ):
            # .getSelectIndexedItem returns None when it should []
            selectedIndices = []
        selectedIndices.reverse()
        for index in selectedIndices:
            if( index < lastUp ):
                self.memberTSL.removeIndexedItem( index )
                self.memberTSL.appendPosition( [index+1, allItems[index-1]] )
                newSelection.append( index+1 )
                change = True
            else:
                newSelection.append( index )
            lastUp -= 1
        # recreate selection
        for index in newSelection:
            self.memberTSL.setSelectIndexedItem( index )
        # update UI
        if( change ):
            self.ui_showChanges(1)
    
    def cmd_select_all(self):
        ''' select all members '''
        #self.memberTSL.selectAll()# broken: 'TextScrollList' object has no attribute 'selectIndexedItem'
        for x in range( len(self.memberTSL.getAllItems()) ):
            self.memberTSL.setSelectIndexedItem( x+1 )
        # update UI color
        self.ui_showChanges( 1 )
    
    def cmd_select_none(self):
        ''' deselect all members '''
        self.memberTSL.deselectAll()
        # update UI color
        self.ui_showChanges( 1 )
    
    def cmd_select_toggle(self):
        ''' toggle all members selection status '''
        # get selected indices
        selectedIndices = self.memberTSL.getSelectIndexedItem()
        if( selectedIndices == None ):
            # .getSelectIndexedItem returns None when it should []
            selectedIndices = []
        # toggle selection
        for x in range( len(self.memberTSL.getAllItems()) ):
            if( x+1 in selectedIndices ):
                self.memberTSL.deselectIndexedItem( x+1 )
            else:
                self.memberTSL.setSelectIndexedItem( x+1 )
        # update UI color
        self.ui_showChanges( 1 )
    #
#
# remove comment from next line, to call the script by executing all the code in this file
#UI()
