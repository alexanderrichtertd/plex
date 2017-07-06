#*********************************************************************
# content   = menu Nuke
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import nuke
import webbrowser

import libLog
import libFunc
import libFileFolder
from tank import Tank

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

all_data      = Tank().data
project_data  = all_data['project']
software_data = all_data['software']

#************************
# FUNC
def add_gizmo_menu(menu):
    for paths in os.getenv('SOFTWARE_SUB_PATH').split(';'):
        for file in os.listdir(paths):
            if file.endswith('.gizmo'):
                gizmo = file.replace('.gizmo', '')
                menu.addCommand('Gizmos/' + gizmo, 'nuke.tcl("{}")'.format(gizmo))

def add_write_node():
    write = nuke.allNodes('arWrite')
    for currentNode in write:
        write_node.nodeCreate(currentNode)

def add_plugin_paths():
    # ADD all IMG paths
    for img in os.getenv('IMG_PATH').split(';'):
        for img_sub in libFileFolder.get_deep_folder_list(path=img, add_path=True):
            nuke.pluginAddPath(img_sub)

    # ADD sub software paths
    for paths in os.getenv('SOFTWARE_SUB_PATH').split(';'):
        nuke.pluginAddPath(paths)


#*******************
# TOOLBAR
add_plugin_paths()

menu_data    = software_data['NUKE']['MENU']
menuNode     = nuke.menu('Nodes').addMenu(project_data['name'], icon = 'nuke.ico')

nuke.addOnScriptSave(add_write_node)

for menu_item in menu_data:
    Tank().software.add_menu(menuNode, menu_item)

menuNode.addSeparator()

add_gizmo_menu(menuNode)


#*******************
# FUNC
def save():
    from utils import arSave
    reload(arSave)
    arSave.main()
    LOG.info('SAVE')


def load():
    from utils import arSaveAs
    reload(arSaveAs)
    arSaveAs.main(True)
    LOG.info('LOAD : arSaveAs')


#********************************
def arWrite():
    reload(write_node)
    nuke.createNode('arWrite')
    LOG.info('arWrite')
