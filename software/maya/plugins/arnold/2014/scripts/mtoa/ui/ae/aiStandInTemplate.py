import re
import maya.cmds as cmds
import maya.mel as mel
from mtoa.ui.ae.utils import aeCallback
import mtoa.core as core
import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

def LoadStandInButtonPush(nodeName):
    basicFilter = 'Arnold Archive (*.ass *.ass.gz *.obj *.ply);;Arnold Procedural (*.so *.dll *.dylib)'
    projectDir = cmds.workspace(query=True, directory=True)     
    ret = cmds.fileDialog2(fileFilter=basicFilter, cap='Load StandIn',okc='Load',fm=1, startingDirectory=projectDir)
    if ret is not None and len(ret):
        ArnoldStandInDsoEdit(nodeName, ret[0], True)

def ArnoldStandInDsoEdit(nodeName, mPath, replace=False) :
    mArchivePath = ''
    nodeName = nodeName.replace('.dso','')
    
    expression = r''
    if replace:
        # Expression to replace frame numbers by #
        expression = r'(.*?)([\._])([0-9#]*)([\.]?)([0-9#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'
    else:
        expression = r'(.*?)([\._])([#]*)([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'

    # If it is a recogniced format
    if re.search(expression,mPath) != None:
        m_groups = re.search(expression,mPath).groups()
        # Single file
        if not m_groups[2]:
            mArchivePath = mPath
            cmds.setAttr(nodeName+'.useFrameExtension',False)
        # Sequence without subframes    
        elif not m_groups[3]:
            cmds.setAttr(nodeName+'.useFrameExtension',True)
            mArchivePath = m_groups[0]+m_groups[1]+'#'*len(m_groups[2])+m_groups[5]
            cmds.setAttr(nodeName+'.useSubFrame',False)
        # Sequence with subframes
        else:
            cmds.setAttr(nodeName+'.useFrameExtension',True)
            mArchivePath = m_groups[0]+m_groups[1]+'#'*len(m_groups[2])+m_groups[3]+'#'*len(m_groups[4])+m_groups[5]
            cmds.setAttr(nodeName+'.useSubFrame',True)
    # Other
    else:
        mArchivePath = mPath
        
    cmds.setAttr(nodeName+'.dso',mArchivePath,type='string')
    if '.so' in mPath or '.dll' in mPath or '.dylib' in mPath:
        cmds.text('standInDataLabel', edit=True, enable=True)
        cmds.textField('standInData', edit=True, enable=True)
    else:
        cmds.text('standInDataLabel', edit=True, enable=False)
        cmds.textField('standInData', edit=True, enable=False)
    cmds.textField('standInDsoPath', edit=True, text=mArchivePath)

def ArnoldStandInBBoxScaleEdit(mScale) :
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    
    # Update value
    cmds.setAttr(node+'.bboxScale',mScale)
    
def ArnoldStandInDataEdit(mData) :
    # Get AE tab name
    nodeName = mel.eval('$tempNode = $gAECurrentTab')
    
    # Set data
    cmds.setAttr(nodeName+'.data',mData,type='string')

def ArnoldStandInTemplateDsoNew(nodeName) :
    cmds.rowColumnLayout( numberOfColumns=3, columnAlign=[(1, 'right'),(2, 'right'),(3, 'left')], columnAttach=[(1, 'right', 0), (2, 'both', 0), (3, 'left', 5)], columnWidth=[(1,145),(2,220),(3,30)] )
    cmds.text(label='Path ')
    path = cmds.textField('standInDsoPath',changeCommand=lambda *args: ArnoldStandInDsoEdit(nodeName, *args))
    cmds.textField( path, edit=True, text=cmds.getAttr(nodeName) )
    cmds.symbolButton('standInDsoPathButton', image='navButtonBrowse.png', command=lambda *args: LoadStandInButtonPush(nodeName))
    
def ArnoldStandInTemplateDataNew(nodeName) :
    cmds.rowColumnLayout( numberOfColumns=2, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0), (2, 'both', 0)], columnWidth=[(1,145),(2,220)] )
    cmds.text('standInDataLabel', label='Data ')
    path = cmds.textField('standInData',changeCommand=ArnoldStandInDataEdit)
    cmds.textField( path, edit=True, text=cmds.getAttr(nodeName))
    filePath=cmds.getAttr(nodeName.replace('.data','.dso'))
    if filePath:
        if '.so' in filePath or '.dll' in filePath or '.dylib' in filePath:
            cmds.text('standInDataLabel', edit=True, enable=True)
            cmds.textField('standInData', edit=True, enable=True)
    else:
        cmds.text('standInDataLabel', edit=True, enable=False)
        cmds.textField('standInData', edit=True, enable=False)

def ArnoldStandInTemplateDsoReplace(plugName) :
    cmds.textField( 'standInDsoPath', edit=True, changeCommand=lambda *args: ArnoldStandInDsoEdit(plugName, *args))
    cmds.textField( 'standInDsoPath', edit=True, text=cmds.getAttr(plugName) )
    cmds.symbolButton('standInDsoPathButton', edit=True, image='navButtonBrowse.png' , command=lambda *args: LoadStandInButtonPush(plugName))

def ArnoldStandInTemplateDataReplace(plugName) :
    cmds.textField( 'standInData', edit=True, text=cmds.getAttr(plugName) )
    filePath=cmds.getAttr(plugName.replace('.data','.dso'))
    if filePath:
        if '.so' in filePath or '.dll' in filePath or '.dylib' in filePath:
            cmds.text('standInDataLabel', edit=True, enable=True)
            cmds.textField('standInData', edit=True, enable=True)
    else:
        cmds.text('standInDataLabel', edit=True, enable=False)
        cmds.textField('standInData', edit=True, enable=False)

