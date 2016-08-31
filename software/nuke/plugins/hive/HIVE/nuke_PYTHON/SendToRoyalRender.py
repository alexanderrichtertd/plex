# Royal Render Plugin script for Fusion 5+
# Author: Royal Render, Holger Schoenberger, Binary Alchemy
# Last change: v 6.02.01
# Copyright (c) 2009-2012 Holger Schoenberger - Binary Alchemy
# rrInstall_Copy: \plugins\
# rrInstall_Change_File: \plugins\menu.py, before "# Help menu", "m =  menubar.addMenu(\"RRender\");\nm.addCommand(\"Submit Comp\", \"nuke.load('rrSubmit_Nuke_5'), rrSubmit_Nuke_5()\")\n\n"

import nuke
import os
import sys
import platform
import random
import string

from xml.etree.ElementTree import ElementTree, Element, SubElement


#####################################################################################
# This function has to be changed if an app should show info and error dialog box   #
#####################################################################################

def writeInfo(msg):
    print(msg)
#    nuke.message(msg)

def writeError(msg):
#    print(msg)
    nuke.message(msg)


##############################################
# JOB CLASS                                  #
##############################################


class rrJob(object):
    """Stores scene information """
    version = ""
    software = ""
    renderer = ""
    requiredPlugins = ""
    sceneName = ""
    sceneDatabaseDir = ""
    seqStart = 0
    seqEnd = 100
    seqStep = 1
    seqFileOffset = 0
    seqFrameSet = ""
    imageWidth = 99
    imageHeight = 99
    imageDir = ""
    imageFileName = ""
    imageFramePadding = 4
    imageExtension = ""
    imagePreNumberLetter = ""
    imageSingleOutput = False
    sceneOS = ""
    camera = ""
    layer = ""
    channel = ""
    maxChannels = 0
    channelFileName = []
    channelExtension = []
    isActive = False
    sendAppBit = ""
    preID = ""
    waitForPreID  = ""
    CustomA  = "Test Custom A"
    CustomB  = ""
    CustomC  = ""
    LocalTexturesFile  = ""
        
    def __init__(self):
        pass

    # from infix.se (Filip Solomonsson)
    def indent(self, elem, level=0):
        i = "\n" + level * ' '
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + " "
            for e in elem:
                self.indent(e, level + 1)
                if not e.tail or not e.tail.strip():
                    e.tail = i + " "
            if not e.tail or not e.tail.strip():
                e.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
        return True

    def subE(self, r, e, t):
        sub = SubElement(r, e)
        sub.text = str(t)
        return sub

    def writeToXMLstart(self, submitOptions ):
        rootElement = Element("RR_Job_File")
        rootElement.attrib["syntax_version"] = "6.0"
        self.subE(rootElement, "DeleteXML", "1")
        self.subE(rootElement, "SubmitterParameter", submitOptions)
        # YOU CAN ADD OTHER NOT SCENE-INFORMATION PARAMETERS USING THIS FORMAT:
        # self.subE(jobElement,"SubmitterParameter","PARAMETERNAME=" + PARAMETERVALUE_AS_STRING)
        return rootElement

    def writeToXMLJob(self, rootElement):

        jobElement = self.subE(rootElement, "Job", "")
        self.subE(jobElement, "Software", self.software)
        self.subE(jobElement, "Renderer", self.renderer)
        self.subE(jobElement, "RequiredPlugins", self.requiredPlugins)
        self.subE(jobElement, "Version", self.version)
        self.subE(jobElement, "SceneName", self.sceneName)
        self.subE(jobElement, "SceneDatabaseDir", self.sceneDatabaseDir)
        self.subE(jobElement, "IsActive", self.isActive)
        self.subE(jobElement, "SeqStart", self.seqStart)
        self.subE(jobElement, "SeqEnd", self.seqEnd)
        self.subE(jobElement, "SeqStep", self.seqStep)
        self.subE(jobElement, "SeqFileOffset", self.seqFileOffset)
        self.subE(jobElement, "SeqFrameSet", self.seqFrameSet)
        self.subE(jobElement, "ImageWidth", int(self.imageWidth))
        self.subE(jobElement, "ImageHeight", int(self.imageHeight))
        self.subE(jobElement, "ImageDir", self.imageDir)
        self.subE(jobElement, "ImageFilename", self.imageFileName)
        self.subE(jobElement, "ImageFramePadding", self.imageFramePadding)
        self.subE(jobElement, "ImageExtension", self.imageExtension)
        self.subE(jobElement, "ImageSingleOutput", self.imageSingleOutput)
        self.subE(jobElement, "ImagePreNumberLetter", self.imagePreNumberLetter)
        self.subE(jobElement, "SceneOS", self.sceneOS)
        self.subE(jobElement, "Camera", self.camera)
        self.subE(jobElement, "Layer", self.layer)
        self.subE(jobElement, "Channel", self.channel)
        self.subE(jobElement, "SendAppBit", self.sendAppBit)
        self.subE(jobElement, "PreID", self.preID)
        self.subE(jobElement, "WaitForPreID", self.waitForPreID)
        self.subE(jobElement, "CustomA", self.CustomA)
        self.subE(jobElement, "CustomB", self.CustomB)
        self.subE(jobElement, "CustomC", self.CustomC)
        self.subE(jobElement, "LocalTexturesFile", self.LocalTexturesFile)
        for c in range(0,self.maxChannels):
           self.subE(jobElement,"ChannelFilename",self.channelFileName[c])
           self.subE(jobElement,"ChannelExtension",self.channelExtension[c])
        return True



    def writeToXMLEnd(self, f,rootElement):
        xml = ElementTree(rootElement)
        self.indent(xml.getroot())

        if not f == None:
            xml.write(f)
            f.close()
        else:
            print("No valid file has been passed to the function")
            try:
                f.close()
            except:
                pass
            return False
        return True



