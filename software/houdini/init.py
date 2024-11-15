#*********************************************************************
# content   = houdini init
# date      = 2020-06-19
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import pipefunc

from tank import Tank


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)


#*********************************************************************
# MENU
def add_menu():
    menu_path = f'{os.getenv("DATA_PROJECT_PATH")}/houdini/MainMenuMaster.xml'

    try:
        with open(menu_path, 'r+') as outfile:
            content = outfile.read()
            find_title = pipefunc.find_inbetween(content, '<label>', '</label>')
            content = content.replace(f'<label>{find_title}</label>', f'<label>{os.getenv("PROJECT_NAME")}</label>')
            print(content)
            # WRITE new XML
            outfile.seek(0)
            outfile.write(content)
            outfile.truncate()
    except: LOG.error(f'FILE not found: {menu_path}', exc_info=True)


add_menu()
