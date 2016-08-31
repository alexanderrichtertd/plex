"""
tweenMachine.py

author:         Justin S Barrett

description:    Tool for creating breakdown or "tween" keyframes between the
                previous and next keys, using a slider to adjust the bias/weight
                that the surrounding keys have over the new key.

usage:          import tweenMachine
                tweenMachine.start()
                
revisions:
    - 04.12.2013 - 3.0.0 - jbarrett
        - Initial publish after conversion to Python
    - 05.22.2015 - 3.0.0b1 - jbarrett
        - First public beta release (limited feature set)
    - 07.11.2015 - 3.0.0b1a - jbarrett
        - Fixed: Overshoot mode reset properly from settings when restarting TM
        - Fixed: When grabbing the global key tangent, make sure it's a string
        - Fixed: If there are no curves to tween, force an empty list
        - Changed: Disabled toolbar opt for Maya 2013 until a fix can be found
        
to-do:
    
"""

#-------------------------------------------------------------------------
#----------------------------------------------------------- Imports -----

# Built-in
import os
import urllib2
import xml.etree.cElementTree as etree

# Third-party
import maya.cmds as mc
import maya.mel as mel

# Custom

#-------------------------------------------------------------------------
#----------------------------------------------------------- Globals -----

__version__ = "3.0.0 b1a"
MAYA_VERSION = mc.about(version=True)

#-------------------------------------------------------------------------
#--------------------------------------------------------- Functions -----

def clear_menu(menu):
    """
    Clear the specified menu of its current contents
    """
    try:
        [mc.deleteUI(i) for i in mc.menu(menu, q=True, ia=True)]
    except:
        pass

def defer_delete(item):
    """
    Defer the deletion of a UI item to prevent Maya from crashing when that UI
    item is still active as it's deleted
    """
    mc.evalDeferred("mc.deleteUI('" + item + "')")
        
def find_ui(uitype):
    found = mc.lsUI(type=uitype)
    if found is None:
        return ""
    for item in found:
        try:
            doctag = eval("mc." + uitype + "(item, q=True, docTag=True)")
        except RuntimeError:
            doctag = ""
        if doctag == "tweenMachine":
            return item
    return ""

def start():
    """
    Convenience function to open the main tweenMachine instance
    """
    TMWindowUI()
    
def inactive():
    """
    Display a warning when a feature is not active
    """
    mc.warning("This tweenMachine feature is not currently active.")

