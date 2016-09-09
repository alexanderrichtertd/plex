#*************************************************************
# title         libFileService
#
# content       gets & sets folders and json files
#
# author        Alexander Richter 
# email         contact@richteralexander.com
#*************************************************************

import os
import glob 
import json





#************************
# JSON
#************************
def setJsonFile(path, content):
    with open(path, 'w') as outfile:
        json.dump(content.__dict__, outfile)


def getJsonFile(path):
    with open(path, 'r') as outfile:
        return json.load(outfile)


print getFileList(r"D:\Dropbox\arPipeline\v002\PUBLISH\data")