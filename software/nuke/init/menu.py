# 07 Week *********************************************************************
# content   = menu Nuke
# date      = 2024-11-08
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import nuke
import importlib
import webbrowser

from plex import Plex


#*********************************************************************
# VARIABLE
LOG = Plex().log(script=__name__)


#*********************************************************************
# FUNCTIONS
def add_gizmo_menu(menu):
    for paths in os.getenv('SOFTWARE_PATH').split(';'):
        for file in os.listdir(paths):
            if file.endswith('.gizmo'):
                gizmo = file.replace('.gizmo', '')
                menu.addCommand('Gizmos/' + gizmo, f'nuke.tcl("{gizmo}")')

def add_write_node():
    import write_node
    for node in nuke.allNodes('arWrite'):
        write_node.create_node(node)


#*********************************************************************
# TOOLBAR
menu_config = Plex().config_software['MENU']
menuNode  = nuke.menu('Nodes').addMenu(Plex().config_project['name'], icon = 'nuke.ico')

nuke.addOnScriptSave(add_write_node)

# ADD menu
Plex().software.add_menu(menuNode)
menuNode.addSeparator()
add_gizmo_menu(menuNode)


#*********************************************************************
# ACTIONS
def save():
    import arSave
    arSave.start()


def load():
    import arLoad
    arLoad.start()


#*********************************************************************
def arWrite():
    importlib.reload(write_node)
    nuke.createNode('arWrite')
