#########################################################################
#
#  SLiBCopyTexSetPathPy.py v0.3 by DGDM
#
#########################################################################

import maya.cmds as cmds
import maya.mel as mel
import os
import time
import shutil

def copyTexturesToProject(object):
    env = mel.eval('getenv SLiBLib;')
    texlistN = cmds.ls(type='RedshiftNormalMap')
    texlist = cmds.ls(type='file')
    textdestination = cmds.workspace(query = True, fullName = True) + "/" + 'sourceimages'
    textdestinationN = cmds.workspace(query = True, fullName = True) + "/" + 'sourceimages'
    si = 'sourceimages'
    window = cmds.window( title="SLiB | INFO:", iconName='Short Name', widthHeight=(400, 330), mxb=False, s=False )
    cmds.columnLayout()
    cmds.progressBar("Copy_progress", h=10, w=400)
    cmds.progressBar('Copy_progress', edit=1, pr=0)
    cmds.progressBar('Copy_progress', edit=1, maxValue=(len(texlist)))
    cmds.cmdScrollFieldReporter(width=400, height=258, clear=True)
    cmds.button( label='CLOSE', width=400, height=30, command=('cmds.deleteUI(\"' + window + '\", window=True)') )
    cmds.setParent( '..' )
    cmds.showWindow( window )
    

    for i in texlist:
        cmds.progressBar('Copy_progress', edit=1, step=1)
        fileName = cmds.getAttr("%s.fileTextureName" %i)
        finalName = fileName.split("}")[-1]
        justName = fileName.split("/")[-1]
        finalPath = textdestination + "/" + justName
        fileOrigin=  env+finalName
        if si in fileName:
            pass
        
        else:            
            try: 
                shutil.copy(fileOrigin, textdestination)
                cmds.setAttr("%s.fileTextureName" %i, finalPath, type="string")
                print 'copying: >>>' + '  ' + i
            except:
            	shutil.copy(finalName, textdestination)
                cmds.setAttr("%s.fileTextureName" %i, finalPath, type="string")
                print 'copying: >>>' + '  ' + i

    for n in texlistN:
        cmds.progressBar('Copy_progress', edit=1, step=1)
        fileNameN = cmds.getAttr("%s.tex0" %n)
        finalNameN = fileNameN.split("}")[-1]
        justNameN = fileNameN.split("/")[-1]
        finalPathN = textdestination + "/" + justNameN
        fileOriginN =  env+finalNameN
        if si in fileNameN:
            pass
        
        else:            
            try:
            	shutil.copy(fileOriginN, textdestinationN)
                cmds.setAttr("%s.tex0" %n, finalPathN, type="string")
                print 'copying: >>>' + '  ' + n
            except:
            	shutil.copy(finalNameN, textdestinationN)
                cmds.setAttr("%s.tex0" %n, finalPathN, type="string")
                print 'copying: >>>' + '  ' + n


    print '\nDONE! \n\nNew Texture Path set to:\n\n' + textdestination