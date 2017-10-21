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
from tank import Tank

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

all_data      = Tank().data
project_data  = all_data['project']
software_data = all_data['software']
wgObject = ''

#*********************************************************************
# FUNC
def add_gizmo_menu(menu):
    for paths in os.getenv('SOFTWARE_SUB_PATH').split(';'):
        for file in os.listdir(paths):
            if file.endswith('.gizmo'):
                gizmo = file.replace('.gizmo', '')
                menu.addCommand('Gizmos/' + gizmo, 'nuke.tcl("{}")'.format(gizmo))

def add_write_node():
    import write_node
    for node in nuke.allNodes('arWrite'):
        write_node.create_node(node)

#*********************************************************************
# TOOLBAR

menu_data    = software_data['NUKE']['MENU']
menuNode     = nuke.menu('Nodes').addMenu(project_data['name'], icon = 'nuke.ico')

nuke.addOnScriptSave(add_write_node)

# ADD menu
Tank().software.add_menu(menuNode)
menuNode.addSeparator()
add_gizmo_menu(menuNode)


#*********************************************************************
# FUNC
def save():
    from utils import arSave
    arSave.start()


def load():
    from utils import arLoad
    arLoad.start()


#*********************************************************************
def arWrite():
    reload(write_node)
    nuke.createNode('arWrite')
