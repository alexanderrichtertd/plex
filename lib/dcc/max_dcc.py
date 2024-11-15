#*********************************************************************
# content   = 3ds Max
# version   = 0.1.0
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os

import MaxPlus

import pipefunc
from tank import Tank
from software import Software


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)


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


    #*********************************************************************
    # MENU
    def open_scene_folder():
        pipefunc.open_folder(MaxPlus.Core.EvalMAXScript("sceneName = maxFilePath + maxFileName").Get())

    def open_project_folder():
        pipefunc.open_folder(os.getenv("PROJECT_PATH"))

    def save():
        import arSave
        arSave.start()

    def load():
        import arLoad
        arLoad.start()

    def get_report():
        pipefunc.help('report')

    def get_help():
        pipefunc.help()
