# content   = 3ds Max
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os

import MaxPlus

import plexfunc
from plex import Plex
from software import Software

LOG = Plex().log(script=__name__)


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


    # MENU ***************************************************************
    def open_scene_folder():
        plexfunc.open_dir(MaxPlus.Core.EvalMAXScript("sceneName = maxFilePath + maxFileName").Get())

    def open_project_folder():
        plexfunc.open_dir(os.getenv("PROJECT_PATH"))

    def save():
        import arSave
        arSave.start()

    def load():
        import arLoad
        arLoad.start()

    def get_report():
        Plex().help('report')

    def get_help():
        Plex().help()
