#*********************************************************************
# content   = houdini init
# version   = 0.1.0
# date      = 2019-10-06
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os
import pipefunc

from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
# MENU
def add_menu():
    menu_path = '{}/houdini/MainMenuMaster.xml'.format(os.getenv('DATA_PROJECT_PATH'))

    try:
        with open(menu_path, 'r+') as outfile:
            content = outfile.read()
            find_title = pipefunc.find_inbetween(content, '<label>', '</label>')
            content = content.replace('<label>{}</label>'.format(find_title), '<label>{}</label>'.format(os.getenv('PROJECT_NAME')))
            print(content)
            # WRITE new XML
            outfile.seek(0)
            outfile.write(content)
            outfile.truncate()
    except: LOG.error('FILE not found: '.format(menu_path), exc_info=True)


add_menu()
