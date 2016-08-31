# 256 pipeline tools
# Shader manager
# Put script to \Documents\maya\201X-x64\scripts 
# In Python tab of Maya script editor execute code:
# import aiShaderManager
# aiShaderManager.windowSHM()


import maya.cmds as cmds
import sys

def textureName(shapeName):
    getAiAttrName = cmds.textFieldGrp('getAiAttrField', q = True, text = True )
    nameFull = cmds.getAttr (shapeName + '.mtoa_constant_' + getAiAttrName)
    if not nameFull :
        nameFull = ''
        texture = 'BLANK'
    else:    
        nameFull = 'sourceimages\\' + nameFull 
        textureExt = nameFull.split('\\')[-1:] #last element in list
        texture = textureExt[0].split('.')[0] 
    return texture, nameFull
    
  
def setTileUV(*args):
    cmds.pickWalk( d = "down" )
    sel = cmds.ls(sl=1,long=1) 
    for i in sel:
        tileUV = cmds.getAttr(i + '.mtoa_constant_mTileUV')
        if tileUV == 1:
            print 'UV Tile = 1'
        else:  
            shaderUV = cmds.listConnections(cmds.listHistory(i ,f=1  ),type='lambert')
            textureUV = cmds.listConnections(shaderUV[0] + '.color' )
            checkP2D = len(cmds.listConnections(textureUV[0] + '.uvCoord') or [])
            if checkP2D == 0:
            
                previewP2D = cmds.shadingNode ('place2dTexture', asTexture = True, n = textureUV[0] + '_P2D')
                cmds.setAttr(previewP2D  + '.repeatU', tileUV)
                cmds.setAttr(previewP2D  + '.repeatV', tileUV)
                
                cmds.connectAttr (previewP2D + '.outUV',  textureUV[0] + '.uvCoord')
                cmds.connectAttr (previewP2D + '.outUvFilterSize',  textureUV[0] + '.uvFilterSize')
                cmds.connectAttr (previewP2D + '.coverage',  textureUV[0] + '.coverage')
                cmds.connectAttr (previewP2D + '.translateFrame',  textureUV[0] + '.translateFrame')
                cmds.connectAttr (previewP2D + '.rotateFrame',  textureUV[0] + '.rotateFrame')
                cmds.connectAttr (previewP2D + '.mirrorU',  textureUV[0] + '.mirrorU')
                cmds.connectAttr (previewP2D + '.mirrorV',  textureUV[0] + '.mirrorV')
                cmds.connectAttr (previewP2D + '.stagger',  textureUV[0] + '.stagger')
                cmds.connectAttr (previewP2D + '.wrapU',  textureUV[0] + '.wrapU')
                cmds.connectAttr (previewP2D + '.wrapV',  textureUV[0] + '.wrapV')
                cmds.connectAttr (previewP2D + '.repeatUV',  textureUV[0] + '.repeatUV')
                cmds.connectAttr (previewP2D + '.vertexUvOne',  textureUV[0] + '.vertexUvOne')
                cmds.connectAttr (previewP2D + '.vertexUvTwo',  textureUV[0] + '.vertexUvTwo')
                cmds.connectAttr (previewP2D + '.vertexUvThree',  textureUV[0] + '.vertexUvThree')
                cmds.connectAttr (previewP2D + '.vertexCameraOne',  textureUV[0] + '.vertexCameraOne')
                cmds.connectAttr (previewP2D + '.noiseUV',  textureUV[0] + '.noiseUV')
                cmds.connectAttr (previewP2D + '.offset',  textureUV[0] + '.offset')
                cmds.connectAttr (previewP2D + '.rotateUV',  textureUV[0] + '.rotateUV')
            else:
                previewP2D = cmds.listConnections(textureUV[0] + '.uvCoord')
                cmds.setAttr(previewP2D[0]  + '.repeatU', tileUV)
                cmds.setAttr(previewP2D[0]  + '.repeatV', tileUV)
                
