#TODO XGEN: This supplies XGEN with some arnold centric settings in the XGEN  GUI 
#  to make this work,  MTOA has to load before the XGEN plugin.  if they are loaded the other way around  XGen does not refresh its list of renderers and it is not added..

import maya
maya.utils.loadStringResourcesForModule(__name__)


import sys
import os.path
import maya.api.OpenMaya as om
import maya.OpenMayaAnim as oma
import maya.cmds as cmds
import maya.mel as mel
from xgenm import XgExternalAPI as xgapi
import xgenm as xg
from xgenm.ui.widgets import *
from xgenm.ui.util.xgUtil import *
from xgenm.ui.tabs.xgRendererTab import *
from xgenm.ui.util.xgProgressBar import setProgressInfo
import ctypes
import types

k_RenderAPIRenderer = "Renderman"
k_RenderAPIRendererObj = k_RenderAPIRenderer + "Renderer"
k_RenderAPIRendererInit = False

def castSelf(selfid):
    # Can't pass self as an object.
    # It's cast to id(self) by the caller
    # and we convert it back to a python object here
    if isinstance(selfid,str):
        return ctypes.cast( int(selfid), ctypes.py_object ).value
    else:
        return selfid

def addMethod( self, method ):
    self.__dict__[method.__name__] = types.MethodType( method, self, xg.ui.tabs.RendermanRendererTabUI )
#
# RenderAPI RendererTab UI callbacks

