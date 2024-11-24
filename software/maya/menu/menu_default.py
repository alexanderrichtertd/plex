# 07 Week *********************************************************************
# content = menu & shelf
#
# date    = 2024-11-24
# author  = contact@alexanderrichtertd.com
#******************************************************************************

import maya.cmds as cmds

from tank import Tank


#******************************************************************************
# VARIABLES
MENU_NAME = Tank().config_project['name'][:20]


#******************************************************************************
# MENU
#******************************************************************************
def create_menu():
    delete_menu()

    menu = cmds.menu(MENU_NAME, parent='MayaWindow',
                     label=MENU_NAME, helpMenu=True, tearOff=True)

    #*************************************************************************
    # SAVE & LOAD
    cmds.menuItem(parent=menu, label='Save', command='print("save")')
    cmds.menuItem(parent=menu, label='Load', command='print("load")')

    # BREAK ******************************************************************
    cmds.menuItem(parent=menu, divider=True)

    #*************************************************************************
    # LIGHT
    light_menu = cmds.menuItem(parent=menu, label='LIGHT', subMenu=True)

    cmds.menuItem(parent=light_menu,
                  label='Light Linker',
                  command='import week_07_light_linker;week_07_light_linker.load()')

    # BREAK ******************************************************************
    cmds.menuItem(parent=menu, divider=True)

    #*************************************************************************
    # HELP
    cmds.menuItem(parent=menu,
                  label='Help',
                  command=f'import webbrowser;webbrowser.open("{Tank().config_project["URL"]["default"]}")')


def delete_menu():
    if cmds.menu(MENU_NAME, query=True, exists=True):
        cmds.deleteUI(MENU_NAME, menu=True)


#*************************************************************************
# SHELF
def create_shelf():
    delete_shelf()

    cmds.shelfLayout(MENU_NAME, parent="ShelfLayout")

    cmds.shelfButton(parent=MENU_NAME,
                     annotation='Light Linker',
                     image1=Tank().get_img_path('icons/default'),
                     command='import week_07_light_linker;week_07_light_linker.load()')


def delete_shelf():
    if cmds.shelfLayout(MENU_NAME, exists=True):
        cmds.deleteUI(MENU_NAME)
