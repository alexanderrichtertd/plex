#*********************************************************************
# content   = startup 3Ds Max
# version   = 0.0.1
# date      = 2018-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import shutil

import MaxPlus

import pipelog
from tank import Tank

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = pipelog.init(script=TITLE)

Tank().init_software()

menu_name = os.getenv('PROJECT_NAME')


#************************
# MENU
def create_menu():
    # copy_splash()
    delete_menu()

    if MaxPlus.MenuManager.MenuExists(menu_name):
        print('The menu ', menu_name, ' already exists')
    else:
        menu = MaxPlus.MenuBuilder(menu_name)
        Tank().software.add_menu(menu)


def delete_menu():
    MaxPlus.MenuManager.UnregisterMenu(unicode(menu_name))


def copy_splash():
    splash_path = Tank().get_img_path("software/max/splash.bmp")
    max_path    = os.path.dirname(Tank().software.data['path'])

    if not os.path.exists(max_path + '/splash.bmp'):
        try: shutil.copy(splash_path, max_path)
        except: LOG.error('FAILED to copy splash: '.format(max_path), exc_info=True)


create_menu()




