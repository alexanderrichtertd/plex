#*********************************************************************
# content   = Maya
# version   = 0.1.0
# date      = 2019-12-01
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os
import sys
import getpass
import subprocess

import maya.mel as mel
import pymel.core as pm

import pipefunc

import tank
from tank import Tank
from classes import software


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
# CLASS
class Maya(software, tank.Singleton):

    @property
    def scene_path(self):
        return pm.sceneName()

    def scene_save(self):
        return pm.saveFile(file)


    def scene_save_as(self, file, setup_scene=False):
        if setup_scene: self.scene_setup(file)
        return pm.saveAs(file)

    def scene_open(self, file):
        return pm.openFile(file, force=True)

    def scene_import(self, file):
        pass

        # # reference or open
        # if ref or ".abc" in self.save_dir or ".obj" in self.save_dir or ".fbx" in self.save_dir:
        #     # file -r -type "mayaBinary"  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "bull_MODEL_v004_jo" -options "v=0;" "K:/30_assets/bull/10_MODEL/WORK/bull_MODEL_v004_jo.mb";
        #     mel.eval('file -r -type "' + s.FILE_FORMAT_CODE["." + self.save_dir.split(".")[-1]] + '" -ignoreVersion -gl -mergeNamespacesOnClash false "' + self.save_dir.replace("\\", "/") + '"')

    def scene_setup(self, file):
        import maya_utils
        maya_utils.setup_scene(file)