def deferStandinLoadChange(nodeName):
    status = cmds.getAttr(nodeName+'.deferStandinLoad')
    if status == False:
        cmds.floatField('standInBBoxScale', edit=True, enable=False)
        cmds.text('standInBBoxScaleLabel', edit=True, enable=False)
    else:
        cmds.floatField('standInBBoxScale', edit=True, enable=True)
        cmds.text('standInBBoxScaleLabel', edit=True, enable=True)

def ArnoldStandInTemplateBBoxScaleNew(nodeName) :
    cmds.rowColumnLayout( numberOfColumns=2, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0), (2, 'left', 0)], columnWidth=[(1,145),(2,70)] )
    cmds.text('standInBBoxScaleLabel', label='Bounding Box Scale ', enable=False)
    path = cmds.floatField('standInBBoxScale', changeCommand=ArnoldStandInBBoxScaleEdit)
    cmds.floatField(path, edit=True, value=cmds.getAttr(nodeName), enable=False)
        
def ArnoldStandInTemplateBBoxScaleReplace(plugName) :
    cmds.floatField('standInBBoxScale', edit=True, value=cmds.getAttr(plugName) )

# #################################
# #################################
# Override Table
# #################################
# #################################
    
def ArnoldStandInTemplateOverrideTableNew(nodeName):
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    cmds.text('standInOverrideLabel1', label=' ')
    cmds.text('standInOverrideLabel2', label=' ')
    cmds.text('standInOverrideLabel3', label='Mute', align='left')
    cmds.text('standInOverrideLabel4', label='On', align='left')
    cmds.text('standInOverrideLabel5', label='Off', align='left')


def ArnoldStandInTemplateOverrideTableReplace(nodeName):
    pass

# #################################
# Opaque Row
# #################################
    
