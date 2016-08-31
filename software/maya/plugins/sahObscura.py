#*************************************************************
# title:        Menu
#
# software:     Maya
#
# content:      Adds a Menu with its functions to MAYA
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************


try:
    import  os
    import  sys
    import  math
    import  time
    import  sched
    import  getpass
    import  subprocess
    import  maya.utils
    import  threading
    import  maya.OpenMaya as openMaya
    import  maya.OpenMayaUI as openMayaUi
    import  maya.cmds as cmds
    import  pymel.core as pm
    import  maya.mel as mel
    from    functools import partial
    from    threading import Timer
    from    xml.dom.minidom import parse, Document
except Exception as e:
    print "Error: importing python modules!!!\n",
    print   e
 
 
class Eval_Thread(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
 
    def run(self, *args):
        maya.utils.executeInMainThreadWithResult(self.eval)
 
    def eval(self, *args):
        self.camera_list = cmds.listRelatives(cmds.ls(type='camera'),type='transform', p=True)
        allItems = cmds.textScrollList('obs_cam_scrollList_a', q=True, allItems=True)
        for o in self.camera_list:
            if o not in allItems:
                cmds.textScrollList('obs_cam_scrollList_a', e=True, append=o)
                cmds.textScrollList('obs_cam_scrollList_a', e=True, font= "boldLabelFont")
 
        for o in allItems:
            if o not in self.camera_list:
                cmds.textScrollList('obs_cam_scrollList_a', e=True, removeItem=str(o))
 
        threading.Timer(2, self.run).start()
 
class functionality(Eval_Thread):
    """docstring for functionality"""
    def __init__(self, *args):
        super(functionality, self).__init__()
 
    def delete_window(self, name, *args):
        if cmds.window(name, query = True, exists =True):
            cmds.deleteUI(name, window = True)
 
    def init_eval(self, *args):
        self.camera_list = cmds.listRelatives(cmds.ls(type='camera'),type='transform', p=True)
        for c in self.camera_list:
            cmds.textScrollList('obs_cam_scrollList_a', e=True, append=c)
        cmds.textScrollList('obs_cam_scrollList_a', e=True, sii=1)
         
    def init_processing(self, *args):
        threading.Timer(3, self.run).start()
 
 
    def delete_windows(self, *args):
        for o in self.build_separate_windows_dict:
            self.delete_window(self.build_separate_windows_dict[o])
        cmds.button("obs_build_button", e=True, label = "Build Separate Panel", c=self.build_separate_windows)
 
    def select_camera(self, name, *args):
        modelPanel_list = cmds.getPanel( type='modelPanel' )
        self.camera_panel_dict  = {}
        for o in modelPanel_list:
            camera = cmds.lookThru( str(o), q=True )
            self.camera_panel_dict[camera] = str(o)
             
        panel = cmds.getPanel (wf=1)
        if panel.startswith("model"):
            query_selected_item = cmds.textScrollList(name, q=True, si=True)[0]
            string = "lookThroughModelPanel " + str(query_selected_item) + " " + str(panel)
            mel.eval(string)
        else:
            cmds.warning("select Model Panel!, current Panel: " + str(panel))
 
    def playblast_render(self, *args):
        try:
            exportPath = pm.fileDialog2(fm=3, okc='Select Folder', cap='Select Folder')[0]
            query_selected_item = cmds.textScrollList('obs_cam_scrollList_a', q=True, si=True)
            panel = cmds.getPanel (wf=1)
            if panel.startswith("model"):
                for o in query_selected_item:
                    string = "lookThroughModelPanel " + str(o) + "  " + str(panel)
                    mel.eval(string)
                    filename = str(exportPath) + "/" + str(o)
                    cmds.playblast(fmt="qt", filename=str(filename), forceOverwrite=True, sequenceTime=False, clearCache=True, viewer=True, showOrnaments=True, fp=4, percent=100, compression="H.264", quality=100)
            else:
                cmds.warning("select Model Panel!, currentPanel: " + str(panel))
        except Exception, e:
            pass
 
    def build_multi_windows(self, *args):
        query_selected_item = cmds.textScrollList('obs_cam_scrollList_a', q=True, si=True)
        self.delete_window('main_build_window')
 
        if len(query_selected_item) == 0:
            cmds.warning("select a Camera")
        else:
            self.build_windows      = {}
            self.build_UI           = {}
            self.build_editor       = {}
            self.build_pane         = {}
            self.build_rest         = {}
            count = 0
            w = cmds.textField('obs_width_field', q=True, tx=True)
            h = cmds.textField('obs_height_field', q=True, tx=True)
            self.build_windows["main_build_window"]     = cmds.window('main_build_window',w=int(w), h=int(h), title = "obscura", sizeable = True, menuBar = False, minimizeButton = True,maximizeButton = True)
            self.build_UI["main_build_scrollLayout"]    = cmds.scrollLayout(parent = self.build_windows["main_build_window"], h=int(h), w=int(w))
            self.build_UI["main_build_column"]          = cmds.columnLayout(columnAttach =("both", 5), parent = self.build_windows["main_build_window"], w=int(w))
 
            iter_pane_range                                     = int(math.floor(len(query_selected_item) / 4))
            for o in range(int(iter_pane_range)):
                self.build_pane[str(o)]                         = cmds.paneLayout(configuration = 'quad', parent = self.build_UI["main_build_column"], h=int(h), w=int(w))
                for i in range(int(4)):
                    self.build_editor[str(i)]                   = cmds.modelEditor(cam = query_selected_item[count], displayTextures=True,shadows=True, displayAppearance='smoothShaded')
                    count += 1
 
            iter_rest_range                                     = len(query_selected_item) % 4
            if int(iter_rest_range) > 0:
                self.build_rest[str(count)]                     = cmds.paneLayout(configuration = 'quad', parent = self.build_UI["main_build_column"], h=int(h), w=int(w))
                for o in range(int(iter_rest_range)):
                    self.build_editor[str(o) + str(count)]      = cmds.modelEditor(cam = query_selected_item[count], displayTextures=True,shadows=True, displayAppearance='smoothShaded')
                    count += 1
 
            cmds.showWindow(self.build_windows["main_build_window"])
 
 
    def build_separate_windows(self, *args):
        query_selected_item = cmds.textScrollList('obs_cam_scrollList_a', q=True, si=True)
        if len(query_selected_item) == 0:
            cmds.warning("select a Camera")
        else:
            self.build_separate_windows_dict    = {}
            self.build_separate_UI              = {}
            te = 0
            le = 0
            count = 0
            for o in query_selected_item:
                w = int(cmds.textField('obs_width_field', q=True, tx=True))/3
                h = int(cmds.textField('obs_height_field', q=True, tx=True))/3
                self.build_separate_windows_dict[str(o)]        = cmds.window(w=int(w), h=int(h), title = str(o), te=int(te), le=int(le), sizeable = True, menuBar = False, minimizeButton = True,maximizeButton = True)
                self.build_separate_UI[str(o) + "form"]         = cmds.formLayout()
                self.build_separate_UI[str(o) + "model"]        = cmds.modelEditor()
                self.build_separate_UI[str(o) + "column"]       = cmds.columnLayout()
 
                cmds.formLayout( self.build_separate_UI[str(o) + "form"], edit=True, attachForm=[(self.build_separate_UI[str(o) + "column"], 'top', 0), (self.build_separate_UI[str(o) + "column"], 'left', 0),
                                (self.build_separate_UI[str(o) + "model"], 'top', 0), (self.build_separate_UI[str(o) + "model"], 'bottom', 0), (self.build_separate_UI[str(o) + "model"], 'right', 0)],
                                attachNone=[(self.build_separate_UI[str(o) + "column"], 'bottom'), (self.build_separate_UI[str(o) + "column"], 'right')],
                                attachControl=(self.build_separate_UI[str(o) + "model"], 'left', 0, self.build_separate_UI[str(o) + "column"]))
                                
                cmds.modelEditor(self.build_separate_UI[str(o) + "model"], edit=True, camera=o, displayTextures=True,shadows=True, displayAppearance='smoothShaded')
                cmds.showWindow(self.build_separate_windows_dict[str(o)])
                count          += 1
                le             +=int(w)
 
                count_range =  6
                multiply_range = 1
                for o in xrange(20):
                    if count == count_range*multiply_range:
                        le = 0
                        te=int(h)*multiply_range
                    multiply_range +=1
 
        cmds.button("obs_build_button", e=True, label = "Delete Windows", c=self.delete_windows)
 
 
    def select_attribute_camera(self, *args):
        panel = cmds.getPanel (wf=1)
        if panel.startswith("model"):
            mel.eval("postModelEditorSelectCamera " + str(panel) + " " + str(panel) + " 0;")
        else:
            cmds.warning("select panel, currentPanel: " + str(panel))
 
 
 
class sah_obscura_UI(functionality):
    """docstring for sah_obscura_UI"""
    def __init__(self, *args):
        super(sah_obscura_UI, self).__init__()
 
        self.delete_window('obs_main_win')
        self.obscura_UI()
         
    def obscura_UI(self, *args):
        main_pane_width                     = 400
        self.UI                             = {}
        self.UI["obs_main_win"]             = cmds.window('obs_main_win', title = "sah_obscura", sizeable = False, menuBar = False, minimizeButton = True,maximizeButton = True, w=int(main_pane_width))
        self.UI["obs_main_column"]          = cmds.columnLayout(parent = self.UI["obs_main_win"])
        self.UI["obs_main_pane"]            = cmds.paneLayout(configuration = 'vertical2', parent = self.UI["obs_main_column"])
        self.UI["obs_sub_cam_column_a"]     = cmds.columnLayout(parent = self.UI["obs_main_pane"], h=int(main_pane_width)/2)
        self.UI["obs_sub_cam_column_b"]     = cmds.columnLayout(parent = self.UI["obs_main_pane"], h=int(main_pane_width)/2)
        self.UI["obs_sub_pane"]             = cmds.paneLayout(configuration = 'horizontal3', parent = self.UI["obs_sub_cam_column_a"], w=int(main_pane_width)/3)
        self.UI["obs_refresh_button"]       = cmds.button(label = "Refresh", parent =self.UI["obs_sub_pane"], c=self.init_processing, w=int(main_pane_width)/3.5)
        self.UI["obs_cam_scrollList_a"]     = cmds.textScrollList('obs_cam_scrollList_a', parent = self.UI["obs_sub_pane"], h=int(main_pane_width)/1.5, sc=partial(self.select_camera, 'obs_cam_scrollList_a'), allowMultiSelection=True)
        self.UI["obs_tabLayout_a"]          = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, parent = self.UI["obs_sub_cam_column_b"])
        self.UI["obs_child_a"]              = cmds.columnLayout(parent = self.UI["obs_tabLayout_a"],columnAttach=("both", 5), h=int(main_pane_width)/2)
        self.UI["obs_child_b"]              = cmds.columnLayout(parent = self.UI["obs_tabLayout_a"], columnAttach=("both", 5), h=int(main_pane_width)/2)
        self.UI["obs_separator_a"]          = cmds.separator(style="none", parent=self.UI["obs_child_a"], h=10)
        self.UI["obs_rowColumn"]            = cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 40), (2, 50)] , parent =self.UI["obs_child_a"])
        self.UI["obs_width_text"]           = cmds.text(label='Width' , parent = self.UI["obs_rowColumn"])
        self.UI["obs_width_field"]          = cmds.textField('obs_width_field',  text="1000", parent = self.UI["obs_rowColumn"])
        self.UI["obs_height_text"]          = cmds.text(label='Height' , parent = self.UI["obs_rowColumn"])
        self.UI["obs_height_field"]         = cmds.textField('obs_height_field', text= "500", parent = self.UI["obs_rowColumn"])
        self.UI["obs_separator_c"]          = cmds.separator(style="none", parent=self.UI["obs_child_a"], h=10)
        self.UI["obs_build_button"]         = cmds.button(label = "Build Multi Panel", parent =self.UI["obs_child_a"], c=self.build_multi_windows, w=int(main_pane_width)/3.5)
        self.UI["obs_separator_b"]          = cmds.separator(style="none", parent=self.UI["obs_child_a"], h=10)
        self.UI["obs_build_button"]         = cmds.button("obs_build_button", label = "Build Separate Panel", parent =self.UI["obs_child_a"], c=self.build_separate_windows, w=int(main_pane_width)/3.5)
        self.UI["obs_separator_b"]          = cmds.separator(style="none", parent=self.UI["obs_child_a"], h=10)
        self.UI["obs_select_button"]        = cmds.button(label = "Select Camera", parent =self.UI["obs_child_a"], c=self.select_attribute_camera, w=int(main_pane_width)/3.5)
        self.UI["obs_playblast_button"]     = cmds.button(label = "Start Playblast", parent =self.UI["obs_child_b"], c=self.playblast_render, w=int(main_pane_width)/3.5)
 
 
        cmds.tabLayout( self.UI["obs_tabLayout_a"], edit=True, tabLabel=((self.UI["obs_child_a"], 'Panels'), (self.UI["obs_child_b"], 'Process')) )
        cmds.showWindow(self.UI["obs_main_win"] )
 
 
        self.init_eval()
        self.init_processing()
 
 