def tween(bias, nodes=None):
    """
    Create the in-between key(s) on the specified nodes
    """
    if isinstance(nodes, list) and not nodes:
        nodes = None
    # Find the current frame, where the new key will be added
    currenttime = mc.timeControl("timeControl1", q=True, ra=True)[0]
    # Figure out which nodes to pull from
    if nodes is not None:
        pullfrom = nodes
    else:
        pullfrom = mc.ls(sl=True)
        if not pullfrom:
            return
    # If attributes are selected, use them to build curve node list
    attributes = mc.channelBox("mainChannelBox", q=True, sma=True)
    if attributes:
        curves = []
        for attr in attributes:
            for node in pullfrom:
                fullnode = "%s.%s" % (node, attr)
                if not mc.objExists(fullnode):
                    continue
                tmp = mc.keyframe(fullnode, q=True, name=True)
                if not tmp:
                    continue
                curves += tmp
    # Otherwise get curves for all nodes
    else:
        curves = mc.keyframe(pullfrom, q=True, name=True)
    mc.waitCursor(state=True)
    # Wrap the main operation in a try/except to prevent the waitcursor from
    # sticking if something should fail
    try:
    	# If we have no curves, force a list
    	if curves is None:
    		curves = []
        # Process all curves
        for curve in curves:
            # Find time for next and previous keys...
            time_prev = mc.findKeyframe(curve, which="previous")
            time_next = mc.findKeyframe(curve, which="next")
            # Find previous and next tangent types
            in_tan_prev = mc.keyTangent(curve, time=(time_prev,), q=True,
                                        itt=True)[0]
            out_tan_prev = mc.keyTangent(curve, time=(time_prev,), q=True,
                                         ott=True)[0]
            in_tan_next = mc.keyTangent(curve, time=(time_next,), q=True,
                                        itt=True)[0]
            out_tan_next = mc.keyTangent(curve, time=(time_next,), q=True,
                                         ott=True)[0]
            # Set new in and out tangent types
            in_tan_new = out_tan_prev
            out_tan_new = in_tan_next
            # However, if any of the types (previous or next) is "fixed",
            # use the global (default) tangent instead
            if "fixed" in [in_tan_prev, out_tan_prev, in_tan_next, out_tan_next]:
                in_tan_new = mc.keyTangent(q=True, g=True, itt=True)[0]
                out_tan_new = mc.keyTangent(q=True, g=True, ott=True)[0]
            elif out_tan_next == "step":
                out_tan_new = out_tan_next
            # Find previous and next key values
            value_prev = mc.keyframe(curve, time=(time_prev,), q=True,
                                     valueChange=True)[0]
            value_next = mc.keyframe(curve, time=(time_next,), q=True,
                                     valueChange=True)[0]
            value_new = value_prev + ((value_next - value_prev) * bias)
            # Set new keyframe and tangents
            mc.setKeyframe(curve, t=(currenttime,), v=value_new,
                           ott=out_tan_new)
            if in_tan_new != "step":
                mc.keyTangent(curve, t=(currenttime,), itt=in_tan_new)
            # If we're using the special tick, set that appropriately
            if SETTINGS["use_special_tick"]:
                mc.keyframe(curve, tds=True, t=(currenttime,))
    except:
        raise
    finally:
        mc.waitCursor(state=False)
        mc.currentTime(currenttime)
        mel.eval("global string $gMainWindow;")
        windowname = mel.eval("$temp = $gMainWindow")
        mc.setFocus(windowname)

#-------------------------------------------------------------------------
#----------------------------------------------------------- Classes -----

class TMData(object):
    """
    Core code for data organization (groups and sets)
    """
    
    def __init__(self):
        # Try to read preferences from option variables; otherwise use defaults
        self.element = None
        self.name = "selected"
        self.groups = []
        # Try to read the existing XML data
        nodes = mc.ls("tmXML*")
        if nodes:
            # If we have more than one, use the first one, but warn the user
            self.node = nodes[0]
            if len(nodes) > 1:
                mc.warning("Multiple tweenMachine data nodes found.  Using"
                           + self.node)
            # If the data is in the old format (tmXML has children), convert it
            if mc.listRelatives(self.node, children=True):
                print "# tweenMachine: Old data found.  Converting..."
                self.root = etree.XML("<tweenMachineData />")
                self.tree = etree.ElementTree(self.root)
                # Create base elements
                opt_element = etree.SubElement(self.root, "options")
                buttons_element = etree.SubElement(self.root, "buttons")
                buttons_element.set("height", str(SETTINGS["button_height"]))
                groups_element = etree.SubElement(self.root, "groups")
                # Convert option data
                slider_vis_node = mc.ls("tmSliderVis*")[0]
                opt_element.set("slider_vis",
                                str(mc.getAttr(slider_vis_node + ".data")))
                button_vis_node = mc.ls("tmSliderVis*")[0]
                opt_element.set("button_vis",
                                str(mc.getAttr(button_vis_node + ".data")))
                # Convert button data
                buttons_node = mc.ls("tmButtons*")[0]
                for node in mc.listRelatives(buttons_node, children=True):
                    suffix = node[-1]
                    bcolor = str(mc.getAttr("tmButtonRGB%s.data" % suffix))
                    bvalue = str(mc.getAttr("tmButtonValue%s.data" % suffix))
                    button_element = etree.SubElement(buttons_element, "button")
                    button_element.set("rgb", bcolor)
                    button_element.set("value", bvalue)
                # Convert groups and sets
                group_node = mc.ls("tmGroups*")[0]
                for node in mc.ls(group_node + "|tmGroup*"):
                    # Get the group name and order
                    gname = str(mc.getAttr(node + ".id"))
                    gorder = str(mc.getAttr(node + ".order"))
                    group_element = etree.SubElement(groups_element, "group")
                    group_element.set("name", gname)
                    group_element.set("index", gorder)
                    # Get the sets in this group
                    for setnode in mc.listRelatives(node, children=True):
                        setname = str(mc.getAttr(setnode + ".id"))
                        setorder = str(mc.getAttr(setnode + ".order"))
                        # Create a set node and add the set objects to it
                        set_element = etree.SubElement(group_element, "set")
                        set_element.set("name", setname)
                        set_element.set("index", setorder)
                        setobjs = []
                        for objnode in mc.listRelatives(setnode, children=True):
                            setobjs.append(str(mc.getAttr(objnode + ".data")))
                        set_element.text = " ".join(setobjs)
            # Otherwise get the data from the node
            else:
                self.root = etree.XML(mc.getAttr(node + ".data"))
                self.tree = etree.ElementTree(self.root)
        # Otherwise start from scratch
        else:
            self.root = etree.XML("""<tweenMachineData>
    <options slider_vis="1" button_vis="1" />
    <buttons height="%s">
         <button rgb="0.6 0.6 0.6" value="-75" />
         <button rgb="0.6 0.6 0.6" value="-60" />
         <button rgb="0.6 0.6 0.6" value="-33" />
         <button rgb="0.6 0.6 0.6" value="0" />
         <button rgb="0.6 0.6 0.6" value="33" />
         <button rgb="0.6 0.6 0.6" value="60" />
         <button rgb="0.6 0.6 0.6" value="75" />
    </buttons>
    <groups />
</tweenMachineData>
""" % SETTINGS["button_height"])
            self.tree = etree.ElementTree(self.root)
        etree.dump(self.tree)
        # Next: replace existing data with new XML data
        # erase old data nodes
            


