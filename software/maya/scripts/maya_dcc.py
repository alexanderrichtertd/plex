#*********************************************************************
# content   = Maya
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import maya.cmds as cmds

from tank import Tank
from software import Software


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)
MENU_NAME = Tank().config_project['name'][:20]


#*********************************************************************
# CLASS
class Maya(Software):
    NAME = 'maya'

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


    #******************************************************************************
    # MENU
    def create_menu(self):
        self.delete_menu()
        print('create menu: Maya')

        menu = cmds.menu(MENU_NAME, parent='MayaWindow', label=MENU_NAME, helpMenu=True, tearOff=True)

        LOG.debug(Tank().config_software['MENU'])
        for menu_item in Tank().config_software['MENU']:
            # print(menu_item)
            for key, value in menu_item.items():
                if value == 'None':
                    print(f'MENU: {key}')
                    sub_menu = cmds.menuItem(parent=menu, label=key, subMenu=True)
                else:
                    print(value)
                    cmds.menuItem(eval(menu_item.format(sub_menu)))


    def delete_menu():
        if cmds.menu(MENU_NAME, query=True, exists=True):
            cmds.deleteUI(MENU_NAME, menu=True)
      
        # # reference or open
        # if ref or ".abc" in self.save_dir or ".obj" in self.save_dir or ".fbx" in self.save_dir:
        #     # file -r -type "mayaBinary"  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "bull_MODEL_v004_jo" -options "v=0;" "K:/30_assets/bull/10_MODEL/WORK/bull_MODEL_v004_jo.mb";
        #     mel.eval('file -r -type "' + s.FILE_FORMAT_CODE["." + self.save_dir.split(".")[-1]] + '" -ignoreVersion -gl -mergeNamespacesOnClash false "' + self.save_dir.replace("\\", "/") + '"')


    #******************************************************************************
    # SNAPSHOT
    # def viewport_snapshot(img_path):
    #     mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')

    #     # playblast one frame to a specific file
    #     currentFrame = str(cmds.currentTime(q=1))
    #     snapshotStr = 'playblast -frame ' + currentFrame + ' -format "image" -cf "' + img_path + '" -v 0 -wh 1024 576 -p 100;'
    #     mel.eval(snapshotStr)

    #     # restore the old format
    #     mel.eval('setAttr "defaultRenderGlobals.imageFormat" `getAttr "defaultRenderGlobals.imageFormat"`;')
    #     LOG.info("maya_viewport_snapshot")


    # def render_snapshot(img_path):
    #     mel.eval('setAttr "defaultRenderGlobals.imageFormat" 8;')

    #     LOG.info("maya_render_snapshot")
    #     return cmds.renderWindowEditor('renderView', e=True, writeImage=img_path)
