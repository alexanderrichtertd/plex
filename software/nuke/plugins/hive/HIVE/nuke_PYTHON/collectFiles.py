#===============================================================================
# NUKE COLLECT FILES 1.2                                                                                  
# By Mariano Antico                                                                                       
# Barraca Post                                                                                            
# www.barraca.com.ar                                                                                      
# www.marianoantico.blogspot.com                                                                          
# Last Updated: September 21, 2011.                                                                           
# All Rights Reserved .
#  
# Description:
# Collect files of the script
#
# Tutorials:
# www.marianoantico.blogspot.com
# www.vimeo.com/29200474
#
# Supported Video Files:
# 'mov', 'avi', 'mpeg', 'mp4', 'R3D'
#
# Installation Notes:
# 
# 1. Copy "collectFiles.py" to nuke plugins directory (Example: "C:\Program Files\Nuke6.1v1\plugins")
# 2. Open "Init.py" located on "C:\Program Files\Nuke6.1v1\plugins"
# 3. And paste this:
# import collectFiles
# 
# 4. Save it and restart nuke
# 5. Open the Script Command window and paste this:
# collectFiles.collectFiles()
# 
# 6. Check the python button and press ok
# 
# 
# Create Menu Node:
# 
# 1. Open "Menu.py" located on "C:\Program Files\Nuke6.1v1\plugins"
# 2. And paste this at the end:
# 
# #Collect Files Menu Node
# collectMenu = nuke.menu("Nodes").addMenu("Collect_Files")
# collectMenu.addCommand('Collect Files', 'collectFiles.collectFiles()')
# collectMenu.addCommand('Help', 'collectFiles.myBlog()')
# 
# Run:
# collectFiles()                                                                                   
#===============================================================================


import nuke
import os
import sys
import shutil
import re
import threading
import time
import webbrowser

# Child Functions
def myBlog():
    url = 'http://www.marianoantico.blogspot.com/'
    webbrowser.open_new(url)

def collectPanel():
    colPanel = nuke.Panel("Collect Files 1.2 by Mariano Antico")
    colPanel.addFilenameSearch("Output Path:", "")
    colPanel.addButton("Cancel")
    colPanel.addButton("OK")

    retVar = colPanel.show()
    pathVar = colPanel.value("Output Path:")

    return (retVar, pathVar)

# Check files
def checkForKnob(node, checkKnob ):
    try:
        node[checkKnob]
    except NameError:
        return False
    else:
        return True

