#*********************************************************************
# content   = Maya
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

from tank import Tank
from software import Software


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)


#*********************************************************************
# CLASS
class Maya(Software):
    import maya.mel as mel
    import pymel.core as pm
    import maya.cmds as cmds

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