class TMGroup(object):
    """
    Container object for a collection of TMSet classes
    """
    
    def __init__(self, element=None, element_parent=None):
        self._element_parent = element_parent
        self.sets = []
        self._element = element
        if self._element is not None:
            # Build list of sets from XML data
            pass
        else:
            self._element = etree.SubElement(self._element_parent, "group", name="")
        
    def add_set(self, name):
        """
        Add the named set
        """
        
    # Properties

    def _get_nodes(self):
        """
        Return all nodes in all contained sets
        """
        allnodes = []
        for set_ in self.sets:
            allnodes += set_.nodes
        return list(set(allnodes))
        
    nodes = property(_get_nodes)

        

class TMSet(object):
    """
    Data class that operates on a predefined list of nodes (or no nodes, in the
    case of the default selected set)
    """
    
    def __init__(self, nodes=None, element=None, groupelement=None):
        self._groupelement = groupelement
        # If we have an element, assume that it contains the list of nodes
        if element is not None:
            self._nodes = element.get("nodes").split()
            self.name = element.get("name")
        else:
            # If we have no element, and no nodes, this is the selected set.
            # Otherwise assume that the list of nodes was passed in, and make a
            # new XML element
            self._nodes = nodes
            if nodes is not None:
                self._element = etree.SubElement(groupelement, "set", name="",
                                                 nodes=" ".join(self._nodes))
        
    # Properties
    
    def _get_nodes(self):
        """
        Returns the list of nodes for this set
        """
        return self._nodes
        
    def _set_nodes(self, nodes=None):
        """
        Sets the list of nodes
        """
        # If no nodes were passed (or None was passed), default to the current selection
        if nodes is None:
            self._nodes = mc.ls(sl=True)
        else:
            self._nodes = nodes
        
    nodes = property(_get_nodes, _set_nodes)
        
        
    
