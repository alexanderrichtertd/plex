import maya.cmds as cmds
import maya.utils as utils
import os.path
import glob
import re
import sys, os
import subprocess
import threading
import mtoa.callbacks as callbacks
import maya.OpenMaya as om
import mtoa.utils as mutils

class MtoARenderToTexture(object):
    window = None
    def __new__(cls, *args, **kwargs):
        if not '_instance' in vars(cls):
            cls._instance = super(MtoARenderToTexture, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if self.window is None:
            self.window = 'MtoARenderToTexture'
            self.listElements = []
            self.column = ''



    def doExport(self):
        outFolder = cmds.textFieldButtonGrp('outputFolder', q=True, tx=True)

        if (outFolder == ''):
            cmds.confirmDialog( title='Render To Texture', message='An Output folder must be selected', button=['Ok'], defaultButton='Ok', cancelButton='Ok', dismissString='Ok' )
            return False


        resolution = cmds.intFieldGrp('resolution', q=True, v1=True)
        aa_sampling = cmds.intFieldGrp('aa_samples', q=True, v1=True)

        filter_type = cmds.optionMenuGrp('filter', q=True, v=True)
        all_udims = cmds.checkBox('all_udims', q=True, v=True)
        filter_width = cmds.floatFieldGrp('filterWidth', q=True, v1=True)
        shader = cmds.textFieldGrp('shader', q=True, tx=True)
        udims = cmds.textFieldGrp('udims', q=True, tx=True)

        selList = cmds.ls(sl=1)

        if (len(selList) == 0):
            cmds.confirmDialog( title='Render To Texture', message='No Geometry Selected', button=['Ok'], defaultButton='Ok', cancelButton='Ok', dismissString='Ok' )
            return False

        cmds.arnoldRenderToTexture(folder=outFolder, shader=shader, resolution=resolution, aa_samples=aa_sampling, filter=filter_type, filter_width=filter_width, all_udims=all_udims, udims=udims )

        cmds.deleteUI(self.window)
        return True

    def doCancel(self):
        cmds.deleteUI(self.window)
        return True

    def browseObjFilename(self):
        ret = cmds.fileDialog2(cap='Select Folder',okc='Select',fm=3)
        if ret is not None and len(ret):
            cmds.textFieldButtonGrp('outputFolder', e=True, text=ret[0])

        return True


    def create(self):

        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window)

        winTitle = "Render To Texture"

        self.window = cmds.window(self.window, widthHeight=(460, 170), title=winTitle)
        self.createUI()


        cmds.setParent(menu=True)
        cmds.showWindow(self.window)

        try:
            initPos = cmds.windowPref( self.window, query=True, topLeftCorner=True )
            if initPos[0] < 0:
                initPos[0] = 0
            if initPos[1] < 0:
                initPos[1] = 0
            cmds.windowPref( self.window, edit=True, topLeftCorner=initPos )
        except :
            pass



    def createUI(self):
        cmds.scrollLayout(childResizable=True,)
        cmds.columnLayout(adjustableColumn=True)
        #cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=1, columnAlign1='left')
        cmds.textFieldButtonGrp('outputFolder', label='Output Folder', cw3=(90,320, 50), text="", buttonLabel='...', buttonCommand=lambda *args: self.browseObjFilename())

        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2, columnAlign2=('left', 'right'))
        cmds.intFieldGrp('resolution', label='Resolution', value1=512, ct2=('left', 'left'),  cw2=(90,110), w=230)
        cmds.intFieldGrp('aa_samples', label='Camera Samples (AA)', cw2=(150,60), value1=3, w=200)
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2, columnAlign2=('left', 'right'))
        cmds.optionMenuGrp('filter', label='Filter ')
        cmds.menuItem( label='blackman_harris' )
        cmds.menuItem( label='box' )
        cmds.menuItem( label='catrom' )
        cmds.menuItem( label='catrom2d' )
        cmds.menuItem( label='closest' )
        cmds.menuItem( label='cone' )
        cmds.menuItem( label='cook' )
        cmds.menuItem( label='cubic' )
        cmds.menuItem( label='disk' )
        cmds.menuItem( label='farthest' )
        cmds.menuItem( label='gaussian' )
        cmds.menuItem( label='heatmap' )
        cmds.menuItem( label='mitnet' )
        cmds.menuItem( label='sync' )
        cmds.menuItem( label='triangle' )
        cmds.menuItem( label='variance' )
        cmds.menuItem( label='video' )

        cmds.optionMenuGrp('filter', e=True, w=230, ct2=('left', 'left'), cw2=(90,110), v='gaussian')

        cmds.floatFieldGrp('filterWidth', label='Filter Width', w=200, ct2=('left', 'left'), cw2=(150,60), value1=2.0)
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=1, columnAlign1='both')
        cmds.textFieldGrp('shader', label='Shader Override', ct2=('left', 'left'), cw2=(90,110), text="", w=380)
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2, columnAlign2=('left', 'right'))
        cmds.textFieldGrp('udims', label='Udims', ct2=('left', 'left'), cw2=(90,110), text="", w=280)
        cmds.checkBox( 'all_udims',label='All Udims', value=False )

        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=4, columnAlign4=('left', 'left', 'left', 'right'))
        cmds.text( '                                             ')

        cmds.button(label='Render', al='right', w=85, h=25, command=lambda *args: self.doExport())
        cmds.text( '              ')
        cmds.button(label='Cancel', al='right', w=85, h=25, command=lambda *args: self.doCancel())
        cmds.setParent("..")