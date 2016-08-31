#*************************************************************
# title         project settings
#
# content       paths & name conventions
#				settings for task, type, software, path, user
#
# author        Alexander Richter 
# email         contact@richteralexander.com
#*************************************************************

import os

#************************
# SETTINGS
#************************
PROJECT_NAME    = "arProject"
RESOLUTION      = [2048, 872]
FPS             = "24"
FPS_TYPE        = "film"

PATH_SHORT      = "M:"
PATH_LONG       = "//bigfoot/mpi"


#************************
# VARIABLES
#************************
MAYA_VERSION    = "2015"
NUKE_VERSION    = "v9.07"
HOUDINI_VERSION = "14.0.361"

RENDERER = {
    "maya"     : "renderman",
    "houdini"  : "mantra"
}


#************************
# ADMIN
#************************
TEAM  = {
    "admin"     : ["arichter"]
}


#************************
# CONTROL GROUPS
#************************
# no DIR in between: e.g. ASSETS/char
TYPE_DIRECT = [TYPE["rnd"], TYPE["assets"], TYPE["shots"]]


#************************
# FORMAT
#************************
FILE_FORMAT = {
    "maya"      : ".mb",
    "nuke"      : ".nk",
    "texture"   : ".tiff",
    "rendering" : ".exr",
    "thumbs"    : ".jpg",
    "img"       : ".png",
    "data"      : ".json",
    "playblast" : ".mov"
}


#************************
# PATH
#************************
PATH_SETTINGS   = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
PATH_PIPELINE   = os.path.dirname(PATH_SETTINGS)
PATH_PROJECT    = os.path.dirname(PATH_PIPELINE)
PATH_SOFTWARE   = PATH_SETTINGS + "/" + "software"

PATH_MAYA       = PATH_SOFTWARE + "/maya"
PATH_NUKE       = PATH_SOFTWARE + "/nuke"
PATH_HOUDINI    = PATH_SOFTWARE + "/houdini"


PATH = {
    "project"           : PATH_PROJECT,
    "pipeline"          : PATH_PIPELINE,
    "software"          : PATH_SOFTWARE,
    "settings"          : PATH_SETTINGS,

    "pipeline_work"     : PATH_PIPELINE + "/" + STATUS["work"],
    "pipeline_publish"  : PATH_PIPELINE + "/" + STATUS["publish"],
    
    "user"              : PATH_PROJECT + "/00_user",

    "footage"           : PATH_PROJECT + "/10_footage",
    "footage_hdri"      : PATH_PROJECT + "/10_footage/hdri",
    "footage_shader"    : PATH_PROJECT + "/10_footage/shader",
    "footage_scene"     : PATH_PROJECT + "/10_footage/scene",
    "footage_textures"  : PATH_PROJECT + "/10_footage/textures",

    "preproduction"     : PATH_PROJECT + "/20_preproduction",
    "rnd"               : PATH_PROJECT + "/25_rnd",
    
    "assets"            : PATH_PROJECT + "/30_assets",
    # "assets_char"       : PATH_PROJECT + "/30_assets/" + TYPE_ASSETS["character"],
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
}


PATH_EXTRA = {
    "scene_shd"         : PATH["footage_scene"] + "/" + RENDERER["maya"] + "_SHD/" + STATUS["publish"] + "/" + RENDERER["maya"] + "_SHD.mb",
    "img_tmp"           : PATH["data_user"] + "/" + os.getenv('username') + "/saveImg" + FILE_FORMAT["thumbs"],
    "preferences"       : PATH["data_user"] + "/" + os.getenv('username') + "/settings_" + os.getenv('username') + FILE_FORMAT["data"]
}


PATH_EXTRA_LOAD = {
    "alembic"           : PATH["shots_alembic"] 
}



#************************
# BATCH
#************************
BATCH = {
    "maya_work"      : PATH["pipeline_work"]    + "/software/maya.bat", 
    "maya_publish"   : PATH["pipeline_publish"] + "/software/maya.bat",     
    "nuke_work"      : PATH["pipeline_work"]    + "/software/nuke.bat", 
    "nuke_publish"   : PATH["pipeline_publish"] + "/software/nuke.bat", 
    "houdini_work"   : PATH["pipeline_work"]    + "/software/houdini.bat", 
    "houdini_publish": PATH["pipeline_publish"] + "/software/houdini.bat" 
}
