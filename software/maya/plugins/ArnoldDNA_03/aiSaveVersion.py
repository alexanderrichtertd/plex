# 256 pipeline tools
# save new version of current scene
# name your scene like "MY_SCENE_NAME_001.mb"
# Put script to \Documents\maya\201X-x64\scripts 
# In Python tab of Maya script editor execute code:
# import aiSaveVersion
# aiSaveVersion.SNV()

import maya.cmds as cmds
import os 
import sys
def SNV(*args):
    # break full name with path on peaces: path, name, ext
    fullName = cmds.file( q =1, sn = 1, shn =1)
    fullNamePath = cmds.file( q =1, sn = 1)
    absName = os.path.dirname(fullNamePath)
    noExtName = fullName.split('.')[0]
    ext = fullName.split('.')[1]
    splitName = noExtName.split('_')
    # increase version
    verIndex = len(splitName) - 1
    newVersion = str(int(splitName[verIndex]) + 1)
    padding = len(newVersion)
    zeros = len(splitName[verIndex]) - padding
    newVersion = '0'*zeros + newVersion
    # create new name with path and extension
    resolvedName = ''
    for i in range(0, verIndex):
        resolvedName += splitName[i] + '_'
    finalNamePath = absName + '/' + resolvedName +  newVersion + '.' + ext
    
    #check if the file exist
    if cmds.file(finalNamePath, q=1, exists = 1) == 1:
        confirm = cmds.confirmDialog ( title='WARNING', message='File exist! Overwrite?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if confirm == 'Yes':
            print 'File saved to a new version with overwrite '
        else:
            sys.exit()
    else:
        print 'File saved to a new version'
    
    #save as new version
    cmds.file( rename= finalNamePath)
    cmds.file( save = True)
    