def getTextureFromShader(*args):                
    cmds.pickWalk( d = "down" )
    sel = cmds.ls(sl=1,long=1)
    
    for i in sel:
        getAiAttrName = cmds.textFieldGrp('getAiAttrField', q = True, text = True )
        shadingGroup = cmds.listConnections(i ,type='shadingEngine')
        shader = cmds.ls(cmds.listConnections(shadingGroup), materials=1)  
        imageFile = cmds.listConnections(shader[0] ,type='file') 
        if not imageFile:
            print 'No shader assigned'
            
        else:
            texture = cmds.getAttr(imageFile[0] + '.fileTextureName')
            texture = texture.replace('/','\\')
            texture =  texture.split('sourceimages\\')[1]
            cmds.setAttr(i + '.mtoa_constant_' + getAiAttrName, texture, type = 'string')
        
        
def assignPREVShader(*args):
    cmds.pickWalk( d = "down" )
    sel = cmds.ls(sl=1,long=1) 
    for i in sel:
        shapeName = ''
        shapeName = i
        texture, nameFull = textureName(i)
        if cmds.objExists ('PREV_' + texture):
            cmds.sets(i, e=1, forceElement = 'PREV_' + texture + 'SG')
        else:
            if texture == 'BLANK':
                previewShader = cmds.shadingNode ('lambert', asShader = True, n = 'PREV_' + texture)
                previewSG = cmds.sets (renderable=True, noSurfaceShader = True, empty = True, n = previewShader  + 'SG')
                cmds.connectAttr (previewShader + '.outColor', previewSG + '.surfaceShader')
                cmds.sets(i, e=1, forceElement = previewSG)
            else:
                previewShader = cmds.shadingNode ('lambert', asShader = True, n = 'PREV_' + texture)
                previewIF = cmds.shadingNode ('file',asTexture = True, n = 'PREV_IF_' + texture)
                previewSG = cmds.sets (renderable=True, noSurfaceShader = True, empty = True, n = previewShader  + 'SG')
                cmds.connectAttr (previewIF  + '.outColor', previewShader + '.color')
                cmds.connectAttr (previewShader + '.outColor', previewSG + '.surfaceShader')
                cmds.setAttr(previewIF + '.fileTextureName', nameFull ,  type = "string")
                cmds.sets(i, e=1, forceElement = previewSG)
            
def deleteShaders(*args):
    previewShaders = cmds.select("PREV_*", allDagObjects=False, noExpand=True)

    meshes = cmds.hyperShade(objects="")
    cmds.hyperShade(assign= 'lambert1' )
    cmds.select(cl =1)
    previewShaders = cmds.select("PREV_*", allDagObjects=False, noExpand=True)
    cmds.delete() 

def getMaterial(*args):
    cmds.pickWalk( d = "down" )
    sel = cmds.ls(sl=1,long=1)
        
    for i in sel:
        shadingGroup = cmds.listConnections(i ,type='shadingEngine')
        mat = (shadingGroup[0])[:-2]
        cmds.setAttr( i + '.mtoa_constant_mMat', mat, type = 'string')

def asignMaterial(*args):
    cmds.pickWalk( d = "down" )
    sel = cmds.ls( sl = True )
    for i in sel:
        mat = cmds.getAttr(i + '.mtoa_constant_mMat')
        matSG = mat + 'SG'
        asign = cmds.sets(i, e =1, forceElement = matSG)

def windowSHM(*args):
    
    if cmds.window("shdrmnWin", exists = 1):
        cmds.deleteUI("shdrmnWin")
    win = cmds.window("shdrmnWin", title = "Shader manager", w = 500, sizeable = 0)
    
    mainLayout = cmds.columnLayout (w = 500)
    
    cmds.rowColumnLayout(w = 500, nc = 4, parent = mainLayout )
    cmds.textFieldGrp( 'getAiAttrField', text = 'mColor')
    cmds.button(label = "GET TX", w= 83, h = 50, c = getTextureFromShader )
    cmds.button(label = "SHOW TX", w= 83, h = 50, c = assignPREVShader)
    cmds.button(label = "TILE UV", w= 83, h = 50, c = setTileUV)

    
    cmds.rowColumnLayout(w = 500, nc = 1, parent = mainLayout )
    cmds.button(label = "DELETE PREVIEW", w= 500, h = 50, c = deleteShaders, parent = mainLayout )
    cmds.separator(height=10, parent = mainLayout)
    
    cmds.rowColumnLayout(w = 500, nc = 2, parent = mainLayout )
    cmds.button(label = "GET MATERIALS", w= 250, h = 50, c =  getMaterial )
    cmds.button(label = "ASSIGN MATERIALS", w= 250, h = 50, c =  asignMaterial )
       
    
    cmds.showWindow(win)