def run():
    """Standardized run() method. Used to call modules functionality"""
 
    sah_obscura_UI()
 
run()




# try:
#     import  os
#     import  sys
#     import  math
#     import  time
#     import  sched
#     import  getpass
#     import  subprocess
#     import  maya.utils
#     import  threading
#     import  maya.OpenMaya as openMaya
#     import  maya.OpenMayaUI as openMayaUi
#     import  maya.cmds as cmds
#     import  pymel.core as pm
#     import  maya.mel as mel
#     from    functools import partial
#     from    threading import Timer
#     from    xml.dom.minidom import parse, Document
# except Exception as e:
#     print "Error: importing python modules!!!\n",
#     print   e
 
 
# class Eval_Thread(threading.Thread):
#     def __init__(self, *args):
#         threading.Thread.__init__(self)
 
#     def run(self, *args):
#         maya.utils.executeInMainThreadWithResult(self.eval)
 
#     def eval(self, *args):
#         self.camera_list = cmds.listRelatives(cmds.ls(type='camera'),type='transform', p=True)
#         allItems = cmds.textScrollList('obs_cam_scrollList_a', q=True, allItems=True)
#         for o in self.camera_list:
#             if o not in allItems:
#                 cmds.textScrollList('obs_cam_scrollList_a', e=True, append=o)
#                 cmds.textScrollList('obs_cam_scrollList_a', e=True, font= "boldLabelFont")
 