def ArnoldStandInTemplateSetIgnoreOpaque(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideOpaque',False)
    cmds.text('standInOpaqueLabel', edit=True, enable=False)
    
def ArnoldStandInTemplateSetOnOpaque(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideOpaque',True)
    cmds.setAttr(node+'.aiOpaque',True)
    cmds.text('standInOpaqueLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSetOffOpaque(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideOpaque',True)
    cmds.setAttr(node+'.aiOpaque',False)
    cmds.text('standInOpaqueLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateOpaqueRowNew(nodeName):
    nodeName = nodeName.replace('.opaqueRow','')
    override = value=cmds.getAttr(nodeName+'.overrideOpaque')
    opaque = value=cmds.getAttr(nodeName+'.aiOpaque')
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    
    cmds.text('standInOpaqueLabel', label='Opaque')
    cmds.text('standInOpaqueOverrideLabel6', label=' ')
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('standInOpaqueIgnore', label=' ', onCommand=ArnoldStandInTemplateSetIgnoreOpaque)
    rb2 = cmds.radioButton('standInOpaqueOn', label=' ' , onCommand=ArnoldStandInTemplateSetOnOpaque)
    rb3 = cmds.radioButton('standInOpaqueOff', label=' ' , onCommand=ArnoldStandInTemplateSetOffOpaque)
    if(not override):
        cmds.radioButton(rb1, edit=True, select=True)
        cmds.text('standInOpaqueLabel', edit=True, enable=False)
    elif(opaque):
        cmds.radioButton(rb2, edit=True, select=True)
    else:
        cmds.radioButton(rb3, edit=True, select=True)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def ArnoldStandInTemplateOpaqueRowReplace(nodeName):
    nodeName = nodeName.replace('.opaqueRow','')
    override = value=cmds.getAttr(nodeName+'.overrideOpaque')
    opaque = value=cmds.getAttr(nodeName+'.aiOpaque')
    
    if(not override):
        cmds.radioButton('standInOpaqueIgnore', edit=True, select=True)
        cmds.text('standInOpaqueLabel', edit=True, enable=False)
    elif(opaque):
        cmds.radioButton('standInOpaqueOn', edit=True, select=True)
        cmds.text('standInOpaqueLabel', edit=True, enable=True)
    else:
        cmds.radioButton('standInOpaqueOff', edit=True, select=True)
        cmds.text('standInOpaqueLabel', edit=True, enable=True)
        
# #################################
# Double Sided Row
# #################################

def ArnoldStandInTemplateSetIgnoreDoubleSided(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideDoubleSided',False)
    cmds.text('standInDoubleSidedLabel', edit=True, enable=False)
    
def ArnoldStandInTemplateSetOnDoubleSided(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideDoubleSided',True)
    cmds.setAttr(node+'.doubleSided',True)
    cmds.text('standInDoubleSidedLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSetOffDoubleSided(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideDoubleSided',True)
    cmds.setAttr(node+'.doubleSided',False)
    cmds.text('standInDoubleSidedLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateDoubleSidedRowNew(nodeName):
    nodeName = nodeName.replace('.doubleSidedRow','')
    override = value=cmds.getAttr(nodeName+'.overrideDoubleSided')
    doubleSided = value=cmds.getAttr(nodeName+'.doubleSided')
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    
    cmds.text('standInDoubleSidedLabel', label='Double Sided')
    cmds.text('standInDoubleSidedOverrideLabel6', label=' ')
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('standInDoubleSidedIgnore', label=' ', onCommand=ArnoldStandInTemplateSetIgnoreDoubleSided)
    rb2 = cmds.radioButton('standInDoubleSidedOn', label=' ' , onCommand=ArnoldStandInTemplateSetOnDoubleSided)
    rb3 = cmds.radioButton('standInDoubleSidedOff', label=' ' , onCommand=ArnoldStandInTemplateSetOffDoubleSided)
    if(not override):
        cmds.radioButton(rb1, edit=True, select=True)
        cmds.text('standInDoubleSidedLabel', edit=True, enable=False)
    elif(doubleSided):
        cmds.radioButton(rb2, edit=True, select=True)
    else:
        cmds.radioButton(rb3, edit=True, select=True)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def ArnoldStandInTemplateDoubleSidedRowReplace(nodeName):
    nodeName = nodeName.replace('.doubleSidedRow','')
    override = value=cmds.getAttr(nodeName+'.overrideDoubleSided')
    opaque = value=cmds.getAttr(nodeName+'.doubleSided')
    
    if(not override):
        cmds.radioButton('standInDoubleSidedIgnore', edit=True, select=True)
        cmds.text('standInDoubleSidedLabel', edit=True, enable=False)
    elif(opaque):
        cmds.radioButton('standInDoubleSidedOn', edit=True, select=True)
        cmds.text('standInDoubleSidedLabel', edit=True, enable=True)
    else:
        cmds.radioButton('standInDoubleSidedOff', edit=True, select=True)
        cmds.text('standInDoubleSidedLabel', edit=True, enable=True)
        
        
# #################################
# Double Receive Shadows
# #################################

def ArnoldStandInTemplateSetIgnoreReceiveShadows(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideReceiveShadows',False)
    cmds.text('standInReceiveShadowsLabel', edit=True, enable=False)
    
def ArnoldStandInTemplateSetOnReceiveShadows(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideReceiveShadows',True)
    cmds.setAttr(node+'.receiveShadows',True)
    cmds.text('standInReceiveShadowsLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSetOffReceiveShadows(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideReceiveShadows',True)
    cmds.setAttr(node+'.receiveShadows',False)
    cmds.text('standInReceiveShadowsLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateReceiveShadowsRowNew(nodeName):
    nodeName = nodeName.replace('.receiveShadowsRow','')
    override = value=cmds.getAttr(nodeName+'.overrideReceiveShadows')
    receiveShadows = value=cmds.getAttr(nodeName+'.receiveShadows')
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    
    cmds.text('standInReceiveShadowsLabel', label='Receive Shadows')
    cmds.text('standInReceiveShadowsOverrideLabel6', label=' ')
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('standInReceiveShadowsIgnore', label=' ', onCommand=ArnoldStandInTemplateSetIgnoreReceiveShadows)
    rb2 = cmds.radioButton('standInReceiveShadowsOn', label=' ' , onCommand=ArnoldStandInTemplateSetOnReceiveShadows)
    rb3 = cmds.radioButton('standInReceiveShadowsOff', label=' ' , onCommand=ArnoldStandInTemplateSetOffReceiveShadows)
    if(not override):
        cmds.radioButton(rb1, edit=True, select=True)
        cmds.text('standInReceiveShadowsLabel', edit=True, enable=False)
    elif(receiveShadows):
        cmds.radioButton(rb2, edit=True, select=True)
    else:
        cmds.radioButton(rb3, edit=True, select=True)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def ArnoldStandInTemplateReceiveShadowsRowReplace(nodeName):
    nodeName = nodeName.replace('.receiveShadowsRow','')
    override = value=cmds.getAttr(nodeName+'.overrideReceiveShadows')
    opaque = value=cmds.getAttr(nodeName+'.receiveShadows')
    
    if(not override):
        cmds.radioButton('standInReceiveShadowsIgnore', edit=True, select=True)
        cmds.text('standInReceiveShadowsLabel', edit=True, enable=False)
    elif(opaque):
        cmds.radioButton('standInReceiveShadowsOn', edit=True, select=True)
        cmds.text('standInReceiveShadowsLabel', edit=True, enable=True)
    else:
        cmds.radioButton('standInReceiveShadowsOff', edit=True, select=True)
        cmds.text('standInReceiveShadowsLabel', edit=True, enable=True)
        
# #################################
# Double Self Shadows
# #################################

def ArnoldStandInTemplateSetIgnoreSelfShadows(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideSelfShadows',False)
    cmds.text('standInSelfShadowsLabel', edit=True, enable=False)
    
def ArnoldStandInTemplateSetOnSelfShadows(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideSelfShadows',True)
    cmds.setAttr(node+'.aiSelfShadows',True)
    cmds.text('standInSelfShadowsLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSetOffSelfShadows(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideSelfShadows',True)
    cmds.setAttr(node+'.aiSelfShadows',False)
    cmds.text('standInSelfShadowsLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSelfShadowsRowNew(nodeName):
    nodeName = nodeName.replace('.selfShadowsRow','')
    override = value=cmds.getAttr(nodeName+'.overrideSelfShadows')
    selfShadows = value=cmds.getAttr(nodeName+'.aiSelfShadows')
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    
    cmds.text('standInSelfShadowsLabel', label='Self Shadows')
    cmds.text('standInSelfShadowsOverrideLabel6', label=' ')
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('standInSelfShadowsIgnore', label=' ', onCommand=ArnoldStandInTemplateSetIgnoreSelfShadows)
    rb2 = cmds.radioButton('standInSelfShadowsOn', label=' ' , onCommand=ArnoldStandInTemplateSetOnSelfShadows)
    rb3 = cmds.radioButton('standInSelfShadowsOff', label=' ' , onCommand=ArnoldStandInTemplateSetOffSelfShadows)
    if(not override):
        cmds.radioButton(rb1, edit=True, select=True)
        cmds.text('standInSelfShadowsLabel', edit=True, enable=False)
    elif(selfShadows):
        cmds.radioButton(rb2, edit=True, select=True)
    else:
        cmds.radioButton(rb3, edit=True, select=True)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def ArnoldStandInTemplateSelfShadowsRowReplace(nodeName):
    nodeName = nodeName.replace('.selfShadowsRow','')
    override = value=cmds.getAttr(nodeName+'.overrideSelfShadows')
    opaque = value=cmds.getAttr(nodeName+'.aiSelfShadows')
    
    if(not override):
        cmds.radioButton('standInSelfShadowsIgnore', edit=True, select=True)
        cmds.text('standInSelfShadowsLabel', edit=True, enable=False)
    elif(opaque):
        cmds.radioButton('standInSelfShadowsOn', edit=True, select=True)
        cmds.text('standInSelfShadowsLabel', edit=True, enable=True)
    else:
        cmds.radioButton('standInSelfShadowsOff', edit=True, select=True)
        cmds.text('standInSelfShadowsLabel', edit=True, enable=True)
        
# #################################
# Double Casts Shadows
# #################################

def ArnoldStandInTemplateSetIgnoreCastsShadows(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideCastsShadows',False)
    cmds.text('standInCastsShadowsLabel', edit=True, enable=False)
    
def ArnoldStandInTemplateSetOnCastsShadows(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideCastsShadows',True)
    cmds.setAttr(node+'.castsShadows',True)
    cmds.text('standInCastsShadowsLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSetOffCastsShadows(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideCastsShadows',True)
    cmds.setAttr(node+'.castsShadows',False)
    cmds.text('standInCastsShadowsLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateCastsShadowsRowNew(nodeName):
    nodeName = nodeName.replace('.castsShadowsRow','')
    override = value=cmds.getAttr(nodeName+'.overrideCastsShadows')
    castsShadows = value=cmds.getAttr(nodeName+'.castsShadows')
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    
    cmds.text('standInCastsShadowsLabel', label='Casts Shadows')
    cmds.text('standInCastsShadowsOverrideLabel6', label=' ')
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('standInCastsShadowsIgnore', label=' ', onCommand=ArnoldStandInTemplateSetIgnoreCastsShadows)
    rb2 = cmds.radioButton('standInCastsShadowsOn', label=' ' , onCommand=ArnoldStandInTemplateSetOnCastsShadows, visible=False)
    rb3 = cmds.radioButton('standInCastsShadowsOff', label=' ' , onCommand=ArnoldStandInTemplateSetOffCastsShadows)
    if(not override):
        cmds.radioButton(rb1, edit=True, select=True)
        cmds.text('standInCastsShadowsLabel', edit=True, enable=False)
    elif(castsShadows):
        cmds.radioButton(rb2, edit=True, select=True)
    else:
        cmds.radioButton(rb3, edit=True, select=True)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def ArnoldStandInTemplateCastsShadowsRowReplace(nodeName):
    nodeName = nodeName.replace('.castsShadowsRow','')
    override = value=cmds.getAttr(nodeName+'.overrideCastsShadows')
    opaque = value=cmds.getAttr(nodeName+'.castsShadows')
    
    if(not override):
        cmds.radioButton('standInCastsShadowsIgnore', edit=True, select=True)
        cmds.text('standInCastsShadowsLabel', edit=True, enable=False)
    elif(opaque):
        cmds.radioButton('standInCastsShadowsOn', edit=True, select=True)
        cmds.text('standInCastsShadowsLabel', edit=True, enable=True)
    else:
        cmds.radioButton('standInCastsShadowsOff', edit=True, select=True)
        cmds.text('standInCastsShadowsLabel', edit=True, enable=True)
        
# #################################
# Double Primary Visibility
# #################################

def ArnoldStandInTemplateSetIgnorePrimaryVisibility(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overridePrimaryVisibility',False)
    cmds.text('standInPrimaryVisibilityLabel', edit=True, enable=False)
    
def ArnoldStandInTemplateSetOnPrimaryVisibility(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overridePrimaryVisibility',True)
    cmds.setAttr(node+'.primaryVisibility',True)
    cmds.text('standInPrimaryVisibilityLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSetOffPrimaryVisibility(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overridePrimaryVisibility',True)
    cmds.setAttr(node+'.primaryVisibility',False)
    cmds.text('standInPrimaryVisibilityLabel', edit=True, enable=True)
    
def ArnoldStandInTemplatePrimaryVisibilityRowNew(nodeName):
    nodeName = nodeName.replace('.primaryVisibilityRow','')
    override = value=cmds.getAttr(nodeName+'.overridePrimaryVisibility')
    primaryVisibility = value=cmds.getAttr(nodeName+'.primaryVisibility')
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    
    cmds.text('standInPrimaryVisibilityLabel', label='Primary Visibility')
    cmds.text('standInPrimaryVisibilityOverrideLabel6', label=' ')
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('standInPrimaryVisibilityIgnore', label=' ', onCommand=ArnoldStandInTemplateSetIgnorePrimaryVisibility)
    rb2 = cmds.radioButton('standInPrimaryVisibilityOn', label=' ' , onCommand=ArnoldStandInTemplateSetOnPrimaryVisibility, visible=False)
    rb3 = cmds.radioButton('standInPrimaryVisibilityOff', label=' ' , onCommand=ArnoldStandInTemplateSetOffPrimaryVisibility)
    if(not override):
        cmds.radioButton(rb1, edit=True, select=True)
        cmds.text('standInPrimaryVisibilityLabel', edit=True, enable=False)
    elif(primaryVisibility):
        cmds.radioButton(rb2, edit=True, select=True)
    else:
        cmds.radioButton(rb3, edit=True, select=True)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def ArnoldStandInTemplatePrimaryVisibilityRowReplace(nodeName):
    nodeName = nodeName.replace('.primaryVisibilityRow','')
    override = value=cmds.getAttr(nodeName+'.overridePrimaryVisibility')
    opaque = value=cmds.getAttr(nodeName+'.primaryVisibility')
    
    if(not override):
        cmds.radioButton('standInPrimaryVisibilityIgnore', edit=True, select=True)
        cmds.text('standInPrimaryVisibilityLabel', edit=True, enable=False)
    elif(opaque):
        cmds.radioButton('standInPrimaryVisibilityOn', edit=True, select=True)
        cmds.text('standInPrimaryVisibilityLabel', edit=True, enable=True)
    else:
        cmds.radioButton('standInPrimaryVisibilityOff', edit=True, select=True)
        cmds.text('standInPrimaryVisibilityLabel', edit=True, enable=True)
        
# #################################
# Double Visible In Reflections
# #################################

def ArnoldStandInTemplateSetIgnoreVisibleInReflections(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInReflections',False)
    cmds.text('standInVisibleInReflectionsLabel', edit=True, enable=False)
    
def ArnoldStandInTemplateSetOnVisibleInReflections(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInReflections',True)
    cmds.setAttr(node+'.visibleInReflections',True)
    cmds.text('standInVisibleInReflectionsLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSetOffVisibleInReflections(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInReflections',True)
    cmds.setAttr(node+'.visibleInReflections',False)
    cmds.text('standInVisibleInReflectionsLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateVisibleInReflectionsRowNew(nodeName):
    nodeName = nodeName.replace('.visibleInReflectionsRow','')
    override = value=cmds.getAttr(nodeName+'.overrideVisibleInReflections')
    visibleInReflections = value=cmds.getAttr(nodeName+'.visibleInReflections')
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    
    cmds.text('standInVisibleInReflectionsLabel', label='Visible In Reflections')
    cmds.text('standInVisibleInReflectionsOverrideLabel6', label=' ')
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('standInVisibleInReflectionsIgnore', label=' ', onCommand=ArnoldStandInTemplateSetIgnoreVisibleInReflections)
    rb2 = cmds.radioButton('standInVisibleInReflectionsOn', label=' ' , onCommand=ArnoldStandInTemplateSetOnVisibleInReflections, visible=False)
    rb3 = cmds.radioButton('standInVisibleInReflectionsOff', label=' ' , onCommand=ArnoldStandInTemplateSetOffVisibleInReflections)
    if(not override):
        cmds.radioButton(rb1, edit=True, select=True)
        cmds.text('standInVisibleInReflectionsLabel', edit=True, enable=False)
    elif(visibleInReflections):
        cmds.radioButton(rb2, edit=True, select=True)
    else:
        cmds.radioButton(rb3, edit=True, select=True)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def ArnoldStandInTemplateVisibleInReflectionsRowReplace(nodeName):
    nodeName = nodeName.replace('.visibleInReflectionsRow','')
    override = value=cmds.getAttr(nodeName+'.overrideVisibleInReflections')
    opaque = value=cmds.getAttr(nodeName+'.visibleInReflections')
    
    if(not override):
        cmds.radioButton('standInVisibleInReflectionsIgnore', edit=True, select=True)
        cmds.text('standInVisibleInReflectionsLabel', edit=True, enable=False)
    elif(opaque):
        cmds.radioButton('standInVisibleInReflectionsOn', edit=True, select=True)
        cmds.text('standInVisibleInReflectionsLabel', edit=True, enable=True)
    else:
        cmds.radioButton('standInVisibleInReflectionsOff', edit=True, select=True)
        cmds.text('standInVisibleInReflectionsLabel', edit=True, enable=True)
        
        
# #################################
# Double Visible In Refractions
# #################################

def ArnoldStandInTemplateSetIgnoreVisibleInRefractions(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInRefractions',False)
    cmds.text('standInVisibleInRefractionsLabel', edit=True, enable=False)
    
def ArnoldStandInTemplateSetOnVisibleInRefractions(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInRefractions',True)
    cmds.setAttr(node+'.visibleInRefractions',True)
    cmds.text('standInVisibleInRefractionsLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSetOffVisibleInRefractions(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInRefractions',True)
    cmds.setAttr(node+'.visibleInRefractions',False)
    cmds.text('standInVisibleInRefractionsLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateVisibleInRefractionsRowNew(nodeName):
    nodeName = nodeName.replace('.visibleInRefractionsRow','')
    override = value=cmds.getAttr(nodeName+'.overrideVisibleInRefractions')
    visibleInRefractions = value=cmds.getAttr(nodeName+'.visibleInRefractions')
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    
    cmds.text('standInVisibleInRefractionsLabel', label='Visible In Refractions')
    cmds.text('standInVisibleInRefractionsOverrideLabel6', label=' ')
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('standInVisibleInRefractionsIgnore', label=' ', onCommand=ArnoldStandInTemplateSetIgnoreVisibleInRefractions)
    rb2 = cmds.radioButton('standInVisibleInRefractionsOn', label=' ' , onCommand=ArnoldStandInTemplateSetOnVisibleInRefractions, visible=False)
    rb3 = cmds.radioButton('standInVisibleInRefractionsOff', label=' ' , onCommand=ArnoldStandInTemplateSetOffVisibleInRefractions)
    if(not override):
        cmds.radioButton(rb1, edit=True, select=True)
        cmds.text('standInVisibleInRefractionsLabel', edit=True, enable=False)
    elif(visibleInRefractions):
        cmds.radioButton(rb2, edit=True, select=True)
    else:
        cmds.radioButton(rb3, edit=True, select=True)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def ArnoldStandInTemplateVisibleInRefractionsRowReplace(nodeName):
    nodeName = nodeName.replace('.visibleInRefractionsRow','')
    override = value=cmds.getAttr(nodeName+'.overrideVisibleInRefractions')
    opaque = value=cmds.getAttr(nodeName+'.visibleInRefractions')
    
    if(not override):
        cmds.radioButton('standInVisibleInRefractionsIgnore', edit=True, select=True)
        cmds.text('standInVisibleInRefractionsLabel', edit=True, enable=False)
    elif(opaque):
        cmds.radioButton('standInVisibleInRefractionsOn', edit=True, select=True)
        cmds.text('standInVisibleInRefractionsLabel', edit=True, enable=True)
    else:
        cmds.radioButton('standInVisibleInRefractionsOff', edit=True, select=True)
        cmds.text('standInVisibleInRefractionsLabel', edit=True, enable=True)
        
        
# #################################
# Double Visible In Diffuse
# #################################

def ArnoldStandInTemplateSetIgnoreVisibleInDiffuse(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInDiffuse',False)
    cmds.text('standInVisibleInDiffuseLabel', edit=True, enable=False)
    
def ArnoldStandInTemplateSetOnVisibleInDiffuse(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInDiffuse',True)
    cmds.setAttr(node+'.aiVisibleInDiffuse',True)
    cmds.text('standInVisibleInDiffuseLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSetOffVisibleInDiffuse(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInDiffuse',True)
    cmds.setAttr(node+'.aiVisibleInDiffuse',False)
    cmds.text('standInVisibleInDiffuseLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateVisibleInDiffuseRowNew(nodeName):
    nodeName = nodeName.replace('.visibleInDiffuseRow','')
    override = value=cmds.getAttr(nodeName+'.overrideVisibleInDiffuse')
    visibleInDiffuse = value=cmds.getAttr(nodeName+'.aiVisibleInDiffuse')
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    
    cmds.text('standInVisibleInDiffuseLabel', label='Visible In Diffuse')
    cmds.text('standInVisibleInDiffuseOverrideLabel6', label=' ')
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('standInVisibleInDiffuseIgnore', label=' ', onCommand=ArnoldStandInTemplateSetIgnoreVisibleInDiffuse)
    rb2 = cmds.radioButton('standInVisibleInDiffuseOn', label=' ' , onCommand=ArnoldStandInTemplateSetOnVisibleInDiffuse, visible=False)
    rb3 = cmds.radioButton('standInVisibleInDiffuseOff', label=' ' , onCommand=ArnoldStandInTemplateSetOffVisibleInDiffuse)
    if(not override):
        cmds.radioButton(rb1, edit=True, select=True)
        cmds.text('standInVisibleInDiffuseLabel', edit=True, enable=False)
    elif(visibleInDiffuse):
        cmds.radioButton(rb2, edit=True, select=True)
    else:
        cmds.radioButton(rb3, edit=True, select=True)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def ArnoldStandInTemplateVisibleInDiffuseRowReplace(nodeName):
    nodeName = nodeName.replace('.visibleInDiffuseRow','')
    override = value=cmds.getAttr(nodeName+'.overrideVisibleInDiffuse')
    opaque = value=cmds.getAttr(nodeName+'.aiVisibleInDiffuse')
    
    if(not override):
        cmds.radioButton('standInVisibleInDiffuseIgnore', edit=True, select=True)
        cmds.text('standInVisibleInDiffuseLabel', edit=True, enable=False)
    elif(opaque):
        cmds.radioButton('standInVisibleInDiffuseOn', edit=True, select=True)
        cmds.text('standInVisibleInDiffuseLabel', edit=True, enable=True)
    else:
        cmds.radioButton('standInVisibleInDiffuseOff', edit=True, select=True)
        cmds.text('standInVisibleInDiffuseLabel', edit=True, enable=True)
        
        
# #################################
# Double Visible In Glossy
# #################################

def ArnoldStandInTemplateSetIgnoreVisibleInGlossy(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInGlossy',False)
    cmds.text('standInVisibleInGlossyLabel', edit=True, enable=False)
    
def ArnoldStandInTemplateSetOnVisibleInGlossy(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInGlossy',True)
    cmds.setAttr(node+'.aiVisibleInGlossy',True)
    cmds.text('standInVisibleInGlossyLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSetOffVisibleInGlossy(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideVisibleInGlossy',True)
    cmds.setAttr(node+'.aiVisibleInGlossy',False)
    cmds.text('standInVisibleInGlossyLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateVisibleInGlossyRowNew(nodeName):
    nodeName = nodeName.replace('.visibleInGlossyRow','')
    override = value=cmds.getAttr(nodeName+'.overrideVisibleInGlossy')
    visibleInGlossy = value=cmds.getAttr(nodeName+'.aiVisibleInGlossy')
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    
    cmds.text('standInVisibleInGlossyLabel', label='Visible In Glossy')
    cmds.text('standInVisibleInGlossyOverrideLabel6', label=' ')
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('standInVisibleInGlossyIgnore', label=' ', onCommand=ArnoldStandInTemplateSetIgnoreVisibleInGlossy)
    rb2 = cmds.radioButton('standInVisibleInGlossyOn', label=' ' , onCommand=ArnoldStandInTemplateSetOnVisibleInGlossy, visible=False)
    rb3 = cmds.radioButton('standInVisibleInGlossyOff', label=' ' , onCommand=ArnoldStandInTemplateSetOffVisibleInGlossy)
    if(not override):
        cmds.radioButton(rb1, edit=True, select=True)
        cmds.text('standInVisibleInGlossyLabel', edit=True, enable=False)
    elif(visibleInGlossy):
        cmds.radioButton(rb2, edit=True, select=True)
    else:
        cmds.radioButton(rb3, edit=True, select=True)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def ArnoldStandInTemplateVisibleInGlossyRowReplace(nodeName):
    nodeName = nodeName.replace('.visibleInGlossyRow','')
    override = value=cmds.getAttr(nodeName+'.overrideVisibleInGlossy')
    opaque = value=cmds.getAttr(nodeName+'.aiVisibleInGlossy')
    
    if(not override):
        cmds.radioButton('standInVisibleInGlossyIgnore', edit=True, select=True)
        cmds.text('standInVisibleInGlossyLabel', edit=True, enable=False)
    elif(opaque):
        cmds.radioButton('standInVisibleInGlossyOn', edit=True, select=True)
        cmds.text('standInVisibleInGlossyLabel', edit=True, enable=True)
    else:
        cmds.radioButton('standInVisibleInGlossyOff', edit=True, select=True)
        cmds.text('standInVisibleInGlossyLabel', edit=True, enable=True)
        
# #################################
# Matte Row
# #################################
    
def ArnoldStandInTemplateSetIgnoreMatte(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideMatte',False)
    cmds.text('standInMatteLabel', edit=True, enable=False)
    
def ArnoldStandInTemplateSetOnMatte(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideMatte',True)
    cmds.setAttr(node+'.aiMatte',True)
    cmds.text('standInMatteLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateSetOffMatte(test):
    # Get AE tab name
    node = mel.eval('$tempNode = $gAECurrentTab')
    cmds.setAttr(node+'.overrideMatte',True)
    cmds.setAttr(node+'.aiMatte',False)
    cmds.text('standInMatteLabel', edit=True, enable=True)
    
def ArnoldStandInTemplateMatteRowNew(nodeName):
    nodeName = nodeName.replace('.matteRow','')
    override = value=cmds.getAttr(nodeName+'.overrideMatte')
    matte = value=cmds.getAttr(nodeName+'.aiMatte')
    
    cmds.rowColumnLayout( numberOfColumns=5, columnAlign=(1, 'right'), columnAttach=[(1, 'right', 0)], columnWidth=[(1,145),(2,20),(3,50),(4,50),(5,50)] )
    
    cmds.text('standInMatteLabel', label='Matte')
    cmds.text('standInMatteOverrideLabel6', label=' ')
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('standInMatteIgnore', label=' ', onCommand=ArnoldStandInTemplateSetIgnoreMatte)
    rb2 = cmds.radioButton('standInMatteOn', label=' ' , onCommand=ArnoldStandInTemplateSetOnMatte)
    rb3 = cmds.radioButton('standInMatteOff', label=' ' , onCommand=ArnoldStandInTemplateSetOffMatte)
    if(not override):
        cmds.radioButton(rb1, edit=True, select=True)
        cmds.text('standInMatteLabel', edit=True, enable=False)
    elif(matte):
        cmds.radioButton(rb2, edit=True, select=True)
    else:
        cmds.radioButton(rb3, edit=True, select=True)
    cmds.setParent( '..' )
    cmds.setParent( '..' )

def ArnoldStandInTemplateMatteRowReplace(nodeName):
    nodeName = nodeName.replace('.matteRow','')
    override = value=cmds.getAttr(nodeName+'.overrideMatte')
    matte = value=cmds.getAttr(nodeName+'.aiMatte')
    
    if(not override):
        cmds.radioButton('standInMatteIgnore', edit=True, select=True)
        cmds.text('standInMatteLabel', edit=True, enable=False)
    elif(matte):
        cmds.radioButton('standInMatteOn', edit=True, select=True)
        cmds.text('standInMatteLabel', edit=True, enable=True)
    else:
        cmds.radioButton('standInMatteOff', edit=True, select=True)
        cmds.text('standInMatteLabel', edit=True, enable=True)

        
        
class AEaiStandInTemplate(ShaderAETemplate):
    def setup(self):
        self.beginScrollLayout()
        
        self.beginLayout('File/Frame', collapse=False)        
        self.addCustom('dso', ArnoldStandInTemplateDsoNew, ArnoldStandInTemplateDsoReplace)
        self.addCustom('data', ArnoldStandInTemplateDataNew, ArnoldStandInTemplateDataReplace)
        self.addControl('standInDrawOverride', label='Viewport Override')
        self.addControl('mode', label='Viewport Draw Mode')
        self.addSeparator()
        self.addControl('frameNumber', label='Frame')
        self.addControl('frameOffset')
        
        self.addSeparator()
        self.addControl('deferStandinLoad', label='Defer StandIn Load', changeCommand=deferStandinLoadChange)
        self.addCustom('bboxScale', ArnoldStandInTemplateBBoxScaleNew, ArnoldStandInTemplateBBoxScaleReplace)
        self.endLayout()
        
        self.beginLayout('Render Stats', collapse=True)
        self.beginNoOptimize()
        
        self.addControl('motionBlur')
        
        self.addSeparator()
        
        self.addControl('overrideLightLinking', label='Override StandIn Light Linking')
        self.addControl('overrideShaders', label='Override StandIn Shaders')
        
        self.addSeparator()
        
        self.addCustom('overrideTable', ArnoldStandInTemplateOverrideTableNew, ArnoldStandInTemplateOverrideTableReplace)

        self.addCustom('castsShadowsRow', ArnoldStandInTemplateCastsShadowsRowNew, ArnoldStandInTemplateCastsShadowsRowReplace)
        self.addCustom('receiveShadowsRow', ArnoldStandInTemplateReceiveShadowsRowNew, ArnoldStandInTemplateReceiveShadowsRowReplace)
        self.addCustom('primaryVisibilityRow', ArnoldStandInTemplatePrimaryVisibilityRowNew, ArnoldStandInTemplatePrimaryVisibilityRowReplace)
        self.addCustom('visibleInReflectionsRow', ArnoldStandInTemplateVisibleInReflectionsRowNew, ArnoldStandInTemplateVisibleInReflectionsRowReplace)
        self.addCustom('visibleInRefractionsRow', ArnoldStandInTemplateVisibleInRefractionsRowNew, ArnoldStandInTemplateVisibleInRefractionsRowReplace)
        self.addCustom('doubleSidedRow', ArnoldStandInTemplateDoubleSidedRowNew, ArnoldStandInTemplateDoubleSidedRowReplace)
        self.addCustom('selfShadowsRow', ArnoldStandInTemplateSelfShadowsRowNew, ArnoldStandInTemplateSelfShadowsRowReplace)
        self.addCustom('opaqueRow', ArnoldStandInTemplateOpaqueRowNew, ArnoldStandInTemplateOpaqueRowReplace)
        self.addCustom('visibleInDiffuseRow', ArnoldStandInTemplateVisibleInDiffuseRowNew, ArnoldStandInTemplateVisibleInDiffuseRowReplace)
        self.addCustom('visibleInGlossyRow', ArnoldStandInTemplateVisibleInGlossyRowNew, ArnoldStandInTemplateVisibleInGlossyRowReplace)
        self.addCustom('matteRow', ArnoldStandInTemplateMatteRowNew, ArnoldStandInTemplateMatteRowReplace)

        self.endNoOptimize()
        self.endLayout()
        
        
        self.beginLayout('Object Display', collapse=True)
        self.addControl('visibility')
        self.addControl('template')
        self.addControl('ghosting')
        self.addControl('intermediateObject')
        self.endLayout()
        
        self.beginLayout('Draw Override', collapse=True)
        self.addControl('overrideDisplayType')
        self.addControl('overrideLevelOfDetail')
        self.addControl('overrideShading')
        self.addControl('overrideTexturing')
        self.addControl('overridePlayback')
        self.addControl('overrideEnabled')
        self.addControl('useObjectColor')
        self.addControl('objectColor')
        self.endLayout()
    

        # include/call base class/node attributes
        pm.mel.AEdependNodeTemplate(self.nodeName)
        
        self.suppress('blackBox')
        self.suppress('containerType')
        self.suppress('templateName')
        self.suppress('viewName')
        self.suppress('iconName')
        self.suppress('templateVersion')
        self.suppress('uiTreatment')
        self.suppress('customTreatment')
        self.suppress('creator')
        self.suppress('creationDate')
        self.suppress('rmbCommand')
        self.suppress('templatePath')
        self.suppress('viewMode')
        self.suppress('ignoreHwShader')
        self.suppress('boundingBoxScale')
        self.suppress('featureDisplacement')
        self.suppress('boundingBoxScale')
        self.suppress('initialSampleRate')
        self.suppress('extraSampleRate')
        self.suppress('textureThreshold')
        self.suppress('normalThreshold')
        self.suppress('lodVisibility')
        self.suppress('ghostingControl')
        self.suppress('ghostPreSteps')
        self.suppress('ghostPostSteps')
        self.suppress('ghostStepSize')
        self.suppress('ghostRangeStart')
        self.suppress('ghostRangeEnd')
        self.suppress('ghostDriver')
        self.suppress('ghostFrames')
        self.suppress('ghosting')
        self.suppress('ghostCustomSteps')
        self.suppress('ghostColorPreA')
        self.suppress('ghostColorPre')
        self.suppress('ghostColorPostA')
        self.suppress('ghostColorPost')
        self.suppress('tweak')
        self.suppress('relativeTweak')
        self.suppress('currentUVSet')
        self.suppress('displayImmediate')
        self.suppress('displayColors')
        self.suppress('displayColorChannel')
        self.suppress('currentColorSet')
        self.suppress('smoothShading')
        self.suppress('drawOverride')
        self.suppress('shadingSamples')
        self.suppress('maxVisibilitySamplesOverride')
        self.suppress('maxVisibilitySamples')
        self.suppress('antialiasingLevel')
        self.suppress('maxShadingSamples')
        self.suppress('shadingSamplesOverride')
        self.suppress('geometryAntialiasingOverride')
        self.suppress('antialiasingLevel')
        self.suppress('volumeSamplesOverride')
        self.suppress('volumeSamples')
        self.suppress('depthJitter')
        self.suppress('ignoreSelfShadowing')
        self.suppress('controlPoints')
        self.suppress('colorSet')
        self.suppress('uvSet')
        self.suppress('weights')
        self.suppress('renderInfo')
        self.suppress('renderLayerInfo')
        self.suppress('compInstObjGroups')
        self.suppress('instObjGroups')
        self.suppress('collisionOffsetVelocityIncrement')
        self.suppress('collisionOffsetVelocityMultiplier')
        self.suppress('collisionDepthVelocityMultiplier')
        self.suppress('collisionDepthVelocityIncrement')
    
        self.addExtraControls()
        self.endScrollLayout()




  
