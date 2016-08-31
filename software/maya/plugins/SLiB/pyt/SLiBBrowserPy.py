#########################################################################
#
#  SLiBBrowserPy.py v1.00 by DGDM
#
#########################################################################

import maya.cmds as cmds
import maya.mel as mel
import time
import os
import shutil
import sys
import platform
import webbrowser
import re
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import gc
from functools import partial

from PySide import QtCore
from PySide import QtGui
from PySide.QtGui import QMainWindow
from PySide.QtGui import QWidget
#import shiboken
from shiboken import wrapInstance 


SLiBImage = mel.eval('getenv SLiBImage;')
SLiBGuiPath = mel.eval('getenv SLiBGui;')
currentRender = cmds.getAttr('defaultRenderGlobals.currentRenderer')


#IMPORT
def SLiBBrowserImport(mode):
    if cmds.iconTextRadioCollection('slAssetCollection', q=1, sl=1) == 'NONE':
        SLiBMessager('Please select something you want to Import!', 'red')
        sys.exit()
    sel = cmds.ls(sl=1, fl=1)
    fileType = os.path.splitext(gib('file'))[1]
    if fileType == '.ma':
        fileType = 'mayaAscii'
    if fileType == '.mb':
        fileType = 'mayaBinary'
    if fileType == '.obj':
        fileType = 'OBJ'
    
    if mode == 'Normal':
        if cmds.menuItem('importREF', q=1, cb=1) != True:
            imported = cmds.file(gib('file'), i=1, type=fileType, uns=0, rnn=1, iv=1)
        else:
            imported = cmds.file(gib('file'), r=1, type=fileType, uns=1, rnn=1, iv=1)
        
        importedMats = cmds.ls(imported, mat=1)
        importedShapes = cmds.ls(imported, s=1)
        shaderList = list(importedMats)
        mainShader=[]
        root = cmds.ls(imported, assemblies=1)
        
        if gib('mainCat') != 'shader':
            i=1
            while cmds.objExists(root[0] + str(i).zfill(3)):
                i+=1
            root = cmds.rename(root[0], root[0] + '_' + str(i).zfill(3))
        
        if len(importedShapes) == 0:
            if len(sel) == 0:
                if len(importedMats) > 1:
                    for e in shaderList:
                        conn = cmds.listConnections(e, s=0)
                        cmds.select(conn)
                        mainShader.append(cmds.ls(sl=1, mat=1))
                    shader = ', '.join(mainShader[1])
                    cmds.rename(shader, shader + '_001')
                else:
                    shader = ', '.join(importedMats)
                    cmds.rename(shader, shader + '_001')

            else:
                if len(importedMats) > 1:
                    for e in shaderList:
                        conn = cmds.listConnections(e, s=0)
                        cmds.select(conn)
                        mainShader.append(cmds.ls(sl=1, mat=1))
                    shader = ', '.join(mainShader[1])
                    cmds.select( sel )
                    cmds.hyperShade( a=shader )
                    cmds.rename(shader, shader + '_001')
                else:
                    shader = ', '.join(importedMats)
                    cmds.select( sel )
                    cmds.hyperShade( a=shader )
                    cmds.rename(shader, shader + '_001')
                    
        SLiBDupFix(padding=3)
        SLiBMessager('IMPORT successful!', 'green')
        cmds.select(root)

        
    else:
        if len(sel) == 0:
            SLiBMessager('Please select target Object(s) or Verticies!', 'red')
            sys.exit()
        else:
            for v in sel:
                if cmds.menuItem('importREF', q=1, cb=1) != True:
                    imported = cmds.file(gib('file'), i=1, type=fileType, uns=0, rnn=1, iv=1)
                else:
                    imported = cmds.file(gib('file'), r=1, type =fileType, uns=1, rnn=1, iv=1)
                
                importedShapes = cmds.ls(imported, s=1)
                root = cmds.ls(imported, assemblies=1)
                
                if gib('mainCat') != 'shader':
                    i=1
                    while cmds.objExists(root[0] + str(i).zfill(3)):
                        i+=1
                    root = cmds.rename(root[0], root[0] + '_' + str(i).zfill(3))
                    
                    curPosition = cmds.xform( v, q=1, t=1, ws=1)
                    curRotation = cmds.xform( v, q=1, ro=1, ws=1)
                
                cmds.setAttr(root + '.tx', curPosition[0])
                cmds.setAttr(root + '.ty', curPosition[1])
                cmds.setAttr(root + '.tz', curPosition[2])
                cmds.setAttr(root + '.rx', curRotation[0])
                cmds.setAttr(root + '.ry', curRotation[1])
                cmds.setAttr(root + '.rz', curRotation[2])
                
                if mode == 'Replace':
                    cmds.delete(v)
                    
        SLiBDupFix(padding=3)
        SLiBMessager('IMPORT successful!', 'green')
                
def SLiBImportTexture():
    fileNode = cmds.shadingNode("file", asTexture=1)
    file = gib('file')
    cmds.setAttr( fileNode + '.fileTextureName', file, type = "string")
    SLiBMessager('IMPORT successful!', 'green')

def SLiBFlushOptionMenu(flushOptionMenu):
    cmds.undoInfo(st=0)
    try:
        menuItems = cmds.optionMenu(flushOptionMenu, q=1, itemListLong=1)
        for curItem in menuItems:
            cmds.deleteUI(curItem, menuItem=1)
    except:
        pass
    SLiBTypeBGChange()

def SLiBTypeBGChange():
    allTypes = cmds.iconTextRadioCollection( 'mainCatCollection', q=1, cia=1)
    for e in allTypes:
        cmds.iconTextRadioButton(e.split('|')[-1], e=1, bgc=[0,0,0])
    cmds.iconTextRadioButton(cmds.iconTextRadioCollection( 'mainCatCollection', q=1, sl=1 ), e=1, bgc=[0,0.75,0.99])

    
#UPDATE INFO
def SLiBBrowserUpdateInfo():
    try:
        cmds.iconTextRadioButton('icon'+lastasset, e=1, bgc=[0.15,0.15,0.15] )
    except:
        pass
    assetPath = os.path.dirname(cmds.iconTextRadioButton(cmds.iconTextRadioCollection('slAssetCollection', q=1, sl=1), q=1, label=1))
    asset = cmds.iconTextRadioButton(cmds.iconTextRadioCollection('slAssetCollection', q=1, sl=1), q=1, annotation=1)
    if gib('mainCat') == 'textures':
        assetPath = SLiBCurrLoc()
        imageFile = cmds.iconTextRadioButton(cmds.iconTextRadioCollection('slAssetCollection', q=1, sl=1), q=1, i=1)
    else:
        f = open(assetPath + '/' + asset + '.info', 'r')
        importNotes = f.read()
        printNotes = str(importNotes)
        cmds.scrollField('SLiB_TEXTFIELD_Info', e=1, text=printNotes)
        imageFile = assetPath + '/' + asset + '.png'
    cmds.iconTextButton('RenderViewButton', e=1, i=imageFile)
    cmds.popupMenu(parent="RenderViewButton", ctl=0, button=3)
    cmds.menuItem(l='Replace Preview Image', command= lambda *args: SLiBReplacePreview())
    cmds.text('SLiB_shaderName', e=1, l=asset, al='center')
    SLiBMessager('Selection Info updated!', 'none')

    cmds.iconTextRadioButton('icon'+asset, e=1, bgc=[0,0.75,0.99] )
    global lastasset
    lastasset = asset

