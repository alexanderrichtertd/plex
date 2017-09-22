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
import shutil

import MaxPlus

import libLog
import libFunc
import libData
import libFileFolder
from tank import Tank

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

Tank().init_software()

menu_name = os.getenv('PROJECT_NAME')


#************************
# MENU
def create_menu():
    # copy_splash()
    delete_menu()

    if MaxPlus.MenuManager.MenuExists(menu_name):
        print ('The menu ', menu_name, ' already exists')
    else:
        menu = MaxPlus.MenuBuilder(menu_name)
        Tank().software.add_menu(menu)


def delete_menu():
    MaxPlus.MenuManager.UnregisterMenu(unicode(menu_name))


def copy_splash():
    splash_path = libData.get_img_path("software/max/splash.bmp")
    max_path    = os.path.dirname(Tank().software.data['path'])

    if not os.path.exists(max_path + '/splash.bmp'):
        try: shutil.copy(splash_path, max_path)
        except: LOG.error('FAILED to copy splash: '.format(max_path), exc_info=True)


create_menu()




