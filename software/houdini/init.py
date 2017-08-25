#*********************************************************************
# content   = houdini init
# version   = 0.0.1
# date      = 2017-08-20
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
import libFunc

import libLog


#*************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#*************************
# MENU
def add_menu():
    menu_path = '{}/houdini/MainMenuMaster.xml'.format(os.getenv('DATA_PROJECT_PATH'))

    try:
        with open(menu_path, 'r+') as outfile:
            content = outfile.read()
            find_title = libFunc.find_inbetween(content, '<label>', '</label>')
            content = content.replace('<label>{}</label>'.format(find_title), '<label>{}</label>'.format(os.getenv('PROJECT_NAME')))
            print content
            # WRITE new XML
            outfile.seek(0)
            outfile.write(content)
            outfile.truncate()
    except: LOG.error('FILE not found: '.format(menu_path), exc_info=True)


add_menu()
