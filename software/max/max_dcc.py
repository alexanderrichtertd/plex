#*********************************************************************
# content   = 3ds Max
# version   = 0.1.0
# date      = 2019-10-06
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os

import MaxPlus

from tank import Tank
from software import Software


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
# CLASS
class Max(Software):

    _NAME = 'max'

    @property
    def scene_path(self):
        return MaxPlus.Core.EvalMAXScript("maxFilePath + maxFileName").Get()

    def scene_save(self):
        return MaxPlus.FileManager.Save()

    def scene_save_as(self, file, setup_scene=False):
        return MaxPlus.FileManager.Save(file)

    def scene_open(self, file):
        return MaxPlus.FileManager.Open(file)

    def scene_import(self, file):
        pass