#         for o in allItems:
#             if o not in self.camera_list:
#                 cmds.textScrollList('obs_cam_scrollList_a', e=True, removeItem=str(o))
 
#         threading.Timer(2, self.run).start()
 
# class functionality(Eval_Thread):
#     """docstring for functionality"""
#     def __init__(self, *args):
#         super(functionality, self).__init__()
 
#     def delete_window(self, name, *args):
#         if cmds.window(name, query = True, exists =True):
#             cmds.deleteUI(name, window = True)
 
#     def init_eval(self, *args):
#         self.camera_list = cmds.listRelatives(cmds.ls(type='camera'),type='transform', p=True)
#         for c in self.camera_list:
#             cmds.textScrollList('obs_cam_scrollList_a', e=True, append=c)
#         cmds.textScrollList('obs_cam_scrollList_a', e=True, sii=1)
         
#     def init_processing(self, *args):
#         threading.Timer(3, self.run).start()
 
 
#     def delete_windows(self, *args):
#         for o in self.build_separate_windows_dict:
#             self.delete_window(self.build_separate_windows_dict[o])
#         cmds.button("obs_build_button", e=True, label = "Build Separate Panel", c=self.build_separate_windows)
 
#     def select_camera(self, name, *args):
#         modelPanel_list = cmds.getPanel( type='modelPanel' )
#         self.camera_panel_dict  = {}
#         for o in modelPanel_list:
#             camera = cmds.lookThru( str(o), q=True )
#             self.camera_panel_dict[camera] = str(o)
             
