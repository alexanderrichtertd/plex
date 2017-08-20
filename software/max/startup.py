#*********************************************************************
# content   = startup 3Ds Max
# version   = 0.0.1
# date      = 2017-08-15
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

import MaxPlus

import libLog
import libFunc
import libFileFolder
from tank import Tank

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

Tank().init_software()

menu_name = os.getenv('PROJECT_NAME')

#************************
# MENU
def create_menu():

    delete_menu()

    if MaxPlus.MenuManager.MenuExists(menu_name):
        print ('The menu ', menu_name, ' already exists')
    else:
        menu = MaxPlus.MenuBuilder(menu_name)

        Tank().software.add_menu(menu)

        # sub_menu = MaxPlus.MenuBuilder(keys)
        # sub_menu.Create(menu_node)

        # menu.AddItem(MaxPlus.ActionFactory.Create('Open Scene Folder2', 'Open Scene Folder', lambda: libFileFolder.open_folder(MaxPlus.Core.EvalMAXScript("sceneName = maxFilePath + maxFileName").Get())))
        # menu.AddItem(MaxPlus.ActionFactory.Create('Open Scene Folder2', 'Open Scene Folder', lambda: libFileFolder.open_folder(MaxPlus.Core.EvalMAXScript("sceneName = maxFilePath + maxFileName").Get())))
        # menu.AddItem(MaxPlus.ActionFactory.Create('Open Project Folder2', 'Open Project Folder', lambda: libFileFolder.open_folder(os.getenv("PROJECT_PATH"))))


        # sub_menu = MaxPlus.MenuBuilder("Plexsub")
        # sub_menu.AddItem(MaxPlus.ActionFactory.Create('Report2', 'Help', libFunc.get_help))

        # menu.AddItem(MaxPlus.ActionFactory.Create('Report2', 'Report', lambda: libFunc.get_help("issues")))

        # menu_setup = menu.Create(MaxPlus.MenuManager.GetMainMenu())
        # main_sub_menu = sub_menu.Create(menu_setup, 0)


def delete_menu():
    MaxPlus.MenuManager.UnregisterMenu(unicode(menu_name))


# reload(startup)
create_menu()



# import MaxPlus
# print 'The Scripts directory is', MaxPlus.PathManager.GetScriptsDir()
# print 'The Temp directory is', MaxPlus.PathManager.GetTempDir()



