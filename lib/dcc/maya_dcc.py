#*********************************************************************
# content   = Maya
# version   = 0.1.0
# date      = 2019-10-06
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

import maya_utils

from tank import Tank
from software import Software


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
# CLASS
class Maya(Software):

    _NAME = 'maya'

    @property
    def scene_path(self):
        return pm.sceneName()

    def scene_save(self, file_path):
        return pm.saveFile(file_path)

    def scene_save_as(self, file_path, setup_scene=False):
        if setup_scene: self.scene_setup(file_path)
        return pm.saveAs(file_path)

    def scene_open(self, file_path):
        return pm.openFile(file_path, force=True)

    def scene_import(self, file_path):
        pass

        # # reference or open
        # if ref or ".abc" in self.save_dir or ".obj" in self.save_dir or ".fbx" in self.save_dir:
        #     # file -r -type "mayaBinary"  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "bull_MODEL_v004_jo" -options "v=0;" "K:/30_assets/bull/10_MODEL/WORK/bull_MODEL_v004_jo.mb";
        #     mel.eval('file -r -type "' + s.FILE_FORMAT_CODE["." + self.save_dir.split(".")[-1]] + '" -ignoreVersion -gl -mergeNamespacesOnClash false "' + self.save_dir.replace("\\", "/") + '"')


    #*********************************************************************
    # SHELF
    def add_shelf(self, shelf_name='', header_footer=True):
        new_shelf  = []
        shelf_data = Tank().data_software['SHELF']

        # GET header scripts
        if header_footer: new_shelf += shelf_data['HEADER']

        # GET main scripts
        if shelf_name in shelf_data:
            new_shelf += shelf_data[shelf_name]
        else:
            LOG.warning('shelf {} doesnt exist'.format(shelf_name))

        # GET footer scripts
        if header_footer: new_shelf += shelf_data['FOOTER']

        LOG.debug('{} - {}'.format(shelf_name, new_shelf))
        if not shelf_name: shelf_name = os.getenv('PROJECT_NAME')

        # DELETE old and CREATE shelf tab
        remove_shelfs = shelf_data.keys() + [shelf_name, os.getenv('PROJECT_NAME')]
        for shelf in remove_shelfs:
            if pm.shelfLayout(shelf, ex=1):
                pm.deleteUI(shelf)

        pm.shelfLayout(shelf_name, p="ShelfLayout")
        pm.setParent(shelf_name)

        # ADD shelf btn
        for btn in new_shelf:
            for key, item in btn.items():
                shelf_btn = 'pm.shelfButton({})'.format(item)
                eval(shelf_btn)

        shelf_nr = len(mel.eval('layout -q -ca ShelfLayout;'))
        mel.eval('shelfTabLayout -edit -selectTabIndex {} ShelfLayout;'.format(shelf_nr))
