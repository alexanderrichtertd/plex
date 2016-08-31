#-*- coding: utf-8 -*-
"""
Simple GUI for Maya 2013-2015 that allows user to quickly and with ease
assign matte id masks to selected objects and preview them.
"""
__author__ = "Dmitry Ryukhtin"
__version__ = "0.1.0"
__email__ = "daymon88@mail.ru"
__web__ = "ryukhtin.com/renderman-studio-mask-picker"

import os
import traceback
import json
import maya.OpenMayaUI as omui

from maya import cmds, mel
from PySide import QtCore, QtGui
from shiboken import wrapInstance

def mayaMainWindow():

    '''returns maya's main window'''
    pointer = omui.MQtUtil.mainWindow()

    # wraps maya's main window object to PySide QWidget object
    return wrapInstance(long(pointer), QtGui.QWidget)

class Masks(object):

    def __init__(self, layer):
        self.layer = layer
        self.suppotedNodes = ['PxrLMDiffuse', 'PxrLMGlass', 'PxrLMPlastic',
                              'PxrLMMetal', 'PxrLMSubsurface', 'PxrDisney']


    def detach(self):

        allShapes = cmds.ls(dag = True, shapes = True, sl = True)
        for i in allShapes:
            try:
                cmds.deleteAttr(i + self.layer)
                print "Succesfully removed %s from %s" % (self.layer, i)
            except:
                print "No %s found on %s, skipping..." % (self.layer, i)

    def select_mask(self, channel):

        self.channel = channel
        #print self.layer
        selList = []
        # get all shapes in the scene
        allShapes = cmds.ls(type = 'mesh')
        # filter those with rman__riattr__user_MatteID0 attribute
        for i in allShapes:
            try:
                value = list(cmds.getAttr(i + self.layer)[0])
                #print value
                #print self.channel
                if value == self.channel:
                    selList.append(i)
            except:
                pass

        if selList:
            cmds.select(clear = True)
            for i in selList:
                # get their direct parents (transforms)
                selTr = cmds.listRelatives(i, parent = True)
                if selTr:
                    # select them all!
                    cmds.select(selTr[0], add = True)
                else:
                    cmds.select(i, add = True)
        else:
            cmds.warning("Selected channel does not contain objects with this color")

    def attach(self, channel):
        '''Attaches mask attribute to all selected transforms'''

        global namePrefix

        namePrefix = "ultiMatteId" # this should remain consistent!
        if not cmds.objExists(namePrefix):
            previousSel = cmds.ls(sl = True, shapes = True, dag = True)
            cmds.shadingNode( "PxrMatteID", name = namePrefix, asTexture = True)
            if previousSel:
                cmds.select(previousSel, replace = True)
            else:
                cmds.select(clear = True)
        else:
            print "skipping %s because it's already esists" % namePrefix

        self.channel = channel

        activeSel = cmds.ls(sl = True, shapes = True, dag = True)
        if not activeSel:
            # dont'do anything
            cmds.warning("Select something first")
        else:
            # do the job
            for i in cmds.ls(sl = True, shapes = True, dag = True):
                if not cmds.getAttr(i + ".intermediateObject"):
                    # assign to those meshes needed attr and color for this attr
                    try:
                        cmds.addAttr(i, ln = self.layer[1:], usedAsColor = True, at = 'float3')
                        cmds.addAttr(i, ln = self.layer[1:] + "R", at = "float", parent = self.layer[1:])
                        cmds.addAttr(i, ln = self.layer[1:] + "G", at = "float", parent = self.layer[1:])
                        cmds.addAttr(i, ln = self.layer[1:] + "B", at = "float", parent = self.layer[1:])

                        cmds.setAttr(i + self.layer, self.channel[0], self.channel[1], self.channel[2], type = "double3")
                        #print "Succesfully added %s" % i + self.layer
                    except RuntimeError:
                        cmds.setAttr(i + self.layer, self.channel[0], self.channel[1],
                                     self.channel[2], type = "double3")
                        #print "%s already exists, setting it's channel to %r" % (i + self.layer, channel)

                    # get all rman materials in selection
                    sg = cmds.listConnections(i, type='shadingEngine')
                    rms_shaders = cmds.ls(cmds.listConnections(sg), materials = True)
                    for sh in rms_shaders:
                        if cmds.nodeType(sh) in self.suppotedNodes:
                            rms_shader = sh
                            print rms_shader
                            break
                        else:
                            rms_shader = None

                    if rms_shader:
                        # make necessary connections
                        try:
                            cmds.connectAttr(namePrefix + ".resultAOV", rms_shader + ".inputAOV", force = True)
                        except RuntimeError:
                            print "connection between %s and %s already exists" % (namePrefix, rms_shader)
                    else:
                        cmds.warning("No renderman shaders have been found on %s" % i)
                else:#if the object is intermediate
                    pass # do nuthin'