class TMWindowUI(object):
    """
    Main tool window
    """
    
    def __init__(self):
        # Import maya.cmds at root namespace for deferred commands
        mc.evalDeferred("import maya.cmds as mc")
        # Check for updates
        if SETTINGS["update_check"]:
            self.update_check()
        # First get an instance of the main data class
        self.data = TMData()
        # Set core variables
        self.docked = SETTINGS["docked"]
        self.show_mode = SETTINGS["show_mode"]
        self.use_overshoot = SETTINGS["use_overshoot"]
        self.use_special_tick = SETTINGS["use_special_tick"]
        self.window = None
        self.set_ui_mode()
        self._build_all_groups()

        # Kick off scriptJobs
        ##scriptJob -p tweenMachineWin -e "SceneOpened" "deleteUI tweenMachineWin; tweenMachine;";
        #scriptJob -p tweenMachineWin -e "NewSceneOpened" "deleteUI tweenMachineWin;";
        #scriptJob -uid tweenMachineWin "tmRestoreTimeControl";

    def _make_window(self):
        """
        Make the core window that will contain all the UI elements
        """
        # Make the main window
        windowname = "tweenMachineWindow"
        if SETTINGS["ui_mode"] != "window":
            windowname = None
        if SETTINGS["ui_mode"] == "window" and mc.window("tweenMachineWindow",
                                                         q=True, ex=True):
            mc.deleteUI("tweenMachineWindow")
        self.window = mc.window(windowname, width=300, height=50,
                 minimizeButton=True, maximizeButton=False, menuBar=True,
                 menuBarVisible=SETTINGS["show_menu_bar"],
                 resizeToFitChildren=True, sizeable=True,
                 title="tweenMachine v%s" % __version__,
                 docTag="tweenMachine", iconName="tweenMachine")
        # Build the base UI elements
        self.main_form = mc.formLayout(parent=self.window)
        self.selected_row = TMSetUI(self.main_form, "Selected")
        mc.formLayout(self.main_form, e=True,
                      attachForm=[(self.selected_row.form, "top", 0),
                                  (self.selected_row.form, "left", 0),
                                  (self.selected_row.form, "right", 0)])
        
    def _make_menus(self):
        """
        Make the menus
        """
        # Force the show_menu_bar to a certain setting in certain modes
        if SETTINGS["ui_mode"] in ["toolbar", "dock"]:
            SETTINGS["show_menu_bar"] = False
        # Make the base menus
        if SETTINGS["show_menu_bar"]:
            menus = mc.window(self.window, q=True, menuArray=True)
            if menus is not None:
                for menu in menus:
                    if mc.menu(menu, q=True, label=True) == "Options":
                        self._opt_menu = menu
            else:
                self._opt_menu = mc.menu(label="Options",
                                          postMenuCommand=self._make_opt_menu)
            mc.evalDeferred("mc.window('%s', e=True, menuBarVisible=True)"
                            % self.window)
        else:
            if not hasattr(self, "popup_menu"):
                self.popup_menu = mc.popupMenu(parent=self.main_form)
            self._opt_menu = mc.menuItem(p=self.popup_menu, label="Options",
                                 postMenuCommand=self._make_opt_menu,
                                 subMenu=True)
        
    def _make_opt_menu(self, *args):
        """
        Make the options menu
        """
        clear_menu(self._opt_menu)
        show_menu = mc.menuItem(p=self._opt_menu, label="Show...", subMenu=True)
        # Menu bar  and label visibility toggles
        if SETTINGS["ui_mode"] in ["window", "dock"]:
            mc.menuItem(p=show_menu, label="Menu Bar",
                        cb=SETTINGS["show_menu_bar"],
                        command=self._toggle_menu_visibility)
        mc.menuItem(p=show_menu, label="Label", cb=SETTINGS["show_label"],
                    command=self._toggle_label_visibility)
        mc.menuItem(p=show_menu, divider=True)
        # Slider and button visibility options
        show_collection = mc.radioMenuItemCollection(parent=show_menu)
        mc.menuItem(p=show_menu, label="Slider and Buttons",
                    rb=self.show_mode == "both",
                    command=lambda x, m="both":self._set_show_mode(m))
        mc.menuItem(p=show_menu, label="Slider Only",
                    rb=self.show_mode == "slider",
                    command=lambda x, m="slider":self._set_show_mode(m))
        mc.menuItem(p=show_menu, label="Buttons Only",
                    rb=self.show_mode == "buttons",
                    command=lambda x, m="buttons":self._set_show_mode(m))
        # UI mode options
        if "2013" not in MAYA_VERSION:
            mc.menuItem(p=self._opt_menu, divider=True)
            mode_menu = mc.menuItem(p=self._opt_menu, label="Mode...",
                                    subMenu=True)
            mode_collection = mc.radioMenuItemCollection(parent=mode_menu)
            mc.menuItem(p=mode_menu, label="Window",
                        rb=SETTINGS["ui_mode"] == "window",
                        command=lambda x, m="window":self.set_ui_mode(m))
            mc.menuItem(p=mode_menu, label="Toolbar",
                        rb=SETTINGS["ui_mode"] == "toolbar",
                        command=lambda x, m="toolbar":self.set_ui_mode(m))
        mc.menuItem(p=self._opt_menu, divider=True)
        mc.menuItem(p=self._opt_menu, label="Overshoot", cb=self.use_overshoot,
                    command=self._toggle_overshoot)
        mc.menuItem(p=self._opt_menu, label="Special Tick Color",
                    cb=self.use_special_tick,
                    command=self._toggle_special_tick)
        
    def _add_group_prompt(self, *args):
        """
        Open a dialog that allows the user to add a new group
        """
        result = mc.promptDialog(title="Add Group", message="Enter group name",
                                 button=["OK", "Cancel"], defaultButton="OK",
                                 cancelButton="Cancel", dismissString="Cancel")
        if result == "OK":
            self._add_group(mc.promptDialog(q=True, text=True))
        
    def _add_group(self, name):
        """
        Create a group with the specified name
        """
        inactive()
        
    def _add_set_pre(self, *args):
        """
        Open a dialog that allows the user to add a new set
        """
        inactive()
        
    def _add_set_post(self):
        """
        Callback from the dialog made by _add_set_pre
        """
        inactive()
        
    def _open_data_manager(self, *args):
        """
        Open the group/set data manager dialog
        """
        inactive()
        
    def _open_button_manager(self, *args):
        """
        Open the group/set data manager dialog
        """
        inactive()

    def _set_show_mode(self, mode):
        """
        Set the show mode
        """
        self.show_mode = mode
        SETTINGS["show_mode"] = mode
        self.selected_row.set_show_mode(mode)
        
    def _toggle_overshoot(self, *args):
        """
        Toggle the overshoot setting
        """
        self.use_overshoot = not self.use_overshoot
        SETTINGS["use_overshoot"] = self.use_overshoot
        self.selected_row.toggle_overshoot()
        
    def _toggle_special_tick(self, *args):
        """
        Toggle the use of the special tick color
        """
        self.use_special_tick = not self.use_special_tick
        SETTINGS["use_special_tick"] = self.use_special_tick
        
    def _toggle_label_visibility(self, *args):
        """
        Toggle visibility of the slider label(s)
        """
        show = not SETTINGS["show_label"]
        SETTINGS["show_label"] = show
        self.selected_row.set_label_visibility(show)
        
    def _toggle_menu_visibility(self, *args):
        """
        Toggle visibility of the window menu
        """
        show = not SETTINGS["show_menu_bar"]
        SETTINGS["show_menu_bar"] = show
        mc.window(self.window, e=True, menuBarVisible=show)
        self._make_menus()
        mc.refresh(force=True)
        if show:
            if self.popup_menu is not None:
                mc.popupMenu(self.popup_menu, e=True, dai=True)
        
    def _build_all_groups(self):
        """
        Build the group interface(s) based on the data in the scene
        """

    def _cleanup(self):
        """
        Clean up stuff when the tool is closed
        """
        # Restore the time control to the animation list
        mc.timeControl("timeControl1", e=True, mlc="animationList")
        
    # ----- Character Sets ---------------------------------------------------#
    
    def _add_character_group(self, *args):
        """
        Add a group that will work with character set data
        """
        inactive()
        
    def _import_character_sets(self, *args):
        """
        Import character set data from scene
        """
        inactive()
        
    # ----- UI Management ----------------------------------------------------#
    
    def set_ui_mode(self, mode=None):
        """
        Set the UI's current state (window, dock, toolbar, HUD)
        """
        oldmode = SETTINGS["ui_mode"]
        # If user is in Maya 2013, force window mode until a fix can be found
        # for toolbar mode
        if "2013" in MAYA_VERSION:
            mode = None
            oldmode = "window"
        # Update the UI appropriately if we're changing modes
        if mode != oldmode:
            if mode is None:
                mode = oldmode
            SETTINGS["ui_mode"] = mode
            # Delete the popup menu variable so that a new one can be made
            if hasattr(self, "popup_menu"):
                del(self.popup_menu)
            # Show the proper UI
            window = self.window
            if self.window is None:
                window = find_ui("window")
            toolbar = find_ui("toolBar")
            dock = find_ui("dockControl")
            self._make_window()
            deleteold = None
            hasmenu = True
            if mode == "window":
                if oldmode == "toolbar" and toolbar:
                    deleteold = toolbar
                    SETTINGS["show_menu_bar"] = True
                if oldmode == "dock" and dock:
                    deleteold = dock
                mc.showWindow(self.window)
            elif mode == "toolbar":
                if toolbar:
                    deleteold = toolbar
                if oldmode == "window" and window:
                    deleteold = window
                if oldmode == "dock" and dock:
                    deleteold = dock
                if not mc.toolBar("tweenMachineToolbar", q=True, exists=True):
                    mc.toolBar("tweenMachineToolbar", height=20,
                               docTag="tweenMachine", content=self.window,
                               area="left", label="tweenMachine")
                    mc.windowPref(restoreMainWindowState="startupMainWindowState")
                else:
                    mc.windowPref(saveMainWindowState="startupMainWindowState")
            elif mode == "dock":
                pass
            elif mode == "hud":
                hasmenu = False
            if hasmenu:
                self._make_menus()
            # If we're deleting an old item, set a deferred command to do so
            if deleteold is not None:
                defer_delete(deleteold)
            
    # ----- File Management --------------------------------------------------#
    
    def new(self, *args):
        """
        Flush all data and start over
        """
        inactive()
        
    def load(self, *args):
        """
        Load groups and sets from a tweenMachine data file
        """
        inactive()
        
    def save(self, *args):
        """
        Save groups and sets to a tweenMachine data file
        """
        inactive()
        
    def update_check(self):
        """
        Check for updates
        """
            

        