#         panel = cmds.getPanel (wf=1)
#         if panel.startswith("model"):
#             query_selected_item = cmds.textScrollList(name, q=True, si=True)[0]
#             string = "lookThroughModelPanel " + str(query_selected_item) + " " + str(panel)
#             mel.eval(string)
#         else:
#             cmds.warning("select Model Panel!, current Panel: " + str(panel))
 
#     def playblast_render(self, *args):
#         try:
#             exportPath = pm.fileDialog2(fm=3, okc='Select Folder', cap='Select Folder')[0]
#             query_selected_item = cmds.textScrollList('obs_cam_scrollList_a', q=True, si=True)
#             panel = cmds.getPanel (wf=1)
#             if panel.startswith("model"):
#                 for o in query_selected_item:
#                     string = "lookThroughModelPanel " + str(o) + "  " + str(panel)
#                     mel.eval(string)
#                     filename = str(exportPath) + "/" + str(o)
#                     cmds.playblast(fmt="qt", filename=str(filename), forceOverwrite=True, sequenceTime=False, clearCache=True, viewer=True, showOrnaments=True, fp=4, percent=100, compression="H.264", quality=100)
#             else:
#                 cmds.warning("select Model Panel!, currentPanel: " + str(panel))
#         except Exception, e:
#             pass
 
