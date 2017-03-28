#*************************************************************
# CONTENT       paths & name conventions
#               settings for task, type, software, path, user
#
# EMAIL         contact@richteralexander.com
#*************************************************************

import os

import getDefault
DEFAULT = getDefault.GetDefault()

# DELETE **********************
from setEnv import SetEnv
SetEnv()
# *****************************

class GetProject(getDefault.GetDefault):

    PROJECT_NAME = "arPipeline"     # REPLACE
    PROJECT_PATH = "D:/arPipeline"  # REPLACE

    RESOLUTION   = [2048, 872]
    FPS          = "24"
    FPS_TYPE     = "film"

    MAYA_VERSION    = "2015"
    NUKE_VERSION    = "9.07"
    HOUDINI_VERISON = "15.56"

    #************************
    # ADMIN
    TEAM  = {
        "all"       : "*",
        "admin"     : ["arichter", "Alex"],
        "core"      : ["arichter"]
    }

    #************************
    # PATH
    PIPELINE_PATH = os.environ["PIPELINE_PATH"]
    SETTINGS_PATH = os.environ["SETTINGS_PATH"]

    IMG_PATH      = os.environ["IMG_PATH"]
    DATA_PATH     = os.environ["DATA_PATH"]
    LIB_PATH      = os.environ["LIB_PATH"]
    SOFTWARE_PATH = os.environ["SOFTWARE_PATH"]

    PATH = {
        "project"           : PROJECT_PATH,
        "pipeline"          : PIPELINE_PATH,
        "settings"          : SETTINGS_PATH,

        # "pipeline_work"     : PIPELINE_PATH + "/" + self.STATUS["work"],
        # "pipeline_publish"  : PIPELINE_PATH + "/" + self.STATUS["publish"],

        "img"               : IMG_PATH,
        "img_btn"           : IMG_PATH + "/btn",
        "img_gif"           : IMG_PATH + "/gif",
        "img_placeholder"   : IMG_PATH + "/placeholder",
        "img_software"      : IMG_PATH + "/software",
        "img_program"       : IMG_PATH + "/program",
        "img_user"          : IMG_PATH + "/user",

        "img_maya"          : IMG_PATH + "/software/maya",
        "img_maya_shelf"    : IMG_PATH + "/software/maya/shelf",

        "img_nuke"          : IMG_PATH + "/software/nuke",
        "img_nuke_menu"     : IMG_PATH + "/software/nuke/menu",
        "img_nuke_banner"   : IMG_PATH + "/software/nuke/banner",

        "lib"               : LIB_PATH,
        "lib_helper"        : LIB_PATH + "/helper",
        "lib_default"       : LIB_PATH + "/default",

        "data"              : DATA_PATH,
        "data_user"         : DATA_PATH + "/user",
        "data_shots"        : DATA_PATH + "/shots", # backup for GoogleDocs
        "data_report"       : DATA_PATH + "/report",
        "data_report_img"   : DATA_PATH + "/report/img",
        #"data_report_history" : DATA_PATH + "/report/" + STATUS["history"],
        "data_log"          : DATA_PATH + "/log",
        "data_reminder"     : DATA_PATH + "/reminder",
        "data_local"        : ("/").join([os.path.expanduser('~'), "pipeline_debug.log"]).replace("/","\\"),

        "user"              : PROJECT_PATH + "/00_user",

        "footage"           : PROJECT_PATH + "/10_footage",
        "footage_hdri"      : PROJECT_PATH + "/10_footage/hdri",
        "footage_shader"    : PROJECT_PATH + "/10_footage/shader",
        "footage_scene"     : PROJECT_PATH + "/10_footage/scene",
        "footage_textures"  : PROJECT_PATH + "/10_footage/textures",

        "preproduction"     : PROJECT_PATH + "/20_pre",
        "rnd"               : PROJECT_PATH + "/25_rnd",

        "assets"            : PROJECT_PATH + "/30_assets",
        # "assets_char"       : PROJECT_PATH + "/30_assets/" + TYPE_ASSETS["char"],
        # "assets_prop"       : PROJECT_PATH + "/30_assets/" + TYPE_ASSETS["prop"],
        # "assets_set"        : PROJECT_PATH + "/30_assets/" + TYPE_ASSETS["set"],
        # "assets_fx"         : PROJECT_PATH + "/30_assets/" + TYPE_ASSETS["fx"],

        "shots"             : PROJECT_PATH + "/40_shots",
        "post"              : PROJECT_PATH + "/40_shots",
        "shots_alembic"     : PROJECT_PATH + "/40_shots/s000_ALEMBIC/40_ANIM/WORK",
        "render"            : PROJECT_PATH + "/45_render",

        "comp"              : PROJECT_PATH + "/40_shots",

        "edit"              : PROJECT_PATH + "/50_edit",
        "edt_cut"           : PROJECT_PATH + "/50_edit/_cut",
        "edit_music"        : PROJECT_PATH + "/50_edit/_music",
        "edit_sound"        : PROJECT_PATH + "/50_edit/_sound",
        "final"             : PROJECT_PATH + "/50_edit/FINAL",

        "software"          : SOFTWARE_PATH,
        "ui"                : SOFTWARE_PATH + "/_ui",
        "utilities"         : SOFTWARE_PATH + "/utilities",

        "maya"              : SOFTWARE_PATH + "/maya",
        "maya_scripts"      : SOFTWARE_PATH + "/maya/scripts",
        "maya_plugins"      : SOFTWARE_PATH + "/maya/plugins",
        "maya_plugins_arnold"   : SOFTWARE_PATH + "/maya/plugins/arnold/", #+ MAYA_VERSION,
        "maya_plugins_renderman": SOFTWARE_PATH + "/maya/plugins/renderman/" + "RenderManStudio-20.9-maya2015",

        "nuke"              : SOFTWARE_PATH + "/nuke",
        "nuke_scripts"      : SOFTWARE_PATH + "/nuke/scripts",
        "nuke_plugins"      : SOFTWARE_PATH + "/nuke/plugins",
        "nuke_gizmos"       : SOFTWARE_PATH + "/nuke/gizmos",
        "nuke_gizmos_menu"  : SOFTWARE_PATH + "/nuke/gizmos/menu",

        "houdini"           : SOFTWARE_PATH + "/houdini",
        "houdini_plugins"   : SOFTWARE_PATH + "/houdini/plugins",
        "houdini_scripts"   : SOFTWARE_PATH + "/houdini/scripts"
        # "houdini_arnold"    : SOFTWARE_PATH + "/houdini/plugins/arnold",}
    }

    PATH_EXTRA = {
        #"scene_shd"         : ("/").join([PATH["footage_scene"], RENDERER["maya"] + "_SHD", STATUS["publish"], GetProject().RENDERER["maya"] + "_SHD.mb"]),
        "img_tmp"           : os.path.expanduser("~") + "temp"
        #"preferences"       : ("/").join([PATH["data_user"], os.getenv('username'), "settings_" + os.getenv('username') + FILE_FORMAT["data"]])
    }

    # PATH_EXTRA_LOAD = {
    #     "alembic"           : PATH["shots_alembic"]
    # }
