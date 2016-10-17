#*************************************************************
# CONTENT       create, search etc in/for file and folders
#
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
import glob
import webbrowser

#************************
# FOLDER
def createFolder(path):
    if len(path.split(".")) > 1:
        path = os.path.dirname(path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            print("WARNING : Can not create folder : %s"% path)

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
# @PARAM  path str.
#         fileType str/strList. "*.py"
#         extension bool. True:[name.py] False:[name]
#         exclude str/strList. "__init__.py" | "__init__" | ["btnReport48", "btnHelp48"]
#
# @RETURN stringList.
def getFileList(path, fileType='*', extension=False, exclude="*"):
    getFile = []

    if(os.path.exists(path)):
        os.chdir(path)
        for fileName in glob.glob(fileType):
            if fileName.split('.')[0] in exclude:
                continue
            if extension:
                getFile.append(fileName)
            else:
                getFile.append((fileName.split('.')[0]))
    return getFile

##
# @BRIEF  GET ALL subfolders in the path
def getDeepFolderList(path):
    getFile = map(lambda x: os.path.basename(x[0]), os.walk(path))
    getFile.pop(0)
    return getFile
