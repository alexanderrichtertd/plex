#*********************************************************************
# content   = menu 3Ds Max
# date      = 2020-06-19
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os

import MaxPlus


#*********************************************************************
def open_scene_folder():
    Tank().open_folder(MaxPlus.Core.EvalMAXScript("sceneName = maxFilePath + maxFileName").Get())

def open_project_folder():
    Tank().open_folder(os.getenv("PROJECT_PATH"))

def save():
    import arSave
    arSave.start()

def load():
    import arLoad
    arLoad.start()

def get_report():
    Tank().help('report')

def get_help():
    Tank().help()
