# 256 pipeline tools
# set sobdivition attributes and turn maya smooth off
# Put script to \Documents\maya\201X-x64\scripts 
# In Python tab of Maya script editor execute code:
# import aiSetSubdiv
# aiSetSubdiv.windowSBD()

import maya.cmds as cmds

def aiSetSubd(aiSubdType):
    cmds.pickWalk( d = "down" )
    sel = cmds.ls(sl=1,long=1) 
    for i in sel:
        cmds.setAttr( i + '.aiSubdivType', aiSubdType)
        
def aiSetIter(iterValue):
    cmds.pickWalk( d = "down" )
    sel = cmds.ls(sl=1,long=1) 
    for i in sel:
        cmds.setAttr( i + '.aiSubdivIterations', iterValue)
        
def aiSmoothOff(*args):
    cmds.pickWalk( d = "down" )
    sel = cmds.ls(sl=1,long=1)
    
    for i in sel:
         cmds.setAttr(i + ".useSmoothPreviewForRender", lock = 0)
         cmds.setAttr(i + ".useSmoothPreviewForRender", 0)
         cmds.setAttr(i + ".smoothLevel", 2)
         cmds.setAttr(i + ".renderSmoothLevel", 0)   
         cmds.setAttr(i + ".renderSmoothLevel", lock = 1)          
            
def windowSBD(*args):
    
    if cmds.window("wSubdiv", exists = 1):
        cmds.deleteUI("wSubdiv")
    win = cmds.window("wSubdiv", title = "SUBDIV", w = 300, h = 100, sizeable = 0)
    
    mainLayout = cmds.columnLayout (w =360)
    layA = cmds.rowColumnLayout(w = 360, nc = 3)
    
    
    cmds.button(label = "NONE", w= 120, h = 50, c = 'aiSetSubd(0)')
    cmds.button(label = "CATCLARK", w= 120, h = 50, c = 'aiSetSubd(1)')
    cmds.button(label = "LINEAR", w= 120, h = 50, c = 'aiSetSubd(2)')
    
    layB = cmds.rowColumnLayout(w = 360, nc = 4, parent = mainLayout )
    cmds.button(label = "1", w= 90, h = 50, c = 'aiSetIter(1)')
    cmds.button(label = "2", w= 90, h = 50, c = 'aiSetIter(2)')
    cmds.button(label = "3", w= 90, h = 50, c = 'aiSetIter(3)')
    cmds.button(label = "4", w= 90, h = 50, c = 'aiSetIter(4)')
    
    layC = cmds.rowColumnLayout(w = 360, nc = 1, parent = mainLayout )
    cmds.button(label = "MAYA SMOOTH OFF", w= 360, h = 50, c = aiSmoothOff)
    
   
    
    cmds.showWindow(win)
    
