#*********************************************************************
# content   = menu 3Ds Max
# version   = 0.1.0
# date      = 2019-10-06
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os

import MaxPlus

import pipefunc


#*********************************************************************
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