# RenderAPIRendererTabUIInit callback
# Called at the end of RenderAPIRendererTab.__init__()
def xgArnoldUI(selfid):
    self = castSelf(selfid)

    # Extend the RenderAPIRendererTab instance with some of our methods
    addMethod( self, xgArnoldRefresh )
    addMethod( self, xgArnoldCurveModeChanged )
    addMethod( self, xgArnoldRenderModeChanged )
    addMethod( self, xgArnoldMotionBlurModeChanged )
    addMethod( self, xgArnoldMotionBlurChanged )
    addMethod( self, xgArnoldPatchesChanged )
    addMethod( self, xgArnoldUseAuxPatchesChanged )

    expand = ExpandUI(maya.stringTable[ 'y_xgenArnoldUI.kArnoldSettings'  ])
    self.arnold_expand_settings = expand
    self.layout().addWidget( expand )


    # Horizontal layout
    row = QtGui.QWidget()
    hbox = QtGui.QHBoxLayout()
    hbox.setSpacing(3)
    hbox.setContentsMargins(1,1,1,1)
    label = QtGui.QLabel(maya.stringTable[ 'y_xgenArnoldUI.kArnoldRenderMode'  ])
    label.setFixedWidth(labelWidth())
    label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
    label.setIndent(10)
    label.setToolTip(maya.stringTable[ 'y_xgenArnoldUI.kArnoldRenderModeAnn'  ])
    hbox.addWidget(label)
    self.arnold_rendermode = QtGui.QComboBox()
    self.arnold_rendermode.setFixedWidth( 120 )
    self.arnold_rendermode.addItem(maya.stringTable[ 'y_xgenArnoldUI.kRenderModeLive'  ], "1" )
    self.arnold_rendermode.addItem(maya.stringTable[ 'y_xgenArnoldUI.kRenderModeBatch' ], "3" )
    self.arnold_rendermode.setToolTip(label.toolTip())
    self.connect(self.arnold_rendermode , QtCore.SIGNAL("activated(int)"), self.xgArnoldRenderModeChanged )
    hbox.addWidget(self.arnold_rendermode)
    filler = QtGui.QWidget()
    hbox.addWidget(filler)
    row.setLayout(hbox)
    expand.addWidget(row)

    # Horizontal layout
    row = QtGui.QWidget()
    hbox = QtGui.QHBoxLayout()
    hbox.setSpacing(3)
    hbox.setContentsMargins(1,1,1,1)
    label = QtGui.QLabel(maya.stringTable[ 'y_xgenArnoldUI.kTools'  ])
    label.setFixedWidth(labelWidth())
    label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
    label.setIndent(10)
    hbox.addWidget(label)

    self.arnold_apply_hair_shader = QtGui.QPushButton()
    self.arnold_apply_hair_shader.setText(maya.stringTable[ 'y_xgenArnoldUI.kArnoldApplyHair'  ])
    self.arnold_apply_hair_shader.setToolTip(maya.stringTable[ 'y_xgenArnoldUI.kArnoldApplyHairAnn'  ])
    self.connect(self.arnold_apply_hair_shader, QtCore.SIGNAL("activated(int)"),
                 lambda: mel.eval("print 'NEED TO ADD CODE HERE TO CREATE AI HAIR AND ASSIGN IT TO DESCRIPTION:'" % (xgg.DescriptionEditor.currentDescription(), xgg.DescriptionEditor.currentPalette )))
    hbox.addWidget(self.arnold_apply_hair_shader)

    filler = QtGui.QWidget()
    hbox.addWidget(filler)
    row.setLayout(hbox)
    expand.addWidget(row)

    expand = ExpandUI(maya.stringTable[ 'y_xgenArnoldUI.kArnoldCurveSettings'  ])
    self.layout().addWidget( expand )
    self.arnold_expand_curve_settings = expand
    
    self.arnold_minPixelWidth = FloatUI( "custom__arnold_minPixelWidth",
                                maya.stringTable[ 'y_xgenArnoldUI.kMinPixelWidthAnn' ],
                                k_RenderAPIRendererObj, 0.0, 10.0, 0.0, 2.0, maya.stringTable[ 'y_xgenArnoldUI.kminPixelWidth'  ], autoPlayblast=False)
                                
                                
    expand.addWidget(self.arnold_minPixelWidth)
    self.arnold_minPixelWidth.xgAttrChanged.connect( self.xgArnoldRefresh )
    

    # Horizontal layout
    row = QtGui.QWidget()
    hbox = QtGui.QHBoxLayout()
    hbox.setSpacing(3)
    hbox.setContentsMargins(1,1,1,1)
    label = QtGui.QLabel(maya.stringTable[ 'y_xgenArnoldUI.kCurveMode'  ])
    label.setFixedWidth(labelWidth())
    label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
    label.setIndent(10)
    label.setToolTip(maya.stringTable[ 'y_xgenArnoldUI.kSplineModeAnn'  ])
    hbox.addWidget(label)
    self.arnold_curveMode = QtGui.QComboBox()
    self.arnold_curveMode.addItem(maya.stringTable[ 'y_xgenArnoldUI.kCurveModeRibbon'  ], "0" )
    self.arnold_curveMode.addItem(maya.stringTable[ 'y_xgenArnoldUI.kCurveModeThick'  ], "1" )
    self.arnold_curveMode.setToolTip(label.toolTip())
    self.connect(self.arnold_curveMode, QtCore.SIGNAL("activated(int)"), self.xgArnoldCurveModeChanged )
    hbox.addWidget(self.arnold_curveMode)
    filler = QtGui.QWidget()
    hbox.addWidget(filler)
    row.setLayout(hbox)
    expand.addWidget(row)



    expand = ExpandUI(maya.stringTable[ 'y_xgenArnoldUI.kArnoldMotionBlurSetttings'  ])
    self.arnold_expand_motion_blur_settings = expand
    self.layout().addWidget( expand )

    
    # Horizontal layout
    row = QtGui.QWidget()
    hbox = QtGui.QHBoxLayout()
    hbox.setSpacing(3)
    hbox.setContentsMargins(1,1,1,1)
    label = QtGui.QLabel(maya.stringTable[ 'y_xgenArnoldUI.kMotionBlur'  ])
    label.setFixedWidth(labelWidth())
    label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
    label.setIndent(10)
    label.setToolTip(maya.stringTable[ 'y_xgenArnoldUI.kArnoldKeyframeLocationAnn'  ])
    hbox.addWidget(label)
    self.arnold_motion_blur = QtGui.QComboBox()
    self.arnold_motion_blur.addItem(maya.stringTable[ 'y_xgenArnoldUI.kArnoldGlobalSettings' ], "0")
    self.arnold_motion_blur.addItem(maya.stringTable[ 'y_xgenArnoldUI.kArnoldOn' ], "1")
    self.arnold_motion_blur.addItem(maya.stringTable[ 'y_xgenArnoldUI.kArnoldOff' ], "2")
    self.arnold_motion_blur.setToolTip(label.toolTip())
    self.connect(self.arnold_motion_blur, QtCore.SIGNAL("activated(int)"), self.xgArnoldMotionBlurChanged )
    hbox.addWidget(self.arnold_motion_blur)
    filler = QtGui.QWidget()
    hbox.addWidget(filler)
    row.setLayout(hbox)
    expand.addWidget(row)

    
    # Horizontal layout
    row = QtGui.QWidget()
    hbox = QtGui.QHBoxLayout()
    hbox.setSpacing(3)
    hbox.setContentsMargins(1,1,1,1)
    self.arnold_motion_blur_mode_label = QtGui.QLabel(maya.stringTable[ 'y_xgenArnoldUI.kMotionBlurMode'  ])
    self.arnold_motion_blur_mode_label.setFixedWidth(labelWidth())
    self.arnold_motion_blur_mode_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
    self.arnold_motion_blur_mode_label.setIndent(10)
    self.arnold_motion_blur_mode_label.setToolTip(maya.stringTable[ 'y_xgenArnoldUI.kArnoldKeyframeLocationAnn'  ])
    hbox.addWidget(self.arnold_motion_blur_mode_label)
    self.arnold_motion_blur_mode = QtGui.QComboBox()
    self.arnold_motion_blur_mode.addItem(maya.stringTable[ 'y_xgenArnoldUI.kArnoldKeyframeLocationStart' ], "0")
    self.arnold_motion_blur_mode.addItem(maya.stringTable[ 'y_xgenArnoldUI.kArnoldKeyframeLocationMiddle' ], "1")
    self.arnold_motion_blur_mode.addItem(maya.stringTable[ 'y_xgenArnoldUI.kArnoldKeyframeLocationEnd' ], "2")
    self.arnold_motion_blur_mode.setToolTip(label.toolTip())
    self.connect(self.arnold_motion_blur_mode, QtCore.SIGNAL("activated(int)"), self.xgArnoldMotionBlurModeChanged )
    hbox.addWidget(self.arnold_motion_blur_mode)
    filler = QtGui.QWidget()
    hbox.addWidget(filler)
    row.setLayout(hbox)
    expand.addWidget(row)
    
    
    self.arnold_motion_blur_steps = IntegerUI( "custom__arnold_motion_blur_steps",
                                maya.stringTable[ 'y_xgenArnoldUI.kArnoldMotionBlurStepsAnn'  ],
                                k_RenderAPIRendererObj,1,15,maya.stringTable[ 'y_xgenArnoldUI.kArnoldMotionBlurSteps'  ], autoPlayblast=False)
    expand.addWidget(self.arnold_motion_blur_steps)
    self.arnold_motion_blur_steps.xgAttrChanged.connect( self.xgArnoldRefresh )

    self.arnold_motion_blur_factor = FloatUI( "custom__arnold_motion_blur_factor",
                                maya.stringTable[ 'y_xgenArnoldUI.kArnoldMotionBlurFactorAnn'  ],
                                k_RenderAPIRendererObj, 0.0, 100.0 , 0.0, 1.0, maya.stringTable[ 'y_xgenArnoldUI.kArnoldMotionBlurFactor'  ], autoPlayblast=False)
    expand.addWidget(self.arnold_motion_blur_factor)
    self.arnold_motion_blur_factor.xgAttrChanged.connect( self.xgArnoldRefresh )
    

    expand = ExpandUI(maya.stringTable[ 'y_xgenArnoldUI.kArnoldAdvancedSettings'  ])
    self.layout().addWidget( expand )
    self.arnold_expand_advanced_settings = expand
    
    self.arnold_useAuxRenderPatch = CheckBoxUI(maya.stringTable[ 'y_xgenArnoldUI.kUsePatchesPath'  ],"custom__arnold_useAuxRenderPatch",
                                    maya.stringTable[ 'y_xgenArnoldUI.kUsePatchesPathAnn'  ],k_RenderAPIRendererObj)

    expand.addWidget(self.arnold_useAuxRenderPatch)
    self.connect(self.arnold_useAuxRenderPatch.boxValue[0],
                 QtCore.SIGNAL("clicked(bool)"), self.xgArnoldUseAuxPatchesChanged)
    
    self.arnold_auxRenderPatch = BrowseUI( "custom__arnold_auxRenderPatch",
                            maya.stringTable[ 'y_xgenArnoldUI.kPatchesPathAnn' ],
                            k_RenderAPIRendererObj, "*.abc", "in", maya.stringTable[ 'y_xgenArnoldUI.kPatchesPath' ])
                                
                                
    expand.addWidget(self.arnold_auxRenderPatch)
    self.connect(self.arnold_auxRenderPatch.textValue, QtCore.SIGNAL("textChanged(const QString&)"), self.xgArnoldPatchesChanged )

    # Register the Arnold renderer in the method combo box
    self.addRenderer("Arnold Renderer")
    global k_RenderAPIRendererInit
    k_RenderAPIRendererInit = True

