# -*- coding: utf-8 -*-
#  SLiB.py by DGDM

import sys
import os
import imp
import maya.cmds as cmds
import maya.mel as mel

#########################################################################

    #!!! Set Path to SLiB Folder here: (use Forward Slash ONLY) !!!

SLiBInstallPath = "M:/_pipeline/WORK/software/maya/plugins/SLiB"  #os.path.dirname(os.path.realpath('__file__')) + '/SLiB'

#########################################################################


guiPath = SLiBInstallPath + '/' + 'gui' + '/'
imgPath = SLiBInstallPath + '/' + 'img' + '/'
pytPath = SLiBInstallPath + '/' + 'pyt' + '/'
libPath = SLiBInstallPath + '/' + 'lib' + '/' 
sys.path.append(pytPath)

import SLiBSetupPy
reload(SLiBSetupPy)

def initializePlugin(obj):
    mel.eval('putenv "SLiBGui"      "' + guiPath + '"')
    mel.eval('putenv "SLiBImage"    "' + imgPath + '"')
    mel.eval('putenv "SLiBLib"      "' + libPath + '"')
    mel.eval('putenv "SLiBPyt"      "' + pytPath + '"')

    reload(SLiBSetupPy)
    SLiBSetupPy.SLiBSetupLoad()
    print 'SLiB: >>> Plug-In successfully loaded!'

def uninitializePlugin(obj):
    reload(SLiBSetupPy)
    SLiBSetupPy.SLiBSetupUnLoad()
    print "SLiB: >>> Plug-In unloaded!"