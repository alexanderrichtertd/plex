import pymel.core as pm
import mtoa.ui.ae.templates as templates
from mtoa.ui.ae.templates import AttributeTemplate, registerTranslatorUI

## we want to add this directory to the path so we can use the extra xgenArnoldUI  files
import os
import sys
localPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(localPath)

import xgenm as xg

class xgmDescriptionTemplate(templates.ShapeTranslatorTemplate):
    def setup(self):
        self.commonShapeAttributes()
        self.addSeparator()
        self.addControl("renderMode", label="Render Mode")
        self.addSeparator()
        self.addControl("motionBlurOverride", label="Motion Blur Override")
        self.addControl("motionBlurMode", label="Motion Blur Mode")
        self.addControl("motionBlurSteps", label="Motion_Blur_Steps")
        self.addControl("motionBlurFactor", label="Motion Blur Factor")
        self.addControl("motionBlurMult", label="Motion Blur Multiplier")
        self.addSeparator()
        self.addControl("aiMinPixelWidth", label="Min Pixel Width")
        self.addControl("aiMode", label= "Curve Mode")
        self.addControl("aiUseAuxRenderPatch", label = "Use Aux Render Patch")
        self.addControl("aiAuxRenderPatch", label= "Auxilary Render Patch")
        

templates.registerTranslatorUI(xgmDescriptionTemplate, "xgmDescription", "xgenTranslator")

# these  are used to build the  "renderer"  callbacks to slot arnold  settings into the  xgen GUI.   the values of these controls 
# are stored on  each description node and can be parsed from there by the translator.
# this is mainly to make  arnold fit into the   XGen workflow better. 

xg.registerCallback( "RenderAPIRendererTabUIInit", "xgenArnoldUI.xgArnoldUI" )
xg.registerCallback( "RenderAPIRendererTabUIRefresh", "xgenArnoldUI.xgArnoldRefresh" )
if xg.xgGlobal.DescriptionEditor is not None:
    xg.xgGlobal.DescriptionEditor.refresh( "Full" )
