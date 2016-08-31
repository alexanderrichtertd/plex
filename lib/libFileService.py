#*************************************************************
# title:        libFileService
#
# content:      gets & sets folders and json files
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import os
import glob 
import json


#************************
# FOLDER & FILES
#************************
def getFolderList(dataPath, fileType='*', ex = False, exclude = "*"):
    getFile = []

    if(os.path.exists(dataPath)):
        os.chdir(dataPath)
        for fileName in glob.glob(fileType):
            if exclude in fileName:
                continue
            if ex:
                getFile.append(fileName)
            else:
                getFile.append((fileName.split('.')[0]))
    return (getFile)


def getAllFolderList(dataPath):
    getFile = []
    os.chdir(dataPath)

    for fileName in os.walk(dataPath):
        getFile.append(os.path.basename(fileName[0]))

    getFile.pop(0)
    return getFile


#************************
# JSON
#************************
def setJsonFile(dataPath, content):
    with open(dataPath, 'w') as outfile:
        json.dump(content.__dict__, outfile)


def getJsonFile(dataPath):
    with open(dataPath, 'r') as outfile:
        return json.load(outfile)