# RenderAPIRendererTabUIRefresh callback
# Called at the end of RenderAPIRendererTab.refresh()
def xgArnoldRefresh(selfid):

    # Init the UI if we missed the init callback (load after xgenToolkit plugin).
    if not k_RenderAPIRendererInit:
        xgArnoldUI(selfid)

        
    self = castSelf(selfid)

    vis = self.renderer.currentText()=="Arnold Renderer"
    self.arnold_expand_settings.setVisible(vis)
    self.arnold_expand_motion_blur_settings.setVisible(vis)
    self.arnold_expand_curve_settings.setVisible(vis)
    self.arnold_expand_advanced_settings.setVisible(vis)

    # Declare the Arnold custom parameters
    self.declareCustomAttr( 'arnold_rendermode', "0" )
    self.declareCustomAttr( 'arnold_curveMode', "0" )
    self.declareCustomAttr( 'arnold_minPixelWidth', "0.0" )
    self.declareCustomAttr( 'arnold_motion_blur', "0" )
    self.declareCustomAttr( 'arnold_motion_blur_mode', "1" )
    self.declareCustomAttr( 'arnold_motion_blur_steps', "2" )
    self.declareCustomAttr( 'arnold_motion_blur_factor', "0.5" )
    self.declareCustomAttr( 'arnold_useAuxRenderPatch', "0" )
    self.declareCustomAttr( 'arnold_auxRenderPatch', "0" )
    
    # Get all the values
    rendermode = int(self.getCustomAttr( "arnold_rendermode" ))
    curvTyp = int (self.getCustomAttr( "arnold_curveMode"))
    minPixW = float (self.getCustomAttr( "arnold_minPixelWidth"))
    mb = int(self.getCustomAttr( "arnold_motion_blur" ))
    mbo = mb is 1
    mb_mode = int(self.getCustomAttr( "arnold_motion_blur_mode" ))
    mb_steps = int(self.getCustomAttr( "arnold_motion_blur_steps" ))
    mb_factor = float(self.getCustomAttr( "arnold_motion_blur_factor" ))
    useAuxRenderPatch = self.getCustomAttr( "arnold_useAuxRenderPatch" ) != "0"
    auxRenderPatch = str(self.getCustomAttr( "arnold_auxRenderPatch" ))
    if auxRenderPatch == "0":
        auxRenderPatch = ""

    # Update the UI
    de = xgg.DescriptionEditor

    self.arnold_rendermode.setCurrentIndex( rendermode )
    self.arnold_curveMode.setCurrentIndex( curvTyp )
    
    self.arnold_minPixelWidth.refresh()
    self.arnold_motion_blur.setCurrentIndex( mb )
    self.arnold_motion_blur_mode.setCurrentIndex( mb_mode )
    self.arnold_motion_blur_steps.refresh()
    self.arnold_motion_blur_factor.refresh()


    self.arnold_motion_blur_mode.setEnabled( mbo )
    self.arnold_motion_blur_mode_label.setEnabled( mbo )
    self.arnold_motion_blur_steps.setEnabled( mbo )
    self.arnold_motion_blur_factor.setEnabled( mbo )
    
    self.arnold_useAuxRenderPatch.refresh()
    self.arnold_auxRenderPatch.refresh()
    self.arnold_auxRenderPatch.setEnabled(useAuxRenderPatch)
    
    pal = de.currentPalette()
    desc = de.currentDescription()

    # Update the exposed geoshader parameters
    if xgg.Maya:
        import maya.cmds as cmds
        descShape = cmds.listRelatives( pal + "|" + desc, shapes=True )

        nExistsName = pal + "|" + desc + "|" + descShape[0]
        nExists = cmds.objExists( nExistsName )
        if nExists:
            cmds.setAttr( nExistsName + ".aiMode", curvTyp )
            cmds.setAttr( nExistsName + ".aiMinPixelWidth", minPixW )
            cmds.setAttr( nExistsName + ".motion_blur_override", mb )
            cmds.setAttr( nExistsName + ".motion_blur_mode", mb_mode )
            cmds.setAttr( nExistsName + ".motion_blur_steps", mb_steps )
            cmds.setAttr( nExistsName + ".motion_blur_factor", mb_factor )
            cmds.setAttr( nExistsName + ".aiUseAuxRenderPatch", useAuxRenderPatch )
            cmds.setAttr( nExistsName + ".aiAuxRenderPatch", auxRenderPatch, type="string")
            if rendermode == 0:
                cmds.setAttr( nExistsName + ".render_mode", 1 ) #  live = 1
            else:
                cmds.setAttr( nExistsName + ".render_mode", 3 ) #  batch = 3
        else:
            print "Couldn't find Description Shape!"