#     def build_multi_windows(self, *args):
#         query_selected_item = cmds.textScrollList('obs_cam_scrollList_a', q=True, si=True)
#         self.delete_window('main_build_window')
 
#         if len(query_selected_item) == 0:
#             cmds.warning("select a Camera")
#         else:
#             self.build_windows      = {}
#             self.build_UI           = {}
#             self.build_editor       = {}
#             self.build_pane         = {}
#             self.build_rest         = {}
#             count = 0
#             w = cmds.textField('obs_width_field', q=True, tx=True)
#             h = cmds.textField('obs_height_field', q=True, tx=True)
#             self.build_windows["main_build_window"]     = cmds.window('main_build_window',w=int(w), h=int(h), title = "obscura", sizeable = True, menuBar = False, minimizeButton = True,maximizeButton = True)
#             self.build_UI["main_build_scrollLayout"]    = cmds.scrollLayout(parent = self.build_windows["main_build_window"], h=int(h), w=int(w))
#             self.build_UI["main_build_column"]          = cmds.columnLayout(columnAttach =("both", 5), parent = self.build_windows["main_build_window"], w=int(w))
 
#             iter_pane_range                                     = int(math.floor(len(query_selected_item) / 4))
#             for o in range(int(iter_pane_range)):
#                 self.build_pane[str(o)]                         = cmds.paneLayout(configuration = 'quad', parent = self.build_UI["main_build_column"], h=int(h), w=int(w))
#                 for i in range(int(4)):
#                     self.build_editor[str(i)]                   = cmds.modelEditor(cam = query_selected_item[count], displayTextures=True,shadows=True, displayAppearance='smoothShaded')
#                     count += 1
 
#             iter_rest_range                                     = len(query_selected_item) % 4
#             if int(iter_rest_range) > 0:
#                 self.build_rest[str(count)]                     = cmds.paneLayout(configuration = 'quad', parent = self.build_UI["main_build_column"], h=int(h), w=int(w))
#                 for o in range(int(iter_rest_range)):
#                     self.build_editor[str(o) + str(count)]      = cmds.modelEditor(cam = query_selected_item[count], displayTextures=True,shadows=True, displayAppearance='smoothShaded')
#                     count += 1
 