class TMSetUI(object):
    """
    Base UI class for a single set, which includes a slider, a set of buttons,
    a numeric field, a check box, and a label
    """
    
    def __init__(self, parent, name, **kwds):
        self.data = TMSet()
        self.name = name
        self.form = mc.formLayout(parent=parent)
        self.showcheck = lambda:self.data.nodes is not None
        self.checkbox = mc.checkBox(parent=self.form, label="",
                                    manage=self.showcheck())
        self.label = mc.text(parent=self.form, label=self.name, width=90,
                             manage=SETTINGS["show_label"])
        mode = SETTINGS["show_mode"]
        self.slider = mc.floatSlider(parent=self.form, min=-100,
                                        max=100, value=0, 
                                        manage=mode in ["both", "slider"],
                                        changeCommand=self.tween_slider,
                                        dragCommand=self.update_field)
        self.field = mc.floatField(parent=self.form, min=-100, max=100, value=0,
                                   width=50, pre=1, step=1,
                                   changeCommand=self.tween_field,
                                   enterCommand=self.tween_field,
                                   dragCommand=self.tween_field)
        # Attach the checkbox
        mc.formLayout(self.form, e=True, 
                      attachForm=[(self.checkbox, "left", 5),
                                  (self.checkbox, "top", 0)])
        # Attach the label
        mc.formLayout(self.form, e=True,
                      attachControl=[(self.label, "left", 5, self.checkbox)])
        mc.formLayout(self.form, e=True,
                      attachForm=[(self.label, "top", 3)])
        labelOffset = 90 * int(SETTINGS["show_label"])
        # Attach the field
        mc.formLayout(self.form, e=True,
                      attachForm=[(self.field, "left", labelOffset),
                                  (self.field, "top", 0)])
        # Attach the slider
        mc.formLayout(self.form, e=True,
                      attachForm=[(self.slider, "left", labelOffset + 55),
                                  (self.slider, "right", 5),
                                  (self.slider, "top", 3)])
        # Build and attach the button row
        self.buttonrow = TMButtonRowUI(self, self.form, **kwds)
        mc.formLayout(self.buttonrow.form, e=True,
                      manage=mode in ["both", "buttons"])
        mc.formLayout(self.form, e=True,
                      attachForm=[(self.buttonrow.form, "left", labelOffset + 55),
                                  (self.buttonrow.form, "top", 5 + (20 * int(mode!="buttons"))),
                                  (self.buttonrow.form, "right", 5)])
        # If overshoot mode is active, then force-toggle the overshoot
        if SETTINGS["use_overshoot"]:
            self.toggle_overshoot()
        
    def tween(self, value):
        """
        Callback when the slider is triggered
        """
        tween((value + 100) / 200.0, self.data.nodes)
        
    def tween_field(self, value):
        """
        Callback when the field value is changed
        """
        mc.floatSlider(self.slider, e=True, value=value)
        self.tween(value)
        
    def tween_slider(self, value):
        """
        Callback when the slider value is changed
        """
        self.update_field(value)
        self.tween(value)
        
    def tween_button(self, value):
        """
        Callback when a button is clicked
        """
        self.update_field(value)
        self.tween_field(value)
        
    def update_field(self, value):
        """
        Update the field without tweening
        """
        mc.floatField(self.field, e=True, value=value)
        
    def set_show_mode(self, mode):
        """
        Set the show mode for this row
        """
        mc.floatSlider(self.slider, e=True, manage=mode in ["both", "slider"])
        mc.formLayout(self.buttonrow.form, e=True,
                      manage=mode in ["both", "buttons"])
        mc.formLayout(self.form, e=True,
                      attachForm=[(self.buttonrow.form, "top",
                                   5 + (20 * int(mode!="buttons")))])
    
    def set_label_visibility(self, mode):
        """
        Set the visibility of the set's label
        """
        mc.text(self.label, e=True, manage=mode)
        # Adjust spacing of other UI elements
        labelOffset = 90 * int(mode)
        mc.formLayout(self.form, e=True,
                      attachForm=[(self.field, "left", labelOffset)])
        mc.formLayout(self.form, e=True,
                      attachForm=[(self.slider, "left", labelOffset + 55)])
        mc.formLayout(self.form, e=True,
                      attachForm=[(self.buttonrow.form, "left", labelOffset + 55)])
        
    def toggle_overshoot(self):
        """
        Toggle the overshoot setting
        """
        if mc.floatSlider(self.slider, q=True, min=True) == -100:
            mc.floatSlider(self.slider, e=True, min=-150, max=150)
            mc.floatField(self.field, e=True, min=-150, max=150)
        else:
            value = mc.floatSlider(self.slider, q=True, value=True)
            if value > 100:
                mc.floatSlider(self.slider, e=True, value=100)
                mc.floatField(self.field, e=True, value=100)
            if value < -100:
                mc.floatSlider(self.slider, e=True, value=-100)
                mc.floatField(self.field, e=True, value=-100)
            mc.floatSlider(self.slider, e=True, min=-100, max=100)
            mc.floatField(self.field, e=True, min=-100, max=100)