#UPDATE SHADER
def SLiBBrowserUpdateShader():
    if gib('mainCat') == 'textures':
        SLiBBrowserUpdateTextures()
    if gib('mainCat') == 'favorites':
        SLiBBrowserUpdateFavorites()
    if (gib('mainCat') == 'shader' or gib('mainCat') == 'objects' or gib('mainCat') == 'lights'):
        if cmds.scrollLayout('SLiBScrollLayoutBrowser', q=1, exists=1):
            cmds.deleteUI('SLiBScrollLayoutBrowser', layout=1)
        
        cmds.scrollLayout('SLiBScrollLayoutBrowser', bgc=[0.15,0.15,0.15], p="SLiB_thumbsframe")
        cmds.popupMenu(parent='SLiBScrollLayoutBrowser', ctl=0, button=3)
        cmds.menuItem(l='Paste', c=lambda *args: SLiBBrowserPaste())
        
        f = open(mel.eval('getenv SLiBLib;') + 'settings/' + 'favorites.txt', 'r')
        Favs = f.read().splitlines()
        
        iconSize = cmds.textField('SLiBThumbSizeComboBox', q=1, text=1)
        if int(iconSize) > 1024:
            iconSize = [1024]
            cmds.textField('SLiBThumbSizeComboBox', e=1, text=iconSize[0])
        coll = cmds.textField('SLiBThumbColumnsComboBox', q=1, text=1)
        if gib('cat') == 'Select...':
            sys.exit()
                
        assetPath = SLiBCurrLoc()
        assetDir = os.listdir(assetPath)
        cmds.optionVar(stringValue = ('SLiBIconCaption', cmds.iconTextCheckBox('SLiBIconCaption', q=1, v=1)))
        cmds.rowColumnLayout('Icons', nc=int(coll), p="SLiBScrollLayoutBrowser")
        if len(assetDir) != 0:
            cmds.iconTextRadioCollection('slAssetCollection')
            cmds.progressBar('PreviewProgress', e=1, pr=0)
            cmds.progressBar('PreviewProgress', e=1, maxValue=(len(assetDir)))
            if cmds.iconTextCheckBox('searchSwitch', q=1, v=1) == 1:
                if len(cmds.textField('SLiB_TEXTFIELD_Search', q=1, text=1)) != 0:
                    fWord = cmds.textField('SLiB_TEXTFIELD_Search', q=1, text=1)
                    NewAssetDir = [k for k in assetDir if fWord.lower() in k.lower()]
                    assetDir = NewAssetDir 
                else:
                    pass
            for curAsset in assetDir:
                curAssetPath = assetPath + '/' + curAsset + '/'
                if curAsset != '.DS_Store':
                    if curAsset != '_SUB':
                        if curAsset != 'sourceimages':
                            assetFile = os.listdir(curAssetPath)
                            for curFile in assetFile:
                                if os.path.isfile(assetPath + '/' + curAsset  + '/' + curFile) == True:
                                    file = os.path.splitext(curFile)[0]
                                    fileEx = os.path.splitext(curFile)[1]
                                    if fileEx == '.mb' or fileEx == '.ma' or fileEx == '.obj':
                                        image = curAssetPath + file + '.png'
                                        if len(iconSize) > 1:
                                            cmds.columnLayout('cell'+file, rowSpacing=2, adj=1, cal='center', columnWidth = int(iconSize)+6, p='Icons')
                                            cmds.iconTextRadioButton('icon'+file, i=image, mw=3, mh=3, w=int(iconSize)+7, h=int(iconSize)+7, onc=lambda *args: SLiBBrowserUpdateInfo(), l=curAssetPath + curFile, ann=file, p='cell'+file)
                                            cmds.popupMenu('pop'+file, parent='icon'+file, ctl=0, button=3, pmc=partial(SLiBBrowserPostMenu, file))
                                            cmds.menuItem(l=file, i=image, bld=1, en=0)
                                            cmds.menuItem(l='', en=0)
                                            cmds.menuItem(l='IMPORT', c=lambda *args: SLiBBrowserImport('Normal'))
                                            cmds.menuItem(divider=1)
                                            if ('/objects/' or '/lights/') in image:
                                                cmds.menuItem(l='IMPORT and Place at Selection', c=lambda *args: SLiBBrowserImport('Place'))
                                                cmds.menuItem(l='IMPORT and Replace Selection', c=lambda *args: SLiBBrowserImport('Replace'))
                                                cmds.menuItem(divider=1)
                                            cmds.menuItem(l='OPEN in Maya', c=lambda *args: SLiBOpenInMaya())
                                            cmds.menuItem(l='OPEN in FileBrowser', c=lambda *args: SLiBOpenInFileBrowser())
                                            cmds.menuItem(divider=1)
                                            cmds.menuItem('favItem'+file, l='ADD to Favorites', c=lambda *args: SLiBAddFav('add'))
                                            cmds.menuItem(divider=1)
                                            cmds.menuItem(l='DELETE', c=lambda *args: SLiBBrowserDelete())
                                            if cmds.optionVar(query = 'SLiBIconCaption') == 'True':
                                                cmds.rowLayout('caption'+file, w=int(iconSize)-6, numberOfColumns=3, adj=1, columnAlign=(1, 'center'), bgc=[0.1,0.1,0.1], p='cell'+file)
                                                cmds.text(label = file, align = 'center', p='caption'+file)
                                                if fileEx == '.ma':
                                                    cmds.iconTextButton(i=SLiBImage + 'SLiB_ma.png', mw=0, mh=0, h=16, w=16, p='caption'+file)
                                                if fileEx == '.mb':
                                                    cmds.iconTextButton(i=SLiBImage + 'SLiB_mb.png', mw=0, mh=0, h=16, w=16, p='caption'+file)
                                                if fileEx == '.obj':
                                                    cmds.iconTextButton(i=SLiBImage + 'SLiB_obj.png', mw=0, mh=0, h=16, w=16, p='caption'+file)
                                                if str(curAssetPath+file+fileEx) in Favs:
                                                    cmds.iconTextButton('favCB'+file, i=SLiBImage + 'SLiB_fav_on.png', mw=0, mh=0, h=16, w=16, p='caption'+file)
                                                    cmds.menuItem('favItem'+file, e=1, l='Remove from Favorites', c=lambda *args: SLiBAddFav('remove'))
                                                else:
                                                    cmds.iconTextButton('favCB'+file, i=SLiBImage + 'SLiB_fav_off.png', mw=0, mh=0, h=16, w=16, p='caption'+file)
                                                #cmds.setParent('..')
                                            cmds.progressBar('PreviewProgress', e=1, step=1)
        
        cmds.progressBar('PreviewProgress', e=1, pr=0)
        SLiBSaveCats()
        cmds.undoInfo(st=1)
        gc.collect()
        
def SLiBBrowserPostMenu(file, *args):
    cmds.iconTextRadioButton('icon'+file, e=1, sl=1)
    SLiBBrowserUpdateInfo()

def SLiBBrowserUpdateTextures():
    if cmds.scrollLayout('SLiBScrollLayoutBrowser', q=1, exists=1):
        cmds.deleteUI('SLiBScrollLayoutBrowser', layout=1)
    cmds.scrollLayout('SLiBScrollLayoutBrowser', p="SLiB_thumbsframe", bgc=[0.15,0.15,0.15])
    cmds.popupMenu(parent='SLiBScrollLayoutBrowser', ctl=0, button=3)
    cmds.menuItem(l='Paste', c=lambda *args: SLiBBrowserPaste())
    
    iconSize = cmds.textField('SLiBThumbSizeComboBox', q=1, text=1)
    iconSize = cmds.textField('SLiBThumbSizeComboBox', q=1, text=1)
    if int(iconSize) > 1024:
        iconSize = [1024]
        cmds.textField('SLiBThumbSizeComboBox', e=1, text=iconSize[0])
    coll = cmds.textField('SLiBThumbColumnsComboBox', q=1, text=1)
    assetPath = SLiBCurrLoc()
    if gib('cat') != 'Select...':
        texturesList = os.listdir(assetPath)
        cmds.optionVar(stringValue = ('SLiBIconCaption', cmds.iconTextCheckBox('SLiBIconCaption', q=1, v=1)))
        cmds.rowColumnLayout('Icons', numberOfColumns=int(coll), p="SLiBScrollLayoutBrowser")
        if len(texturesList) != 0:
            cmds.iconTextRadioCollection('slAssetCollection', p='Icons')
            cmds.progressBar('PreviewProgress', e=1, pr=0)
            cmds.progressBar('PreviewProgress', e=1, maxValue=(len(texturesList)))
            if cmds.iconTextCheckBox('searchSwitch', q=1, v=1) == 1:
                if len(cmds.textField('SLiB_TEXTFIELD_Search', q=1, text=1)) != 0:
                    fWord = cmds.textField('SLiB_TEXTFIELD_Search', q=1, text=1)
                    NewAssetDir = [k for k in texturesList if fWord.lower() in k.lower()]
                    texturesList = NewAssetDir 
                else:
                    pass
            for curAsset in texturesList:
                if curAsset != '.DS_Store' and curAsset != '_SUB' and curAsset != '_THUMBS' and curAsset != '.mayaSwatches':
                    file = os.path.splitext(curAsset)[0]
                    fileEx = os.path.splitext(curAsset)[1]
                    cmds.progressBar('PreviewProgress', e=1, step=1)
                    if os.path.isfile(assetPath + '/_THUMBS' + '/' + file + fileEx) == True:
                        image = assetPath + '/_THUMBS' + '/' + file + fileEx
                    else:
                        SLiBMessager('Texture Preview Image(s) not found! Using Original...', 'yellow')
                        image = assetPath + '/' + file + fileEx
                    if len(iconSize) > 1:
                        if cmds.optionVar(query = 'SLiBIconCaption') == 'True':
                           cmds.columnLayout(rowSpacing = 6, columnWidth = int(iconSize))
                        assetIcon = cmds.iconTextRadioButton('icon'+file, i=image, mw=3, mh=3, h=int(iconSize), w=int(iconSize), onc=lambda *args: SLiBBrowserUpdateInfo(), l= assetPath + '/' + curAsset, ann=file)
                        cmds.popupMenu(parent='icon'+file, ctl=0, button=3, pmc=partial(SLiBBrowserPostMenu, file))
                        cmds.menuItem(l=file, i=image, bld=1, en=0)
                        cmds.menuItem(l='', en=0)
                        cmds.menuItem(l='IMPORT', command=lambda *args: SLiBImportTexture())
                        cmds.menuItem( divider=1 )
                        cmds.menuItem(l='OPEN in FileBrowser', command=lambda *args: SLiBOpenInFileBrowser())
                        cmds.menuItem( divider=1 )
                        cmds.menuItem(l='Delete', command=lambda *args: SLiBBrowserDelete())
                        if cmds.optionVar(query = 'SLiBIconCaption') == 'True':
                            cmds.text(label = file, width = int(iconSize), align = 'center')
                            cmds.setParent('..')
                len(iconSize) > 1
    cmds.progressBar('PreviewProgress', edit=1, pr=0)
    SLiBSaveCats()
    cmds.undoInfo(st=1)
    cmds.flushUndo()
        
