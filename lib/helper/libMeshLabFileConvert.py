#*************************************************************
# title:        libMeshLabFileConvert
#
# content:      converts all types of files with MESHLAB
#
# dependencies: userSetup
#
# author:       Alexander Richter 
# email:        contact@richteralexander.com
#*************************************************************

import os
import glob
from subprocess import call


#************************
# VARIABLES
#************************
meshLab     = "C:/Program Files/VCG/MeshLab/meshlabserver"

src         = [""]
replaceSrc  = "D:/Dropbox/ClothCap/FOOTAGE"
replaceDst  = "M:/10_footage"

srcFileFormat = "ply"
dstFileFormat = "obj"


#************************
# FUNCTIONS
#************************
def getFolderList(dataPath, fileType='*', ex = False):
    getFile = []

    if(os.path.exists(dataPath)):
        os.chdir(dataPath)
        for file in glob.glob(fileType):
            if ex:
                getFile.append(file)
            else:
                getFile.append((file.split('.')[0]))
    return (getFile)


#************************
# CONVERT
#************************
def convertFiles(newPath):
    replacePath = newPath.replace(replaceSrc, replaceDst)

    if not os.path.exists(replacePath):
        os.makedirs(replacePath)

    fileList = getFolderList(newPath, "*" + srcFileFormat, True)

    for fileName in fileList:
        cmd = meshLab + " -i " + newPath + "/" + fileName + " -o " + replacePath + "/" + fileName.replace(srcFileFormat, dstFileFormat)
        #print cmd
        call(cmd)

    print "I am done!"


#************************
# START
#************************
def start():
    for path in src:
        convertFiles(path)


start()