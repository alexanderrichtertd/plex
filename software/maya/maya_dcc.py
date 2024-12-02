# content   = Maya
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import maya.mel as mel
import maya.cmds as cmds

from plex import Plex
from software import Software

LOG = Plex().log(script=__name__)


class Maya(Software):
    menu_name = Plex().config_plex['name']
    name = 'maya'

    @property
    def scene_path(self):
        return cmds.file(query=True, sceneName=True)

    def scene_save(self, file_path):
        cmds.file(rename=file_path)
        return cmds.file(save=True)

    def scene_open(self, file_path):
        return cmds.file(file_path, open=True, force=True)

    def scene_import(self, file_path):
        return cmds.file(file_path, i=True)

    def scene_reference(self, file_path):
        return cmds.file(file_path, reference=True)


    # MENU ***************************************************************
    def create_menu(self):
        self.delete_menu()
        print('create menu: Maya')

        menu = cmds.menu(self.menu_name, parent='MayaWindow', label=self.menu_name, helpMenu=True, tearOff=True)

        menu_config = Plex().config_software['MENU']
        LOG.debug(f'Menu items: {menu_config}')

        for menu_item in menu_config:
            for key, value in menu_item.items():
                if isinstance(value, list):
                    sub_menu = cmds.menuItem(parent=menu, label=key, subMenu=True)
                    for sub_item in value:
                        for label, command in sub_item.items():
                            if label == 'break':
                                cmds.menuItem(parent=sub_menu, divider=True)
                            else:
                                cmds.menuItem(parent=sub_menu, label=label, command=command)
                else:
                    if key == 'break':
                        cmds.menuItem(parent=menu, divider=True)
                    else:
                        cmds.menuItem(parent=menu, label=key, command=value)
        

    def delete_menu(self):
        if cmds.menu(self.menu_name, query=True, exists=True):
            cmds.deleteUI(self.menu_name, menu=True)
        
        # # reference or open
        # if ref or ".abc" in self.save_dir or ".obj" in self.save_dir or ".fbx" in self.save_dir:
        #     # file -r -type "mayaBinary"  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "bull_MODEL_v004_jo" -options "v=0;" "K:/30_assets/bull/10_MODEL/WORK/bull_MODEL_v004_jo.mb";
        #     mel.eval('file -r -type "' + s.FILE_FORMAT_CODE["." + self.save_dir.split(".")[-1]] + '" -ignoreVersion -gl -mergeNamespacesOnClash false "' + self.save_dir.replace("\\", "/") + '"')


    # SNAPSHOT ***************************************************************
    def viewport_snapshot(self, img_path):
        mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')

        # playblast one frame to a specific file
        currentFrame = str(cmds.currentTime(q=1))
        snapshotStr = 'playblast -frame ' + currentFrame + ' -format "image" -cf "' + img_path + '" -v 0 -wh 1024 576 -p 100;'
        mel.eval(snapshotStr)

        # restore the old format
        mel.eval('setAttr "defaultRenderGlobals.imageFormat" `getAttr "defaultRenderGlobals.imageFormat"`;')
        LOG.info("maya_viewport_snapshot")


    def render_snapshot(self, img_path):
        mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')

        LOG.info("maya_render_snapshot")
        return cmds.renderWindowEditor('renderView', e=True, writeImage=img_path)
