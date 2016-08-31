'''
 Copyright (C) 1997-2010 Autodesk, Inc., and/or its licensors.
 All rights reserved.

 The coded instructions, statements, computer programs, and/or related
 material (collectively the "Data") in these files contain unpublished
 information proprietary to Autodesk, Inc. ("Autodesk") and/or its licensors,
 which is protected by U.S. and Canadian federal copyright law and by
 international treaties.

 The Data is provided for use exclusively by You. You have the right to use,
 modify, and incorporate this Data into other products for purposes authorized
 by the Autodesk software license agreement, without fee.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. AUTODESK
 DOES NOT MAKE AND HEREBY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES
 INCLUDING, BUT NOT LIMITED TO, THE WARRANTIES OF NON-INFRINGEMENT,
 MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR ARISING FROM A COURSE
 OF DEALING, USAGE, OR TRADE PRACTICE. IN NO EVENT WILL AUTODESK AND/OR ITS
 LICENSORS BE LIABLE FOR ANY LOST REVENUES, DATA, OR PROFITS, OR SPECIAL,
 DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES, EVEN IF AUTODESK AND/OR ITS
 LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY OR PROBABILITY OF SUCH DAMAGES.
'''

import os
import math
import re

import pymel.core as pm

import mtoa.utils as utils
from mtoa.ui.ae.templates import createTranslatorMenu
from mtoa.callbacks import *
import mtoa.core as core
import mtoa.aovs as aovs

from maya.app.stereo import stereoCameraRig

MENU_SEPARATOR = ('-', None)

PLE_MAX_Y =  768
PLE_MAX_X = 1024

# Use global variables because MEL do not have a concept of enum or
# constants. These values are used to define the action to take in
# the renderable camera menus.
CAM_MENU_CAMERA     = 1
CAM_MENU_STEREOPAIR = 2
CAM_MENU_ADD        = 3
CAM_MENU_IGNORE     = 4




def _listStereoRigs():
    return [pm.nt.DagNode(x) for x in stereoCameraRig.listRigs(True) or []]
def _isMono(camera):
    return not stereoCameraRig.rigRoot(camera.name())

def getMultiCameraChildren(camera):
    cameras = []
    if pm.pluginInfo("stereoCamera", query=True, loaded=True):
        import maya.app.stereo.stereoCameraRig as stereoCameraRig
        if stereoCameraRig.isRigRoot(str(camera)):
            # camera.leftCam.get() does not work on Maya2011
            try:
                result = camera.leftCam.inputs()[0]
                if result:
                    cameras.append(result)
                    result = camera.rightCam.inputs()[0]
                    if result:
                        cameras.append(result)
            except IndexError:
                pm.warning("Stereo camera %s is missing required connections" % camera)
    return cameras

def fileTypeToExtension(fileType):
   if (fileType == "jpeg") :
       return "jpg"
   elif (fileType == "tiff") :
       return "tif"
   else :
       return fileType


# ----------------------------------------------------------------------------
# Utility procedures used by other procedures in this file.
# Must be used to account for multiple instances of the same tab.
#
def setParentToArnoldCommonTab():
    # First set the parent to the correct tab layout.
    # Account for the special "all renderers" master layer layout
    # when we are using render layers
    if pm.mel.isDisplayingAllRendererTabs():
        renderer = pm.melGlobals.get('gMasterLayerRendererName', 'string')
    else:
        renderer = utils.currentRenderer()

    tabLayout = pm.mel.rendererTabLayoutName(renderer)
    pm.setParent(tabLayout)

    # Now set the parent to the correct column layout
    pm.setParent('commonTabColumn')