#             cmds.showWindow(self.build_windows["main_build_window"])
 
 
#     def build_separate_windows(self, *args):
#         query_selected_item = cmds.textScrollList('obs_cam_scrollList_a', q=True, si=True)
#         if len(query_selected_item) == 0:
#             cmds.warning("select a Camera")
#         else:
#             self.build_separate_windows_dict    = {}
#             self.build_separate_UI              = {}
#             te = 0
#             le = 0
#             count = 0
#             for o in query_selected_item:
#                 w = int(cmds.textField('obs_width_field', q=True, tx=True))/3
#                 h = int(cmds.textField('obs_height_field', q=True, tx=True))/3
#                 self.build_separate_windows_dict[str(o)]        = cmds.window(w=int(w), h=int(h), title = str(o), te=int(te), le=int(le), sizeable = True, menuBar = False, minimizeButton = True,maximizeButton = True)
#                 self.build_separate_UI[str(o) + "form"]         = cmds.formLayout()
#                 self.build_separate_UI[str(o) + "model"]        = cmds.modelEditor()
#                 self.build_separate_UI[str(o) + "column"]       = cmds.columnLayout()
 
#                 cmds.formLayout( self.build_separate_UI[str(o) + "form"], edit=True, attachForm=[(self.build_separate_UI[str(o) + "column"], 'top', 0), (self.build_separate_UI[str(o) + "column"], 'left', 0),
#                                 (self.build_separate_UI[str(o) + "model"], 'top', 0), (self.build_separate_UI[str(o) + "model"], 'bottom', 0), (self.build_separate_UI[str(o) + "model"], 'right', 0)],
#                                 attachNone=[(self.build_separate_UI[str(o) + "column"], 'bottom'), (self.build_separate_UI[str(o) + "column"], 'right')],
#                                 attachControl=(self.build_separate_UI[str(o) + "model"], 'left', 0, self.build_separate_UI[str(o) + "column"]))
                                
#                 cmds.modelEditor(self.build_separate_UI[str(o) + "model"], edit=True, camera=o, displayTextures=True,shadows=True, displayAppearance='smoothShaded')
#                 cmds.showWindow(self.build_separate_windows_dict[str(o)])
#                 count          += 1
#                 le             +=int(w)
 
#                 count_range =  6
#                 multiply_range = 1
#                 for o in xrange(20):
#                     if count == count_range*multiply_range:
#                         le = 0
#                         te=int(h)*multiply_range
#                     multiply_range +=1
 
#         cmds.button("obs_build_button", e=True, label = "Delete Windows", c=self.delete_windows)
 
 
#     def select_attribute_camera(self, *args):
#         panel = cmds.getPanel (wf=1)
#         if panel.startswith("model"):
#             mel.eval("postModelEditorSelectCamera " + str(panel) + " " + str(panel) + " 0;")
#         else:
#             cmds.warning("select panel, currentPanel: " + str(panel))
 
 
 
# class sah_obscura_UI(functionality):
#     """docstring for sah_obscura_UI"""
#     def __init__(self, *args):
#         super(sah_obscura_UI, self).__init__()
 
#         self.delete_window('obs_main_win')
#         self.obscura_UI()
         
