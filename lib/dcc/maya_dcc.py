#*********************************************************************
# content   = Maya
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

from tank import Tank
from software import Software


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)


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
        shelf_config = Tank().config_software['SHELF']

        # GET header scripts
        if header_footer: new_shelf += shelf_config['HEADER']

        # GET main scripts
        if shelf_name in shelf_config:
            new_shelf += shelf_config[shelf_name]
        else:
            LOG.warning(f'shelf {shelf_name} doesnt exist')

        # GET footer scripts
        if header_footer: new_shelf += shelf_config['FOOTER']

        LOG.debug(f'{shelf_name} - {new_shelf}')
        if not shelf_name: shelf_name = Tank().plex_context['project_name']

        # DELETE old and CREATE shelf tab
        remove_shelfs = shelf_config.keys() + [shelf_name, Tank().plex_context['project_name']]
        for shelf in remove_shelfs:
            if pm.shelfLayout(shelf, ex=1):
                pm.deleteUI(shelf)

        pm.shelfLayout(shelf_name, p="ShelfLayout")
        pm.setParent(shelf_name)

        # ADD shelf btn
        for btn in new_shelf:
            for key, item in btn.items():
                shelf_btn = f'pm.shelfButton({item})'
                eval(shelf_btn)

        shelf_nr = len(mel.eval('layout -q -ca ShelfLayout;'))
        mel.eval(f'shelfTabLayout -edit -selectTabIndex {shelf_nr} ShelfLayout;')


    #******************************************************************************
    # SNAPSHOT
    def viewport_snapshot(img_path):
        mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')

        # playblast one frame to a specific file
        currentFrame = str(cmds.currentTime(q=1))
        snapshotStr = 'playblast -frame ' + currentFrame + ' -format "image" -cf "' + img_path + '" -v 0 -wh 1024 576 -p 100;'
        mel.eval(snapshotStr)

        # restore the old format
        mel.eval('setAttr "defaultRenderGlobals.imageFormat" `getAttr "defaultRenderGlobals.imageFormat"`;')
        LOG.info("maya_viewport_snapshot")


    def render_snapshot(img_path):
        mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')

        LOG.info("maya_render_snapshot")
        return cmds.renderWindowEditor('renderView', e=True, writeImage=img_path)
