import maya.cmds as cmds
import maya.utils as utils
import os.path
import glob
import re
import sys, os
import subprocess
import threading

def getUdims(texture):
    return glob.glob(re.sub(r'(<udim[:]?[0-9]*>)','????',texture))
    
def isImage(file):
    ext = os.path.splitext(file)[1]
    if (ext == '.jpeg' or ext == '.jpg' or ext == '.tiff' or ext == '.tif' or
        ext == '.png' or ext == '.exr' or ext == '.hdr' or ext == '.bmp' or
        ext == '.tga'):
        return True
    return False
    
def updateProgressMessage(window, created, toCreate, errors):
    ctrlPath = '|'.join([window, 'groupBox_2', 'label_8']);
    cmds.text(ctrlPath, edit=True, label="Created: {0} of {1}".format(created,toCreate));
    if errors is not 0:
        ctrlPath = '|'.join([window, 'groupBox_2', 'label_9']);
        cmds.text(ctrlPath, edit=True, label="Warning: {0} errors".format(errors));
    else:
        ctrlPath = '|'.join([window, 'groupBox_2', 'label_9']);
        cmds.text(ctrlPath, edit=True, label="");

class MakeTxThread (threading.Thread):
    def __init__(self,manager):
        self.txManager = manager
        threading.Thread.__init__(self)
        self.filesCreated = 0
        self.createdErrors = 0
        
    def run (self):
        self.filesCreated = 0
        self.createdErrors = 0
        self.createTx()
        self.txManager.thread = []
    
    # create a .tx file with the provided options. It will wait until it is finished
    def makeTx(self, texture):
        cmd = 'maketx';
        cmd += ' -o "' + os.path.splitext(texture)[0] + '.tx"'
        
        # Custom options
        ctrlPath = '|'.join([self.txManager.window, 'groupBox_2', 'lineEdit']);
        cmd += ' '+utils.executeInMainThreadWithResult(cmds.textField, ctrlPath, query=True, text=True);
        
        cmd += ' "'+texture+'"'
        #print cmd
        if os.name == 'nt':
            proc = subprocess.Popen(cmd, creationflags=subprocess.SW_HIDE, shell=True)
        else:
            proc = subprocess.Popen(cmd, shell=True)
        return proc.wait()
        
    def createTx(self):
        if not self.txManager.selectedFiles:
            return
            
        ctrlPath = '|'.join([self.txManager.window, 'groupBox_2', 'pushButton_7']);
        utils.executeDeferred(cmds.button,ctrlPath, edit=True, enable=True);
            
        for texture in self.txManager.selectedFiles:
            if not texture:
                continue;
            # stopCreation has been called   
            if not self.txManager.process:
                break;
            # Process all the files that match the <udim> tag    
            if 'udim' in os.path.basename(texture):
                udims = getUdims(texture)
                for udim in udims:
                    # stopCreation has been called   
                    if not self.txManager.process:
                        break;
                    if self.makeTx(udim) is 0:
                        self.filesCreated += 1
                    else:
                        self.createdErrors += 1
                        
                        
                    utils.executeDeferred(updateProgressMessage, self.txManager.window, self.filesCreated, self.txManager.filesToCreate, self.createdErrors) 
                        
            else:
                if self.makeTx(texture) is 0:
                    self.filesCreated += 1
                else:
                    self.createdErrors += 1
                    
            utils.executeDeferred(updateProgressMessage, self.txManager.window, self.filesCreated, self.txManager.filesToCreate, self.createdErrors)
        
        ctrlPath = '|'.join([self.txManager.window, 'groupBox_2', 'pushButton_7']);
        utils.executeDeferred(cmds.button, ctrlPath, edit=True, enable=False);
        self.txManager.process = True
        utils.executeDeferred(self.txManager.updateList)


