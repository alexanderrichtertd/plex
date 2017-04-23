#*********************************************************************
# content   = menu Nuke
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
import sys
import nuke
import webbrowser

import libLog
# import libData

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#*******************
# TOOLBAR

# menu_data = libData.get_data('software')['NUKE']['menu']

# menuNode = nuke.menu('Nodes').addMenu(s.PROJECT_NAME, icon = 'nuke_toolbar.png')

# create_menu(menuNode, menu_data)
# add_gizmo_menu(menuNode)

# menuNode.addCommand('Save', lambda: save(), 'ctrl+alt+s', "save.ico")
# menuNode.addCommand('Load', lambda: load(), 'alt+l', "load.ico")

# menuNode.addSeparator()

# menuNode.addCommand('arWrite', lambda: arWrite(), 'alt+w', "write.ico")
# menuNode.addSeparator()


# menuNode.addCommand("Plugins/rrSubmit", lambda: rrender(), 'alt+b', "rrender.ico")
# menuNode.addCommand('Plugins/Renderthreads', lambda: renderthreads(), 'alt+v', "renderthreads.ico")
# menuNode.addCommand('Plugins/AtoN', lambda: startAton(), 'alt+a', "aton.ico")

# menuNode.addSeparator()

# menuNode.addCommand('Report', lambda: report(), 'alt+r', "report.ico")
# menuNode.addCommand('Help', lambda: help_open(), 'alt+h', "help.ico")

# m = menuNode.findItem('Write')
# m.setEnabled(False)

#************************
# MENU
def create_menu(menu_node, new_command):
    for keys, item in new_command.keys(), new_command.items():
        print item
        if isinstance(item, dict):
            new_menu = item.keys() # nuke.menu('Nodes').addMenu(item.keys())
            create_menu(new_menu, item)
        else:
            print('{} - {}').format(menu_node, keys)
            # menu_node.(exec(item))

#************************
# GIZMOS
def add_gizmo_menu(menu):
  for file in os.listdir(s.PATH["nuke_gizmos"]):
    if file.endswith('.gizmo'):
      gizmo = file.replace('.gizmo', '')
      menu.addCommand('Nodes/' + gizmo, 'nuke.tcl(\'' + str(gizmo) + '\')')


#************************
# FUNC
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

def arWrite():
    nuke.createNode("arWrite")
    LOG.info('arWrite')

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

def report():
    from utilities import arReport
    reload(arReport)
    arReport.start(currentScript = 'other')
    LOG.info('REPORT')


def help_open():
    libFunction.getHelp()
    LOG.info('HELP')


#************************
# INIT
def setWriteNode():
    from scripts import writeNode

    write = nuke.allNodes("arWrite")
    for currentNode in write:
        writeNode.nodeCreate(currentNode)


nuke.addOnScriptSave(setWriteNode)


