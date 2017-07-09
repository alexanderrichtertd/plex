#*********************************************************************
# content   = maya menu
# version   = 0.6.0
# date      = 2017-07-10
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

import maya.cmds as cmds

from tank import Tank


#*************************
 # MENU
def load_menu():
      delete_menu()

      menu = cmds.menu(os.getenv('PROJECT_NAME').replace(' ',''), hm = 1, p = 'MayaWindow',
                       l = os.getenv('PROJECT_NAME').replace(' ',''), to = 1, )

      for menu_item in Tank().data['software']['MAYA']['MENU']:
            Tank().software.add_menu(menu, menu_item)


def delete_menu():
      if cmds.menu(os.getenv('PROJECT_NAME').replace(' ',''), query = True, exists = True):
            cmds.deleteUI(os.getenv('PROJECT_NAME').replace(' ',''), menu = True)

