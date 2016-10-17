#*************************************************************
# CONTENT       paths & name conventions
#               settings for task, type, software, path, user
#
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
from getDefault import GetDefault

# DELETE **********************
from setEnv import SetEnv
SetEnv()
# *****************************

class GetProject(GetDefault):

    PROJECT_NAME = "arPipeline"
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
    PATH_PROJECT  = os.environ["PROJECT_PATH"]
    PATH_PIPELINE = os.environ["PIPELINE_PATH"]
    PATH_SETTINGS = os.environ["SETTINGS_PATH"]

    PATH_IMG      = os.environ["IMG_PATH"]
    PATH_DATA     = os.environ["DATA_PATH"]
    PATH_LIBRARY  = os.environ["LIBRARY_PATH"]
    PATH_SOFTWARE = os.environ["SOFTWARE_PATH"]

    PATH = {
        "project"           : PATH_PROJECT,
        "pipeline"          : PATH_PIPELINE,
        "settings"          : PATH_SETTINGS,

        # "pipeline_work"     : PATH_PIPELINE + "/" + self.STATUS["work"],
        # "pipeline_publish"  : PATH_PIPELINE + "/" + self.STATUS["publish"],

        "img"               : PATH_IMG,
        "img_btn"           : PATH_IMG + "/btn",
        "img_gif"           : PATH_IMG + "/gif",
        "img_placeholder"   : PATH_IMG + "/placeholder",
        "img_software"      : PATH_IMG + "/software",
        "img_program"       : PATH_IMG + "/program",
        "img_user"          : PATH_IMG + "/user",

        "img_maya"          : PATH_IMG + "/software/maya",
        "img_maya_shelf"    : PATH_IMG + "/software/maya/shelf",

        "img_nuke"          : PATH_IMG + "/software/nuke",
        "img_nuke_menu"     : PATH_IMG + "/software/nuke/menu",
        "img_nuke_banner"   : PATH_IMG + "/software/nuke/banner",

        "lib"               : PATH_LIBRARY,
        "lib_helper"        : PATH_LIBRARY + "/helper",
        "lib_default"       : PATH_LIBRARY + "/default",

        "data"              : PATH_DATA,
        "data_user"         : PATH_DATA + "/user",
        "data_shots"        : PATH_DATA + "/shots", # backup for GoogleDocs
        "data_report"       : PATH_DATA + "/report",
        "data_report_img"   : PATH_DATA + "/report/img",
        #"data_report_history" : PATH_DATA + "/report/" + STATUS["history"],
        "data_log"          : PATH_DATA + "/log",
        "data_reminder"     : PATH_DATA + "/reminder",
        "data_local"        : ("/").join([os.path.expanduser('~'), "pipeline_debug.log"]).replace("/","\\"),

        "user"              : PATH_PROJECT + "/00_user",

        "footage"           : PATH_PROJECT + "/10_footage",
        "footage_hdri"      : PATH_PROJECT + "/10_footage/hdri",
        "footage_shader"    : PATH_PROJECT + "/10_footage/shader",
        "footage_scene"     : PATH_PROJECT + "/10_footage/scene",
        "footage_textures"  : PATH_PROJECT + "/10_footage/textures",

        "preproduction"     : PATH_PROJECT + "/20_pre",
        "rnd"               : PATH_PROJECT + "/25_rnd",

        "assets"            : PATH_PROJECT + "/30_assets",
        # "assets_char"       : PATH_PROJECT + "/30_assets/" + TYPE_ASSETS["char"],
        # "assets_prop"       : PATH_PROJECT + "/30_assets/" + TYPE_ASSETS["prop"],
        # "assets_set"        : PATH_PROJECT + "/30_assets/" + TYPE_ASSETS["set"],
        # "assets_fx"         : PATH_PROJECT + "/30_assets/" + TYPE_ASSETS["fx"],

        "shots"             : PATH_PROJECT + "/40_shots",
        "post"              : PATH_PROJECT + "/40_shots",
        "shots_alembic"     : PATH_PROJECT + "/40_shots/s000_ALEMBIC/40_ANIM/WORK",
        "render"            : PATH_PROJECT + "/45_render",

        "comp"              : PATH_PROJECT + "/40_shots",

        "edit"              : PATH_PROJECT + "/50_edit",
        "edt_cut"           : PATH_PROJECT + "/50_edit/_cut",
        "edit_music"        : PATH_PROJECT + "/50_edit/_music",
        "edit_sound"        : PATH_PROJECT + "/50_edit/_sound",
        "final"             : PATH_PROJECT + "/50_edit/FINAL",

        "software"          : PATH_SOFTWARE,
        "ui"                : PATH_SOFTWARE + "/_ui",
        "utilities"         : PATH_SOFTWARE + "/utilities",

        "maya"              : PATH_SOFTWARE + "/maya",
        "maya_scripts"      : PATH_SOFTWARE + "/maya/scripts",
        "maya_plugins"      : PATH_SOFTWARE + "/maya/plugins",
        "maya_plugins_arnold"   : PATH_SOFTWARE + "/maya/plugins/arnold/", #+ MAYA_VERSION,
        "maya_plugins_renderman": PATH_SOFTWARE + "/maya/plugins/renderman/" + "RenderManStudio-20.9-maya2015",

        "nuke"              : PATH_SOFTWARE + "/nuke",
        "nuke_scripts"      : PATH_SOFTWARE + "/nuke/scripts",
        "nuke_plugins"      : PATH_SOFTWARE + "/nuke/plugins",
        "nuke_gizmos"       : PATH_SOFTWARE + "/nuke/gizmos",
        "nuke_gizmos_menu"  : PATH_SOFTWARE + "/nuke/gizmos/menu",

        "houdini"           : PATH_SOFTWARE + "/houdini",
        "houdini_plugins"   : PATH_SOFTWARE + "/houdini/plugins",
        "houdini_scripts"   : PATH_SOFTWARE + "/houdini/scripts"
        # "houdini_arnold"    : PATH_SOFTWARE + "/houdini/plugins/arnold",}
    }

    PATH_EXTRA = {
        #"scene_shd"         : ("/").join([PATH["footage_scene"], RENDERER["maya"] + "_SHD", STATUS["publish"], GetProject().RENDERER["maya"] + "_SHD.mb"]),
        "img_tmp"           : os.path.expanduser("~") + "temp"
        #"preferences"       : ("/").join([PATH["data_user"], os.getenv('username'), "settings_" + os.getenv('username') + FILE_FORMAT["data"]])
    }

    # PATH_EXTRA_LOAD = {
    #     "alembic"           : PATH["shots_alembic"]
    # }
