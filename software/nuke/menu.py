#*********************************************************************
# content   = menu Nuke
# version   = 0.0.1
# date      = 2019-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os
import nuke
import webbrowser

from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)

PROJECT_DATA  = Tank().data_project
SOFTWARE_DATA = Tank().data_software


#*********************************************************************
# FUNCTIONS
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
menu_data = SOFTWARE_DATA['NUKE']['MENU']
menuNode  = nuke.menu('Nodes').addMenu(PROJECT_DATA['name'], icon = 'nuke.ico')

nuke.addOnScriptSave(add_write_node)

# ADD menu
Tank().software.add_menu(menuNode)
menuNode.addSeparator()
add_gizmo_menu(menuNode)


#*********************************************************************
# ACTIONS
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
