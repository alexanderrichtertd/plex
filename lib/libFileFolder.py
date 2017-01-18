#*************************************************************
# CONTENT       create, search etc in/for file and folders
#*********************************************************************
# content   = create, search etc in/for file and folders
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <contact@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import glob
import logging
import webbrowser

import libLog

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.initLog(script=TITLE)

#************************
# FOLDER
# @BRIEF  creates a folder, checks if it already exists,
#         creates the folder above if the path is a file
def createFolder(path):
    if len(path.split(".")) > 1:
        path = os.path.dirname(path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            print("WARNING : Can not create folder : %s"% path)

# @BRIEF  opens folder even if file is given
def openFolder(path):
    if os.path.exists(path):
        if len(path.split(".")) > 1:
            path = os.path.dirname(path)
        webbrowser.open(path)
    else:
        print("WARNING : Not valid path : %s"% path)
    return path


#************************
# FILES
# @BRIEF  get a file/folder list with specifics
#
# @PARAM  path string.
#         file_type string/string[]. "*.py"
#         extension bool. True:[name.py] False:[name]
#         exclude string /string[]. "__init__.py" | "__init__" | ["btnReport48", "btnHelp48"]
#
# @RETURN strint[].
def getFileList(path, file_type='*', extension=False, exclude="*", path_add = False):
    getFile = []

    if(os.path.exists(path)):
        os.chdir(path)
        for file_name in glob.glob(file_type):
            if file_name.split('.')[0] in exclude:
                continue
            if path_add:
                file_name = os.path.normpath(('/').join([path,file_name]))
            if extension:
                getFile.append(file_name)
            else:
                getFile.append((file_name.split('.')[0]))
    return getFile

##
# @BRIEF  GET ALL subfolders in the path
def getDeepFolderList(path):
    getFile = map(lambda x: os.path.basename(x[0]), os.walk(path))
    getFile.pop(0)
    return getFile