class TMButtonRowUI(object):
    """
    UI for the row of buttons within a single TM set
    """
    
    def __init__(self, setUI, parentform, **kwds):
        self.set = setUI
        self.edit = kwds.get("edit", False)
        if "button_data" in kwds:
            data = kwds["button_data"]
        else:
            # Use the default data
            data = SETTINGS["default_button_data"]
        self.data = TMButtonRowData(data)
        self.form = mc.formLayout(parent=parentform, height=10,
                                  nd=(10 * len(self.data)))
        self.buttons = ()
        self.refresh()
            
    def refresh(self):
        """
        Refresh the items in the row
        """
        [mc.deleteUI(button) for button in self.buttons]
        buttons = []
        index = 0
        for index, element in enumerate(self.data):
            buttons.append(mc.iconTextButton(parent=self.form,
                           height=SETTINGS["button_height"],
                           backgroundColor=element.color,
                           #label=str((index*buttonwidth)/100.0),
                           style="textOnly",
                           command=lambda v=element.value:self.tween(v)))
            left = (index * 10) + 1
            right = ((index + 1) * 10) - 1
            mc.formLayout(self.form, e=True,
                          attachPosition=[(buttons[-1], "left", 0, left),
                                          (buttons[-1], "right", 0, right),
                                          (buttons[-1], "top", 0, 0)])
        self.buttons = tuple(buttons)
    
    def tween(self, value):
        """
        Call the tween method of the set
        """
        if not self.edit:
            self.set.tween_button(value)



