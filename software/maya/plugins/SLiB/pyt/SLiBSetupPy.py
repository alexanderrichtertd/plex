#########################################################################
#
#  SLiBSetupPy.py v0.1 by DGDM
#
#########################################################################


import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import string
import compiler
import platform
import time

def SLiBSetupMenu():
    print "SLib"
    # gMainWindow = mel.eval('$temp1=$gMainWindow')
    # if cmds.menu('SLiBMenu', query = True, exists = True):
    #     cmds.deleteUI('SLiBMenu', menu = True)
    # SLiBMenu = cmds.menu('SLiBMenu', parent = gMainWindow, tearOff = True, label = 'SLiB')
    # #cmds.menuItem(parent = 'SLiBMenu', label = 'Settings', command = 'import SLiBBrowserPy;reload(SLiBBrowserPy);SLiBBrowserPy.SLiBSetupSettingsUI()')
    # #cmds.menuItem(parent = 'SLiBMenu', divider=True)    
    # cmds.menuItem(parent = 'SLiBMenu', label = 'SLiB Browser ...', command = 'import SLiBBrowserPy;reload(SLiBBrowserPy);SLiBBrowserPy.SLiBBrowserUI()')
    # cmds.menuItem(parent = 'SLiBMenu', divider=True)
    # cmds.menuItem(parent = 'SLiBMenu', label = 'SLiB FloorGen ...', command = 'import SLiBFloorGenPY;reload(SLiBFloorGenPY)')
    # cmds.menuItem(parent = 'SLiBMenu', divider=True) 
    # cmds.menuItem(parent = 'SLiBMenu', label = 'SLiB Leuchtkraft ...', command = 'import SLiBLeuchtkraftPY;reload(SLiBLeuchtkraftPY);SLiBLeuchtkraftPY.create()')
    # cmds.menuItem(parent = 'SLiBMenu', divider=True) 
    # cmds.menuItem(parent = 'SLiBMenu', label = 'SLiB Partikel ...', command = 'import SLiBPartikelPY;reload(SLiBPartikelPY);SLiBPartikelPY.partikel()')
    # cmds.menuItem(parent = 'SLiBMenu', divider=True) 
    # cmds.menuItem(parent = 'SLiBMenu', label = 'Homepage', command = 'import maya;maya.cmds.showHelp("http://store.cgfront.com", absolute=True)')

def SLiBSetupMenuRemove():
    if cmds.menu('SLiBMenu', query = True, exists = True):
        cmds.deleteUI('SLiBMenu', menu = True)
 
def SLiBSetupLoad():
    SLiBSetupMenu()

def SLiBSetupUnLoad():
    SLiBSetupMenuRemove() 