#     def obscura_UI(self, *args):
#         main_pane_width                     = 400
#         self.UI                             = {}
#         self.UI["obs_main_win"]             = cmds.window('obs_main_win', title = "sah_obscura", sizeable = False, menuBar = False, minimizeButton = True,maximizeButton = True, w=int(main_pane_width))
#         self.UI["obs_main_column"]          = cmds.columnLayout(parent = self.UI["obs_main_win"])
#         self.UI["obs_main_pane"]            = cmds.paneLayout(configuration = 'vertical2', parent = self.UI["obs_main_column"])
#         self.UI["obs_sub_cam_column_a"]     = cmds.columnLayout(parent = self.UI["obs_main_pane"], h=int(main_pane_width)/2)
#         self.UI["obs_sub_cam_column_b"]     = cmds.columnLayout(parent = self.UI["obs_main_pane"], h=int(main_pane_width)/2)
#         self.UI["obs_sub_pane"]             = cmds.paneLayout(configuration = 'horizontal3', parent = self.UI["obs_sub_cam_column_a"], w=int(main_pane_width)/3)
#         self.UI["obs_refresh_button"]       = cmds.button(label = "Refresh", parent =self.UI["obs_sub_pane"], c=self.init_processing, w=int(main_pane_width)/3.5)
#         self.UI["obs_cam_scrollList_a"]     = cmds.textScrollList('obs_cam_scrollList_a', parent = self.UI["obs_sub_pane"], h=int(main_pane_width)/1.5, sc=partial(self.select_camera, 'obs_cam_scrollList_a'), allowMultiSelection=True)
#         self.UI["obs_tabLayout_a"]          = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, parent = self.UI["obs_sub_cam_column_b"])
#         self.UI["obs_child_a"]              = cmds.columnLayout(parent = self.UI["obs_tabLayout_a"],columnAttach=("both", 5), h=int(main_pane_width)/2)
#         #self.UI["obs_child_b"]              = cmds.columnLayout(parent = self.UI["obs_tabLayout_a"], columnAttach=("both", 5), h=int(main_pane_width)/2)
#         self.UI["obs_separator_a"]          = cmds.separator(style="none", parent=self.UI["obs_child_a"], h=10)
#         self.UI["obs_rowColumn"]            = cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 40), (2, 50)] , parent =self.UI["obs_child_a"])
#         self.UI["obs_width_text"]           = cmds.text(label='Width' , parent = self.UI["obs_rowColumn"])
#         self.UI["obs_width_field"]          = cmds.textField('obs_width_field',  text="1000", parent = self.UI["obs_rowColumn"])
#         self.UI["obs_height_text"]          = cmds.text(label='Height' , parent = self.UI["obs_rowColumn"])
#         self.UI["obs_height_field"]         = cmds.textField('obs_height_field', text= "500", parent = self.UI["obs_rowColumn"])
#         self.UI["obs_separator_c"]          = cmds.separator(style="none", parent=self.UI["obs_child_a"], h=10)
#         self.UI["obs_build_button"]         = cmds.button(label = "Build Multi Panel", parent =self.UI["obs_child_a"], c=self.build_multi_windows, w=int(main_pane_width)/3.5)
#         self.UI["obs_separator_b"]          = cmds.separator(style="none", parent=self.UI["obs_child_a"], h=10)
#         self.UI["obs_build_button"]         = cmds.button("obs_build_button", label = "Build Separate Panel", parent =self.UI["obs_child_a"], c=self.build_separate_windows, w=int(main_pane_width)/3.5)
#         self.UI["obs_separator_b"]          = cmds.separator(style="none", parent=self.UI["obs_child_a"], h=10)
#         self.UI["obs_select_button"]        = cmds.button(label = "Select Camera", parent =self.UI["obs_child_a"], c=self.select_attribute_camera, w=int(main_pane_width)/3.5)
#         self.UI["obs_separator_b"]          = cmds.separator(style="none", parent=self.UI["obs_child_a"], h=10)
#         self.UI["obs_playblast_button"]     = cmds.button(label = "Start Playblast", parent =self.UI["obs_child_a"], c=self.playblast_render, w=int(main_pane_width)/3.5)
 
#         cmds.tabLayout( self.UI["obs_tabLayout_a"], edit=True, tabLabel=(self.UI["obs_child_a"], 'Panels') )
#         cmds.showWindow(self.UI["obs_main_win"] )
 
#         self.init_eval()
#         self.init_processing()
 
 
# def run():
#     """Standardized run() method. Used to call modules functionality"""
 
#     sah_obscura_UI()
 
# run()