# 256 pipeline tools
# add attributes mtoa_constant_ of different data types to an jbject shapes
# select jject shapes, run script
# possible enter several attribute names with spase(mMask_A mMask_B mMask_C)
# Put script to \Documents\maya\201X-x64\scripts 
# In Python tab of Maya script editor execute code:
# import aiCreateAttr
# aiCreateAttr.windowADD()

import maya.cmds as cmds
from functools import partial

def addFloatAttr(*args):
    floatAttrName = cmds.textFieldGrp( 'floatText', q = True, text = True ).split(' ')
    cmds.pickWalk( d = "down" )
    selected = cmds.ls(sl=1,long=1)
    for member in selected:
        for i in floatAttrName:
            if cmds.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                print 'attribute ' + i + ' already exist!'
            else:
                cmds.addAttr(member, ln = "mtoa_constant_" + i, nn = i, dv =1)
                
def delFloatAttr(*args):
    floatAttrName = cmds.textFieldGrp( 'floatText', q = True, text = True ).split(' ')
    cmds.pickWalk( d = "down" )
    selected = cmds.ls(sl=1,long=1)
    for member in selected:
        for i in floatAttrName:
            if cmds.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                cmds.deleteAttr(member + '.mtoa_constant_' + i)
            else:
                print 'attribute ' + i + ' not exist!'
    
def addStringAttr(*args):
    stringAttrName = cmds.textFieldGrp( 'stringText', q = True, text = True ).split(' ')
    cmds.pickWalk( d = "down" )
    selected = cmds.ls(sl=1,long=1)
    for member in selected:
        for i in stringAttrName:
            if cmds.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                print 'attribute ' + i + ' already exist!'
            else:
                cmds.addAttr(member, ln = "mtoa_constant_" + i, nn = i, dt = 'string')
def delStringAttr(*args):
    floatAttrName = cmds.textFieldGrp( 'stringText', q = True, text = True ).split(' ')
    cmds.pickWalk( d = "down" )
    selected = cmds.ls(sl=1,long=1)
    for member in selected:
        for i in floatAttrName:
            if cmds.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                cmds.deleteAttr(member + '.mtoa_constant_' + i)
            else:
                print 'attribute ' + i + ' not exist!'

def addColorAttr(*args):
    colorAttrName = cmds.textFieldGrp( 'colorText', q = True, text = True ).split(' ')
    cmds.pickWalk( d = "down" )
    selected = cmds.ls(sl=1,long=1)
    for member in selected:
        for i in colorAttrName:
            if cmds.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                print 'attribute ' + i + ' already exist!'
            else:
                cmds.addAttr(member, ln = "mtoa_constant_" + i, nn = i , uac = 1, at ="float3" )
                cmds.addAttr(member, ln = "red_" + i, at = "float", p = "mtoa_constant_" + i )
                cmds.addAttr(member, ln = "grn_" + i, at = "float", p = "mtoa_constant_" + i )
                cmds.addAttr(member, ln = "blu_" + i, at = "float", p = "mtoa_constant_" + i )
                
def delColorAttr(*args):
    floatAttrName = cmds.textFieldGrp( 'colorText', q = True, text = True ).split(' ')
    cmds.pickWalk( d = "down" )
    selected = cmds.ls(sl=1,long=1)
    for member in selected:
        for i in floatAttrName:
            if cmds.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                cmds.deleteAttr(member + '.mtoa_constant_' + i)
            else:
                print 'attribute ' + i + ' not exist!'

def addAll(*agrs):
    addFloatAttr()
    addStringAttr()
    addColorAttr()

def delAll(*args):
    delFloatAttr()
    delStringAttr()
    delColorAttr()
    
def windowADD(*args):
    
    if cmds.window("myWin", exists = 1):
        cmds.deleteUI("myWin")
    win = cmds.window("myWin", title = "ADD ATTRIBUTES", w = 500, h = 100, sizeable = 0)
    
    mainLayout = cmds.columnLayout (w =400)
    myLayout = cmds.rowColumnLayout(w = 400, nc = 3)
    
    cmds.textFieldGrp( 'floatText' , w = 200, text = 'mTileUV mBump mGain')
    cmds.button (label = "ADD FLOAT", w = 100, c = addFloatAttr)
    cmds.button (label = "DEL FLOAT", w = 100, c = delFloatAttr)
    cmds.textFieldGrp( 'stringText', w = 200, text = 'mColor mDisp mMat')
    cmds.button (label = "ADD STRING", w = 100, c = addStringAttr)
    cmds.button (label = "DEL STRING", w = 100, c = delStringAttr)
    cmds.textFieldGrp( 'colorText', w = 200, text = 'mMask_A')
    cmds.button(label = "ADD COLOR", w = 100, c = addColorAttr)
    cmds.button (label = "DEL COLOR", w = 100, c = delColorAttr)
    cmds.button (label = 'ADD ALL', w= 400, h = 50, parent = mainLayout, c = addAll)
    cmds.button (label = 'DELETE ALL', w= 400, h = 50, parent = mainLayout, c = delAll)


   
    cmds.showWindow(win)
       