def SLiBBrowserUpdateType():
    SLiBFlushOptionMenu('SLiBTypeComboBox')
    print 'SLiB >>> Category Menu flushed!'
    typeList =  os.listdir(gib('library') + gib('mainCat') + '/')
    if len(typeList) != 0:
        cmds.optionMenu('SLiBTypeComboBox', e=1, enable=1, cc=lambda *args: SLiBBrowserUpdateSubType())
        cmds.setParent('SLiBTypeComboBox', menu=1)
        cmds.menuItem(label = 'Select...')
        for curType in typeList:
            if curType != '.DS_Store':
                cmds.menuItem(label = curType)
        #cmds.optionMenu('SLiBTypeComboBox', e=1, v='Select...')
    else:
        if cmds.scrollLayout('SLiBScrollLayoutBrowser', q=1, ex=1):
            cmds.deleteUI('SLiBScrollLayoutBrowser', layout = 1)
    SLiBBrowserUpdateSubType()

def SLiBBrowserUpdateTypeOnly():
    SLiBFlushOptionMenu('SLiBTypeComboBox')
    print 'SLiB >>> Category Menu flushed!'
    typeList =  os.listdir(gib('library') + gib('mainCat') + '/')
    if len(typeList) != 0:
        typeList = list(typeList)
        cmds.optionMenu('SLiBTypeComboBox', e=1, enable=1)
        cmds.setParent('SLiBTypeComboBox', menu=1)
        cmds.menuItem(label = 'Select...')
        for curType in typeList:
            if curType != '.DS_Store':
                cmds.menuItem(label = curType)

#UPDATE SUB CAT
def SLiBBrowserUpdateSubType():
    SLiBFlushOptionMenu('SLiBSubTypeComboBox')
    print 'SLiB >>> SubCategory Menu flushed!'
    if gib('cat') == 'Select...':
        if cmds.scrollLayout('SLiBScrollLayoutBrowser', q=1, exists=1):
            cmds.deleteUI('SLiBScrollLayoutBrowser', layout=1)
            sys.exit()
    else:
        try:
            subTypeList = os.listdir(gib('library') + gib('mainCat') + '/' + gib('cat') + '/_SUB')
        except:
            os.mkdir(gib('library') + gib('mainCat') + '/' + gib('cat') + '/_SUB')
            subTypeList = os.listdir(gib('library') + gib('mainCat') + '/' + gib('cat') + '/_SUB')
            
        if len(subTypeList) != 0:
            cmds.optionMenu('SLiBSubTypeComboBox', e=1, enable=1, cc=lambda *args: SLiBBrowserUpdateShader())
            cmds.setParent('SLiBSubTypeComboBox', menu = 1)
            cmds.menuItem(label = 'Select...')
            for curType in subTypeList:
                if curType != '.DS_Store':
                    cmds.menuItem(label = curType)
            #cmds.optionMenu('SLiBSubTypeComboBox', e=1, v='Select...')
            SLiBBrowserUpdateShader()
        else:
            cmds.optionMenu('SLiBSubTypeComboBox', e=1, enable=0)
            SLiBBrowserUpdateShader()
    
def SLiBBrowserUpdateSubTypeOnly():
    SLiBFlushOptionMenu('SLiBSubTypeComboBox')
    print 'SLiB >>> SubCategory Menu flushed!'
    if gib('cat') == 'Select...':
        if cmds.scrollLayout('SLiBScrollLayoutBrowser', q=1, exists=1):
            cmds.deleteUI('SLiBScrollLayoutBrowser', layout=1)
            sys.exit()
    else:
        subTypeList = os.listdir(gib('library') + gib('mainCat') + '/' + gib('cat') + '/_SUB')
        if len(subTypeList) != 0:
            cmds.optionMenu('SLiBSubTypeComboBox', e=1, enable=1, cc=lambda *args: SLiBBrowserUpdateShader())
            cmds.setParent('SLiBSubTypeComboBox', menu=1)
            cmds.menuItem(label = 'Select...')
            for curType in subTypeList:
                if curType != '.DS_Store':
                    cmds.menuItem(label = curType)
        else:
            cmds.optionMenu('SLiBSubTypeComboBox', e=1, enable=0)

def SLiBNameFromSelection():
    sel = cmds.ls(sl=1)
    if len(sel) == 0:
        SLiBMessager('Please select an Oject to get the Name from!', 'red')
        sys.exit()
    cmds.textField('SLiB_TEXTFIELD_Name', e=1, text=sel[0])
    
def SLiBBrowserDelete():
    if gib('mainCat') == 'textures':
        deleteFolder = gib('file')
        cmds.sysFile( deleteFolder, delete=1 )
    else:
        deleteFolder = os.path.dirname(gib('file'))
        shutil.rmtree(deleteFolder)
        
    cmds.iconTextButton('RenderViewButton', e=1, i=SLiBImage + 'browser_logo.png')
    cmds.text('SLiB_shaderName', e=1, l='', al='center')
    cmds.evalDeferred(lambda: SLiBBrowserUpdateShader() )
    SLiBMessager('Removed!', 'green')
    