class TMButtonRowData(object):
    """
    Data for a row of buttons
    """
    
    def __init__(self, data):
        self.buttons = tuple([TMButtonData(element) for element in data])

    def __len__(self):
        return len(self.buttons)

    def __iter__(self):
        """
        Part of the iteration protocol
        """
        self.iter_index = -1
        return self
        
    def next(self):
        """
        Part of the iteration protocol
        """
        self.iter_index += 1
        try:
            return self.buttons[self.iter_index]
        except:
            raise StopIteration
        
        


class TMButtonData(object):
    """
    Data for a single button in a row
    """
    
    def __init__(self, data):
        self.value, self.color = data
        
    def change_value(self, value):
        """
        Change the value of this button
        """
        self.value = value
    
    def change_color(self, color):
        """
        Change the color of this button
        """
        self.color = color
        
    def __repr__(self):
        """
        Return a tuple that represents the data
        """
        return (self.value, self.color)




class TMSettings(dict):
    """
    Convenience class to get/set global settings via an option variable
    """
    
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        # Search for existing option variable.  If it doesn't exist, make it
        # using the default options
        self.name = "tweenMachineSettings"
        if mc.optionVar(exists=self.name):
            data = eval(mc.optionVar(q=self.name))
            for key in data:
                self[key] = data[key]
        # Add new items if they don't exist
        if "use_special_tick" not in self:
            self["special_tick"] = False
        if "slider_width" not in self:
            self["slider_width"] = 200
        if "docked" not in self:
            self["docked"] = False
        if "show_mode" not in self:
            self["show_mode"] = "both"
        if "use_overshoot" not in self:
            self["use_overshoot"] = False
        if "use_special_tick" not in self:
            self["use_special_tick"] = False
        if "default_button_data" not in self:
            self["default_button_data"] = ((-75, (0.6, 0.6, 0.6)),
                                           (-60, (0.6, 0.6, 0.6)),
                                           (-33, (0.6, 0.6, 0.6)),
                                           (0, (0.6, 0.6, 0.6)),
                                           (33, (0.6, 0.6, 0.6)),
                                           (60, (0.6, 0.6, 0.6)),
                                           (75, (0.6, 0.6, 0.6)))
        if "button_height" not in self:
            self["button_height"] = 8
        if "show_label" not in self:
            self["show_label"] = True
        if "show_menu_bar" not in self:
            self["show_menu_bar"] = True
        if "update_check" not in self:
            self["update_check"] = False
        if "ui_mode" not in self:
            self["ui_mode"] = "window"
        
    def __setitem__(self, key, value):
        """
        Set the named item, and save the data back to the optionVar
        """
        dict.__setitem__(self, key, value)
        mc.optionVar(stringValue=(self.name, str(self)))
        
        

#-------------------------------------------------------------------------
#----------------------------------------------------------- Default -----

SETTINGS = TMSettings()

if __name__ == "__main__":
    # Create a instance of the settings class, then kick off the main window
    TMWindowUI()
