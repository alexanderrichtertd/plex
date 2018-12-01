#*********************************************************************
# content   = menu 3Ds Max
# version   = 0.0.1
# date      = 2018-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os

import MaxPlus

import libFunc

def open_scene_folder():
    libFunc.open_folder(MaxPlus.Core.EvalMAXScript("sceneName = maxFilePath + maxFileName").Get())

def open_project_folder():
    libFunc.open_folder(os.getenv("PROJECT_PATH"))

def save():
    import arSave
    arSave.start()

def load():
    import arLoad
    arLoad.start()

def get_report():
    libFunc.get_help('issues')

def get_help():
    libFunc.get_help()
