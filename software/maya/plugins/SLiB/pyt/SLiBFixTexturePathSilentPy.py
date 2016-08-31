#########################################################################
#
#  SLiBFixTexturePathSilentPy.py v0.1
#
#########################################################################


import maya.cmds as cmds
import os
import sys


def SLiBFiXiTs():
    
    global slibTexPath
    slibTexPath = cmds.optionVar(query = 'SLiBLib') + '/' + '../' + '/'
    numTexfiles=len(rawlist)
    cleanList = [str(item) for item in missingFiles]
    missing=len(missingFiles)
    if missing:
        print 'Searching...'
        new(slibTexPath)
            
    else:
        pass
        #print 'Nothing to Fix!'
    
    missingN=len(missingFilesN)
    if missingN:
        print 'Searching...'
        newN(slibTexPath)
    
    else:
        pass
        #print 'Nothing to Fix!'
    
    print '\n' + str(missing) + ' Missing TextureFile(s) Found and Fixed!'
    print '\n' + str(missingN) + ' Missing NormalMap(s) Found and Fixed!'
    
##### DEF TEXFILES #####
def new(slibTexPath):
    for name in missingFiles:
        for root,dirs,files in os.walk(slibTexPath):
            print 'Searching in: ', root
            if name in files:
                print '%s Missing File found! New Path set to: >>> ' % name, root 
                newpath = os.path.join(root,name)
                replace(name, newpath)

def replace(name, newpath):
    for k in mydic.keys():
        if name in k:
            cmds.setAttr(k[0] + '.fileTextureName', newpath, type = 'string')

rawlist = cmds.ls(type='file')
slibTexPath=''
mydic=dict()
missingFiles =[]
numMissingFiles = len(missingFiles)


for each in rawlist:
    x = cmds.getAttr(each + '.fileTextureName')
    xsplit = x.split('/')
    y = xsplit[-1]
    mydic[each,y]=x
    
for k, v in mydic.items():
    if os.path.exists(v):
        print k[1], ' : ---> exists! No need to change Texture Path...'
        mydic.pop(k)
    else:
        missingFiles.append(k[1])
        
##### DEF NORMAL #####
def newN(slibTexPath):
    for name in missingFilesN:
        for root,dirs,files in os.walk(slibTexPath):
            print 'Searching in: ', root
            if name in files:
                print '%s Missing NormalMap found! New Path set to: >>> ' % name, root 
                newpath = os.path.join(root,name)
                replaceN(name, newpath)

def replaceN(name, newpath):
    for kN in mydicN.keys():
        if name in kN:
            cmds.setAttr(kN[0] + '.tex0', newpath, type = 'string')
            
slibTexPath=''
rawlistN = cmds.ls(type='RedshiftNormalMap')
mydicN=dict()
missingFilesN =[]
nummissingFilesN = len(missingFilesN)

for eachN in rawlistN:
    xN = cmds.getAttr(eachN + '.tex0')
    xsplit = xN.split('/')
    yN = xsplit[-1]
    mydicN[eachN,yN]=xN
    
for kN, vN in mydicN.items():
    if os.path.exists(vN):
        print kN[1], ' : ---> exists! No need to change Texture Path...'
        mydicN.pop(kN)
    else:
        missingFilesN.append(kN[1])