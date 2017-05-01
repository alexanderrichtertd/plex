#*********************************************************************
# content   = maya menu
# version   = 0.0.1
# date      = 2017-01-01
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

import libLog
import libFunc
import software


#************************
# START MAYA
libFunc.console_header()


#*************************
 # MENU
def load_menu():
      delete_menu()

      menu = cmds.menu(s.PROJECT_NAME.replace(' ',''), hm = 1, p = 'MayaWindow',
                       l = os.getenv('PROJECT_NAME').replace(' ',''), to = 1, )

      software.Software().add_menu(menu)


      #*************************
      # SHD
      # toolMenu = cmds.menuItem(p = menu, l = 'SHD', sm = True)

      # cmds.menuItem(p = toolMenu,
      #             l = 'Reference SHD_SCENE',
      #             c = 'from scripts.SHD import referenceSCENE_SHD\nreferenceSCENE_SHD.start()')

      # cmds.menuItem(p = toolMenu,
      #             l = 'Combine SHD and MODEL',
      #             c = 'from scripts.SHD import combineSHD_MODEL\ncombineSHD_MODEL.start()')

      # cmds.menuItem(p = toolMenu,
      #             l = 'Unite Shader and Group',
      #             c = 'from scripts.SHD import uniteShaderGroup\nuniteShaderGroup.start()')



      # #*************************
      # # ANIM
      # toolMenu = cmds.menuItem(p = menu, l = 'ANIM', sm = True)

      # cmds.menuItem(p = toolMenu,
      #             l = 'Playblast Custom',
      #             c = 'from scripts.ANIM import createPlayblast\nreload(createPlayblast)\ncreatePlayblast.start()')

      # cmds.menuItem(p = toolMenu,
      #             l = 'prSelection',
      #             c = 'from scripts.ANIM import prSelectionUi\nreload(prSelectionUi)\nprSelectionUi.UI()')



      # #*************************
      # # RENDER
      # #*************************
      # toolMenu = cmds.menuItem(p = menu, l = 'RENDER', sm = True, en = 0)

      # cmds.menuItem(p = toolMenu,
      #             l = 'Set Render Settings',
      #             c = 'from scripts.RENDER import renderSettings\nrenderSettings.start()')

      # cmds.menuItem(p = toolMenu,
      #             l = 'Low Render Settings',
      #             c = 'from scripts.RENDER import renderSettings\nrenderSettings.lowRenderSetting()')

      # cmds.menuItem(p = toolMenu,
      #             l = 'High Render Settings',
      #             c = 'from scripts.RENDER import renderSettings\nrenderSettings.highRenderSetting()')




def delete_menu():
      if cmds.menu(s.PROJECT_NAME.replace(' ',''), query = True, exists = True):
            cmds.deleteUI(s.PROJECT_NAME.replace(' ',''), menu = True)