# Callback after description creation to switch to Arnold render
def xgArnoldOnCreateDescription( param ):
    params = str(param).split(',')
    if len(params)==2:
        xg.setAttr( "renderer", "Arnold Renderer", params[1], params[0], "RendermanRenderer" )

def xgArnoldCurveModeChanged(self,index):
    self.setCustomAttr( "arnold_curveMode", str(index) )
    self.xgArnoldRefresh()

def xgArnoldRenderModeChanged(self,index):
    self.setCustomAttr( "arnold_rendermode", str(index) )
    self.xgArnoldRefresh()

def xgArnoldMotionBlurModeChanged(self,index):
    self.setCustomAttr( "arnold_motion_blur_mode", str(index) )
    self.xgArnoldRefresh()

def xgArnoldMotionBlurChanged(self,index):
    self.setCustomAttr( "arnold_motion_blur", str(index) )
    self.xgArnoldRefresh()

def xgArnoldPatchesChanged(self, data):
    self.setCustomAttr( "arnold_auxRenderPatch", str(data) )
    self.xgArnoldRefresh()

def xgArnoldUseAuxPatchesChanged(self, state):
    self.setCustomAttr( "arnold_useAuxRenderPatch", str(int(state)) )
    if state:
        self.arnold_auxRenderPatch.setEnabled(True)
    else:
        self.arnold_auxRenderPatch.setEnabled(False)
    self.xgArnoldRefresh()
