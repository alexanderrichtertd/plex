#*********************************************************************
# content   = startup 3Ds Max
# date      = 2020-06-19
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import shutil

import MaxPlus

from tank import Tank


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)
menu_name = Tank().plex_context['project_name']
Tank().init_software()



#*********************************************************************
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
    max_path    = os.path.dirname(Tank().software.config['path'])

    if not os.path.exists(max_path + '/splash.bmp'):
        try:
            shutil.copy(splash_path, max_path)
        except:
            LOG.error(f'FAILED to copy splash: {max_path}', exc_info=True)


create_menu()
