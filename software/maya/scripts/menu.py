#*********************************************************************
# content   = maya menu
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <contact@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys
import glob

import maya.cmds as cmds

import libLog
import libFunc


#************************
# START MAYA
libFunc.console_header()


#*************************
 # MENU
def load_menu():
      delete_menu()

      menu = cmds.menu(s.PROJECT_NAME.replace(" ",""), hm = 1, p = 'MayaWindow',
                       l = s.PROJECT_NAME.replace(" ",""), to = 1, )


      #*************************
      # SAVE & LOAD
      cmds.menuItem(p = menu, l = 'arSave',
                    c = 'from utilities import arSave\nreload(arSave)\narSave.start()')#, en = 0)
      cmds.menuItem(p = menu, l = 'arLoad',
                    c = 'from utilities import arSaveAs\nreload(arSaveAs)\narSaveAs.start(True)')#, en = 0)


      #***************************************************************************
      cmds.menuItem(p = menu,
                    d = True)

      #*************************
      # TASKS MENU
      scriptList = {}
      folderList = libFileService.getAllFolderList(path)

      # add folders as submenu
      for folder in folderList:
            scriptList[folder] = libFileService.getFolderList(path + "/"
                               + folder, fileType="*.py", exclude="__init__.py")

      # add scripts as menu
      for folderName, scriptName in scriptList.items():
            if not len(scriptName):
                  continue

            toolMenu = cmds.menuItem(p = menu, l = folderName, sm = True)

            cmds.menuItem(p = toolMenu,
                        l = scriptName, #'Alembic Export',
                        c = ('from scripts.' + folderName + " import " + scriptName + "\n" + scriptName + '.start()'))


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


      #*************************
      # RIG
      # toolMenu = cmds.menuItem(p = menu, l = 'RIG', sm = True)

      # cmds.menuItem(p = toolMenu,
      #             l = 'ngSkinTools',
      #             c = 'from ngSkinTools.ui.mainwindow import MainWindow\nMainWindow.open()')


      # #*************************
      # # ANIM
      # toolMenu = cmds.menuItem(p = menu, l = 'ANIM', sm = True)

      # cmds.menuItem(p = toolMenu,
      #             l = 'Alembic Export',
      #             c = 'from scripts.ANIM import alembicExport\nalembicExport.start()')

      # cmds.menuItem(p = toolMenu,
      #             l = 'Arc Tracker',
      #             c = 'import maya.mel as mel\nmel.eval("arctracker110")')

      # cmds.menuItem(p = toolMenu,
      #             l = 'Tween Machine',
      #             c = 'import maya.mel as mel\nmel.eval("tweenMachine")')

      # cmds.menuItem(p = toolMenu,
      #             l = 'Playblast Custom',
      #             c = 'from scripts.ANIM import createPlayblast\nreload(createPlayblast)\ncreatePlayblast.start()')

      # cmds.menuItem(p = toolMenu,
      #             l = 'prSelection',
      #             c = 'from scripts.ANIM import prSelectionUi\nreload(prSelectionUi)\nprSelectionUi.UI()')


      # #*************************
      # # LIGHT
      # toolMenu = cmds.menuItem(p = menu, l = 'LIGHT', sm = True) #, en = 0)

      # # cmds.menuItem(p = toolMenu,
      # #             l = 'ALEMBIC IMPORT',
      # #             c = 'from scripts.LIGHT import alembicImport\nalembicImport.start()')

      # cmds.menuItem(p = toolMenu,
      #             l = 'UltiMatte Mask Picker',
      #             c = 'from scripts.LIGHT import bgUltiMatteMaskPicker\nbgUltiMatteMaskPicker.UI()')


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


      #*************************
      # UTILITIES
      toolMenu = cmds.menuItem(p = menu, l = 'Utilities', sm = True)

      cmds.menuItem(p = toolMenu,
                  l = 'Position Selected',
                  c = 'from scripts import utilities\nutilities.positionSelected()')

      cmds.menuItem(p = toolMenu,
                  l = 'Fix Render Layer Bug',
                  c = 'import maya.mel as mel\nmel.eval("fixRenderLayerOutAdjustmentErrors;")')


      #***************************************************************************
      cmds.menuItem(p = menu,
                   d = True)

      #*************************
      # PLUGINS
      toolMenu = cmds.menuItem(p = menu, l = 'Plugins', sm = True)

      # cmds.menuItem(p = toolMenu,
      #             l = 'Refresh All Scripts',
      #             c = 'from lib import libFunction.refreshAllScripts()')

      cmds.menuItem(p = toolMenu,
                  l = 'AtoN',
                  c = 'from scripts import aton\naton = aton.Aton()\naton.show()')

      cmds.menuItem(p = toolMenu,
                  l = 'SLiBBrowser',
                  c = 'import SLiBBrowserPy;reload(SLiBBrowserPy);SLiBBrowserPy.SLiBBrowserUI()')

      cmds.menuItem(p = toolMenu,
                  l = 'Import | Export Obj Sequence',
                  c = 'import maya.mel as mel\nmel.eval("craOBJSequences")')


      #***************************************************************************
      cmds.menuItem(p = menu,
                   d = True)

      #*************************
      # HELP
      cmds.menuItem(p = menu,
                  l = 'arReport',
                  c = 'from utilities import arReport\nreload(arReport)\narReport.start()')

      cmds.menuItem(p = menu,
                  l = 'Help',
                  c = 'import webbrowser\nwebbrowser.open("https://www.filmakademie.de/wiki/display/AISPD/arPipeline+|+Maya")')


def delete_menu():
      if cmds.menu(s.PROJECT_NAME.replace(" ",""), query = True, exists = True):
            cmds.deleteUI(s.PROJECT_NAME.replace(" ",""), menu = True)

