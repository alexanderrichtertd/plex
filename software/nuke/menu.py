#*************************************************************
# title:        menu
#
# function:     starup script for Nuke Menu
#           
# depencence:   set "NUKE_PATH=%PLUGINS_PATH%;%NUKE_PATH%"
#
# author:       Alexander Richter 
# email:        contact@richteralexander.com
#*************************************************************

import os
import sys
import nuke
import webbrowser

import settings as s

# sys.path.append(s.PATH['lib'])
import libUser
import libFunction


#************************
# LOG
#************************
import libLog
import logging

TITLE = "nuke"
os.environ["SOFTWARE"] = TITLE


#************************
# LOG
#************************
import logging
LOG   = libLog.initLog(software=os.environ["SOFTWARE"], script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))
LOG.info("START")


#************************
# GIZMOS
#************************
def buildGizmoMenu(menu):
  for file in os.listdir(s.PATH["nuke_gizmos"]):
    if file.endswith('.gizmo'):
      gizmo = file.replace('.gizmo', '')
      menu.addCommand('Nodes/' + gizmo, 'nuke.tcl(\'' + str(gizmo) + '\')')


#************************
# INIT
#************************
print ("\nWelcome " + libUser.getCurrentUser())
print ("\n" + s.PROJECT_NAME + ": MENU")


menuNode = nuke.menu('Nodes').addMenu(s.PROJECT_NAME, icon = 'nuke_toolbar.png')


#*******************
# TOOLBAR
#*******************
menuNode.addCommand('Save', lambda: save(), 'ctrl+alt+s', "save.ico")
menuNode.addCommand('Load', lambda: load(), 'alt+l', "load.ico")

menuNode.addSeparator()

menuNode.addCommand('arWrite', lambda: arWrite(), 'alt+w', "write.ico")
menuNode.addSeparator()

buildGizmoMenu(menuNode)

menuNode.addCommand("Plugins/rrSubmit", lambda: rrender(), 'alt+b', "rrender.ico")
menuNode.addCommand('Plugins/Renderthreads', lambda: renderthreads(), 'alt+v', "renderthreads.ico")
menuNode.addCommand('Plugins/AtoN', lambda: startAton(), 'alt+a', "aton.ico")

menuNode.addSeparator()

menuNode.addCommand('Report', lambda: report(), 'alt+r', "report.ico")
menuNode.addCommand('Help', lambda: helpWeb(), 'alt+h', "help.ico")

# m = menuNode.findItem('Write')
# m.setEnabled(False)


def save():
    from utilities import arSave
    reload(arSave)
    arSave.start()
    LOG.info('SAVE')


def load():
    from utilities import arSaveAs
    reload(arSaveAs)
    arSaveAs.start(True)
    LOG.info('LOAD : arSaveAs')


#********************************
def arWrite():
    nuke.createNode("arWrite")
    LOG.info('arWrite')


#********************************
def startAton():
    nuke.createNode("Aton")
    LOG.info('AtoN')


#********************************
def rrender():
    import rrenderSubmit
    nuke.load('rrenderSubmit')
    rrenderSubmit.rrSubmit_Nuke()
    LOG.info('ROYAL RENDER : rrenderSubmit')


def renderthreads():
    plugin_nuke.showPopup()
    LOG.info('RENDERTHREADS : Vincent')


# def run_renderthreadsT():
#     from plugins.renderthreads import renderthreads
#     reload(renderthreads)
#     renderthreads.run()
#     LOG.info('RENDERTHREADS : Timm')


#********************************
def report():
    from utilities import arReport
    reload(arReport)
    arReport.start(currentScript = 'other')
    LOG.info('REPORT')


def helpWeb():
    libFunction.getHelp()
    LOG.info('HELP')


#************************
# INIT
#************************
def setWriteNode():
    from scripts import writeNode

    write = nuke.allNodes("arWrite")
    for currentNode in write:     
        writeNode.nodeCreate(currentNode)

    
nuke.addOnScriptSave(setWriteNode)