##############################################
# Global Functions                           #
##############################################

def getRR_Root():
    if os.environ.has_key('RR_ROOT'):
        return os.environ['RR_ROOT']
    HCPath="%"
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        HCPath="%RRLocationWin%"
    elif (sys.platform.lower() == "darwin"):
        HCPath="%RRLocationMac%"
    else:
        HCPath="%RRLocationLx%"
    if HCPath[0]!="%":
        return HCPath
    writeError("This plugin was not installed via rrWorkstationInstaller!")


def getNewTempFileName():
    random.seed()
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        if os.environ.has_key('TEMP'):
            nam=os.environ['TEMP']
        else:
            nam=os.environ['TMP']
        nam+="\\"
    else:
        nam="/tmp/"
    nam+="rrSubmitNuke_"
    nam+=str(random.randrange(1000,10000,1))
    nam+=".xml"
    return nam

def getRRSubmitterPath():
    ''' returns the rrSubmitter filename '''
    rrRoot = getRR_Root()
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        rrSubmitter = rrRoot+"\\win__rrSubmitter.bat"
    elif (sys.platform.lower() == "darwin"):
        rrSubmitter = rrRoot+"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter"
    else:
        rrSubmitter = rrRoot+"/lx__rrSubmitter.sh"
    return rrSubmitter


def getOSString():
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        return "win"
    elif (sys.platform.lower() == "darwin"):
        return "osx"
    else:
        return "lx"

    
def submitJobsToRR(jobList,submitOptions):
    tmpFileName = getNewTempFileName()
    tmpFile = open(tmpFileName, "w")
    xmlObj= jobList[0].writeToXMLstart(submitOptions)
    for submitjob in jobList:
        submitjob.writeToXMLJob(xmlObj)
    ret = jobList[0].writeToXMLEnd(tmpFile,xmlObj)
    if ret:
        writeInfo("Job written to " + tmpFile.name)
    else:
        writeError("Error - There was a problem writing the job file to " + tmpFile.name)
    os.system(getRRSubmitterPath()+"  \""+tmpFileName+"\"")



###########################################
# Read Nuke file                          #
###########################################

