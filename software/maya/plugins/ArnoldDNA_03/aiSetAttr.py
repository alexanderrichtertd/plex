#256 pipeline tools
#set MTOA attributes
# Put script to \Documents\maya\201X-x64\scripts 
# In Python tab of Maya script editor execute code:
# import aiSetAttr
# aiSetAttr.windowSET()


import maya.cmds as cmds

def setFloatAttribute(*args):
    floatAttrName = cmds.textField( 'floatAttrName', q = True, text = True )
    floatAttrValue = float(cmds.textField( 'floatAttrValue' , q = True, text = True))
    sel = cmds.ls(sl=1, long=1,)
    for i in sel:
        cmds.setAttr(i + ".mtoa_constant_" + floatAttrName, floatAttrValue )
    
def setStringAttribute(*args):
    stringAttrName = cmds.textField( 'stringAttrName', q = True, text = True )
    stringAttrValue = cmds.textField( 'stringAttrValue', q = True, text = True )
    sel = cmds.ls(sl=1, long=1,)
    for i in sel:
        cmds.setAttr(i + ".mtoa_constant_" + stringAttrName, stringAttrValue , type = "string")

def setColorAttribute(*args):
    colorAttrName = cmds.textField( 'colorAttrName', q = True, text = True )
    colorAttrValue = cmds.textField( 'colorAttrValue', q = True, text = True )
    sel = cmds.ls(sl=1, long=1,)
    if colorAttrValue == 'R' or colorAttrValue == 'r':
        for i in sel:
            cmds.setAttr(i + ".mtoa_constant_" + colorAttrName, 1, 0, 0, type="double3")

    elif colorAttrValue == 'G' or colorAttrValue == 'g':
        
        for i in sel:
            cmds.setAttr(i + ".mtoa_constant_" + colorAttrName, 0, 1, 0, type="double3")
    elif colorAttrValue == 'B' or colorAttrValue == 'b':
        for i in sel:
            cmds.setAttr(i + ".mtoa_constant_" + colorAttrName, 0, 0, 1, type="double3")      
    else:
        print 'NON RGB COLOR!'      

def windowSET(*args):
    if cmds.window("myWin_CA", exists = 1):
        cmds.deleteUI("myWin_CA")
    win = cmds.window("myWin_CA", title = "SET ATTRIBUTES", w = 300, h = 100, sizeable = 0)
    
    mainLayout = cmds.columnLayout(w = 300)
    rowColumnLayout = cmds.rowColumnLayout(w = 300, nc = 3)
    
    cmds.textField( 'floatAttrName' , w = 80, text = 'mTileUV')
    cmds.textField( 'floatAttrValue' , w = 120, text = '256')
    cmds.button(label = "SET FLOAT", w= 100,  c = setFloatAttribute)
       
    cmds.textField( 'stringAttrName' , w = 80, text = 'mColor')
    cmds.textField( 'stringAttrValue' , w = 120, text = 'texture.tif')
    cmds.button(label = "SET STRING", w= 100,  c = setStringAttribute)
    
    cmds.textField( 'colorAttrName' , w = 80, text = 'mMask_A')
    cmds.textField( 'colorAttrValue' , w = 120, text = 'R')
    cmds.button(label = "SET COLOR", w= 100,  c = setColorAttribute)
       
    cmds.showWindow(win)