class RmsMaskUi(QtGui.QDialog):

    def __init__(self, winParent = mayaMainWindow() ):
        super(RmsMaskUi, self).__init__(winParent)

        self.currentColor = [0, 0, 0]
        # instantiate classes
        self.matteid0 = Masks(".rman__riattr__user_MatteID0")
        self.matteid1 = Masks(".rman__riattr__user_MatteID1")
        self.matteid2 = Masks(".rman__riattr__user_MatteID2")
        self.matteid3 = Masks(".rman__riattr__user_MatteID3")
        self.matteid4 = Masks(".rman__riattr__user_MatteID4")
        self.matteid5 = Masks(".rman__riattr__user_MatteID5")
        self.matteid6 = Masks(".rman__riattr__user_MatteID6")
        self.matteid7 = Masks(".rman__riattr__user_MatteID7")

        self.previewMode = False
        self.currentMask = self.matteid0

        self.allMasks = [self.matteid0, self.matteid1, self.matteid2, self.matteid3,
                         self.matteid4, self.matteid5, self.matteid6, self.matteid7]

    def create(self):
        '''
        Create UI
        '''
        self.setWindowTitle("RMS mask picker 2015")
        self.setObjectName("RMSMaskPickerWindow")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setGeometry(600, 400, 400, 500)

        # declare buttons
        self.createControls()
        # show our layout
        self.createLayout()
        # connect buttons to their functions
        self.createConnections()
        self.createStyleSheets()

    def createControls(self):

        self.windowTitle = QtGui.QLabel("UltiMatte RMS Mask Picker")
        self.windowTitle.setObjectName("header")
        self.windowTitle.setMinimumWidth(400)

        self.selectButton = QtGui.QPushButton("Select")
        self.selectButton.setToolTip("Select objects with mask")
        self.attachButton = QtGui.QPushButton("Attach")
        self.attachButton.setToolTip("Attach mask to selected")
        self.detachButton = QtGui.QPushButton("Detach")
        self.detachButton.setToolTip("Remove current layer from selected objects")

        self.colorButton = QtGui.QPushButton()
        self.colorButton.setMinimumHeight(30)
        self.colorButton.setObjectName("colorB")

        self.toggleButtons = []
        self.toggleDict = {} # label: widget

        for i in range( len(self.allMasks) ):
            label = self.allMasks[i].layer[-8:]

            button = QtGui.QPushButton(label)
            self.toggleButtons.append(button)
            self.toggleDict[label] = self.allMasks[i]


    def createLayout(self):

        # declare main layout which is vertical layout
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setContentsMargins(6, 6, 6, 6)

        # grid layout is for radio buttons
        gridLayout = QtGui.QGridLayout()

        # horizontal layout for select, attach and detach buttons
        twoButtonsLayout = QtGui.QHBoxLayout()

        twoButtonsLayout.addWidget(self.selectButton)
        twoButtonsLayout.addWidget(self.attachButton)
        twoButtonsLayout.addWidget(self.detachButton)

        # CONTINUE FROM HERE
        # add color dialog layout with colored button that leads to cmds.colordDialog, and color slider
        # rearrande matte id togle buttons in two rows
        colorLayout = QtGui.QHBoxLayout()
        colorLayout.addWidget(self.colorButton)

        # (widget, row, column)
        for i in range(0, len(self.allMasks), 2):
            gridLayout.addWidget(self.toggleButtons[i], i, 0)
            self.toggleButtons[i].setCheckable(True)
            self.toggleButtons[i].setAutoExclusive(True)
            if i == 0:
                self.toggleButtons[i].setChecked(True)

        for i in range(1, len(self.allMasks), 2):
            gridLayout.addWidget(self.toggleButtons[i], i - 1, 1)
            self.toggleButtons[i].setCheckable(True)
            self.toggleButtons[i].setAutoExclusive(True)

        topFrame = QtGui.QFrame(self)
        topFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        topFrameLayout = QtGui.QVBoxLayout()
        topFrameLayout.setContentsMargins(6, 6, 6, 6)
        topFrameLayout.addLayout(gridLayout)
        topFrameLayout.addLayout(colorLayout)
        topFrameLayout.addLayout(twoButtonsLayout)

        topFrame.setLayout(topFrameLayout)

        mainLayout.addWidget(self.windowTitle)
        mainLayout.addWidget(topFrame)
        mainLayout.addStretch()

        self.setLayout(mainLayout)

    def createConnections(self):

        for i in self.toggleButtons:
            i.clicked.connect(self.set_current_mask)

        self.selectButton.clicked.connect(self.select_meshes)
        self.attachButton.clicked.connect(self.attach_mask)
        self.detachButton.clicked.connect(self.detach_mask)
        self.colorButton.clicked.connect(self.set_color)

    def createStyleSheets(self):
        '''
        All style sheets are being created and assigned here
        '''
        self.loadStyle()
        self.windowTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.colorButtonSheet = """
QPushButton#colorB {{
    border-width: 0px;
    border-radius: 1px;
    background-color: rgb( {0}, {1}, {2} )
}}
QPushButton:checked {{
    background-color: #ffa729;
    color: black;
}}
QPushButton:hover {{
    border: 1px solid #ffa729;
}}
QLabel#header {{
    font-size: 22px;
    color: #dddddd;
    border: 0px solid #333333;
    border-radius: 5px;
    margin: 2px 2px 2px 2px; /*top-right-bottom-left*/
    }}
QPushButton {{
    background-color: #464646;
    font-size: 12px;
}}

"""
        self.set_color_swatch()