class MtoATxManager(object):
    use=None;
    def __init__(self):
        MtoATxManager.use = self;
        path = os.path.dirname(os.path.abspath(__file__))
        self.uiFile = os.path.join(path,'txManager.ui');
        self.window = '';
        self.textures = []   # pairs [texture_name, status] where status is:
                             #   -1 (does not exists),
                             #    0 (.tx file),
                             #    1 (has a processed .tx file),
                             #    2 (does not have a processed .tx file)
        self.listElements = []
        self.selectedFiles = []
        self.filesToCreate = 0
        
        self.filesCreated = 0
        self.createdErrors = 0
        self.deletedFiles = 0
        
        self.thread = []
        self.process = True
        
    def create(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window);
        self.window = cmds.loadUI(uiFile=self.uiFile, verbose=False)
        
        cmds.showWindow(self.window);
        try:
            initPos = cmds.windowPref( self.window, query=True, topLeftCorner=True )
            if initPos[0] < 0:
                initPos[0] = 0
            if initPos[1] < 0:
                initPos[1] = 0
            cmds.windowPref( self.window, edit=True, topLeftCorner=initPos )
        except :
            pass
        
        ctrlPath = '|'.join([self.window, 'radioButton']);
        cmds.radioButton(ctrlPath, edit=True, select=True);
        
        ctrlPath = '|'.join([self.window, 'groupBox_4']);
        cmds.control(ctrlPath, edit=True, enable=False);
        
        ctrlPath = '|'.join([self.window, 'groupBox_2', 'pushButton_7']);
        cmds.button(ctrlPath, edit=True, enable=False);
        
        ctrlPath = '|'.join([self.window, 'groupBox_2', 'lineEdit']);
        cmds.textField(ctrlPath, edit=True, text="-u --oiio");
        
    # Update the Scroll List with the texture files in the scene and check its status
    def updateList(self):
        self.textures = []
        list = cmds.ls(type='file')
        for node in list:
            texture = cmds.getAttr(node+'.fileTextureName')
            if texture:
                self.textures.append(texture)
                    
        list = cmds.ls(type='aiImage')
        for node in list:
            texture = cmds.getAttr(node+'.filename')
            if texture:
                self.textures.append(texture)
            
        totalFiles = 0;
        missingFiles = 0;    
        for i in range(len(self.textures)):
            ext = os.path.splitext(self.textures[i])[1]
            
            # A .tx texture
            if(ext == '.tx'):
                # File, does not have <udim> tag and does not exists
                if not 'udim' in os.path.basename(self.textures[i]) and not os.path.exists(self.textures[i]):
                    self.textures[i] = ([self.textures[i],-1])
                    missingFiles+=1
                    
                # File has <udim> tag
                elif 'udim' in os.path.basename(self.textures[i]):
                    udims = getUdims(self.textures[i])
                    # If any file match to the <udim> tag, the file exists
                    if(len(udims) > 0):
                        self.textures[i] = ([self.textures[i],0])
                        totalFiles+=len(udims)
                        
                    # If no files match the <udim> tag, the file does not exists.
                    else:
                        self.textures[i] = ([self.textures[i],-1])
                        missingFiles+=1
                        
                # File, does not have <udim> tag and exists
                else:
                    self.textures[i] = ([self.textures[i],0])
                    totalFiles+=1
                    
            # Not a .tx texture
            else:
                # File exists and has a processed .tx file
                if(os.path.exists(os.path.splitext(self.textures[i])[0]+'.tx') and os.path.exists(self.textures[i]) ):
                    self.textures[i] = ([self.textures[i],1])
                    totalFiles+=1
                else:
                    # File has <udim> tag
                    if('udim' in os.path.basename(self.textures[i])):
                        udims = getUdims(self.textures[i])
                        allTxExists = True
                        for udim in udims:
                            if not os.path.exists(os.path.splitext(udim)[0]+'.tx'):
                                allTxExists = False
                                break
                        # If no files match the <udim> tag, the file does not exists.
                        if len(udims) == 0:
                            self.textures[i] = ([self.textures[i],-1])
                            missingFiles+=1
                        # All the matching files has a processed .tx file
                        elif allTxExists:
                            self.textures[i] = ([self.textures[i],1])
                            totalFiles+=len(udims)
                        # Any matching file does not have a processed .tx file
                        else:
                            self.textures[i] = ([self.textures[i],2])
                            totalFiles+=len(udims)
                    # File without <udim> tag and without processed .tx file
                    else:
                        # The file does not exists
                        if not os.path.exists(self.textures[i]):
                            self.textures[i] = ([self.textures[i],-1])
                            missingFiles+=1
                        # Existing un processed file
                        else:
                            self.textures[i] = ([self.textures[i],2])
                            totalFiles+=1

        ctrlPath = '|'.join([self.window, 'groupBox', 'listWidget']);

        listSize = cmds.textScrollList(ctrlPath, query=True, numberOfItems=True);
        for x in range(listSize,0,-1):
            cmds.textScrollList(ctrlPath, edit=True, removeIndexedItem=x);
        
        for texture in self.textures:
            if(texture[1] == 0):
                cmds.textScrollList(ctrlPath, edit=True, append=['[tx] '+texture[0]]);
            elif(texture[1] == 1):
                cmds.textScrollList(ctrlPath, edit=True, append=['(tx) '+texture[0]]);
            elif(texture[1] == 2):
                cmds.textScrollList(ctrlPath, edit=True, append=['       '+texture[0]]);
            elif(texture[1] == -1):
                cmds.textScrollList(ctrlPath, edit=True, append=['~~  '+texture[0]]);

        self.listElements = cmds.textScrollList(ctrlPath, query=True, ai=True);
                
        ctrlPath = '|'.join([self.window, 'groupBox', 'label_5']);
        cmds.text(ctrlPath, edit=True, label="Total Files: {0}".format(totalFiles));
        
        ctrlPath = '|'.join([self.window, 'groupBox', 'label_6']);
        if(missingFiles > 0):
            cmds.text(ctrlPath, edit=True, label="<font color=#FE6565>Missing Files: {0}</font>".format(missingFiles));
        else:
            cmds.text(ctrlPath, edit=True, label="");
    
    def stopCreation(self, *args):
        self.process = False
    
    # Updates the Scroll List and also the process progress message
    # Only to be used when a refresh button is pressed, as it will remove any progress information shown
    def refreshList(self, *args):
        self.updateList()   
        
        #Only update this text when button is pressed, not when called from createTx or deleteTx    
        updateProgressMessage(self.window, 0, 0, 0)
        ctrlPath = '|'.join([self.window, 'groupBox_3', 'label_10']);
        cmds.text(ctrlPath, edit=True, label="");
            
    def selectAll(self, *args):
        self.updateList()
        if self.listElements:
            all_idx = [i+1 for i, texture in enumerate(self.listElements) if texture.startswith('       ') or texture.startswith('(tx) ')]
            ctrlPath = '|'.join([self.window, 'groupBox', 'listWidget']);
            cmds.textScrollList(ctrlPath, edit=True, deselectAll=True);
            cmds.textScrollList(ctrlPath, edit=True, selectIndexedItem=all_idx);
            
            self.selectedFilesFromList()
        
    # Select all textures that does not have a processed .tx file
    def selectNonTx(self, *args):
        self.updateList()
        if self.listElements:
            all_idx = [i+1 for i, texture in enumerate(self.listElements) if texture.startswith('       ')]
            ctrlPath = '|'.join([self.window, 'groupBox', 'listWidget']);
            cmds.textScrollList(ctrlPath, edit=True, deselectAll=True);
            cmds.textScrollList(ctrlPath, edit=True, selectIndexedItem=all_idx);
            
            self.selectedFilesFromList()
    
    def selectChange(self, *args):
        self.selectedFilesFromList()
        
    def selectLine(self, *args):
        ctrlPath = '|'.join([self.window, 'groupBox', 'listWidget']);
        
        listElements = cmds.textScrollList(ctrlPath, query=True, ai=True);
        selectedList = cmds.textScrollList(ctrlPath, query=True, si=True);
        selectedIndexList = cmds.textScrollList(ctrlPath, query=True, sii=True);

        selected = selectedList[0];
        firstIndex = listElements.index(selected)
        number = selectedIndexList[0] - firstIndex
        
        if selected.startswith('       '):
            selected = selected.replace('       ','',1)
        elif selected.startswith('(tx) '):
            selected = selected.replace('(tx) ','',1)
        elif selected.startswith('[tx] '):
            selected = selected.replace('[tx] ','',1)
        elif selected.startswith('~~  '):
            selected = selected.replace('~~  ','',1)
        
        list = cmds.ls(type='file')
        for node in list:
            texture = cmds.getAttr(node+'.fileTextureName')
            if texture == selected:
                number -= 1
                if number == 0:
                    cmds.select(node)
                    return
                    
        list = cmds.ls(type='aiImage')
        for node in list:
            texture = cmds.getAttr(node+'.filename')
            if texture == selected:
                number -= 1
                if number == 0:
                    cmds.select(node)
                    return
    
    # Set the variables self.selectedFiles, self.filesToCreate, self.filesCreated and self.createdErrors
    #  from the Scroll List selection
    def selectedFilesFromList(self):
        ctrlPath = '|'.join([self.window, 'groupBox', 'listWidget']);
        self.selectedFiles = cmds.textScrollList(ctrlPath, query=True, si=True);
        
        self.filesToCreate = 0
        self.filesCreated = 0
        self.createdErrors = 0
        
        if not self.selectedFiles:
            updateProgressMessage(self.window, 0, 0, 0)    
            return
        
        list = cmds.textScrollList(ctrlPath, query=True, ai=True);
        
        for i in range(len(self.selectedFiles)):
            texture = self.selectedFiles[i]
            if texture.startswith('       '):
                self.selectedFiles[i] = texture.replace('       ','',1)
            elif texture.startswith('(tx) '):
                self.selectedFiles[i] = texture.replace('(tx) ','',1)
            else:
                self.selectedFiles[i] = ""
                continue;
            texture = self.selectedFiles[i]
            if 'udim' in os.path.basename(texture):
                udims = getUdims(texture)
                self.filesToCreate += len(udims)
            else:
                self.filesToCreate += 1
        
        updateProgressMessage(self.window, self.filesCreated, self.filesToCreate, 0)
        ctrlPath = '|'.join([self.window, 'groupBox_3', 'label_10']);
        cmds.text(ctrlPath, edit=True, label="");
        
    # Set the variables self.selectedFiles, self.filesToCreate, self.filesCreated and self.createdErrors
    #  from the Folder selected
    def selectedFilesFromFolder(self, *args):
        ctrlPath = '|'.join([self.window, 'groupBox_4', 'lineEdit_2']);
        folder = cmds.textField(ctrlPath, query=True, text=True);
        
        self.selectedFiles = []
        
        self.filesToCreate = 0
        self.filesCreated = 0
        self.createdErrors = 0
        
        ctrlPath = '|'.join([self.window, 'groupBox_4', 'checkBox']);
        recursive = cmds.checkBox(ctrlPath, query=True, value=True);
        
        if os.path.isdir(folder):
            if recursive:
                for root, dirs, files in os.walk(folder):
                    for texture in files:
                        if (isImage(texture)):
                            self.selectedFiles.append(os.path.join(root, texture))
                            self.filesToCreate += 1
            else:
                files = os.listdir(folder)
                for texture in files:
                    if (isImage(texture)):
                        self.selectedFiles.append(os.path.join(folder, texture))
                        self.filesToCreate += 1
                
        updateProgressMessage(self.window, self.filesCreated, self.filesToCreate, 0)
        ctrlPath = '|'.join([self.window, 'groupBox_3', 'label_10']);
        cmds.text(ctrlPath, edit=True, label="");


    # Open a dialog to select a folder and update the information about it
    def selectFolder(self, *args):
        ctrlPath = '|'.join([self.window, 'groupBox_4', 'lineEdit_2']);
        folder = cmds.textField(ctrlPath, query=True, text=True);
        if not os.path.isdir(folder):
            folder = cmds.workspace(query=True, directory=True)     
        ret = cmds.fileDialog2(cap='Select Folder',okc='Select',fm=2, startingDirectory=folder)
        if ret is not None and len(ret):
            ctrlPath = '|'.join([self.window, 'groupBox_4', 'lineEdit_2']);
            cmds.textField(ctrlPath, edit=True, text=ret[0]);
            self.selectedFilesFromFolder()
    
    # Delete the processed .tx files selected
    def deleteTx(self, *args):
        ctrlPath = '|'.join([self.window, 'radioButton']);
        selection = cmds.radioButton(ctrlPath, query=True, select=True);
        
        self.deletedFiles = 0
        ctrlPath = '|'.join([self.window, 'groupBox_3', 'label_10']);
        
        if selection:
            self.selectedFilesFromList()
        else:
            self.selectedFilesFromFolder()

        if not self.selectedFiles:
            cmds.text(ctrlPath, edit=True, label="Deleted: {0}".format(self.deletedFiles));
            return
            
        for texture in self.selectedFiles:
            if not texture:
                continue;
            if 'udim' in os.path.basename(texture):
                udims = getUdims(texture)
                for udim in udims:
                    txFile = os.path.splitext(udim)[0]+".tx"
                    if os.path.isfile(txFile):
                        os.remove(txFile)
                        self.deletedFiles += 1
            else:
                txFile = os.path.splitext(texture)[0]+".tx"
                if os.path.isfile(txFile):
                    os.remove(txFile)
                    self.deletedFiles += 1

            cmds.text(ctrlPath, edit=True, label="Deleted: {0}".format(self.deletedFiles));
        self.updateList()
   
    # Create the processed .tx files in another thread to avoid locking the UI
    def createTx(self, *args):
        if not self.thread:
            self.thread = MakeTxThread(self)
            self.thread.start()