def SLiBBrowserRename():
    result = cmds.promptDialog(title='Rename', message='Enter Name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
    if result == 'OK':
        if gib('mainCat') == 'textures':
            renameFolder = gib('file')
            renameExt = os.path.splitext(gib('file'))[1]
            newName = cmds.promptDialog(q=1, t=1).replace(' ','_')
            cmds.sysFile(renameFolder, rename=SLiBCurrLoc() + '/' + newName + renameExt )
            cmds.evalDeferred(lambda: SLiBBrowserUpdateShader())
            SLiBMessager('Renamed!', 'green')

        else:
            renameFolder = os.path.dirname(gib('file'))
            renameFile = os.path.splitext(gib('file'))[0]
            newName = cmds.promptDialog(q=1, t=1).replace(' ','_')
            newDir = gib('file').rsplit('/', 2)[0] + '/' + newName
            if os.path.isdir(newDir) == 1:
                SLiBMessager('Name already exists!', 'red')
                sys.exit()
            else:
                shutil.move(renameFolder, newDir)
            
            allFiles = [os.path.join(newDir,fn) for fn in next(os.walk(newDir))[2]]

            for e in allFiles:
                file = os.path.splitext(e)[0]
                fileExt = os.path.splitext(e)[1]
                os.rename(e, newDir + "/" + newName + fileExt)

            path = newDir
            
            fav = str((gib('file')))
            favfileExt = os.path.splitext(fav)[1]
            newfav = gib('file').rsplit('/', 2)[0] + '/' + newName + '/' + newName + favfileExt
            f = open(mel.eval('getenv SLiBLib;') + 'settings/' + 'favorites.txt', 'r')
            Favs = f.read().splitlines()
            if fav in Favs:
                Favs.remove(fav)
                Favs.append(newfav)
                f = open(mel.eval('getenv SLiBLib;') + 'settings/' + 'favorites.txt', 'w')
                f.write("\n".join(Favs))
                f.close()
                
            SLiBMessager('Renamed!', 'green')

            cmds.evalDeferred(lambda: (SLiBBrowserUpdateShader(), cmds.iconTextRadioButton('icon'+newName, e=1, sl=1)) )
            SLiBTexPathChangeWarning(path)

    else:
        sys.exit()

#BROWSER DOCK
def SLiBBrowserDockedUI():
    if cmds.menuItem('dockMenu', q=1, cb=1) == 1:
        if cmds.dockControl('slBrowserDock', q=1, exists=1):
            cmds.deleteUI('slBrowserDock')
        
        mainWindow = cmds.paneLayout(parent = mel.eval('$temp1=$gMainWindow'))
        cmds.dockControl('slBrowserDock', a='right', label = 'SLiB Browser v1.0', content = mainWindow, aa = ['right', 'left'] )
        cmds.control(slBrowserUI, e=1, parent = mainWindow)
    if cmds.menuItem('dockMenu', q=1, cb=1) == 0:
        cmds.dockControl('slBrowserDock', e=1, fl=1)

#BROWSER UI
def SLiBBrowserUI():
    if cmds.window('SLiBBrowser', q=1, exists=1):
        cmds.deleteUI('SLiBBrowser')
    if cmds.iconTextRadioCollection('mainCatCollection', q=1, exists=1):
        mainCatItem = cmds.iconTextRadioCollection( 'mainCatCollection', q=1, cia=1)
        for e in mainCatItem:
            cmds.deleteUI(e)
        cmds.deleteUI('mainCatCollection')
    cleanList=['slAssetCollection','Load','dock','Save','File','importREF','Import','ExportOptions','exportFRZ','exportPIV','exportMA','exportMB','exportOBJ','exportTEX','Export','CollectTex','FixTex','SearchLoc','SNR','EditDic','Tools','MassExport','GenThumbs','Batch','SLiBTypeComboBox','SLiBSubTypeComboBox']
    for e in cleanList:
        try:
            cmds.deleteUI(e)
            str(e) + ' deleted'
        except:
            str(e) + ' not found'
            pass

    mel.eval("optionVar -iv inViewMessageEnable true;")
    if currentRender == 'vray':
        try:
            mel.eval('unifiedRenderGlobalsWindow')
            cmds.window('unifiedRenderGlobalsWindow', e=1, vis=0)
            print 'Render Settings Window initialized'
        except:
            pass
    try:
        os.mkdir(mel.eval('getenv SLiBLib;') + '/' +  'Writable')
        cmds.sysFile(mel.eval('getenv SLiBLib;') + '/' +  'Writable', red=1)
    except:
        cmds.confirmDialog(m='Could not write to specified Library folder: \n' + mel.eval('getenv SLiBLib;') + '\nEither change your permissions or run Maya as Administrator')
        sys.exit()

    global slBrowserUI
    slBrowserUI = cmds.loadUI(uiFile = SLiBGuiPath + 'SLiBBrowser.ui')
    cmds.setParent(slBrowserUI)
    cmds.iconTextButton('freezeTrans', mw=0, mh=0, w=32, h=32, c=lambda *args: SLiBFreeze(), i=SLiBImage+'slib_freezetransform.png', ann=' Freeze Transformations ', p='exportTools1')
    cmds.iconTextButton('autoPlacePivot', mw=0, mh=0, w=32, h=32, c=lambda *args: SLiBAutoPLacePivot(), i=SLiBImage+'slib_autoplacepivot.png', ann=' Move Object to Origin and Pivot to Bottom ', p='exportTools2')
    cmds.iconTextCheckBox('SLiBIconCaption', mw=0, mh=0, w=32, h=32, i=SLiBImage + 'slib_ic_off.png', si=SLiBImage + 'slib_ic_on.png', cc=lambda *args: SLiBBrowserUpdateShader(), ann=' Icon Caption ON / OFF ', p='SLiBIconCaption_Layout')
    cmds.iconTextButton('SLiBIconCaption', mw=0, mh=0, w=32, h=32, i=SLiBImage + 'slib_fresh_on.png', c=lambda *args: SLiBBrowserUpdateShader(), ann=' Refresh Previews ', p='SLiBIconCaption_Layout')
    if cmds.optionVar(query = 'SLiBIconCaption') == 'True':
        cmds.iconTextCheckBox('SLiBIconCaption', e=1, v=1)
    cmds.textField('SLiBThumbSizeComboBox', e=1, changeCommand = lambda *args: SLiBBrowserUpdateShader())
    cmds.popupMenu(parent="SLiBThumbSizeComboBox", ctl=0, button=3)
    cmds.menuItem(l='64', command= lambda *args: (cmds.textField('SLiBThumbSizeComboBox', e=1, text='64'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='128', command= lambda *args: (cmds.textField('SLiBThumbSizeComboBox', e=1, text='128'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='196', command= lambda *args: (cmds.textField('SLiBThumbSizeComboBox', e=1, text='196'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='256', command= lambda *args: (cmds.textField('SLiBThumbSizeComboBox', e=1, text='256'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='384', command= lambda *args: (cmds.textField('SLiBThumbSizeComboBox', e=1, text='384'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='512', command= lambda *args: (cmds.textField('SLiBThumbSizeComboBox', e=1, text='512'), SLiBBrowserUpdateShader()))
    cmds.popupMenu(parent="SLiBThumbColumnsComboBox", ctl=0, button=3)
    cmds.menuItem(l='1', command= lambda *args: (cmds.textField('SLiBThumbColumnsComboBox', e=1, text='1'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='2', command= lambda *args: (cmds.textField('SLiBThumbColumnsComboBox', e=1, text='2'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='3', command= lambda *args: (cmds.textField('SLiBThumbColumnsComboBox', e=1, text='3'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='4', command= lambda *args: (cmds.textField('SLiBThumbColumnsComboBox', e=1, text='4'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='5', command= lambda *args: (cmds.textField('SLiBThumbColumnsComboBox', e=1, text='5'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='6', command= lambda *args: (cmds.textField('SLiBThumbColumnsComboBox', e=1, text='6'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='7', command= lambda *args: (cmds.textField('SLiBThumbColumnsComboBox', e=1, text='7'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='8', command= lambda *args: (cmds.textField('SLiBThumbColumnsComboBox', e=1, text='8'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='9', command= lambda *args: (cmds.textField('SLiBThumbColumnsComboBox', e=1, text='9'), SLiBBrowserUpdateShader()))
    cmds.menuItem(l='10', command= lambda *args: (cmds.textField('SLiBThumbColumnsComboBox', e=1, text='10'), SLiBBrowserUpdateShader()))
    cmds.optionMenu('SLiBTypeComboBox', e=1, changeCommand = lambda *args: SLiBBrowserUpdateShader())
    cmds.iconTextButton('RenderViewButton', w=256, h=256, mh=0, mw=0, image = SLiBImage + 'browser_logo_lt.png', c=lambda *args: SLiBBrowserRender(), p='rv_holder')
    cmds.popupMenu(parent="SLiB_TEXTFIELD_Name", ctl=0, button=3)
    cmds.menuItem(l='Name from Selection', command= lambda *args:  SLiBNameFromSelection())
    if currentRender == 'redshift':
        cmds.popupMenu(parent="SLiB_BUTTON_Render", ctl=0, button=3)
        cmds.menuItem(l='Reload (Redshift)', command= lambda *args:  SliBBrowserReloadRender())
    cmds.iconTextCheckBox('searchSwitch', mw=0, mh=0, w=32, h=32, i=SLiBImage + 'slib_search_off.png', si=SLiBImage + 'slib_search_on.png', onc=lambda *args: SLiBBrowserUpdateShader(), ofc=lambda *args: SLiBSearchOff(), p='SLiB_BUTTON_Search')
    cmds.popupMenu(parent="SLiB_TEXTFIELD_Info", ctl=0, button=3)
    cmds.menuItem(l='Replace Notes', command= lambda *args:  SLiBReplaceNotes())
    cmds.textField('SLiB_TEXTFIELD_Search', e=1, cc=lambda *args: (cmds.iconTextCheckBox('searchSwitch', e=1, v=1), SLiBBrowserUpdateShader()), ec=lambda *args: (cmds.iconTextCheckBox('searchSwitch', e=1, v=1), SLiBBrowserUpdateShader()), aie=1)
    cmds.popupMenu(parent="SLiB_TEXTFIELD_Search", ctl=0, button=3)
    cmds.menuItem(l='Clear', command= lambda *args: (cmds.textField('SLiB_TEXTFIELD_Search', e=1, text=''), SLiBBrowserUpdateShader()))
    cmds.textField('SLiBThumbColumnsComboBox', e=1, cc=lambda *args: SLiBBrowserUpdateShader())

    cmds.menu(label='File', allowOptionBoxes=0)
    cmds.menuItem('Load', label='Load Shaderball Scene...', c=lambda *args: loadTestRoom())
    cmds.menuItem( divider=1 )
    cmds.menuItem('dockMenu', label='Dock Browser Window', checkBox=0, c=lambda *args: SLiBBrowserDockedUI())
    cmds.menuItem( divider=1 )
    cmds.menuItem('Save', label='Save Window Settings', c=lambda *args: SLiBSaveWindowSettings())
    
    cmds.menu('Import', label='Import', allowOptionBoxes=1 )
    cmds.menuItem('importREF', label='as Reference', checkBox=0 )
    
    cmds.menu('Tools', label='Tools', allowOptionBoxes=0 )
    cmds.menuItem('CollectTex', label='Collect Texture(s) -> Current Project', c=lambda *args: "import SLiBCopyTexSetPathPy; reload(SLiBCopyTexSetPathPy); SLiBCopyTexSetPathPy.copyTexturesToProject(object) ")
    cmds.menuItem( divider=1 )
    cmds.menuItem('FixTex', label='Fix Missing Texture(s)', c="import SLiBCopyTexSetPathPy; reload(SLiBCopyTexSetPathPy); SLiBCopyTexSetPathPy.copyTexturesToProject(object) ")
    cmds.menuItem('SearchLoc', label='Specify Search Location', ob=1, c=lambda *args: SLiBTexPathUI())
    
    cmds.menu('Batch', label='Batch', allowOptionBoxes=0 )
    cmds.menuItem('GenThumbs', label='Generate Thumbs for Textures...', c=lambda *args: SLiBBatchTextures() )
    cmds.iconTextRadioCollection( 'mainCatCollection')
    cmds.iconTextRadioButton('SHADER', st='textOnly', l='SHADER', bgc=[0,0,0], p='SLiB_AssetType', cc=lambda *args: SLiBLChangeType())
    cmds.iconTextRadioButton('OBJECTS', st='textOnly', l='OBJECTS', bgc=[0,0,0], p='SLiB_AssetType', cc=lambda *args: SLiBLChangeType())
    cmds.iconTextRadioButton('LIGHTS', st='textOnly', l='LIGHTS', bgc=[0,0,0], p='SLiB_AssetType', cc=lambda *args: SLiBLChangeType())
    cmds.iconTextRadioButton('TEXTURES', st='textOnly', l='TEXTURES', bgc=[0,0,0], p='SLiB_AssetType', cc=lambda *args: SLiBLChangeType())
    cmds.iconTextRadioButton('FAVORITES', st='textOnly', l='FAVORITES', bgc=[0,0,0], p='SLiB_AssetType', cc=lambda *args: SLiBBrowserUpdateFavorites())
    cmds.iconTextRadioButton('SHADER', e=1, sl=1)
    cmds.showWindow(slBrowserUI)
    try:
        SLiBLoadWindowSettings()
    except:
        pass
    SLiBBrowserUpdateType()
    print 'SLiB >>> SLiB Browser loaded\n',
    SLiBMessager('SLiB Browser loaded', 'green')
    
def SLiBLChangeType():
    if gib('mainCat') == 'favorites':
        SLiBBrowserUpdateFavorites()
    else:
        SLiBBrowserUpdateTypeOnly()
        try: 
            SLiBLoadCat()
        except:
            pass
        SLiBBrowserUpdateSubTypeOnly()
        try:
            SLiBLoadSubCat()
        except:
            pass
        SLiBBrowserUpdateShader()
    
def gib(x):
    if x == 'library':
        library = mel.eval('getenv SLiBLib;')
        return library
    if x == 'mainCat':
        mainCat = cmds.iconTextRadioCollection('mainCatCollection', q=1, sl=1).lower()
        return mainCat
    if x == 'cat':
        cat = cmds.optionMenu('SLiBTypeComboBox', q=1, v=1)
        return cat
    if x == 'subCat':
        subCat = cmds.optionMenu('SLiBSubTypeComboBox', q=1, v=1)
        return subCat
    if x == 'file':
        try:
            file = cmds.iconTextRadioButton(cmds.iconTextRadioCollection('slAssetCollection', q=1, sl=1), q=1, label=1)
            return file
        except:
            SLiBMessager('No Shader/Asset selected!', 'red')
            
    if x == 'name':
        name = cmds.textField('SLiB_TEXTFIELD_Name', q=1, text=1).replace(' ','_')
        return name
    if x == 'size':
        ObjX = abs(cmds.getAttr(selection+".boundingBoxMaxX")) + abs(cmds.getAttr(selection+".boundingBoxMinX"))
        ObjY = abs(cmds.getAttr(selection+".boundingBoxMaxY")) + abs(cmds.getAttr(selection+".boundingBoxMinY"))
        ObjZ = abs(cmds.getAttr(selection+".boundingBoxMaxZ")) + abs(cmds.getAttr(selection+".boundingBoxMinZ"))
        return ObjX,ObjY,ObjZ
    if x == 'position':
        ObjPos = cmds.xform(selection, q=1, t=1)
        return ObjPos
    
def SLiBCurrLoc():
    if cmds.optionMenu('SLiBSubTypeComboBox', q=1, ni=1) == 0:
        currLoc = gib('library') + gib('mainCat') + '/' + gib('cat')
    if cmds.optionMenu('SLiBSubTypeComboBox', q=1, ni=1) != 0:
        if gib('subCat') == 'Select...':
            currLoc = gib('library') + gib('mainCat') + '/' + gib('cat')
        else:
            currLoc = gib('library') + gib('mainCat') + '/' + gib('cat') + '/_SUB/' + gib('subCat')
    return currLoc
        
def SLiBSearchOff():
    cmds.textField('SLiB_TEXTFIELD_Search', e=1, text='')
    SLiBBrowserUpdateShader()
    
def SLiBSaveCats():
    if gib('mainCat') == 'shader':
        global oldShaderCat
        oldShaderCat = gib('cat')
        #print oldShaderCat  + ' << as last Shader Category saved\n',
        if cmds.optionMenu('SLiBSubTypeComboBox', q=1, ni=1) != 0:
            global oldShaderSubCat
            oldShaderSubCat = gib('subCat')
            #print oldShaderSubCat + ' << as last Shader SubCategory saved\n',
    if gib('mainCat') == 'objects':
        global oldObjectCat
        oldObjectCat = gib('cat')
        #print oldObjectCat + ' << as last Asset Category saved\n',
        if cmds.optionMenu('SLiBSubTypeComboBox', q=1, ni=1) != 0:
            global oldObjectSubCat
            oldObjectSubCat = gib('subCat')
            #print oldObjectSubCat + ' << as last Asset SubCategory saved\n',
    if gib('mainCat') == 'lights':
        global oldLightCat
        oldLightCat = gib('cat')
        #print oldLightCat + ' << as last Light Category saved\n',
        if cmds.optionMenu('SLiBSubTypeComboBox', q=1, ni=1) != 0:
            global oldLightSubCat
            oldLightSubCat = gib('subCat')
            #print oldLightSubCat + ' << as last Light SubCategory saved\n',
    if gib('mainCat') == 'textures':
        global oldTextureCat
        oldTextureCat = gib('cat')
        #print oldTextureCat + ' << as last Texture Category saved\n',
        if cmds.optionMenu('SLiBSubTypeComboBox', q=1, ni=1) != 0:
            global oldTextureSubCat
            oldTextureSubCat = gib('subCat')
            #print oldTextureSubCat + ' << as last Texture SubCategory saved\n',


def SLiBLoadCat():
    if gib('mainCat') == 'shader':
        try:
            cmds.optionMenu('SLiBTypeComboBox', e=1, v=oldShaderCat)
            #print oldShaderCat + ' >> as last used Shader Category loaded\n',
        except:
            cmds.optionMenu('SLiBTypeComboBox', e=1, v='Select...')
    if gib('mainCat') == 'objects':
        try:
            cmds.optionMenu('SLiBTypeComboBox', e=1, v=oldObjectCat)
            #print oldObjectCat + ' >> as last used Asset Category loaded\n',
        except:
            cmds.optionMenu('SLiBTypeComboBox', e=1, v='Select...')
    if gib('mainCat') == 'lights':
        try:
            cmds.optionMenu('SLiBTypeComboBox', e=1, v=oldLightCat)
            #print oldLightCat + ' >> as last used Light Category loaded\n',
        except:
            cmds.optionMenu('SLiBTypeComboBox', e=1, v='Select...')
    if gib('mainCat') == 'textures':
        try:
            cmds.optionMenu('SLiBTypeComboBox', e=1, v=oldTextureCat)
            #print oldTextureCat + ' >> as last used Texture Category loaded\n',
        except:
            cmds.optionMenu('SLiBTypeComboBox', e=1, v='Select...')

def SLiBLoadSubCat():
    if gib('mainCat') == 'shader':
        try:
            cmds.optionMenu('SLiBSubTypeComboBox', e=1, v=oldShaderSubCat)
            #print oldShaderSubCat + ' >> as last used Shader SubCategory loaded\n',
        except:
            pass
    if gib('mainCat') == 'objects':
        try:
            cmds.optionMenu('SLiBSubTypeComboBox', e=1, v=oldObjectSubCat)
            #print oldObjectSubCat + ' >> as last used Asset SubCategory loaded\n',
        except:
            pass
    if gib('mainCat') == 'lights':
        try:
            cmds.optionMenu('SLiBSubTypeComboBox', e=1, v=oldLightSubCat)
            #print oldLightSubCat + ' >> as last used Light SubCategory loaded\n',
        except:
            pass
    if gib('mainCat') == 'textures':
        try:
            cmds.optionMenu('SLiBSubTypeComboBox', e=1, v=oldTextureSubCat)
            #print oldTextureSubCat + ' >> as last used Texture SubCategory loaded\n',
        except:
            pass
            
def SLiBBrowserCreateDir():
    result = cmds.promptDialog(title='Create New Category', message='Enter Name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
    if result == 'OK':
        newDirName = cmds.promptDialog(q=1, t=1).replace(' ','_')
        newDir = gib('library') + gib('mainCat') + '/' + newDirName
        if os.path.isdir(newDir) == 1:
            SLiBMessager('Category already exists!', 'red')
            sys.exit()
        else:
            cmds.sysFile( newDir, makeDir=1 )
            cmds.sysFile( newDir + '/_SUB', makeDir=1 )
            SLiBBrowserUpdateTypeOnly()
            cmds.optionMenu('SLiBTypeComboBox', e=1, v=newDirName)
            SLiBBrowserUpdateSubType()
            SLiBBrowserUpdateShader()
            SLiBMessager('Cat < ' + str(newDirName) + ' > created.', 'green')
    else:
        sys.exit()
    
def SLiBBrowserRemoveDir():
    if gib('mainCat') == 'textures':
        deleteDir = SLiBCurrLoc()
        cmds.sysFile( deleteDir + '/_SUB', red=1 )
        cmds.sysFile( deleteDir + '/_THUMBS', red=1 )
    else:
        deleteDir = gib('library') + gib('mainCat') + '/' + gib('cat')
    
    if len(os.listdir(deleteDir)) == 1:
        if os.listdir(deleteDir)[0] == '_SUB':
            cmds.sysFile( deleteDir + '/_SUB', red=1 )
            cmds.sysFile( deleteDir, red=1 )
    else:
        SLiBMessager('Category is not empty!', 'red')
        sys.exit()
    SLiBBrowserUpdateType()
    SLiBBrowserUpdateSubType()
    SLiBMessager('Cat < ' + str(deleteDir) + ' > removed.', 'green')

def SLiBBrowserCreateSubDir():
    result = cmds.promptDialog(title='Create New SubCategory', message='Enter Name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
    if result == 'OK':
        newSubDirName = cmds.promptDialog(q=1, t=1).replace(' ','_')
        newSubDir = gib('library') + gib('mainCat') + '/' + gib('cat') + '/_SUB/' + newSubDirName
        if os.path.isdir(newSubDir) == 1:
            SLiBMessager('SubCategory already exists!', 'red')
            sys.exit()
        else:
            cmds.sysFile( newSubDir, makeDir=1 )
            SLiBBrowserUpdateSubType()
            cmds.optionMenu('SLiBSubTypeComboBox', e=1, v=newSubDirName)
            SLiBBrowserUpdateShader()
            SLiBMessager('Cat < ' + str(newSubDirName) + ' > created.', 'green')
    else:
        sys.exit()

def SLiBBrowserRemoveSubDir():
    deleteSubDir = gib('library') + gib('mainCat') + '/' + gib('cat') + '/_SUB/' + gib('subCat')
    cmds.sysFile( deleteSubDir, red=1 )
    SLiBMessager('SubCat < ' + str(deleteSubDir) + ' > removed.', 'green')
    SLiBBrowserUpdateSubType()
    SLiBBrowserUpdateShader()
    
def SLiBReplacePreview():
    if gib('mainCat') == 'textures':
        SLiBMessager('Textures not supported!', 'red')
        sys.exit()
    else:
        if cmds.iconTextRadioCollection('slAssetCollection', q=1, sl=1) == 'NONE':
            SLiBMessager('Please select something!', 'red')
            sys.exit()
        else:
            oldOne = cmds.iconTextRadioCollection('slAssetCollection', q=1, sl=1)
            newPreview = os.path.splitext(gib('file'))[0]
            newOne = cmds.iconTextButton('RenderViewButton', q=1, i=1)
            image = om.MImage()
            image.readFromFile(newOne)
            image.resize( 512, 512 )
            image.writeToFile(newPreview + '.png', 'png')
            SLiBBrowserUpdateShader()
            cmds.iconTextRadioButton(oldOne, e=1, sl=1)
            SLiBMessager('Preview Image replaced!', 'green')
        
def SLiBReplaceNotes():
    if gib('mainCat') == 'textures':
        SLiBMessager('Textures not supported!', 'red')
        sys.exit()
    else:
        if cmds.iconTextRadioCollection('slAssetCollection', q=1, sl=1) == 'NONE':
            SLiBMessager('Please select something!', 'red')
            sys.exit()
        else:
            notesFile = os.path.splitext(gib('file'))[0]
            notes = cmds.scrollField('SLiB_TEXTFIELD_Info', q=1, text=1)
            f = open(notesFile + '.info', 'w')
            f.write(str(notes))
            f.close()
            SLiBMessager('Notes updated!', 'green')

def SLiBBrowserPlayBlast():
    object = cmds.ls(sl=1)
    #try:
    #    initialView = omui.M3dView().active3dView()    
    #    camDP = om.MDagPath()
    #    initialView.getCamera(camDP)
    #    camFn = om.MFnCamera(camDP)
    #    camera1 = cmds.modelPanel(cmds.getPanel(wf=1), q=1, cam=1)
    #    camera0 = cmds.listRelatives(camera1)[0]
    #except:
    #    cmds.confirmDialog(m="Please select Viewport you want to PlayBlast from!")
    #    sys.exit()

    storePath = cmds.workspace(q=1, fn=1) + "/" + 'images/'
    imageName = storePath+'/'+'icontemp'
    renderGlobals = cmds.getAttr("defaultRenderGlobals.imageFormat")
    perspPanel = cmds.getPanel( withLabel='Persp View')
    cmds.setFocus(perspPanel)
    cmds.select(cl=True)
    playBlast = cmds.playblast(forceOverwrite = 1, framePadding = 0, viewer = 0, showOrnaments = 0, frame = cmds.currentTime(q = 1), widthHeight = [512,512], percent = 100, format = 'iff', compression = 'png', filename = imageName)
    playBlast = playBlast.replace('####', '0')
    cmds.deleteUI('RenderViewButton')
    cmds.iconTextButton('RenderViewButton', w=256, h=256, mh=0, mw=0, image = playBlast, c=lambda *args: SLiBBrowserRender(), p='rv_holder')
    cmds.popupMenu(parent="RenderViewButton", ctl=0, button=3)
    cmds.menuItem(l='Replace Preview Image', command= lambda *args:  SLiBReplacePreview())
    try:
        cmds.select(object)
    except:
        pass
        
def SLiBBrowserRender():
    try:
        initialView = omui.M3dView().active3dView()    
        camDP = om.MDagPath()
        initialView.getCamera(camDP)
        camFn = om.MFnCamera(camDP)
        camera1 = cmds.modelPanel(cmds.getPanel(wf=1), q=1, cam=1)
        camera0 = cmds.listRelatives(camera1)[0]
    except:
        SLiBMessager('Please select Viewport you want to Render from!', 'red')
        sys.exit()
    
    cmds.setAttr('defaultResolution.width', 512)
    cmds.setAttr('defaultResolution.height', 512)
    aspRatio = float(cmds.getAttr('defaultResolution.width'))/float(cmds.getAttr('defaultResolution.height'))
    cmds.setAttr('defaultResolution.deviceAspectRatio', aspRatio)
    try:
        cmds.setAttr('vraySettings.wi',512)
        cmds.setAttr('vraySettings.he', 512)
        aspRatio = float(cmds.getAttr('vraySettings.wi'))/float(cmds.getAttr('vraySettings.he'))
        cmds.setAttr('vraySettings.aspr', aspRatio)
    except:
        pass
    
    SliBBrowserStopRender()
    if currentRender == 'arnold':
        cmds.arnoldRender(cam=camera1)

    if currentRender == 'vray':
        mel.eval("vrend -ipr false;")
        cmds.setAttr('vraySettings.vfbOn', 0)
        cmds.setAttr('vraySettings.samplerType', 1)
        cmds.setAttr ('vraySettings.sRGBOn', 1)
        mel.eval("vrend -cam "+camera0+";")
        
    if currentRender == 'redshift':
        cmds.setAttr("defaultRenderGlobals.imageFormat", 51)
        cmds.rsRender( r=1, cam=camera0)
        
    if currentRender == 'mentalRay':
        cmds.Mayatomr(pv=1, cam=camera0)
        
    if currentRender == 'mayaSoftware':
        mel.eval("renderIntoNewWindow render")

    imageName = cmds.workspace(q=1, fn=1) + '/images/' + 'icontemp' + '.png'
    renderGlobals = cmds.getAttr("defaultRenderGlobals.imageFormat")
    cmds.setAttr("defaultRenderGlobals.imageFormat", 32)
    cmds.renderWindowEditor('renderView', e=1, wi=imageName)
    cmds.setAttr("defaultRenderGlobals.imageFormat", renderGlobals)
    cmds.deleteUI('RenderViewButton')
    cmds.iconTextButton('RenderViewButton', w=256, h=256, mh=0, mw=0, i=imageName, c=lambda *args: SLiBBrowserRender(), p='rv_holder')
    cmds.popupMenu(parent="RenderViewButton", ctl=0, button=3)
    cmds.menuItem(l='Replace Preview Image', command= lambda *args:  SLiBReplacePreview())
    if currentRender == 'mayaSoftware':
        if cmds.window('renderViewWindow', q=1, exists=1):
            cmds.deleteUI('renderViewWindow')
    
def SliBLoadFromRV():
    imageName = cmds.workspace(q=1, fn=1) + '/images/' + 'icontemp' + '.png'
    renderGlobals = cmds.getAttr("defaultRenderGlobals.imageFormat")
    cmds.setAttr("defaultRenderGlobals.imageFormat", 32)
    cmds.renderWindowEditor('renderView', e=1, wi=imageName)
    cmds.setAttr("defaultRenderGlobals.imageFormat", renderGlobals)
    cmds.deleteUI('RenderViewButton')
    cmds.iconTextButton('RenderViewButton', w=256, h=256, mh=0, mw=0, i=imageName, c=lambda *args: SLiBBrowserRender(), p='rv_holder')
    cmds.popupMenu(parent="RenderViewButton", ctl=0, button=3)
    cmds.menuItem(l='Replace Preview Image', command= lambda *args:  SLiBReplacePreview())
    
def SliBLoadFromFile():
    imageName = cmds.fileDialog(m=0)
    if len(imageName) == 0:
        sys.exit()
    else:
        cmds.deleteUI('RenderViewButton')
        cmds.iconTextButton('RenderViewButton', w=256, h=256, mh=0, mw=0, i=imageName, c=lambda *args: SLiBBrowserRender(), p='rv_holder')
        cmds.popupMenu(parent="RenderViewButton", ctl=0, button=3)
        cmds.menuItem(l='Replace Preview Image', command= lambda *args:  SLiBReplacePreview())

def SliBBrowserStopRender():
    try:
        if currentRender == 'arnold':
            cmds.arnoldIpr(mode='stop')
        if currentRender == 'vray':
            mel.eval('vrayProgressEnd;')
            mel.eval("vrend -ipr false;")
        if currentRender == 'redshift':
            cmds.rsRender( r=1, stopIpr=1)
    except:
        pass
        
def SliBBrowserReloadRender():
    cmds.deleteUI('RenderViewButton')
    imageName = cmds.workspace(q=1, fn=1) + '/images/' + 'icontemp' + '.png'
    try:
        cmds.iconTextButton('RenderViewButton', w=256, h=256, mh=0, mw=0, i=imageName, c=lambda *args: SLiBBrowserRender(), p='rv_holder')
    except:
        cmds.iconTextButton('RenderViewButton', w=256, h=256, mh=0, mw=0, i=SLiBImage + 'browser_logo.png', c=lambda *args: SLiBBrowserRender(), p='rv_holder')
    cmds.popupMenu(parent="RenderViewButton", ctl=0, button=3)
    cmds.menuItem(l='Replace Preview Image', command= lambda *args:  SLiBReplacePreview())

##### SLiB | TEX FINDER #####        
def SLiBTexPathUI():
    SLiBTexPathUI = cmds.loadUI(uiFile = SLiBGuiPath + 'SLiBTexPath.ui')
    if cmds.window(SLiBTexPathUI, exists = 1):
        cmds.deleteUI(SLiBTexPathUI)
    SLiBTexPathUI = cmds.loadUI(uiFile = SLiBGuiPath + 'SLiBTexPath.ui')
    cmds.showWindow(SLiBTexPathUI)
    cmds.window(SLiBTexPathUI, e=1, titleBar = 1, topEdge = 1)
        
def SLiBTexPathButton():
    filePath = cmds.fileDialog2(startingDirectory = os.sep, fileMode = 3)
    try:
        if platform.system() == 'Windows':
            texturePathEdit = cmds.textField('SLiBLibTexPath', e=1, text = filePath[0].replace('/', '\\'))
        else:
            texturePathEdit = cmds.textField('SLiBLibTexPath', e=1, text = filePath[0])
    except:
        pass

def SLiBTexPathSave():
    TexPath = cmds.textField('SLiBLibTexPath', q=1, text=1)
    if TexPath != cmds.optionVar(q = 'TexPath'):
        if not os.path.exists(TexPath):
            SLiBMessager('No valid Path entered?!', 'red')
            return None
        cmds.optionVar(stringValue = ('TexPath', TexPath.replace('\\', '/')))
    cmds.deleteUI("SLiBTexPathUI")

def SLiBDupFix(padding=3):
    badXforms = [f for f in cmds.ls() if '|' in f]
    badXformsUnlock = [f for f in badXforms if cmds.lockNode(f,q=1,lock=1)[0] == False]
    count = 0
    countDict = {}
    for f in badXformsUnlock:
        countDict[f] = f.count('|')
    for key,value in sorted(countDict.iteritems(),reverse=True, key=lambda (key,value): (value,key)):
        n = 1
        newObj = cmds.rename(key,key.split('|')[-1]+'_'+str(n).zfill(padding))
        while newObj.count('|') > 0:
            n += 1
            basename = newObj.split('|')[-1]
            newName = '_'.join(basename.split('_')[0:-1])+'_'+str(n).zfill(padding)
            newObj = cmds.rename(newObj,newName)
        print 'renamed %s to %s' % (key,newObj)
        count = count+1
    if count < 1:
        pass
    else:
        print 'SLiB >>> Found and renamed '+ str(count) +' Duplicates.',

def loadTestRoom():
    answer = cmds.confirmDialog( title='Warning', message='Please make sure you saved the current scene! \nDo you want to proceed?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    if answer == 'Yes':
        needSave = cmds.file(q=1, modified=1)
        testroomfile = gib('library') + '/scene/' + currentRender + '_SLiB_ShaderTestRoom_hdri.ma'
        cmds.file( f=1, new=1 )
        cmds.file( testroomfile, o=1 )
        savename = cmds.workspace(q = 1, fullName = 1) + '/' + currentRender + '_' + cmds.date().replace (" ", "_").replace ("/", "").replace (":", "") + '.ma'
        cmds.file( rename=savename )
        cmds.file( save=1, type='mayaAscii' )
        SLiBMessager('ShaderBall Scene for ' + str(currentRender) + ' loaded!', 'green')
    else:
        sys.exit()
        
def SLiBSaveWindowSettings():
    SLIBPrefs = []
    docked = cmds.menuItem('dockMenu', q=1, cb=1)
    winX = cmds.window('SLiBBrowser', q=1, w=1)
    winY = cmds.window('SLiBBrowser', q=1, h=1)
    res = str(cmds.textField('SLiBThumbSizeComboBox', q=1, text=1))
    col = str(cmds.textField('SLiBThumbColumnsComboBox', q=1, text=1))
    impRef = cmds.menuItem('importREF' , q=1, cb=1)

    
    SLIBPrefs.append(docked)
    SLIBPrefs.append(winX)
    SLIBPrefs.append(winY)
    SLIBPrefs.append(res)
    SLIBPrefs.append(col)
    SLIBPrefs.append('onlyPro')
    SLIBPrefs.append(impRef)
    SLIBPrefs.append('onlyPro')
    SLIBPrefs.append('onlyPro')
    SLIBPrefs.append('onlyPro')
    SLIBPrefs.append('onlyPro')
    
    f = open(mel.eval('getenv SLiBLib;') + 'settings/' + 'windowPrefs.txt', 'w')
    f.write(str(SLIBPrefs).replace("'",'').replace(' ','').replace('[','').replace(']','').replace('True','1').replace('False','0'))
    f.close()
    SLiBMessager('Window Layout saved!', 'green')

def SLiBLoadWindowSettings():
    f = open(mel.eval('getenv SLiBLib;') + 'settings/' + 'windowPrefs.txt', 'r')
    s = f.read()
    p = s.split(',')
    
    if int(p[0]) == 1:
        cmds.menuItem('dockMenu', e=1, cb=1)
        SLiBBrowserDockedUI()
        cmds.dockControl('slBrowserDock', e=1, w=int(p[1]))
        #cmds.dockControl('slBrowserDock', e=1, h=int(p[2]))
    
    if int(p[0]) == 0:
        cmds.window('SLiBBrowser', e=1, w=int(p[1]))
        cmds.window('SLiBBrowser', e=1, h=int(p[2]))
    cmds.iconTextRadioCollection('mainCatCollection', e=1, sl=p[5])
    cmds.textField('SLiBThumbSizeComboBox', e=1, text=int(p[3]))
    cmds.textField('SLiBThumbColumnsComboBox', e=1, text=int(p[4]))
    cmds.menuItem('importREF' , e=1, cb=int(p[6]))

    
def SLiBBatchTextures():
    assetPath = SLiBCurrLoc()
    destPath = assetPath + '/_THUMBS/'
    failed=[]
    if gib('mainCat') == 'textures':
        if gib('cat') != 'Select...':
            if os.path.isdir(destPath) != True:
                os.mkdir(destPath)
            textureList = os.listdir(assetPath)
            for file in textureList:
                if 'swatch' not in file:
                    if '_THUMBS' not in file:
                        if '_SUB' not in file:
                            cmds.progressBar('PreviewProgress', e=1, maxValue=len(textureList))
                            p = os.path.join(assetPath,file)
                            d = os.path.join(destPath,file)
                            try:
                                image = om.MImage()
                                image.readFromFile(p)
                                image.resize( 512, 512 )
                                image.writeToFile(d, 'png')
                                print 'SLIB >>> Thumbnail generated for: ' + file
                            except:
                                print 'SLIB>>> Failed for: ' + file
                                failed.append(file)
                            cmds.progressBar('PreviewProgress', e=1, step=1)
            cmds.progressBar('PreviewProgress', e=1, pr=0)
            SLiBBrowserUpdateTextures()
            if len(failed) != 0:
                SLiBMessager('Thumbnail Generation failed for: ' + str(len(failed)) + 'File(s)! Please check Script Editor.', 'red')
            else:
                SLiBMessager('Thumbnail Generation finished!', 'green')
        else:
            SLiBMessager('Please select a Texture Category!', 'red')
            sys.exit()
    else:
        SLiBMessager('Only working with Textures!', 'red')
        sys.exit()
        
def SLiBFreeze():
    obj = cmds.ls(sl=1)
    if len(obj) != 0:
        cmds.makeIdentity(obj, apply=1, t=1, r=1, s=1, n=0)
        SLiBMessager('Freezed!', 'blue')
    else:
        SLiBMessager('Please select an Object!', 'red')

def SLiBAutoPLacePivot():
    obj = cmds.ls(sl=1)
    if len(obj) != 0:
        cmds.xform(obj, cp=1)
        bbox = cmds.exactWorldBoundingBox()
        bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
        cmds.xform(obj, piv=bottom, ws=1)
        cmds.move( 0, 0, 0, obj, rpr=1 )
        SLiBMessager("Object moved to Origin and Pivot placed at bottom!", 'blue')
    else:
        SLiBMessager('Please select an Object!', 'red')
        
def SLiBMessager(message, color):
    cmds.textField('SLiB_TEXTFIELD_Message', e=1 , text=message)
    if color == 'none':
        cmds.textField('SLiB_TEXTFIELD_Message', e=1 , bgc=[0.15,0.15,0.15])  #neutral
    if color == 'green':
        cmds.textField('SLiB_TEXTFIELD_Message', e=1 , bgc=[0,0.9,0])   #success
    if color == 'yellow':
        cmds.textField('SLiB_TEXTFIELD_Message', e=1 , bgc=[1,0.5,0])   #yellow
    if color == 'red':
        cmds.textField('SLiB_TEXTFIELD_Message', e=1 , bgc=[0.9,0,0])   #error
    if color == 'blue':
        cmds.textField('SLiB_TEXTFIELD_Message', e=1 , bgc=[0,0.75,0.99])   #blue
        
def SLiBAddFav(mode):
    fav = str((gib('file')))
    file = cmds.iconTextRadioButton(cmds.iconTextRadioCollection('slAssetCollection', q=1, sl=1), q=1, ann=1) 
    f = open(mel.eval('getenv SLiBLib;') + 'settings/' + 'favorites.txt', 'r')
    Favs = f.read().splitlines()
    tempFavs = Favs
    if mode == 'add':
        if fav in Favs:
            SLiBMessager('Already a Favorite!', 'red')
            sys.exit()
        if fav not in Favs:
            tempFavs.append(fav)
            f = open(mel.eval('getenv SLiBLib;') + 'settings/' + 'favorites.txt', 'w')
            f.write("\n".join(tempFavs))
            f.close()
            if gib('mainCat') != 'favorites':
                cmds.iconTextButton('favCB'+file, e=1, i=SLiBImage + 'SLiB_fav_on.png')
                cmds.menuItem('favItem'+file, e=1, l='Remove from Favorites', c=lambda *args: SLiBAddFav('remove'))
            SLiBMessager('Added to Favorites!', 'green')
            if gib('mainCat') == 'favorites':
                cmds.evalDeferred(lambda: SLiBBrowserUpdateShader())

    if mode == 'remove':
        Favs.remove(fav)
        f = open(mel.eval('getenv SLiBLib;') + 'settings/' + 'favorites.txt', 'w')
        f.write("\n".join(Favs))
        f.close()
        SLiBMessager('Removed from Favorites!', 'green')
        if gib('mainCat') != 'favorites':
            cmds.iconTextButton('RenderViewButton', e=1, i=SLiBImage + 'browser_logo.png')
            cmds.text('SLiB_shaderName', e=1, l='', al='center')
            cmds.iconTextButton('favCB'+file, e=1, i=SLiBImage + 'SLiB_fav_off.png')
            cmds.menuItem('favItem'+file, e=1, l='ADD to Favorites', c=lambda *args: SLiBAddFav('add'))
        if gib('mainCat') == 'favorites':
            cmds.evalDeferred(lambda: SLiBBrowserUpdateShader())
        
def SLiBBrowserUpdateFavorites():
    SLiBFlushOptionMenu('SLiBTypeComboBox')
    SLiBFlushOptionMenu('SLiBSubTypeComboBox')
    cmds.optionMenu('SLiBTypeComboBox', e=1, en=0)
    cmds.optionMenu('SLiBSubTypeComboBox', e=1, en=0)
    
    if cmds.scrollLayout('SLiBScrollLayoutBrowser', q=1, exists=1):
        cmds.deleteUI('SLiBScrollLayoutBrowser', layout=1)
    
    cmds.scrollLayout('SLiBScrollLayoutBrowser', p="SLiB_thumbsframe", bgc=[0.15,0.15,0.15])
    iconSize = cmds.textField('SLiBThumbSizeComboBox', q=1, text=1)
    iconSize = cmds.textField('SLiBThumbSizeComboBox', q=1, text=1)
    if int(iconSize) > 1024:
        iconSize = [1024]
        cmds.textField('SLiBThumbSizeComboBox', e=1, text=iconSize[0])
    coll = cmds.textField('SLiBThumbColumnsComboBox', q=1, text=1)
    cmds.optionVar(stringValue = ('SLiBIconCaption', cmds.iconTextCheckBox('SLiBIconCaption', q=1, v=1)))
    cmds.rowColumnLayout('Icons', nc=int(coll), p="SLiBScrollLayoutBrowser")
    cmds.iconTextRadioCollection('slAssetCollection', p='Icons')
    
    f = open(mel.eval('getenv SLiBLib;') + 'settings/' + 'favorites.txt', 'r')
    Favs = f.read().splitlines()
    if len(Favs) != 0:
        cmds.progressBar('PreviewProgress', e=1, pr=0)
        cmds.progressBar('PreviewProgress', e=1, maxValue=(len(Favs)))
        for curFile in Favs:
            if os.path.isfile(curFile) == True:
                curAssetPath = os.path.dirname(curFile)
                file = os.path.basename(curFile)
                fileName = os.path.splitext(file)[0]
                fileEx = os.path.splitext(curFile)[1]
                if fileEx == '.mb' or fileEx == '.ma' or fileEx == '.obj':
                    image =  curAssetPath + '/' +  fileName + '.png'
                    if len(iconSize) > 1:
                        if cmds.optionVar(query = 'SLiBIconCaption') == 'True':
                           cmds.columnLayout(rowSpacing = 6, columnWidth = int(iconSize))
                        cmds.iconTextRadioButton('icon'+str(fileName), i=image, mw=3, mh=3, h=int(iconSize), w=int(iconSize), onc=lambda *args: SLiBBrowserUpdateInfo(), l=curFile, ann=fileName)
                        cmds.popupMenu('pop'+str(fileName), parent='icon'+str(fileName), ctl=0, button=3, pmc=partial(SLiBBrowserPostMenu, fileName))
                        cmds.menuItem(l=fileName, i=image, bld=1, en=0)
                        cmds.menuItem(l='', en=0)
                        cmds.menuItem(l='IMPORT', c=lambda *args: SLiBBrowserImport('Normal'))
                        cmds.menuItem(divider=1)
                        if ('/objects/' or '/lights/') in image:
                            cmds.menuItem(l='IMPORT and Place at Selection', c=lambda *args: SLiBBrowserImport('Place'))
                            cmds.menuItem(l='IMPORT and Replace Selection', c=lambda *args: SLiBBrowserImport('Replace'))
                        cmds.menuItem(divider=1)
                        cmds.menuItem(l='REMOVE from Favorites', c=lambda *args: SLiBAddFav('remove'))
                        if cmds.optionVar(query = 'SLiBIconCaption') == 'True':
                            cmds.text(label = fileName, w=int(iconSize), align = 'center')
                            cmds.setParent('..')
                        cmds.progressBar('PreviewProgress', e=1, step=1)
                            
    cmds.progressBar('PreviewProgress', e=1, pr=0)
    cmds.undoInfo(st=1)
        