####SLOTS START

    def loadStyle(self):
        # to be implemented later
        pass

    def set_color_swatch(self):
        self.newColorButtonSheet = self.colorButtonSheet.format(self.currentColor[0], self.currentColor[1], self.currentColor[2])
        self.setStyleSheet(self.newColorButtonSheet)

    def set_color(self):
        cursor = QtGui.QCursor()
        p = cursor.pos()
        x = p.x()
        y = p.y()
        offset = 250
        result = cmds.colorEditor(position = [x - offset, y - 100], mini = True,
            rgb = self.convert_color(self.currentColor, "to1") )
        buffer = result.split()
        if '1' == buffer[-1]:
              values = cmds.colorEditor(query = True, rgb = True)
              self.currentColor = self.convert_color(values, "to255")
              self.set_color_swatch()
        else:
              print 'Editor was dismissed'

    def convert_color(self, value, mode):

        if mode == "to255":
            result = [value[0]*255, value[1]*255, value[2]*255 ]
        elif mode == "to1":
            result = [value[0]/255.0, value[1]/255.0, value[2]/255.0 ]
        else:
            pass
        #print value, result
        return result

    def select_meshes(self):
        self.sendColor = self.convert_color(self.currentColor, "to1")
        self.currentMask.select_mask(self.sendColor)

    def detach_mask(self):
        self.currentMask.detach()

    def attach_mask(self):
        self.sendColor = self.convert_color(self.currentColor, "to1")
        self.currentMask.attach(self.sendColor)

    def set_current_mask(self):

        sender = self.sender()
        self.currentMask = self.toggleDict[sender.text()]


####SLOTS END


def UI(*args):

    # Development workaround for PySide winEvent error (Maya 2014)
    # Make sure the UI is deleted before recreating
    global rmsMaskWindow

    try:
        rmsMaskWindow.deleteLater()
        cmds.deleteUI('rmsDocking')
        print "deleted maya dock"
    except:
        pass

    # Create minimal UI object
    rmsMaskWindow = RmsMaskUi()
    rmsMaskWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    print "class instantiated"

    # Delete the UI if errors occur to avoid causing winEvent
    # and event errors (in Maya 2014)
    try:
        rmsMaskWindow.create()
        print "window created"

        if (cmds.dockControl('rmsDocking', q = True, ex = True) ):
            cmds.deleteUI('rmsDocking')
            print "deleted maya dock2"
        print "trying to create dock"
        try:
            dock = cmds.dockControl('rmsDocking', label='Rms Mask dock',
                allowedArea = 'right', area = 'right', floating = False,
                width = 400, content = 'RMSMaskPickerWindow' ) # self.setObjectName()
        except:
            pass
        print "dock created"

        rmsMaskWindow.show()

    except:
        rmsMaskWindow.close()
        rmsMaskWindow.deleteLater()
        traceback.print_exc()

if __name__ == "__main__":
    UI()