def rrSubmit_fillGlobalSceneInfo(newJob):
    newJob.version = nuke.NUKE_VERSION_STRING
    newJob.software = "Nuke"
    newJob.sceneOS = getOSString()
    newJob.sceneName = nuke.root().name()
    newJob.seqStart = nuke.root().firstFrame()
    newJob.seqEnd = nuke.root().lastFrame()
    newJob.imageFileName = ""


def rrSubmit_CreateAllJob(jobList,noLocalSceneCopy):
    newJob= rrJob()
    rrSubmit_fillGlobalSceneInfo(newJob)
    n = nuke.allNodes('Write')
    mainNode = True
    for writeNode in n:
        if (writeNode['disable'].value()):
            continue
        pathScripted=writeNode['file'].value()
        if ( (pathScripted.lower().find("root.name")>=0) or (pathScripted.lower().find("root().name")>=0) ):
            noLocalSceneCopy[0]=True
        if (mainNode):
            if (writeNode['use_limit'].value()):
                newJob.seqStart = writeNode['first'].value()
                newJob.seqEnd = writeNode['last'].value()
            newJob.imageFileName= nuke.filename(writeNode)
            mainNode = False
        else:
            newJob.maxChannels= newJob.maxChannels + 1
            newJob.channelFileName.append(string.replace(string.replace(nuke.filename(writeNode),"%v","l"),"%V","left"))
            newJob.channelExtension.append("")
    if ( (newJob.imageFileName.find("%V")>=0) or (newJob.imageFileName.find("%v")>=0)):
        newJob.maxChannels= newJob.maxChannels + 1
        newJob.channelFileName.append(string.replace(string.replace(newJob.imageFileName,"%v","l"),"%V","left"))
        newJob.channelExtension.append("")
        newJob.imageFileName = string.replace(string.replace(newJob.imageFileName,"%v","r"),"%V","right")
    newJob.layer= "** All **"
    newJob.isActive = True
    jobList.append(newJob)


def rrSubmit_CreateSingleJobs(jobList):
    n = nuke.allNodes('Write')
    for i in n:
        if (i['disable'].value()):
            continue
        newJob= rrJob()
        rrSubmit_fillGlobalSceneInfo(newJob)
        if (i['use_limit'].value()):
           newJob.seqStart = i['first'].value()
           newJob.seqEnd = i['last'].value()
        newJob.imageFileName= nuke.filename(i)
        if ( (newJob.imageFileName.find("%V")>=0) or (newJob.imageFileName.find("%v")>=0)):
            newJob.maxChannels= newJob.maxChannels + 1
            newJob.channelFileName.append(string.replace(string.replace(newJob.imageFileName,"%v","l"),"%V","left"))
            newJob.channelExtension.append("")
            newJob.imageFileName = string.replace(string.replace(newJob.imageFileName,"%v","r"),"%V","right")
        newJob.layer= i['name'].value()
        newJob.isActive = False
        jobList.append(newJob)


def rrSubmit_addPluginLicenses(jobList):
    n = nuke.allNodes()
    plugins=""
    for i in n:
        if (i.Class().find(".sapphire.")>=0):
            plugins="Sapphire"
            break;
    for i in n:
        if (i.Class().find(".revisionfx.rsmb")>=0):
            plugins=plugins+";Reelsmart"
            break;
    for i in n:
        if (i.Class().find(".myPlugin.")>=0):
            plugins=plugins+";MyPlugin"
            break;
        
    if (len(plugins)>0):
        for job in jobList:
            job.requiredPlugins=plugins

    

def rrSubmit_Nuke_5():
    writeInfo ("rrSubmit v 6.02.01")
    nuke.scriptSave()
    CompName = nuke.root().name()
    if ((CompName==None) or (len(CompName)==0)):
        writeError("Nuke comp not saved!")
        return
    jobList= []
    noLocalSceneCopy= [False]
    rrSubmit_CreateAllJob(jobList,noLocalSceneCopy)
    rrSubmit_CreateSingleJobs(jobList)
    submitOptions=""
    if (noLocalSceneCopy[0]):
        submitOptions="AllowLocalSceneCopy=0~0"
    rrSubmit_addPluginLicenses(jobList)
    submitJobsToRR(jobList,submitOptions)
      
    