def createArnoldTargetFilePreview():

    oldParent = pm.setParent(query=True)

    pm.columnLayout('targetFilePreview', adjustableColumn=True)

    pm.text('exampleText0',
              align="left",
              font="smallBoldLabelFont",
              label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kPath"))

    pm.text('exampleArnoldText1',
              align="left",
              font="smallBoldLabelFont",
              label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kFileName"))

    pm.text('exampleArnoldText2',
              align="left",
              font="smallBoldLabelFont",
              label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kTo"))

    pm.text('exampleText3',
              align="left",
              font="smallBoldLabelFont",
              label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kImageSize"))

    pm.setParent(oldParent)

    # This target file preview is affected by a number of attributes.
    # If any of those attributes change, this preview needs to be updated.
    #
    # Here we fill an array with the names of all of the current renderer's
    # attributes which affect the naming of the target file.
    #
    attrArray = ["defaultRenderGlobals.imageFilePrefix",
                 "defaultRenderGlobals.outFormatControl",
                 "defaultRenderGlobals.imfPluginKey",
                 "defaultRenderGlobals.outFormatExt",
                 "defaultRenderGlobals.animation",
                 "defaultRenderGlobals.byFrameStep",
                 "defaultRenderGlobals.extensionPadding",
                 "defaultRenderGlobals.startFrame",
                 "defaultRenderGlobals.endFrame",
                 "defaultRenderGlobals.modifyExtension",
                 "defaultRenderGlobals.startExtension",
                 "defaultRenderGlobals.byExtension",
                 "defaultRenderGlobals.periodInExt",
                 "defaultResolution.fields",
                 "defaultRenderGlobals.fieldExtControl",
                 "defaultRenderGlobals.oddFieldExt",
                 "defaultRenderGlobals.evenFieldExt",
                 "defaultRenderGlobals.putFrameBeforeExt",
                 "defaultResolution.width",
                 "defaultResolution.height",
                 "defaultResolution.dotsPerInch",
                 "defaultResolution.imageSizeUnits",
                 "defaultResolution.pixelDensityUnits",
                 "defaultRenderGlobals.renderVersion",
                 "defaultArnoldRenderOptions.aovMode",
                 "defaultArnoldDriver.mergeAOVs"]

    # Now we establish scriptJobs to invoke the procedure which updates the
    # target file preview when any of the above attributes change.

    for attr in attrArray:
        pm.scriptJob(attributeChange = (attr,updateArnoldTargetFilePreview),
                        parent='targetFilePreview')


    pm.scriptJob(event = ('workspaceChanged',
                            updateArnoldTargetFilePreview),
                            parent='targetFilePreview')

    updateArnoldTargetFilePreview()

def updateArnoldTargetFilePreview(*args):
    '''
    Description:
    This procedure is called any time an attribute change occurs which
       would affect the name(s) of the file(s) that would be created when the
       user performs a render.
    This procedure updates the lines of text in the General tab that allow
    the user to see what files are going to be created when they render.
    '''

    oldParent = pm.setParent(query=True)

    if pm.mel.isDisplayingAllRendererTabs():
        renderer = pm.melGlobals.get('gMasterLayerRendererName', 'string')
    else:
        renderer = utils.currentRenderer()

    tabLayout = pm.mel.rendererTabLayoutName(renderer)
    if pm.tabLayout(tabLayout, exists=True):
        pm.setParent(tabLayout)

    #
    # Update the File Name portion of the preview.
    #

    title1 = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kNewFileName")
    title2 = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kNewTo")

    kwargs = {}
    tokens = {}
    try:
        prefix = pm.getAttr('defaultRenderGlobals.imageFilePrefix')
    except:
        pass
    else:
        if prefix:
            kwargs['path'] = prefix

    kwargs['createDirectory'] = False
    kwargs['leaveUnmatchedTokens'] = True
    aovsEnabled = pm.getAttr('defaultArnoldRenderOptions.aovMode') and aovs.getAOVs(enabled=True, exclude=['beauty', 'RGBA', 'RGB'])
    if aovsEnabled:
        tokens['RenderPass'] = '<RenderPass>'
    kwargs['strictAOVs'] = not (aovsEnabled and not pm.getAttr('defaultArnoldDriver.mergeAOVs'))
    tokens['Frame'] = pm.getAttr('defaultRenderGlobals.startFrame')
    first = utils.getFileName('relative', tokens, **kwargs)

    if os.path.isabs(first):
        # the entered path is absolute so there is no prepended path
        pm.text('exampleText0', edit=True, label='')
    else:
        #
        # Update the Path portion of the preview.
        #
    
        # get the project's image directory
        #
        imgDir = pm.workspace(fileRuleEntry="images")
        fullPath = pm.workspace(expandName=imgDir)
        pathLabel = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kNewPath")
        path = pm.format(pathLabel, s=fullPath)
        pm.text('exampleText0', edit=True, label=path)

    pm.text('exampleArnoldText1', edit=True, label=pm.format(title1, s=first))
    settings = pm.api.MCommonRenderSettingsData()
    pm.api.MRenderUtil.getCommonRenderSettings(settings)
    if settings.isAnimated():
        tokens['Frame'] = pm.getAttr('defaultRenderGlobals.endFrame')
        last = utils.getFileName('relative', tokens, **kwargs)
        pm.text('exampleArnoldText2', edit=True, label=pm.format(title2, s=last))
    else:
        pm.text('exampleArnoldText2', edit=True, label="")

    #
    # Update the Image Size portion of the preview.
    #

    # Get attributes
    #
    width = pm.getAttr('defaultResolution.width')
    height = pm.getAttr('defaultResolution.height')
    dpi = pm.getAttr('defaultResolution.dotsPerInch')
    sizeUnits = pm.getAttr('defaultResolution.imageSizeUnits')
    resUnits = pm.getAttr('defaultResolution.pixelDensityUnits')

    # Default measurement units to inches if pixels selected
    if sizeUnits == 0:
        sizeUnits = 1


    gMeasurementUnitsNames = pm.melGlobals.get('gMeasurementUnitsNames', 'string[]')
    gResolutionUnitsNames = pm.melGlobals.get('gResolutionUnitsNames', 'string[]')

    if not gResolutionUnitsNames:
        pm.mel.source("resolutionFormats.mel")
        gMeasurementUnitsNames = pm.melGlobals['gMeasurementUnitsNames']
        gResolutionUnitsNames = pm.melGlobals['gResolutionUnitsNames']

    # Convert from pixels to the correct measurement units
    docWidth = pm.mel.convertMeasurement(pm.mel.convertPixelsToInches(width, dpi), "inches", gMeasurementUnitsNames[sizeUnits])

    docHeight = pm.mel.convertMeasurement(pm.mel.convertPixelsToInches(height, dpi), "inches", gMeasurementUnitsNames[sizeUnits])

    # Convert from DPI to the correct resolution units
    res = pm.mel.convertResolutionMeasurement(dpi, "pixels/inch", gResolutionUnitsNames[resUnits])

    # Convert to strings, rounding applicable floats to 1 decimal place
    imW = width
    imH = height

    docW = pm.mel.setDecimalPrecision(docWidth, 1.0)
    docH = pm.mel.setDecimalPrecision(docHeight, 1.0)
    units = pm.mel.resolutionFormats_melToUI(gMeasurementUnitsNames[sizeUnits])
    resVal = pm.mel.setDecimalPrecision(res, 1.0)

    resUnitsStr = pm.mel.resolutionFormats_melToUI(gResolutionUnitsNames[resUnits])

    imageLabel = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kNewImageSize")
    imageSizeString = pm.format(imageLabel, s=(imW, imH, docW, docH, units, resVal, resUnitsStr))

    pm.text('exampleText3', edit=True, label=imageSizeString)

    pm.setParent(oldParent)


def insertArnoldKeywordMenuCallback(token):

    setParentToArnoldCommonTab()

    # if not yet set, then replace name with token
    prefix = pm.textFieldGrp('mayaSoftwareFileName', query=True, text=True)
    if prefix == pm.mel.eval('uiRes("m_createMayaSoftwareCommonGlobalsTab.kNotSetUsingFilename")'):
        pm.textFieldGrp('mayaSoftwareFileName', e=True, text=token, forceChangeCommand=True)
    else:
        pm.textFieldGrp('mayaSoftwareFileName', e=True, insertText=token, forceChangeCommand=True)


def createArnoldInsertKeywordMenu(parent):

    pm.popupMenu(parent, edit=True, deleteAllItems=True)

    pm.setParent(parent, menu=True)

    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kFileNameKeywords"), enable=0)
    pm.menuItem(divider=True)
    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kKeywordScene"),
                  command=pm.Callback(insertArnoldKeywordMenuCallback, "<Scene>"))
    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kKeywordLayer"),
                  command=pm.Callback(insertArnoldKeywordMenuCallback, "<RenderLayer>"))
    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kKeywordCamera"),
                  command=pm.Callback(insertArnoldKeywordMenuCallback, "<Camera>"))
    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kKeywordRPFG"),
                  command=pm.Callback(insertArnoldKeywordMenuCallback, "<RenderPassFileGroup>"))
    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kKeywordRenderPass"),
                  command=pm.Callback(insertArnoldKeywordMenuCallback, "<RenderPass>"))
    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kKeywordRenderPassType"),
                  command=pm.Callback(insertArnoldKeywordMenuCallback, "<RenderPassType>"))
    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kKeywordExtension"),
                  command=pm.Callback(insertArnoldKeywordMenuCallback, "<Extension>"))
    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kKeywordVersion"),
                  command=pm.Callback(insertArnoldKeywordMenuCallback, "<Version>"))
    date = pm.date(format="YY_MM_DD")
    pm.menuItem(label=(pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kKeywordDate") + date),
                  command=pm.Callback(insertArnoldKeywordMenuCallback,  date))
    time = pm.date(format="hh-mm-ss")
    pm.menuItem(label=(pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kKeywordTime") + time),
                  command=pm.Callback(insertArnoldKeywordMenuCallback, time))

# ----------------------------------------------------------------------------
# Code to create and update the Image File Output frame
#
def createArnoldFileNamePrefixControl():

    # Create the control
    #
    pm.textFieldGrp('mayaSoftwareFileName',
                     label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kFileNamePrefix"),
                     annotation=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kFileNamePrefixAnn"))

    popup = pm.popupMenu(parent='mayaSoftwareFileName|field')
    pm.popupMenu(popup, edit=True, postMenuCommand=Callback(createArnoldInsertKeywordMenu, popup))

    # connect the label, so we can change its color
    pm.connectControl('mayaSoftwareFileName', 'defaultRenderGlobals.imageFilePrefix', index=1)
    pm.connectControl('mayaSoftwareFileName', 'defaultRenderGlobals.imageFilePrefix', index=2)

    # Create a scriptJob which will update the control when the value of the
    # attribute it represents is changed.
    #
    pm.scriptJob(parent='mayaSoftwareFileName',
                 attributeChange=("defaultRenderGlobals.imageFilePrefix", updateArnoldFileNamePrefixControl))


def changeArnoldFileNamePrefix(*args):

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    prefix = pm.textFieldGrp('mayaSoftwareFileName', query=True, text=True)
    prefixAttr = "defaultRenderGlobals.imageFilePrefix"

    if prefix != pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kNotSetUsingFilename") and pm.mel.isValidFileNamePrefix(prefix):
        # The user has set the prefix to something, and it is a valid name, so
        # we will set the value of the corresponding attribute.
        #
        pm.setAttr(prefixAttr, prefix, type="string")
    else:
        # The user has set the prefix to an invalid value. We will refresh the
        # UI to show the current value, which has not been changed.
        #
        updateArnoldFileNamePrefixControl()

    pm.setParent(oldParent)

def updateArnoldFileNamePrefixControl(*args):
    #
    #  Procedure Name:
    #      changeFileName
    #
    #  Description:
    #    This procedure is called when the user changes the file
    #    prefix.  It sets the internal representation of the prefix
    #    and then updates the example to show the changes.
    #
    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    prefix = pm.getAttr("defaultRenderGlobals.imageFilePrefix")

    if prefix:
        pm.textFieldGrp('mayaSoftwareFileName', edit=True, text=prefix)
    else:
        pm.textFieldGrp('mayaSoftwareFileName',
                    edit=True,
                    text=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kNotSetUsingFilename"))

    pm.setParent(oldParent)


def createArnoldFileNameFormatControl():

    pm.optionMenuGrp('extMenu',
                    label= pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kFrameAnimationExt"),
                    changeCommand=changeArnoldFileNameFormat)


    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kExt1"))
    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kExt2"))
    pm.menuItem('mayaSoftwareNameDotFrameDotExtension', label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kExt3"))
    pm.menuItem('mayaSoftwareNameDotExtensionDotFrame', label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kExt4"))
    pm.menuItem('mayaSoftwareNameDotFrame', label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kExt5"))
    pm.menuItem('mayaSoftwareFrameDotExtension', label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kExt6"))
    pm.menuItem('mayaSoftwareNameUnderFrameDotExtension', label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kExt7"))
    pm.menuItem('mayaSoftwareMultiFrame', label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kExt8"))
    pm.menuItem('mayaSoftwareMultiFrameDotExtension', label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kExt9"))

    attrArray=[]
    attrArray.append("defaultRenderGlobals.outFormatControl")
    attrArray.append("defaultRenderGlobals.animation")
    attrArray.append("defaultRenderGlobals.periodInExt")
    attrArray.append("defaultRenderGlobals.putFrameBeforeExt")
    attrArray.append("defaultRenderGlobals.imageFormat")
    attrArray.append("defaultRenderGlobals.imfPluginKey")

    # Now we establish scriptJobs to invoke the procedure which updates the
    # file name format control when any of the above attributes change.
    #
    for attr in attrArray:
        pm.scriptJob(attributeChange=(attr, updateArnoldFileNameFormatControl),
                     parent='extMenu')


def changeArnoldFileNameFormat(*args):
    '''
    Procedure Name:
        changeExtension
    
    Description:
      This procedure is called when the user changes the format
      of the file extension.  It sets the internal representation
      and then updates the example to show the changes.
    
    Note:
      Although the user sees only one control to change the
      extension, it actually affects more than one value.
    '''
    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    item = pm.optionMenuGrp('extMenu', q=True, sl=True)

    pm.mel.setMayaSoftwareFrameExt(fileTypeToExtension(item), 0)

    # Update the batch render window if it exists
    #
    if pm.mel.exists("updateBatchRenderWindowTitle"):
        pm.mel.updateBatchRenderWindowTitle()

    pm.setParent(oldParent)

def updateArnoldFileNameFormatControl(*args):

    oldParent = pm.setParent(query=True)

    setParentToArnoldCommonTab()

    frameBeforeExt  = pm.getAttr("defaultRenderGlobals.putFrameBeforeExt")
    useAnim         = pm.getAttr("defaultRenderGlobals.animation")
    imageUse        = pm.getAttr("defaultRenderGlobals.outFormatControl")
    period          = pm.getAttr("defaultRenderGlobals.periodInExt")

    if pm.getAttr('defaultRenderGlobals.imageFormat') == 31: # Check if PSD format
        multiframe = 0
        psdFormat = 1
    else:
        multiframe = pm.mel.multiframeFormat(pm.mel.getImfImageType())
        psdFormat = 0
    activeMenuItem = 0

    # Update Frame/Animation Ext menuItems and enable only the relevant ones.
    #
    notMultiFrameOrPsd = not multiframe or psdFormat

    pm.menuItem('mayaSoftwareNameDotFrameDotExtension', edit=True, enable=notMultiFrameOrPsd)
    pm.menuItem('mayaSoftwareNameDotExtensionDotFrame', edit=True, enable=notMultiFrameOrPsd)
    pm.menuItem('mayaSoftwareNameDotFrame', edit=True, enable=notMultiFrameOrPsd)
    pm.menuItem('mayaSoftwareFrameDotExtension', edit=True, enable=notMultiFrameOrPsd)
    pm.menuItem('mayaSoftwareNameUnderFrameDotExtension', edit=True, enable=notMultiFrameOrPsd)
    pm.menuItem('mayaSoftwareMultiFrame',edit=True, enable=multiframe)
    pm.menuItem('mayaSoftwareMultiFrameDotExtension',edit=True, enable=multiframe)

    if multiframe:
        if useAnim:
            if imageUse == 1:     # no extension
                activeMenuItem = 8
            else:
                activeMenuItem = 9
        else:
            if imageUse == 1:     # no extension
                activeMenuItem = 1
            else:
                activeMenuItem = 2
    else:
        if useAnim:
            if imageUse == 1:
                activeMenuItem = 5
            else:
                if frameBeforeExt == 0:
                    activeMenuItem = 4
                else:
                    if period == 1: # period in extension
                        activeMenuItem = 3
                    elif period == 2: # underscore in extension
                        activeMenuItem = 7
                    else: # $period == 0
                        activeMenuItem = 6
        else:
            if imageUse == 1:
                activeMenuItem = 1
            else:
                activeMenuItem = 2

    pm.optionMenuGrp('extMenu', edit=True, sl=activeMenuItem)

    # Also update the frame number controls to enable/disable them according
    # to whether or not they are being used.
    #
    updateArnoldFrameNumberControls()

    pm.setParent(oldParent)

def createArnoldUseCustomExtensionControl():

    pm.checkBoxGrp('useCustomExtensionCtrl',
                   numberOfCheckBoxes=1,
                   label='',
                   label1=pm.mel.uiRes('m_createMayaSoftwareCommonGlobalsTab.kUseCustomExtension'),
                   cc=changeArnoldUseCustomExtension)

    pm.scriptJob(parent='useCustomExtensionCtrl',
                 attributeChange=("defaultRenderGlobals.outFormatControl", updateArnoldUseCustomExtensionControl))

def updateArnoldUseCustomExtensionControl():
    
    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab();
    useImage = pm.getAttr('defaultRenderGlobals.outFormatControl') !=  1

    pm.checkBoxGrp('useCustomExtensionCtrl',
                   e=True,
                   value1=cmds.getAttr('defaultRenderGlobals.outFormatControl') == 2,
                   enable=useImage)

    pm.setParent(oldParent)

def changeArnoldUseCustomExtension(*args, **kwargs):
    #  Procedure Name:
    #      changeCustomExtensionCheck
    #
    #  Description:
    #		This procedure is called when the user turns the custom
    #		extension on or off.  It sets the internal representation
    #		and then updates the example to show the changes.
    #
    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab();
    isOn = pm.checkBoxGrp('useCustomExtensionCtrl', query=True, value1=True)
    if isOn:
        pm.setAttr('defaultRenderGlobals.outFormatControl', 2)
    else:
        # We have to figure out if there should be an extension
        # at all or not.
        #
        item = pm.optionMenuGrp('extMenu', query=True, select=True)
        
        if item == 1 or item == 5:
            pm.setAttr('defaultRenderGlobals.outFormatControl', 1)
        else:
            pm.setAttr('defaultRenderGlobals.outFormatControl', 0)
        
        pm.setParent(oldParent)

def createArnoldCustomExtensionControl():

    pm.attrControlGrp('userExt',
                      label=pm.mel.uiRes('m_createMayaSoftwareCommonGlobalsTab.kExtension'),
                      attribute='defaultRenderGlobals.outFormatExt')
    
    pm.connectControl('userExt', 'defaultRenderGlobals.outFormatExt', index=1)

    pm.scriptJob(parent='userExt',
                 attributeChange=('defaultRenderGlobals.outFormatControl', updateArnoldCustomExtensionControl))

def updateArnoldCustomExtensionControl():
    oldParent = pm.setParent(query=True)
    
    setParentToArnoldCommonTab();
    
    useImage = pm.getAttr('defaultRenderGlobals.outFormatControl') != 1
    value1 = pm.getAttr('defaultRenderGlobals.outFormatControl') == 2
    useExt = useImage and value1
    
    pm.attrControlGrp('userExt', edit=True, enable=useExt)
    
    pm.setParent(oldParent)

def createArnoldImageFormatControl():

    cRenderer = utils.currentRenderer()
    if cRenderer == "mentalRay":
        return pm.mel.createMRImageFormatControl()
    if cRenderer == "mayaSoftware":
        return pm.mel.createMayaImageFormatControl()

    parent = pm.setParent(query=True)

    # Delete the control if it already exists
    #
    fullPath = "%s|imageMenuMayaSW" % parent
    if pm.layout(fullPath, exists=True):
        pm.deleteUI(fullPath)

    # TODO: connect node to options
    createTranslatorMenu('defaultArnoldDriver', 
                         label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kImageFormatMenu"),
                         nodeType='aiAOVDriver',
                         default='exr',
                         optionMenuName='imageMenuMayaSW')

    # We need to create controls that we don't need to avoid
    # Maya errors because of the harcoded code. keep them hidden
    pm.columnLayout('cl_output_compression', vis=0, rowSpacing=0)
    pm.button('renderGlobalsCompression', label="", enable=False)
    pm.attrEnumOptionMenuGrp('multiCamNamingMenu', label="")
    pm.textFieldGrp('multiCamCustomToken', label="")
    pm.setParent('..')

    pm.scriptJob(
        parent=parent,
        attributeChange=("defaultArnoldDriver.aiTranslator",
                         updateArnoldImageFormatControl))

#    changeArnoldImageFormat()
    return "imageMenuMayaSW"


def updateArnoldImageFormatControl(*args):
    core.createOptions()
    curr = pm.getAttr('defaultArnoldDriver.aiTranslator')
    pm.setAttr('defaultRenderGlobals.imageFormat', 51)
    pm.setAttr('defaultRenderGlobals.imfkey', str(curr))

def extendToShape(dag):
    'Return the camera shape from this dag object'
    try:
        return dag.getShape()
    except AttributeError:
        return dag

def getCameras():
    '''
    Return a tuple of (ortho, mono, stereo) camera lists, converting camera
    shapes to transforms
    '''
    ortho = [pm.PyNode(x) for x in pm.listCameras(orthographic=True) or []]
    mono = []
    stereo = []
    # List all mono perspective cameras first
    for camera in pm.listCameras(perspective=True) or []:
        camera = pm.PyNode(camera)
        if _isMono(camera):
            # Ensure to use its shape node
            mono.append(camera)
        else:
            stereo.append(camera)
    return ortho, mono, stereo

def arnoldCameraMaskChange(ui, camera, mask_name):
    val = pm.checkBoxGrp(ui, q=True, value1=True)
    if _isMono(camera):
        camera.attr(mask_name).set(val)
    else:
        lCam = camera.leftCam.get()
        rCam = camera.rightCam.get()
        lCam.attr(mask_name).set(val)
        rCam.attr(mask_name).set(val)

def arnoldChangedCamera(camera, cameraMode, menu):
    '''
    callback used when the user changed a renderable camera.
    camera is the previous camera
    cameraMode was its type
    menu is the menu item used for this change
    '''

    data = CAM_MENU_CAMERA

    if menu:
        sel = pm.optionMenuGrp(menu, q=True, select=True) - 1
        items = pm.optionMenuGrp(menu, q=True, itemListShort=True)
        data = pm.menuItem(items[sel], query=True, data=True)


    if data == CAM_MENU_IGNORE:
        # Make sure to reselect the first entry, in case user clicked
        # on the separator.
        pm.optionMenuGrp(menu, edit=True, select=1)
        return

    newCamNeedLayerAdj = False
    currentLayer = pm.editRenderLayerGlobals(q=True, currentRenderLayer=True)
    isBaseLayer = not pm.getAttr(currentLayer + '.identification')

    # If replacing a camera, start by making the selected camera
    # non-renderable.
    if data in [CAM_MENU_CAMERA, CAM_MENU_STEREOPAIR]:
        if cameraMode == CAM_MENU_IGNORE:
            # There was no previous renderable camera,
            # always create adjustments if not on the master layer.
            if not isBaseLayer:
                newCamNeedLayerAdj = True
        else:
            if cameraMode == CAM_MENU_CAMERA:
                cameras = [camera]
            else:
                cameras = getMultiCameraChildren(camera)

            for cam in cameras:
                camShape = extendToShape(cam)

                # Create adjustments if we are not on the master layer
                if not isBaseLayer and not newCamNeedLayerAdj:
                    # If the source had an adjustment, create one on the
                    # new camera as well.
                    if camShape.renderable.inputs():
                        newCamNeedLayerAdj = True;
                camShape.renderable.set(False)

    elif data == CAM_MENU_ADD:
        # Create adjustments if not on the master layer.
        if not isBaseLayer:
            newCamNeedLayerAdj = True

    # Now process the new value
    if menu != "":
        new = pm.optionMenuGrp(menu, query=True, value=True)
        cameras = []
        if data == CAM_MENU_CAMERA:
            cameras.append(pm.PyNode(new))
        elif data == CAM_MENU_STEREOPAIR:
            pairStr = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kStereoPair")
            stereoCam = new[:-len(pairStr)]
            cameras = getMultiCameraChildren(pm.nt.DagNode(stereoCam))
        elif data == CAM_MENU_ADD:
            # Mark renderable the first non renderable camera we can find
            allCameraShapes = pm.ls(cameras=True)
            for cameraShape in allCameraShapes:
                if not cameraShape.renderable.get():
                    cameras.append(cameraShape)
                    break

        # Now make the new cameras renderable
        for cam in cameras:
            if newCamNeedLayerAdj:
                pm.editRenderLayerAdjustment(cam.renderable)
            cam.renderable.set(True)

    # Finally force recomputing the UI
    pm.evalDeferred(updateArnoldCameraControl)

def setArnoldCheckboxFromAttr(camera, chkbox, attr):
    if pm.hasAttr(camera, 'stereoRigType'):
        # camera.leftCam.get() does not work on Maya2011
        try:
            camera = camera.leftCam.inputs()[0]
        except IndexError:
            return
    val = camera.attr(attr).get()
    pm.checkBoxGrp(chkbox, e=True, value1=val)


def updateArnoldCameraControl(*args):

    pm.melGlobals.initVar('string', 'gRenderableCameraListMenu')

    oldParent = pm.setParent(query=True)

    setParentToArnoldCommonTab()
    cameraLayout = pm.setParent('mayaSoftwareCameraLayout')

    # Unmanage the layout while we edit it, it will update faster
    pm.columnLayout(cameraLayout, edit=True, visible=0)
    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)

    # Empty the layout first
    for child in pm.columnLayout(cameraLayout, query=True, childArray=True) or []:
        pm.deleteUI(child)

    # Populate all stereo cameras and mono camera
    orthoCams, monoCams, stereoCams = getCameras()

    renderableCameras = []
    nonRenderableCameras = [MENU_SEPARATOR]

    # List all mono perspective cameras first
    for camera in monoCams:
        if camera.renderable.get():
            renderableCameras.append((camera, False))
        else:
            nonRenderableCameras.append((camera, False))

    # Remove the separator if nothing was added.
    if nonRenderableCameras and nonRenderableCameras[-1] == MENU_SEPARATOR:
        nonRenderableCameras.pop()

    # list all stereo cameras rigs, and the mono cameras in the rig.
    rigs = _listStereoRigs()
    if rigs:
        for rig in rigs:
            nonRenderableCameras.append(MENU_SEPARATOR)
            # rig.leftCam.get() does not work in Maya2011
            try:
                lCam = rig.leftCam.inputs()[0].getShape()
                rCam = rig.rightCam.inputs()[0].getShape()
            except IndexError:
                pm.warning("Stereo camera %s is missing required connections" % rig)
                continue
            cameras = rig.listRelatives(type="camera", allDescendents=True)
            # Add an entry for the rig pair if at least one cam is not
            # renderable. Use the + character to mark it.
            skipLR = False
            if lCam.renderable.get() and rCam.renderable.get():
                renderableCameras.append((rig, True))
                skipLR = True
            else:
                nonRenderableCameras.append((rig, True))

            for camShape in cameras:
                camera = camShape.getParent()
                if camShape.renderable.get():
                    if (camShape == lCam or camShape == rCam):
                        if not skipLR:
                            renderableCameras.append((camera, False))
                        else:
                            nonRenderableCameras.append((camera, False))
                    else:
                        renderableCameras.append((camera, False))
                else:
                    nonRenderableCameras.append((camera, False))
        # Remove the separator if nothing was added.
        if nonRenderableCameras and nonRenderableCameras[-1] == MENU_SEPARATOR:
            nonRenderableCameras.pop()

    # List all the ortho cameras
    nonRenderableCameras.append(MENU_SEPARATOR)

    for camera in orthoCams:
        # Ensure to use its shape node
        if camera.renderable.get():
            renderableCameras.append((camera, False))
        else:
            nonRenderableCameras.append((camera, False))

    # Remove the separator if nothing was added
    if nonRenderableCameras and nonRenderableCameras[-1] == MENU_SEPARATOR:
        nonRenderableCameras.pop()

    # If there is no renderable camera on this layer, add a fake
    # entry so that users can switch to an existing one.
    if not renderableCameras:
        isFakeCam = True
        renderableCameras.append((pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kNoRenderableCamSelect"), False))
    else:
        isFakeCam = False

    pm.columnLayout()
    for s, (camera, isStereo) in enumerate(renderableCameras):
        if s % 10 == 9:
            pm.setParent('..')
            pm.columnLayout()

        pm.columnLayout()

        if s > 0:
            pm.separator()

        if isFakeCam:
            cameraMode = CAM_MENU_IGNORE
        elif isStereo:
            cameraMode = CAM_MENU_STEREOPAIR
        else:
            cameraMode = CAM_MENU_CAMERA

        pm.rowLayout(nc=2, cw2=(340, 30), cl2=("left", "right"))
        optMenu = pm.optionMenuGrp(cw=(1, 141), label="Renderable Camera")

        pm.optionMenuGrp(optMenu,
                         edit=True,
                         changeCommand=pm.Callback(arnoldChangedCamera, camera, cameraMode, optMenu))

        # The first item is the current renderable camera
        if cameraMode == CAM_MENU_STEREOPAIR:
            thisCamLabel = '%s%s'%(camera, pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kStereoPair"))
        else:
            thisCamLabel = camera

        pm.menuItem(label=thisCamLabel, data=CAM_MENU_IGNORE)
        # Save this as a global variable for others to access
        pm.melGlobals['gRenderableCameraListMenu'] = str(optMenu)

        # Insert cameras
        for nonRenderableCamera, isStereo2 in nonRenderableCameras:
            if (nonRenderableCamera, isStereo2) == MENU_SEPARATOR:
                pm.menuItem(divider=1, data=CAM_MENU_IGNORE)
            elif isStereo2:
                # Stereo rig
                label = '%s%s'%(nonRenderableCamera, pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kStereoPair"))
                pm.menuItem(label=label, data=CAM_MENU_STEREOPAIR)
            else:
                # Mono camera.
                pm.menuItem(label=nonRenderableCamera, data=CAM_MENU_CAMERA)

        # Insert add menuItem
        if not isFakeCam and nonRenderableCamera:
            pm.menuItem(divider=1, data=CAM_MENU_IGNORE)
            pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kAddRenderCam"), data=CAM_MENU_ADD)

        if not isFakeCam:
            # connect the label, so we can change its color
            camShape = extendToShape(camera)
            pm.connectControl(optMenu, "%s.renderable"%camShape, index=1)

            if len(renderableCameras) > 1:
                pm.iconTextButton(style="iconOnly",
                                    image="removeRenderable.png",
                                    annotation=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kNonRendCam"),
                                    width=20,
                                    height=20,
                                    command=pm.Callback(arnoldChangedCamera, camera, cameraMode, ''))

        pm.setParent('..')

        if not isFakeCam:
            pm.columnLayout()
            chkbox = pm.checkBoxGrp(numberOfCheckBoxes=1,
                                    label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kAlphaChannel"))
            pm.checkBoxGrp(chkbox, e=True, cc=pm.Callback(arnoldCameraMaskChange, chkbox, camera, 'mask'))
            setArnoldCheckboxFromAttr(camera, chkbox, "mask")
            pm.connectControl(chkbox, "%s.mask"%camShape, index=1)
            pm.connectControl(chkbox, "%s.mask"%camShape, index=2)
            chkbox = pm.checkBoxGrp(numberOfCheckBoxes=1,
                                    label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kDepthChannel"))
            pm.checkBoxGrp(chkbox, e=True, cc=pm.Callback(arnoldCameraMaskChange, chkbox, camera, 'depth'))
            setArnoldCheckboxFromAttr(camera, chkbox, "depth")
            pm.connectControl(chkbox, "%s.depth"%camShape, index=1)
            pm.connectControl(chkbox, "%s.depth"%camShape, index=2)

            pm.setParent('..')
        pm.setParent('..')
    pm.setParent('..')

    #
    #  Invoke any user supplied code. This callback is published and
    #  needs to remain consistent in future versions of Maya.
    #
    if pm.mel.exists("renderableCameraListUserCallback"):
        # Use catchQuiet in case no callback is supplied, we don't
        # want that to show an error.
        pm.mel.eval('catchQuiet( eval("source \"renderableCameraListUserCallback\"")')

    pm.setParent('..')

    pm.setUITemplate('attributeEditorTemplate', popTemplate=True)
    pm.columnLayout(cameraLayout, edit=True, visible=1)

    pm.setParent(oldParent)

    updateArnoldTargetFilePreview()

def updateArnoldFrameNumberControls(*args):

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    useAnim      = pm.getAttr("defaultRenderGlobals.animation")
    useCustomExt = pm.getAttr("defaultRenderGlobals.modifyExtension")
    multiframe = pm.mel.multiframeFormat(pm.mel.getImfImageType())

    pm.attrControlGrp('startFrameCtrl',
                        edit=True,
                        enable=useAnim)
    pm.attrControlGrp('endFrameCtrl',
                        edit=True,
                        enable=useAnim)
    pm.attrControlGrp('byFrameStepCtrl',
                        edit=True,
                        enable=useAnim)
    pm.attrControlGrp('extensionPaddingCtrl',
                        edit=True,
                        enable=(useAnim and not multiframe))
    pm.attrControlGrp('modifyExtensionCtrl',
                        edit=True,
                        enable=(useAnim and not multiframe))
    pm.attrControlGrp('startExtensionCtrl',
                        edit=True,
                        enable=(useAnim and useCustomExt and not multiframe))
    pm.attrControlGrp('byExtensionCtrl',
                        edit=True,
                        enable=(useAnim and useCustomExt and not multiframe))

    pm.setParent(oldParent)

def createArnoldRenderVersionKeywordMenu(parent):

    pm.popupMenu(parent, edit=True, deleteAllItems=True)
    pm.setParent(parent, menu=True)
    
    pm.menuItem(label=pm.mel.uiRes('m_createMayaSoftwareCommonGlobalsTab.kVersionTitle'), enable=0)
    pm.menuItem(divider=True)
    
    val = pm.textFieldGrp('renderVersionCtrl', q=True, text=True)
    ival, ival2 = ('1', '2')
    match = re.search('^(\d+)|(\d+)$', val)
    if match:
        i = int(match.group())
        if i > 0:
            ival2 = val.replace(str(i), str(i + 1))
            ival = val.replace(str(i), str(i - 1))
        else:
            ival = '1'

    #callBack = pm.textFieldGrp("renderVersionCtrl", e=True, text="^1s", forceChangeCommand=True)
    formatString = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kVersionNumber")
    pm.menuItem(label=formatString.replace('^1s', ival),
                command=Callback(pm.textFieldGrp, 'renderVersionCtrl', e=True, text=ival, forceChangeCommand=True))

    pm.menuItem(label=formatString.replace('^1s', ival2),
                command=Callback(pm.textFieldGrp, 'renderVersionCtrl', e=True, text=ival2, forceChangeCommand=True))

    date = pm.date(format="YY_MM_DD")
    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kVersionDate").replace('^1s', date),
                command=Callback(pm.textFieldGrp, 'renderVersionCtrl', e=True, text=date, forceChangeCommand=True))
    
    time = pm.date(format="hh-mm-ss")
    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kVersionTime").replace('^1s', time),
                command=Callback(pm.textFieldGrp, 'renderVersionCtrl', e=True, text=time, forceChangeCommand=True))

def updateArnoldRenderVersionControl():
    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab();
    
    version = pm.getAttr('defaultRenderGlobals.renderVersion')
    version = '' if not version else version
    pm.textFieldGrp('renderVersionCtrl', edit=True, text=version)
    
    pm.setParent(oldParent)

def changeArnoldRenderVersion(*args, **kwargs):
    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab();
    
    version = pm.textFieldGrp('renderVersionCtrl', query=True, text=True)
    pm.setAttr('defaultRenderGlobals.renderVersion', version, type="string")
    
    pm.setParent(oldParent)

def createArnoldCommonImageFile():
    '''
    Procedure Name:
        createArnoldCommonImageFile
    
    Description:
        Creates the UI in the "Image File Output" expand/collapse section.
      This section is always created so is treated differently
      then the sections created when the tab is expanded.
    '''

    parent = pm.setParent(query=True)

    # Delete the control if it already exists
    #
    fullPath = "%s|imageFileOutputSW"%parent
    if pm.layout(fullPath, exists=True):
        pm.deleteUI(fullPath)

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)

    pm.columnLayout('imageFileOutputSW', adjustableColumn=True)

    createArnoldFileNamePrefixControl()

    createArnoldImageFormatControl()

    createArnoldFileNameFormatControl()


    pm.attrControlGrp('extensionPaddingCtrl',
                        attribute='defaultRenderGlobals.extensionPadding',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kFramePadding"),
                        hideMapButton=True)
    
    pm.separator()
     
    createArnoldUseCustomExtensionControl()
    createArnoldCustomExtensionControl()
    
    pm.textFieldGrp('renderVersionCtrl',
                    label=pm.mel.uiRes('m_createMayaSoftwareCommonGlobalsTab.kVersionLabel'),
                    annotation=pm.mel.uiRes('m_createMayaSoftwareCommonGlobalsTab.kVersionLabelAnn'),
                    cc=changeArnoldRenderVersion)
    if pm.mel.getApplicationVersionAsFloat() >= 2011:
        popup = pm.popupMenu(parent='renderVersionCtrl|field')
    else:
        popup = pm.popupMenu(parent='renderVersionCtrl')
        
    pm.popupMenu(popup, edit=True, postMenuCommand=Callback(createArnoldRenderVersionKeywordMenu, popup))
    pm.connectControl('renderVersionCtrl', 'defaultRenderGlobals.renderVersion', index=1)
    pm.scriptJob(parent='renderVersionCtrl',
                 attributeChange=('defaultRenderGlobals.renderVersion', updateArnoldRenderVersionControl))
    
    updateArnoldRenderVersionControl()
    updateArnoldUseCustomExtensionControl()
    updateArnoldCustomExtensionControl()

    pm.setParent(parent)
    pm.setUITemplate(popTemplate=True)

    # Perform an initial update of the UI created above, so that controls
    # which are not directly connected to attributes are properly initialized.
    #
    updateArnoldFileNamePrefixControl()
    updateArnoldImageFormatControl()


def createArnoldCommonFrameRange():
    '''
      Procedure Name:
          createArnoldCommonFrameRange
    
      Description:
          Creates the UI in the "Frame Range" expand/collapse section.
        This section is always created so is treated differently
        then the sections created when the tab is expanded.
    '''

    parent = pm.setParent(query=True)

    # Delete the control if it already exists
    #
    fullPath = "%s|frameRangeSW"%parent
    if pm.layout(fullPath, exists=True):
        pm.deleteUI(fullPath)

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)

    pm.columnLayout('frameRangeSW', adjustableColumn=True)

    pm.attrControlGrp('startFrameCtrl',
                        attribute='defaultRenderGlobals.startFrame',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kStartFrame"),
                        hideMapButton=True)

    pm.attrControlGrp('endFrameCtrl',
                        attribute='defaultRenderGlobals.endFrame',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kEndFrame"),
                        hideMapButton=True)

    pm.attrControlGrp('byFrameStepCtrl',
                        attribute='defaultRenderGlobals.byFrameStep',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kByFrame"),
                        hideMapButton=True)

    pm.separator()

    pm.checkBoxGrp('modifyExtensionCtrl',
                     cc=updateArnoldFrameNumberControls,
                     label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kRenumberFramesUsing"))

    pm.connectControl('modifyExtensionCtrl', 'defaultRenderGlobals.modifyExtension', index=1)
    pm.connectControl('modifyExtensionCtrl', 'defaultRenderGlobals.modifyExtension', index=2)

    '''
    pm.attrControlGrp('modifyExtensionCtrl',
                        attribute='defaultRenderGlobals.modifyExtension',
                        changeCommand=pm.Callback(updateArnoldFrameNumberControls),
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kRenumberFramesUsing"))
    '''


    pm.attrControlGrp('startExtensionCtrl',
                        attribute='defaultRenderGlobals.startExtension',
                        enable=pm.getAttr('defaultRenderGlobals.modifyExtension'),
                        hideMapButton=True,
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kStartNumber"))

    pm.attrControlGrp('byExtensionCtrl',
                        attribute='defaultRenderGlobals.byExtension',
                        enable=pm.getAttr('defaultRenderGlobals.modifyExtension'),
                        hideMapButton=True,
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kRenumberByFrame"))

    pm.setParent(parent)
    pm.setUITemplate(popTemplate=True)

    # Perform an initial update of the UI created above, so that controls
    # which are not directly connected to attributes are properly initialized.
    #
    updateArnoldFileNameFormatControl()


def createArnoldCommonRenderCameras():
    '''
    Procedure Name:
        createArnoldCommonRenderCameras
    
    Description:
        Creates the UI in the "Renderable Cameras" expand/collapse section.
      This section is always created so is treated differently
      then the sections created when the tab is expanded.
    '''

    parent = pm.setParent(query=True)

    # Delete the control if it already exists
    #
    fullPath = "%s|renderableCamerasSW"%parent
    if pm.layout(fullPath, exists=True):
        pm.deleteUI(fullPath)


    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)

    pm.columnLayout('renderableCamerasSW', adjustableColumn=True)

    # Cameras ------------------------------------------------
    pm.columnLayout('mayaSoftwareCameraLayout')
    updateArnoldCameraControl()
    pm.setParent('..')

    pm.setParent(parent)
    pm.setUITemplate(popTemplate=True)

# ----------------------------------------------------------------------------
# Code to create and update the Resolution frame
#

def createArnoldCommonResolution():
    '''
    Procedure Name:
        createArnoldCommonResolution
    
    Description:
        Creates the UI in the "Resolution" expand/collapse section.
    '''

    #
    # Make sure the list of predefined resolutions has been read in.
    #
    gImageFormatData = pm.melGlobals.get('gImageFormatData', 'string[]')
    gUserImageFormatData = pm.melGlobals.get('gUserImageFormatData', 'string[]')

    if not gImageFormatData:
        pm.mel.source('imageFormats.mel')
        gImageFormatData = pm.melGlobals['gImageFormatData']


    if not pm.mel.eval('exists imageFormats_melToUI'):
        pm.mel.source('imageFormats.mel')
        gUserImageFormatData = pm.melGlobals['gUserImageFormatData']


    gResolutionUnitsNames = pm.melGlobals.get('gResolutionUnitsNames', 'string[]')
    gMeasurementUnitsNames = pm.melGlobals.get('gMeasurementUnitsNames', 'string[]')

    if not gResolutionUnitsNames:
        pm.mel.source('resolutionFormats.mel')
        gResolutionUnitsNames = pm.melGlobals['gResolutionUnitsNames']

    isMayaEvalVersion = pm.about(ev=True)
    gPLEImageFormatData = []
    if isMayaEvalVersion:
        gImageFormatData = gPLEImageFormatData

    if pm.mel.exists("userImageFormats.mel") and len(gUserImageFormatData) == 0:
        # Yes, we need the eval here, to avoid doing the source
        # until we know whether the file actually exists
        pm.mel.eval('catchQuiet( eval("userImageFormats.mel"))')
        gUserImageFormatData = pm.melGlobals['gUserImageFormatData']

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)

    parent = pm.setParent(q=True)
    # If the UI is created already then just update the attribute values.
    if pm.columnLayout("%s|rgResolutionLayout"%parent, exists=True):
        updateArnoldResolution()
        return

    pm.columnLayout('rgResolutionLayout', adjustableColumn=True)
    resItem = 1
    numResolutionPresets = len(gImageFormatData)
    allResNodes = pm.ls(type='resolution')
    numResolutionNodePresets = len(allResNodes) - 1
    gImageFormatDividerPosition = pm.melGlobals.get('gImageFormatDividerPosition', 'int')
    pm.optionMenuGrp('resolutionMenu',
                     label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kPresets"),
                     changeCommand=changeArnoldResolution)

    pm.menuItem(label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kCustom"))
    for resItem in range(0, numResolutionPresets):

        if resItem == gImageFormatDividerPosition:
            pm.menuItem(label="---------------------", enable=False)
        else:
            item = gImageFormatData[resItem]
            tokens = item.split(' ')
            numTokens = len(tokens)

            # Change any underscore into a space;
            # some names may have up to 2 underscores in them,
            # so we do this twice.
            #
            niceName = tokens[0].replace(' ', '_').replace('"', '\\"')
            uiName = pm.mel.imageFormats_melToUI(niceName)
            pm.menuItem(label=uiName)

    for item in gUserImageFormatData:
        tokens = item.split(' ')

        # Change any underscore into a space;
        # some names may have up to 2 underscores in them,
        # so we do this twice.
        #
        niceName = tokens[0].replace(' ', '_').replace('"', '\"')
        pm.menuItem(label=niceName)

    for resItem in range(0, numResolutionNodePresets):
        pm.menuItem(label=allResNodes[resItem + 1])

    pm.separator()

    pm.checkBoxGrp('aspectLockCheck',
                     numberOfCheckBoxes=1,
                     label="",
                     label1=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kMaintainWidthHeightRatio"))

    pm.connectControl('aspectLockCheck', 'defaultResolution.aspectLock', index=2)

    pm.radioButtonGrp('ratioLockRadio',
                      numberOfRadioButtons=2,
                      vertical=True,
                      label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kMaintainRatio"),
                      label1=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kPixelAspect"),
                      label2=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kDeviceAspect"),
                      on1=pm.Callback(pm.setAttr, "defaultResolution.lockDeviceAspectRatio", 0),
                      on2=pm.Callback(pm.setAttr, "defaultResolution.lockDeviceAspectRatio", 1),
                      data1=0,
                      data2=1)


    pm.connectControl('ratioLockRadio', 'defaultResolution.lockDeviceAspectRatio', index=1)

    pm.floatFieldGrp('mayaSoftwareResWidth',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kWidth"),
                        changeCommand=changeArnoldAspectLockWidth)

    pm.connectControl('mayaSoftwareResWidth', 'defaultResolution.width', index=1)

    pm.floatFieldGrp('mayaSoftwareResHeight', label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kHeight"),
                        changeCommand=changeArnoldAspectLockHeight)

    pm.connectControl('mayaSoftwareResHeight', 'defaultResolution.height', index=1)

    pm.optionMenuGrp('sizeUnitsMenu',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kSizeUnits"),
                        changeCommand=updateArnoldResolution)

    # Construct all menu items
    for i, melUnit in enumerate(gMeasurementUnitsNames):
        pm.menuItem(label=pm.mel.resolutionFormats_melToUI(melUnit), data=i)

    # connect the label, so we can change its color
    pm.connectControl('sizeUnitsMenu', 'defaultResolution.imageSizeUnits', index=1)
    # connect the menu, so it will always match the attribute
    pm.connectControl('sizeUnitsMenu', 'defaultResolution.imageSizeUnits', index=2)

    pm.separator(style='none', h=5)

    pm.floatFieldGrp('mayaSoftwareRes',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kResolution"),
                        changeCommand=changeArnoldRes)

    pm.connectControl('mayaSoftwareRes', 'defaultResolution.dotsPerInch', index=1)

    pm.optionMenuGrp('resUnitsMenu',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kResolutionUnits"),
                        changeCommand=updateArnoldResolution)

    # Construct all menu items
    for i, melUnit in enumerate(gResolutionUnitsNames):
        pm.menuItem(label=pm.mel.resolutionFormats_melToUI(melUnit), data=i)

    # connect the label, so we can change its color
    pm.connectControl('resUnitsMenu', 'defaultResolution.pixelDensityUnits', index=1)
    # connect the menu, so it will always match the attribute
    pm.connectControl('resUnitsMenu', 'defaultResolution.pixelDensityUnits', index=2)

    pm.separator()

    pm.floatFieldGrp('resRatio',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kDeviceAspectRatio"),
                        changeCommand=updateArnoldDeviceAspectRatio)

    # connect the label, so we can change its color
    pm.connectControl('resRatio', 'defaultResolution.deviceAspectRatio', index=1)
    # connect the menu, so it will always match the attribute
    pm.connectControl('resRatio', 'defaultResolution.deviceAspectRatio', index=2)

    pm.floatFieldGrp('pixRatio',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kPixelAspectRatio"),
                        changeCommand=updateArnoldPixelAspectRatio)

    # connect the label, so we can change its color
    pm.connectControl('pixRatio', 'defaultResolution.pixelAspect', index=1)
    # connect the menu, so it will always match the attribute
    pm.connectControl('pixRatio', 'defaultResolution.pixelAspect', index=2)

    pm.setParent('..')
    pm.setUITemplate(popTemplate=True)

    # Make sure the values are right
    updateArnoldResolution()

    # Set up script jobs for those attributes which require updating of
    # multiple controls.
    # This is especially important when a user changes render layers.
    #
    attrArray = []
    attrArray.append("defaultResolution.width")
    attrArray.append("defaultResolution.height")
    attrArray.append("defaultResolution.dotsPerInch")
    attrArray.append("defaultResolution.imageSizeUnits")
    attrArray.append("defaultResolution.pixelDensityUnits")

    for attr in attrArray:
        pm.scriptJob(attributeChange=(attr, updateArnoldResolution),
                        parent=pm.setParent(query=True))



def changeArnoldRes(*args):
    '''
     Description:
        Called when the resolution field is changed.
        Updates the corresponding attribute, converting to DPI.
    '''

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    gResolutionUnitsNames = pm.melGlobals.get('gResolutionUnitsNames', 'string[]')
    oldDPI = pm.getAttr('defaultResolution.dotsPerInch')
    value = pm.floatFieldGrp('mayaSoftwareRes', q=True, v1=True)

    # Convert from the current resolution units to DPI
    resUnits = pm.getAttr('defaultResolution.pixelDensityUnits')
    newDPI = pm.mel.convertResolutionMeasurement(value, gResolutionUnitsNames[resUnits], "pixels/inch")

    # Check that value is within value range
    if newDPI < 1.0:
        pm.warning(pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kResolutionDPIWarn"))
        newDPI = 1.0

    oldWidth = pm.getAttr('defaultResolution.width')
    newWidth = oldWidth
    oldHeight = pm.getAttr('defaultResolution.height')
    newHeight = oldHeight

    # Change pixel width/height only if the image size units are not
    # currently set as pixels
    #
    sizeUnits = pm.getAttr('defaultResolution.imageSizeUnits')
    if sizeUnits != 0: # 0 corresponds to pixels
        newWidth = math.floor( oldWidth * newDPI/oldDPI + 0.5 )
        newHeight = math.floor( oldHeight * newDPI/oldDPI + 0.5 )

    # Account for version restrictions and bounds
    #
    isMayaEvalVersion = pm.about(ev=True)
    PLE_MAX_X = 1024
    PLE_MAX_Y =  768

    if isMayaEvalVersion:
        warnMsg = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kDPICannotBeAchieved")
        warnDisp = ''
        # Check width
        if newWidth > PLE_MAX_X:
            warnDisp = pm.format(warnMsg, s=(PLE_MAX_X, PLE_MAX_Y))
            pm.warning(warnDisp)
            newWidth = PLE_MAX_X
            # Adjust DPI to maintain constant document size
            newDPI = oldDPI * newWidth/oldWidth
            # Adjust height to maintain correct ratio
            newHeight = oldHeight * newWidth/oldWidth

        # Check height
        if newHeight > PLE_MAX_Y:
            warnDisp = pm.format(warnMsg, s=(PLE_MAX_X, PLE_MAX_Y))
            pm.warning(warnDisp)
            newHeight = PLE_MAX_Y
            # Adjust DPI to maintain constant document size
            newDPI = oldDPI * newHeight/oldHeight
            # Adjust width to maintain correct ratio
            newWidth = oldWidth * newHeight/oldHeight


    if newWidth < 2:
        pm.warning(pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kWidthWarning"))
        newWidth = 2

    if newHeight < 2:
        pm.warning(pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kHeightWarning"))
        newHeight = 2


    # All attributes should now be correct
    pm.setAttr('defaultResolution.dotsPerInch', newDPI)
    pm.setAttr('defaultResolution.width', newWidth)
    pm.setAttr('defaultResolution.height', newHeight)

    # Update the values, will correct any invalid entries
    updateArnoldResolution()

    pm.setParent(oldParent)


def updateArnoldResolution(*args):
    '''
    Procedure Name:
        updateArnoldResolution
    
    Description:
        Gets the real values from the nodes and sets the UI based
      on these values.  This procedure updates all of the resolution
      values.
    '''

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    width = pm.getAttr('defaultResolution.width')
    height = pm.getAttr('defaultResolution.height')
    aspect = pm.getAttr('defaultResolution.deviceAspectRatio')
    dpi = pm.getAttr('defaultResolution.dotsPerInch')
    resItem = 0
    whichRes = 1 # use "Custom" if no match is found
    allResNodes = pm.ls(type='resolution')

    gImageFormatData = pm.melGlobals.get('gImageFormatData', 'string[]')
    gUserImageFormatData = pm.melGlobals.get('gUserImageFormatData', 'string[]')
    gDefaultDpi = pm.melGlobals.get('gDefaultDpi', 'float')

    numResolutionPresets = len(gImageFormatData)
    numUserResolutionPresets = len(gUserImageFormatData)
    numResolutionNodePresets = len(allResNodes) - 1
    resWidth = 0
    resHeight = 0
    resAspect = 0
    resDpi = 0

    for resItem in range(0, numResolutionPresets):

        item = gImageFormatData[resItem]
        tokens = item.split()
        numTokens = len(tokens)

        if numTokens == 5:

            resWidth = float(tokens[1])
            resHeight = float(tokens[2])
            resAspect = float(tokens[3])
            resDpi = float(tokens[4])

            # Check all values, including DPI. If the DPI in the array is 0
            # (i.e. unspecified), then any dpi is considered a match.
            if width == resWidth and height == resHeight \
                  and math.fabs(aspect - resAspect) < 0.001 \
                  and (resDpi==0 or math.fabs(dpi - resDpi)) < 0.001:

                # We add _2_ to $resItem below: 1 because we're
                # skipping the first item (Custom) in the list, and 1
                # because the optionMenu items are numbered starting at 1,
                # but our list in $gImageFormatData is indexed starting at 0.
                whichRes = resItem + 2
                break
        else:
            invalidImageFormat = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kInvalidImageFormat")
            warnMsg = pm.format(invalidImageFormat, s=item)
            pm.warning(warnMsg)

    # If no match was found in the built-in resolutions,
    # check out the user-defined ones
    #
    if whichRes == 1:
        for resItem in range(0, numUserResolutionPresets):
            item = gUserImageFormatData[resItem]
            tokens = item.split()
            numTokens = len(tokens)

            # User may or may not have specified a resolution.
            # Ensure compatibility.
            #
            if numTokens == 4 or numTokens == 5:
                resWidth = float(tokens[1])
                resHeight = float(tokens[2])
                resAspect = float(tokens[3])
                if numTokens == 5:
                    resDpi = float(tokens[4])
                else:
                    resDpi = gDefaultDpi

                if width == resWidth and height == resHeight \
                     and math.fabs(aspect - resAspect) < 0.001 \
                     and (resDpi==0 or math.fabs(dpi - resDpi)) < 0.001:

                    whichRes = numResolutionPresets + resItem + 2
                    break
            else:
                invalidImageFormat = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kInvalidUserImageFormat")
                warnMsg = pm.format(invalidImageFormat, s=item)
                pm.warning(warnMsg)

    # If no match was found in the user-defined resolutions,
    # see if there are any 'extra' resolution nodes in the scene.
    #
    if whichRes == 1:
        for resItem in range(0, numResolutionNodePresets):

            # We assume the 0th item in the list of resolution nodes is
            # the default one, which is created implicitly...
            #
            resNodeName = allResNodes[resItem + 1]

            resWidth = pm.getAttr(resNodeName + ".width")
            resHeight = pm.getAttr(resNodeName + ".height")
            resAspect = pm.getAttr(resNodeName + ".deviceAspectRatio")

            if width == resWidth and height == resHeight \
                  and math.fabs(aspect - resAspect) < 0.001:

                # We add _2_ to $resItem below: 1 because we're
                # skipping the first item (Custom) in the list, and 1
                # because the optionMenu items are numbered starting at 1,
                # but our list in $gImageFormatData is indexed starting at 0.
                #
                whichRes = numResolutionPresets + numUserResolutionPresets + resItem + 2
                break

    pm.optionMenuGrp('resolutionMenu', edit=True, sl=whichRes)

    pm.checkBoxGrp('aspectLockCheck', edit=True, v1=pm.getAttr('defaultResolution.aspectLock'))
    resNode = pm.PyNode('defaultResolution')
    pm.floatFieldGrp('resRatio', edit=True, v1=aspect)
    adjustArnoldPixelAspect(resNode)
    resNode.pixelAspect.set(pm.floatFieldGrp('pixRatio', q=True, v1=True))
    pm.radioButtonGrp('ratioLockRadio',
                        edit=True,
                        select=resNode.lockDeviceAspectRatio.get()+1)
    #
    # Update the UI controls for image size and resolution
    #
    gMeasurementUnitsNames = pm.melGlobals['gMeasurementUnitsNames']
    gResolutionUnitsNames = pm.melGlobals['gResolutionUnitsNames']

    sizeUnits = resNode.imageSizeUnits.get()
    resUnits = resNode.pixelDensityUnits.get()

    # Update width and height fields
    docWidth = float(width)
    docHeight = float(height)

    precision = 0 # To ensure pixel values are displayed without decimals
    if sizeUnits != 0:
        # Convert from pixels to the correct measurement units
        docWidth = pm.mel.convertMeasurement(pm.mel.convertPixelsToInches( width, dpi ), "inches", gMeasurementUnitsNames[sizeUnits])
        docHeight = pm.mel.convertMeasurement(pm.mel.convertPixelsToInches( height, dpi ), "inches", gMeasurementUnitsNames[sizeUnits])
        precision = 3

    pm.floatFieldGrp('mayaSoftwareResWidth', edit=True, precision=precision, v1=docWidth)
    pm.floatFieldGrp('mayaSoftwareResHeight', edit=True, precision=precision, v1=docHeight)

    # Update resolution field
    # Convert from DPI to the correct resolution units
    res = pm.mel.convertResolutionMeasurement(dpi, "pixels/inch", gResolutionUnitsNames[resUnits])
    pm.floatFieldGrp('mayaSoftwareRes', edit=True, precision=3, v1=res)

    # "Size Units" and "Resolution Units" fields automatically update
    # because they are attached to a harness

    pm.setParent(oldParent)


def changeArnoldResolution(*args):
    '''
    Procedure Name:
        changeResolution
    
    Description:
      This procedure is called when the user selects a different
      resolution.  It sets the internal representation
      and then updates the example to show the changes.
    '''

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    gImageFormatData = pm.melGlobals['gImageFormatData']
    gUserImageFormatData = pm.melGlobals['gUserImageFormatData']
    gDefaultDpi = pm.melGlobals['gDefaultDpi']

    # We are suppose to get proper image formats for PLE.
    isMayaEvalVersion = pm.about(ev=True)
    if isMayaEvalVersion:
        gPLEImageFormatData = pm.melGlobals['gPLEImageFormatData']
        gImageFormatData = gPLEImageFormatData

    numResolutionPresets = len(gImageFormatData)
    numUserResolutionPresets = len(gUserImageFormatData)
    allResNodes = pm.ls(type='resolution')
    numResolutionNodePresets = len(allResNodes) - 1
    tokens = []
    resItem = pm.optionMenuGrp('resolutionMenu', q=True, sl=True)
    resWidth = 0
    resHeight = 0
    resAspect = 0
    resDpi = 0 # signals preset doesn't contain dpi info
    item = ''

    # Item #1 is Custom, which doesn't change the fields
    # We subtract _2_ from $resItem below: 1 because we're
    # skipping the first item (Custom) in the list, and 1
    # because the optionMenu items are numbered starting at 1,
    # but our list in $gImageFormatData is indexed starting at 0.
    #
    if resItem > 1:
        if resItem > (numResolutionPresets + 1):
            if resItem > (numResolutionPresets + numUserResolutionPresets + 1):
                # It's one of the user-defined resolution nodes' presets
                resNode = allResNodes[resItem - numResolutionPresets - numUserResolutionPresets - 1]
                resWidth = resNode.width.get()
                resHeight = resNode.height.get()
                resAspect = resNode.deviceAspectRatio.get()
            else:
                # It's one of the user-defined resolution presets
                item = gUserImageFormatData[resItem - numResolutionPresets - 2]
                tokens = item.split()
                resWidth = float(tokens[1])
                resHeight = float(tokens[2])
                resAspect = float(tokens[3])
                if len(tokens) == 5:  # user has included the dpi field
                    resDpi = float(tokens[4])
                else:
                    resDpi = gDefaultDpi # default dpi
        else:
            # It's one of the built-in resolution presets
            item = gImageFormatData[resItem - 2]
            tokens = item.split()
            numTokens = len(tokens)
            resWidth = float(tokens[1])
            resHeight = float(tokens[2])
            resAspect = float(tokens[3])
            resDpi = float(tokens[4])

        pm.setAttr("defaultResolution.width", resWidth)
        pm.setAttr("defaultResolution.height", resHeight)
        pm.setAttr("defaultResolution.deviceAspectRatio", resAspect)
        pm.setAttr("defaultResolution.lockDeviceAspectRatio", 0)
        pixelAspect = float(resHeight)/float(resWidth)*resAspect
        pm.setAttr("defaultResolution.pixelAspect", pixelAspect)

        # Set the dpi if it's non-zero
        if resDpi != 0:
            pm.setAttr("defaultResolution.dotsPerInch", resDpi)


        # Set the proper field ordering if PAL or NTSC.
        if pm.getAttr('defaultResolution.height') == 576: # PAL
            pm.setAttr("defaultResolution.oddFieldFirst", 0)
            if pm.columnLayout('rgFieldLayout', exists=True) and pm.mel.exists('updateFieldOptions'):
                pm.mel.updateFieldOptions()
        elif pm.getAttr('defaultResolution.height') == 486: # NTSC
            pm.setAttr("defaultResolution.oddFieldFirst", 1)
            if pm.columnLayout('rgFieldLayout', exists=True) and pm.mel.exists('updateFieldOptions'):
                pm.mel.updateFieldOptions()

    updateArnoldResolution()

    pm.setParent(oldParent)



def updateArnoldPixelDeviceRatios(node):
    '''
    This is called when the resolution changes. Update the pixel or the
    device aspect ration as necessary.
    '''
    aspect = float(node.width.get()) / float(node.height.get())

    if node.lockDeviceAspectRatio.get() == 0:
        aspect = aspect * node.pixelAspect.get()
        node.deviceAspectRatio.set(aspect)
    else:
        aspect = node.deviceAspectRatio.get() / aspect
        node.pixelAspect.set(aspect)

def checkArnoldAspectLockWidth(node):
    if node.aspectLock.get():
        value = node.width.get()
        aspect = node.pixelAspect.get()
        aspect /= node.deviceAspectRatio.get()

        #fix for bug#269698, plus 0.5 to give round value
        rez = (aspect * value) + 0.5

        if pm.about(ev=True):
            if rez > PLE_MAX_Y:
                warnMsg = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kImageResolutionLimited")
                dispMsg = pm.format(warnMsg, s=(PLE_MAX_X,PLE_MAX_Y))
                pm.warning(dispMsg)
                rez = PLE_MAX_Y

        node.height.set(rez)

    updateArnoldPixelDeviceRatios(node)

def checkArnoldAspectLockHeight(node):
    if node.aspectLock.get():
        value = node.height.get()
        aspect = node.pixelAspect.get()
        aspect /= node.deviceAspectRatio.get()

        #fix for bug#269698, plus 0.5 to give round value
        rez = (value/aspect) + 0.5

        if pm.about(ev=True):
            if rez > PLE_MAX_X:
                warnMsg = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kImageResolutionLimited")
                dispMsg = pm.format(warnMsg, s=(PLE_MAX_X, PLE_MAX_Y))
                pm.warning(dispMsg)
                rez = PLE_MAX_X

        node.width.set(rez)

    updateArnoldPixelDeviceRatios(node)


def changeArnoldAspectLockWidth(*args):
    '''
    Procedure Name:
        changeArnoldAspectLockWidth
    
    Description:
      This procedure is called when the user changes the
      resolution width.  It sets the internal representation
      then looks at the ratio lock etc and changes any other
      values that rely on it.
    '''

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    widthValue = pm.floatFieldGrp('mayaSoftwareResWidth', q=True, v1=True)

    gMeasurementUnitsNames = pm.melGlobals['gMeasurementUnitsNames']

    resNode = pm.PyNode('defaultResolution')
    dpi = resNode.dotsPerInch.get()
    sizeUnits = resNode.imageSizeUnits.get()

    if sizeUnits != 0:
        # Convert the obtained value to inches, then to pixels
        requestedWidth = pm.mel.convertInchesToPixels(pm.mel.convertMeasurement(widthValue, gMeasurementUnitsNames[sizeUnits], "inches"), dpi)
    else: # the width value is in pixels, so no need to convert
        requestedWidth = widthValue

    if pm.about(ev=True):
        if requestedWidth > PLE_MAX_X:
            warnMsg = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kImageResolutionLimited")
            dispMsg = pm.format(warnMsg, s=(PLE_MAX_X, PLE_MAX_Y))
            pm.warning(dispMsg)
            requestedWidth = PLE_MAX_X

    if requestedWidth < 2:
        pm.warning(pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kWidthWarning"))
        requestedWidth = 2

    resNode.width.set(requestedWidth)
    pm.optionMenuGrp('resolutionMenu', edit=True, sl=1)
    checkArnoldAspectLockWidth(resNode)

    # Update the values
    updateArnoldResolution()

    pm.setParent(oldParent)


def changeArnoldAspectLockHeight(*args):
    '''
    Procedure Name:
        changeArnoldAspectLockHeight
    
    Description:
      This procedure is called when the user changes the
      resolution width.  It sets the internal representation
      then looks at the ratio lock etc and changes any other
      values that rely on it.
    '''
    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    heightValue = pm.floatFieldGrp('mayaSoftwareResHeight', q=True, v1=True)

    gMeasurementUnitsNames = pm.melGlobals['gMeasurementUnitsNames']

    resNode = pm.PyNode('defaultResolution')
    dpi = resNode.dotsPerInch.get()
    sizeUnits = resNode.imageSizeUnits.get()

    if sizeUnits != 0:
        # Convert the obtained value to inches, then to pixels
        requestedHeight = pm.mel.convertInchesToPixels(pm.mel.convertMeasurement(heightValue, gMeasurementUnitsNames[sizeUnits], "inches"),dpi)
    else:
        # the width value is in pixels, so no need to convert
        requestedHeight = heightValue

    if pm.about(ev=True):
        if requestedHeight > PLE_MAX_Y:
            warnMsg = pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kImageResolutionLimited")
            dispMsg = pm.format(warnMsg, s=(PLE_MAX_X, PLE_MAX_Y))
            pm.warning(dispMsg)
            requestedHeight = PLE_MAX_Y

    if requestedHeight < 2:
        pm.warning(pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kHeightWarning"))
        requestedHeight = 2

    resNode.height.set(requestedHeight)
    pm.optionMenuGrp('resolutionMenu', edit=True, sl=1)
    checkArnoldAspectLockHeight(resNode)

    # Set the proper field ordering if PAL or NTSC.
    if requestedHeight == 576: # PAL
        resNode.oddFieldFirst.set(0)
        if pm.columnLayout('rgFieldLayout', exists=True):
            if pm.mel.exists('updateFieldOptions'):
                pm.mel.updateFieldOptions()


    elif requestedHeight == 486: # NTSC
        resNode.oddFieldFirst.set(1)
        if pm.columnLayout('rgFieldLayout', exists=True):
            if pm.mel.exists('updateFieldOptions'):
                pm.mel.updateFieldOptions()

    # Update the values
    updateArnoldResolution()

    pm.setParent(oldParent)


def adjustArnoldPixelAspect(node):

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    aspect = node.deviceAspectRatio.get()
    width = node.width.get()
    height = node.height.get()
    pixelAspect = float(width) / float(height)
    pixelAspect = aspect / pixelAspect
    pm.floatFieldGrp('pixRatio', e=True, v1=pixelAspect)

    pm.setParent(oldParent)


def adjustArnoldDeviceAspect(node):

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    devAspect = node.deviceAspectRatio
    width = node.width.get()
    height = node.height.get()

    pixelAspect = pm.floatFieldGrp('pixRatio', q=True, v1=True)
    aspect = float(width) / float(height)
    aspect = pixelAspect * aspect
    pm.setAttr(devAspect, aspect)
    pm.floatFieldGrp('resRatio', edit=True, v1=aspect)

    pm.setParent(oldParent)


def updateArnoldPixelAspectRatio(*args):

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()
    resNode = pm.PyNode('defaultResolution')
    resNode.pixelAspect.set(pm.floatFieldGrp('pixRatio', q=True, v1=True))
    adjustArnoldDeviceAspect(resNode)
    updateArnoldResolution()

    pm.setParent(oldParent)


def updateArnoldDeviceAspectRatio(*args):

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    pm.setAttr('defaultResolution.deviceAspectRatio', pm.floatFieldGrp('resRatio', q=True, v1=True))
    adjustArnoldPixelAspect(pm.PyNode('defaultResolution'))
    updateArnoldResolution()

    pm.setParent(oldParent)


# ----------------------------------------------------------------------------
# Code to update pre/post layer/frame pm.mel callbacks
#

def changeArnoldMelCallbacks(control, attr):

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    val = pm.textFieldGrp(control, query=True, text=True)
    pm.setAttr(attr, val, type="string")

    pm.setParent(oldParent)


def updateArnoldMelCallbacks(*args):

    oldParent = pm.setParent(query=True)
    setParentToArnoldCommonTab()

    pm.textFieldGrp('preRenderLayerMelSwGrp', edit=True, text=pm.getAttr('defaultRenderGlobals.preRenderLayerMel'))
    pm.textFieldGrp('postRenderLayerMelSwGrp', edit=True, text=pm.getAttr('defaultRenderGlobals.postRenderLayerMel'))
    pm.textFieldGrp('preRenderMelSwGrp', edit=True, text=pm.getAttr('defaultRenderGlobals.preRenderMel'))
    pm.textFieldGrp('postRenderMelSwGrp', edit=True, text=pm.getAttr('defaultRenderGlobals.postRenderMel'))

    pm.setParent(oldParent)


# ----------------------------------------------------------------------------
# Code to create and update the Render Options frame
#

def createArnoldCommonRenderOptions():

    parent = pm.setParent(query=True)

    pm.setUITemplate('attributeEditorTemplate', pushTemplate=True)


    pm.columnLayout(adjustableColumn=True)

    pm.attrControlGrp('preMelSwGrp',
                        attribute='defaultRenderGlobals.preMel',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kPreRenderMEL"),
                        preventOverride=True)

    pm.attrControlGrp('postMelSwGrp',
                        attribute='defaultRenderGlobals.postMel',
                        label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kPostRenderMEL"),
                        preventOverride=True)

    pm.textFieldGrp('preRenderLayerMelSwGrp',
                      label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kPreRenderLayerMEL"),
                      changeCommand=pm.Callback(changeArnoldMelCallbacks, "preRenderLayerMelSwGrp", "defaultRenderGlobals.preRenderLayerMel"))

    pm.textFieldGrp('postRenderLayerMelSwGrp',
                      label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kPostRenderLayerMEL"),
                      changeCommand=pm.Callback(changeArnoldMelCallbacks, "postRenderLayerMelSwGrp", "defaultRenderGlobals.postRenderLayerMel"))

    pm.textFieldGrp('preRenderMelSwGrp',
                      label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kPreRenderFrameMEL"),
                      changeCommand=pm.Callback(changeArnoldMelCallbacks, "preRenderMelSwGrp", "defaultRenderGlobals.preRenderMel"))

    pm.textFieldGrp('postRenderMelSwGrp',
                      label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kPostRenderFrameMEL"),
                      changeCommand=pm.Callback(changeArnoldMelCallbacks, "postRenderMelSwGrp", "defaultRenderGlobals.postRenderMel"))

    pm.connectControl('preRenderLayerMelSwGrp', 'defaultRenderGlobals.preRenderLayerMel', index=1)
    pm.connectControl('postRenderLayerMelSwGrp', 'defaultRenderGlobals.postRenderLayerMel', index=1)
    pm.connectControl('preRenderMelSwGrp', 'defaultRenderGlobals.preRenderMel', index=1)
    pm.connectControl('postRenderMelSwGrp', 'defaultRenderGlobals.postRenderMel', index=1)

    if pm.about(evalVersion=True):
        pm.attrControlGrp('preMelSwGrp', e=True, enable=False)
        pm.attrControlGrp('postMelSwGr', e=True, enable=False)
        pm.textFieldGrp('preRenderLayerMelSwGrp', e=True, enable=False)
        pm.textFieldGrp('postRenderLayerMelSwGrp', e=True, enable=False)
        pm.textFieldGrp('preRenderMelSwGrp', e=True, enable=False)
        pm.textFieldGrp('postRenderMelSwGrp', e=True, enable=False)

    updateArnoldMelCallbacks()

    # Set up script jobs for those attributes which require updating of
    # multiple controls.
    # This is especially important when a user changes render layers.
    for attr in ['preRenderLayerMel', 'preRenderLayerMel', 'preRenderMel', 'postRenderMel']:
        plug = 'defaultRenderGlobals.' + attr
        pm.scriptJob(parent = pm.setParent(query=True), attributeChange=(plug, updateArnoldMelCallbacks))

    pm.setParent(parent)
    pm.setUITemplate(popTemplate=True)



#==================================================================
# Common Tab
#==================================================================

def updateArnoldRendererCommonGlobalsTab(*args):

    '''
     Description:
     This procedure is called when the current renderer changes to be the
     Arnold Renderer.
     This procedure updates controls in the Common tab of the Maya Software
     renderer to reflect values which may have been copied from the previous
     current renderer.
    '''
    # Re check for aiOptions node to exists
    core.createOptions()

    updateArnoldFileNamePrefixControl()
    updateArnoldFileNameFormatControl()

    # Must recreate the Image Format option menu because it is renderer specific.
    # This is only required for the master layer layout.
    #
    '''
    if( isDisplayingAllRendererTabs()){

        // Set the correct parent
        setParentToArnoldCommonTab();
        setParent rgImageFileFrame;

        // Recreate the tab
        createArnoldCommonImageFile();
    }
    '''
    updateArnoldImageFormatControl()
    updateArnoldCameraControl()
    updateArnoldResolution()
    updateArnoldMelCallbacks()
    updateArnoldTargetFilePreview()


def createArnoldRendererCommonGlobalsTab():
    '''
     Description:
     This procedure is called when building the render globals tabs for the
     Maya Software renderer.
     This procedure builds the "General" tab for the Maya Software renderer.
    '''

    # Make sure the aiOptions node exists
    core.createOptions()

    parentForm = pm.setParent(query=True)

    createArnoldTargetFilePreview()

    pm.setParent(parentForm)

    pm.scrollLayout('scrollLayout',horizontalScrollBarThickness=0)

    commonTabColumn = pm.columnLayout('commonTabColumn', adjustableColumn=True)

    # Image File Name
    #
    pm.frameLayout('rgImageFileFrame',
                     label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kImageFileOutput"),
                     collapsable=True,
                     collapse=False)

    createArnoldCommonImageFile()

    pm.setParent(commonTabColumn)

    # Frame Range Output
    #
    pm.frameLayout('rgFrameRangeFrame',
                     label="Frame Range",
                     collapsable=True,
                     collapse=False)

    createArnoldCommonFrameRange()

    pm.setParent(commonTabColumn)

    # Renderable Cameras
    #
    pm.frameLayout('rgRenderableCamerasFrame',
                     label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kRenderableCameras"),
                     collapsable=True,
                     collapse=False)


    createArnoldCommonRenderCameras()

    pm.setParent(commonTabColumn)

    # Resolution ("Image Size") Section
    #
    pm.frameLayout('rgResolutionFrame',
                     label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kLayoutImageSize"),
                     collapsable=True,
                     collapse=False)


    createArnoldCommonResolution()

    pm.setParent(commonTabColumn)

    # Render Options
    #
    pm.frameLayout('mayaSoftwareOptionFrame',
                     label=pm.mel.uiRes("m_createMayaSoftwareCommonGlobalsTab.kRenderOptions"),
                     collapsable=True,
                     collapse=True)

    createArnoldCommonRenderOptions()

    pm.setParent(commonTabColumn)

    pm.setParent(parentForm)

    pm.formLayout(parentForm,
                    edit=True,
                    af=[('targetFilePreview',"top", 5),
                        ('targetFilePreview', "left", 0),
                        ('targetFilePreview', "right", 0),
                        ('scrollLayout', "bottom", 0),
                        ('scrollLayout', "left", 0),
                        ('scrollLayout', "right", 0)],
                    an=[('targetFilePreview', "bottom")],
                    ac=[('scrollLayout', "top", 5, 'targetFilePreview')])

    # Update the target file preview.
    #
    updateArnoldTargetFilePreview()