# Parent Function
def collectFiles():
    panelResult = collectPanel()

    #copy script to target directory
    script2Copy = nuke.root()['name'].value()
    scriptName = os.path.basename(nuke.Root().name())

    fileNames = []
    paddings = ['%01d', '%02d', '%03d', '%04d', '%05d', '%06d', '%07d', '%08d', '%d', '%1d']
    videoExtension = ['mov', 'avi', 'mpeg', 'mpg', 'mp4', 'R3D']
    cancelCollect = 0

    # hit OK
    if panelResult[0] == 1 and panelResult[1] != '':
        targetPath = panelResult[1]

        # Check to make sure a file path is not passed through
        if os.path.isfile(targetPath):
            targetPath = os.path.dirname(targetPath)

        # Make sure target path ends with a slash (for consistency)
        if not targetPath.endswith('/'):
            targetPath += '/'

        # Check if local directory already exists. Ask to create it if it doesn't
        if not os.path.exists(targetPath):
            if nuke.ask("Directory does not exist. Create now?"):
                try:
                    os.makedirs(targetPath)
                except:
                    raise Exception, "Something's not working!"
                    return False
            else:
                nuke.message("Cannot proceed without valid target directory.")
                return False
       
        # Get script name
        scriptName = os.path.basename(nuke.Root().name())
    
        footagePath = targetPath + 'footage/'
        if (os.path.exists(footagePath)):
            pass
        else:
            os.mkdir(footagePath)

        task = nuke.ProgressTask("Collect Files 1.2")
        count = 0

        for fileNode in nuke.allNodes():
            if task.isCancelled():
                cancelCollect = 1
                break
            count += 1
            task.setMessage("Collecting file:   " + str(fileNode))
            task.setProgress(count*100/len(nuke.allNodes()))


            if checkForKnob(fileNode, 'file'):
                if not checkForKnob(fileNode, 'Render'):
                    fileNodePath = fileNode['file'].value()
                    if (fileNodePath == ''):
                        continue
                    else:
                        readFilename = fileNodePath.split("/")[-1]
                        
                        if checkForKnob(fileNode, 'first'):

                            if (fileNodePath.endswith(tuple(videoExtension))):
                                newFilenamePath = footagePath + fileNodePath.split("/")[-1]
                                if (os.path.exists(newFilenamePath)):
                                    print (newFilenamePath + '     DUPLICATED')
                                else:
                                    if (os.path.exists(fileNodePath)):
                                        shutil.copy2(fileNodePath, newFilenamePath)
                                        print (newFilenamePath + '     COPIED')                                       
                                    else:
                                        print (newFilenamePath + '     MISSING')        

                            else:
                                # frame range
                                frameFirst = fileNode['first'].value()
                                frameLast = fileNode['last'].value()
                                framesDur = frameLast - frameFirst
                                
                                if (frameFirst == frameLast):
                                    newFilenamePath = footagePath + readFilename
                                    if (os.path.exists(newFilenamePath)):
                                        print (newFilenamePath + '     DUPLICATED')
                                    else:
                                        if (os.path.exists(fileNodePath)):
                                            shutil.copy2(fileNodePath, newFilenamePath)
                                            print (newFilenamePath + '     COPIED')                             
                                        else:
                                            print (newFilenamePath + '     MISSING')

                                else:
                                    dirSeq = fileNodePath.split("/")[-2] + '/'
                                    newFilenamePath = footagePath + dirSeq
                                    if (os.path.exists(newFilenamePath)):
                                        print (newFilenamePath + '     DUPLICATED')
                                    else:
                                        os.mkdir(newFilenamePath)
    
                                    # rename sequence
                                    for frame in range(framesDur + 1):
                                        for pad in paddings:
            
                                            # Copy sequence file
                                            if (re.search(pad, fileNodePath.split("/")[-1])):
                                                originalSeq = fileNodePath.replace(pad, str(pad % frameFirst))
                                                frameSeq = fileNodePath.split("/")[-1].replace(pad, str(pad % frameFirst))
                                                fileNames.append (frameSeq)
                                                newSeq = newFilenamePath + frameSeq
                                                frameFirst += 1
                                                task.setMessage("Collecting file:   " + frameSeq)
        
                                                if (os.path.exists(newSeq)):
                                                    print (newSeq + '     DUPLICATED')
                                                else:
                                                    if (os.path.exists(originalSeq)):
                                                        shutil.copy(originalSeq, newSeq)
                                                        print (newSeq + '     COPIED')                      
                                                    else:
                                                        print (newSeq + '     MISSING')

                                    print ('\n')
                            
                        # Copy single file
                        else:
                            newFilenamePath = footagePath + fileNodePath.split("/")[-1]
                            if (os.path.exists(newFilenamePath)):
                                print (newFilenamePath + '     DUPLICATED')
                            else:
                                if (os.path.exists(fileNodePath)):
                                    shutil.copy2(fileNodePath, newFilenamePath)
                                    print (newFilenamePath + '     COPIED')
                                else:
                                    print (newFilenamePath + '     MISSING')

            else:
                pass

        
        if (cancelCollect == 0):
            # Save script to archive path
            newScriptPath = targetPath + scriptName
            nuke.scriptSaveAs(newScriptPath)
    
            #link files to new path
            for fileNode in nuke.allNodes():
                if checkForKnob(fileNode, 'file'):
                    if not checkForKnob(fileNode, 'Render'):
                        fileNodePath = fileNode['file'].value()
                        if (fileNodePath == ''):
                            continue
                        else:
                            
                            if checkForKnob(fileNode, 'first'):                            
                                if (fileNodePath.endswith(tuple(videoExtension))):
                                    fileNodePath = fileNode['file'].value()
                                    readFilename = fileNodePath.split("/")[-1]
                                    reloadPath = '[file dirname [value root.name]]/footage/' + readFilename
                                    fileNode['file'].setValue(reloadPath)
                                else:
                                    # frame range
                                    frameFirst = fileNode['first'].value()
                                    frameLast = fileNode['last'].value()
        
                                    if (frameFirst == frameLast):
                                        fileNodePath = fileNode['file'].value()
                                        readFilename = fileNodePath.split("/")[-1]
                                        reloadPath = '[file dirname [value root.name]]/footage/' + readFilename
                                        fileNode['file'].setValue(reloadPath)
                                    else:
                                        fileNodePath = fileNode['file'].value()
                                        dirSeq = fileNodePath.split("/")[-2] + '/'
                                        readFilename = fileNodePath.split("/")[-1]
                                        reloadPath = '[file dirname [value root.name]]/footage/' + dirSeq + readFilename
                                        fileNode['file'].setValue(reloadPath)
                            
                            else:
                                fileNodePath = fileNode['file'].value()
                                readFilename = fileNodePath.split("/")[-1]
                                reloadPath = '[file dirname [value root.name]]/footage/' + readFilename
                                fileNode['file'].setValue(reloadPath)
                    else:
                        pass
                else:
                    pass
    
            nuke.scriptSave()
            del task        
            print ('COLLECT DONE!!')
            nuke.message('COLLECT DONE!!')

        else:
            del task
            print ('COLLECT CANCELLED - Toma Rojo Puto')
            nuke.message('COLLECT CANCELLED')

    # If they just hit OK on the default ellipsis...
    elif panelResult[0] == 1 and panelResult[1] == '':
        nuke.message("Select a path")
        return False

    # hit CANCEL
    else:
        print ('COLLECT CANCELLED')
