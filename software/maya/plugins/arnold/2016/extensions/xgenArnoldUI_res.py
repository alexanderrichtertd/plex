import maya


# control strings

maya.stringTable['y_xgenArnoldUI.kArnoldSettings'] = u'Arnold Settings'

maya.stringTable['y_xgenArnoldUI.kArnoldRenderMode'] = u'Render Mode'
maya.stringTable['y_xgenArnoldUI.kRenderModeLive'] = u'Live'
maya.stringTable['y_xgenArnoldUI.kRenderModeBatch'] = u'Batch Render'

maya.stringTable['y_xgenArnoldUI.kArnoldEnableMotionBlur'] = u'Motion Blur'

maya.stringTable['y_xgenArnoldUI.kArnoldOverrideMotionBlur'] = u'Override Motion Blur'

maya.stringTable['y_xgenArnoldUI.kMotionBlur'] = u'Motion Blur'
maya.stringTable['y_xgenArnoldUI.kArnoldGlobalSettings'] = u'Use Global Settings'
maya.stringTable['y_xgenArnoldUI.kArnoldOn'] = u'On'
maya.stringTable['y_xgenArnoldUI.kArnoldOff'] = u'Off'

maya.stringTable['y_xgenArnoldUI.kMotionBlurMode'] = u'Position'
maya.stringTable['y_xgenArnoldUI.kArnoldKeyframeLocationStart'] = u'Start on Frame'
maya.stringTable['y_xgenArnoldUI.kArnoldKeyframeLocationMiddle'] = u'Center on Frame'
maya.stringTable['y_xgenArnoldUI.kArnoldKeyframeLocationEnd'] = u'End on Frame'

maya.stringTable['y_xgenArnoldUI.kArnoldMotionBlurSteps'] = u'Keys'
maya.stringTable['y_xgenArnoldUI.kArnoldMotionBlurFactor'] = u'Length'
maya.stringTable['y_xgenArnoldUI.kArnoldMotionBlurMultiplier'] = u'Multiplier'

maya.stringTable['y_xgenArnoldUI.kTools'] = u'Tools'
maya.stringTable['y_xgenArnoldUI.kArnoldApplyHair'] = u'Apply Hair Shader'


maya.stringTable['y_xgenArnoldUI.kArnoldCurveSettings'] = u'Arnold Curve Settings'
maya.stringTable['y_xgenArnoldUI.kminPixelWidth'] = u'Min Pixel Width'
maya.stringTable['y_xgenArnoldUI.kCurveMode'] = u'Mode'
maya.stringTable['y_xgenArnoldUI.kCurveModeRibbon'] = u'Ribbon'
maya.stringTable['y_xgenArnoldUI.kCurveModeThick'] = u'Thick'
maya.stringTable['y_xgenArnoldUI.kCurveModeOriented'] = u'Oriented'
maya.stringTable['y_xgenArnoldUI.kCurveModeFlat'] = u'Flat'

maya.stringTable['y_xgenArnoldUI.kArnoldAdvancedSettings'] = u'Arnold Advanced Settings'
maya.stringTable['y_xgenArnoldUI.kUsePatchesPath'] = u'Use Aux Render Patch'
maya.stringTable['y_xgenArnoldUI.kPatchesPath'] = u'Auxilary Render Patch'




# annotations
maya.stringTable['y_xgenArnoldUI.kArnoldMotionBlurSetttings'] = u'Arnold Motion Blur Settings'
maya.stringTable['y_xgenArnoldUI.kArnoldApplyHairAnn'] = u"Apply default arnold XGen Hair Shader to the current Description.\nThe shader reacts to 'root_color', 'tip_color' and 'back_color' XGen custom shader parameters."
maya.stringTable['y_xgenArnoldUI.kArnoldMotionBlurMultiplierAnn'] = u'Motion Factor multiplies the computed motion vectors.\nUse it to attenuate or accentuate the motion blur effect.'
maya.stringTable['y_xgenArnoldUI.kSplineModeAnn'] = u'Curve Primitive can be rendered as "ribbon", "oriented" or "thick".\nWhen "ribbon" is selected, "Face Camera" in Primitive Attributes will determine \nif "ribbon" or "oriented" will be used.'
maya.stringTable['y_xgenArnoldUI.kArnoldRenderModeAnn'] = u"'Live' allows XGen to query patches and guide animation directly from Maya.\nThis mode doesn't support Motion Blur and will try to reuse information the preview generated.\n\n'Batch Render' mode will always read geometry and animation from files.\n'Batch Render' mode is always on when doing a Batch Render.\nYou must first export the patches and guide animation to caches.\nUse this mode to make sure your caches are properly exported before doing a Batch Render."
maya.stringTable['y_xgenArnoldUI.kArnoldKeyframeLocationAnn'] = u'The motion offset when calculating motion blur.'
maya.stringTable['y_xgenArnoldUI.kArnoldEnableMotionBlurAnn'] = u'Enable Motion Blur.\nTo compute the motion vectors, XGen needs to sample animated geometry and guide animations at multiple times.\nMake sure you export everything like for a Batch render.'
maya.stringTable['y_xgenArnoldUI.kArnoldOverrideMotionBlurAnn'] = u'Override the scene Motion Blur values.'
maya.stringTable['y_xgenArnoldUI.kParametricSubdivisionsAnn'] = u'For Linear, defines the number of segments to use between control points.\nFor Cubic, defines a recursive number of subdivisions between control points.'
maya.stringTable['y_xgenArnoldUI.kArnoldGeoshadersAnn'] = u'Setup a arnold geometry shader used to generate the XGen render time geometry.\nBy default, the setup is automatically done when a new description is created.\nYou can perform the setup manually for the current Description by clicking the Setup button.'
maya.stringTable['y_xgenArnoldUI.kArnoldMotionBlurFactorAnn'] = u'Motion Blur time interval.'
maya.stringTable['y_xgenArnoldUI.kSubPixelSizeAnn'] = u"Subdivides geometry until edges hit a maximal length in pixel size.\nIt is view and resolution dependent.\nValues below 1.0 will split the geometry within the same pixel.\nThis is usefull to render very thin hair with tube normals and a high number of samples.\nValues above 1.0 will produce geometry that don't look perfectly smooth.\nIt's usefull to optimize render time if the geometry is far away from the camera."
maya.stringTable['y_xgenArnoldUI.kApproximationMethodAnn'] = u"Type of arnold approximation to use when subdividing render time hair bezier curves or card NURBS patches.\n'No Approximation' won't subdivide the render time geometry.\n'Parametric Approximation' subdivides render time geometry a number of times between control points.\n'Fine Approximation' subdivides until edges hit a given length in pixel size. It's view dependent."
maya.stringTable['y_xgenArnoldUI.kArnoldMotionBlurStepsAnn'] = u'Defines the number of times the XGen geometry is evaluated to produced non-linear motion blur.\nA lower value makes the render go faster but the motion blur effect might not capture the rotation of teh primitives.'
maya.stringTable['y_xgenArnoldUI.kMinPixelWidthAnn'] = u'Arnold Minimum pixel width for curves'
maya.stringTable['y_xgenArnoldUI.kUsePatchesPathAnn'] = u'Override the Patch .abc file'
maya.stringTable['y_xgenArnoldUI.kPatchesPathAnn'] = u'Override the Patch .abc file'
