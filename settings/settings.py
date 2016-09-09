#*************************************************************
# title         settings
#
# content       paths & name conventions
#               settings for task, type, software, path, user
#
# author        Alexander Richter 
# email         contact@richteralexander.com
#*************************************************************

import os

#************************
# SETTINGS
#************************
PROJECT_NAME    = "arPipeline"
RESOLUTION      = [2048, 872]
FPS             = "24"
FPS_TYPE        = "film"

RENDERER = {
    "maya"     : "renderman",
    "houdini"  : "mantra"
}


#************************
# VARIABLES
#************************
# MAYA_VERSION    = "2015"
# NUKE_VERSION    = "v9.07"
# HOUDINI_VERSION = "14.0.361"

PROGRAM_FILES   = os.environ["ProgramFiles"] # "C:/Program Files"

PATH_SHORT      = "M:"
PATH_LONG       = "//bigfoot/mpi"


#************************
# ADMIN
#************************
TEAM  = {
    "all"       : "*",
    "admin"     : ["arichter"],
    "core"      : ["arichter"]
}


#************************
# WORK & PUBLISH
#************************
STATUS = {
    "work"      : "WORK",
    "publish"   : "PUBLISH",
    "render"    : "images",
    "thumbs"    : "thumbs",
    "history"   : "_history"
}


#************************
# TYPE
#************************
TYPE = {
    "rnd"    : "RND",
    "assets" : "ASSETS",
    "shots"  : "SHOTS"
    #"post"   : "POST"
}


TYPE_ASSETS = {
    "character" : "char",
    "prop"      : "prop",
    "set"       : "set",
    "fx"        : "fx"
}


#************************
# CONTROL GROUPS
#************************
# no DIR in between: e.g. ASSETS/char
TYPE_DIRECT = [TYPE["rnd"], TYPE["assets"], TYPE["shots"]]


#************************
# TASK
#************************
TASK_TYPE = { 
    TYPE["rnd"] :      {"groom"         : "GROOM",
                        "animation"     : "ANIM",
                        "lighting"      : "LIGHT",
                        "fx"            : "FX"},

    TYPE["assets"]:    {"photoscan"     : "SCAN",
                        "modeling"      : "MODEL",
                        "groom"         : "GROOM",
                        "texturing"     : "TEX",
                        "shading"       : "SHD",
                        "rigging"       : "RIG",
                        "muscle"        : "MUSCLE"},

    TYPE["shots"] :    {"plate"         : "PLATE",
                        "track"         : "TRACK",
                        "animation"     : "ANIM",
                        "fx"            : "FX",
                        "lighting"      : "LIGHT",
                        "rendering"     : "RENDER",
                        "compositing"   : "COMP"},

    "POST" :           {"editing"       : "EDIT",
                        "cut"           : "CUT",
                        "final"         : "FINAL"}
}


TASK = {}
TASK.update(TASK_TYPE[TYPE["rnd"]])
TASK.update(TASK_TYPE[TYPE["assets"]])
TASK.update(TASK_TYPE[TYPE["shots"]])
TASK.update(TASK_TYPE["POST"])


TASK_DEFAULT_FOLDER = {  
    #"photoscan"     : "00_" + TASK["photoscan"],
    "modeling"      : "10_" + TASK["modeling"],
    "groom"         : "15_" + TASK["groom"],
    "animation"     : "20_" + TASK["animation"],
    "shading"       : "30_" + TASK["shading"],
    "lighting"      : "40_" + TASK["lighting"],
    "muscle"        : "50_" + TASK["muscle"]
}


TASK_ASSETS_FOLDER = {  
    #"photoscan"     : "00_" + TASK["photoscan"],
    "modeling"      : "10_" + TASK["modeling"],
    "groom"         : "15_" + TASK["groom"],
    "texturing"     : "20_" + TASK["texturing"],
    "shading"       : "30_" + TASK["shading"],
    "rigging"       : "40_" + TASK["rigging"],
    "muscle"        : "50_" + TASK["muscle"]
}


TASK_SHOTS_FOLDER = {   
    #"plate"         : "00_" + TASK["plate"],
    #"track"         : "10_" + TASK["track"],
    "animation"     : "20_" + TASK["animation"],
    "fx"            : "30_" + TASK["fx"],
    "lighting"      : "40_" + TASK["lighting"],
    "rendering"     : "50_" + TASK["rendering"],
    "compositing"   : "60_" + TASK["compositing"]
}


TASK_FOLDER = {  
    "editing"       : "30_" + TASK["editing"], 
    "cut"           : "30_" + TASK["cut"],  
    "final"         : "40_" + TASK["final"]  
}


TASK_FOLDER.update(TASK_ASSETS_FOLDER)
TASK_FOLDER.update(TASK_SHOTS_FOLDER)


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


FILE_FORMAT_CODE = {
    ".ma"        : "mayaAscii",
    ".mb"        : "mayaBinary",
    ".obj"       : "OBJ",
    ".abc"       : "Alembic",
    ".nk"        : "nuke",
    ".tif"       : "tiff",
    ".exr"       : "openExr",
    ".avi"       : "avi",
    ".jpg"       : "jpeg"
}


FILE_FORMAT_LOAD = {
    "maya"      : [".mb", ".ma", ".abc"], #, ".fbx", ".obj"],
    "texture"   : [".ptx", ".tif", ".exr"]
}


FILE_FORMAT_REF = {
    "maya"      : [".abc", ".fbx", ".obj"],
    "texture"   : [".ptx", ".tif", ".exr"]
}


#************************
# PATH
#************************
PATH_SETTINGS   = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
PATH_PIPELINE   = (os.path.dirname(PATH_SETTINGS))
PATH_PROJECT    = os.path.dirname(PATH_PIPELINE)
PATH_SOFTWARE   = PATH_PIPELINE + "/" + "software"


PATH = {
    "project"           : PATH_PROJECT,
    "pipeline"          : PATH_PIPELINE,
    "software"          : PATH_SOFTWARE,
    "settings"          : PATH_SETTINGS,

    "pipeline_work"     : PATH_PIPELINE + "/" + STATUS["work"],
    "pipeline_publish"  : PATH_PIPELINE + "/" + STATUS["publish"],
    
    "utilities"         : PATH_SETTINGS + "/utilities",

    "img"               : PATH_SETTINGS + "/img",
    "img_banner"        : PATH_SETTINGS + "/img/banner",
    "img_btn"           : PATH_SETTINGS + "/img/btn",
    "img_gif"           : PATH_SETTINGS + "/img/gif",
    "img_placeholder"   : PATH_SETTINGS + "/img/placeholder",
    "img_software"      : PATH_SETTINGS + "/img/software",
    "img_program"       : PATH_SETTINGS + "/img/program",
    "img_user"          : PATH_SETTINGS + "/img/user",

    "img_maya"          : PATH_SETTINGS + "/img/software/maya",
    "img_maya_shelf"    : PATH_SETTINGS + "/img/software/maya/shelf",

    "img_nuke"          : PATH_SETTINGS + "/img/software/nuke",
    "img_nuke_menu"     : PATH_SETTINGS + "/img/software/nuke/menu",
    "img_nuke_banner"   : PATH_SETTINGS + "/img/software/nuke/banner",

    "lib"               : PATH_SETTINGS + "/lib",
    "lib_helper"        : PATH_SETTINGS + "/lib/helper",
    "lib_default"       : PATH_SETTINGS + "/lib/default",
    
    "data"              : PATH_SETTINGS + "/data",
    "data_user"         : PATH_SETTINGS + "/data/user",
    "data_shots"        : PATH_SETTINGS + "/data/shots", # backup for GoogleDocs
    "data_report"       : PATH_SETTINGS + "/data/report",
    "data_report_img"   : PATH_SETTINGS + "/data/report/img",
    "data_report_history" : PATH_SETTINGS + "/data/report/" + STATUS["history"],
    "data_log"          : PATH_SETTINGS + "/data/log",
    "data_reminder"     : PATH_SETTINGS + "/data/reminder",

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

    "maya"              : PATH_SOFTWARE + "/maya",
    "maya_scripts"      : PATH_SOFTWARE + "/maya/scripts",   
    "maya_plugins"      : PATH_SOFTWARE + "/maya/plugins",
    "maya_plugins_arnold"   : PATH_SOFTWARE + "/maya/plugins/arnold/" + MAYA_VERSION,
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
    "scene_shd"         : PATH["footage_scene"] + "/" + RENDERER["maya"] + "_SHD/" + STATUS["publish"] + "/" + RENDERER["maya"] + "_SHD.mb",
    "img_tmp"           : PATH["data_user"] + "/" + os.getenv('username') + "/saveImg" + FILE_FORMAT["thumbs"],
    "preferences"       : PATH["data_user"] + "/" + os.getenv('username') + "/settings_" + os.getenv('username') + FILE_FORMAT["data"]
}


PATH_EXTRA_LOAD = {
    "alembic"           : PATH["shots_alembic"] 
}


#************************
# SOFTWARE
#************************
SOFTWARE = {
    "maya"      : PROGRAM_FILES + "/Autodesk/Maya" + MAYA_VERSION + "/bin/maya.exe",
    "nuke"      : PROGRAM_FILES + "/Nuke" + NUKE_VERSION + "/Nuke9.0.exe",
    "houdini"   : PROGRAM_FILES + "/Side Effects Software/Houdini " + HOUDINI_VERSION + "/bin/houdinifx.exe",
    "rv"        : PROGRAM_FILES + "/Tweak/RV/bin/rv.exe",
    "ptxview"   : PATH["maya_plugins_renderman"] + "/rmantree/bin/ptxview"
}


#************************
# PLACEHOLDER
#************************
PLACEHOLDER = {
    "shot"      : PATH["img_placeholder"] + "/shot" + FILE_FORMAT["img"], 
    "user"      : PATH["img_placeholder"] + "/user" + FILE_FORMAT["img"], 
    "report"    : PATH["img_placeholder"] + "/report" + FILE_FORMAT["img"], 
    "image"     : PATH["img_placeholder"] + "/image" + FILE_FORMAT["img"], 
    "program"   : PATH["img_placeholder"] + "/program" + FILE_FORMAT["img"], 
    "banner"    : PATH["img_placeholder"] + "/banner" + FILE_FORMAT["img"]
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


#************************
# NAMING CONVENTION
#************************
# shot      : s000 - s + 3digits (first)
# shotName  : shotName - after shotNr (maybe)
# assets    : assetname (first)
# taks      : task in TASK_TYPE[kategory].keys()
# version   : v + 3 digits
# user      : 2 alphanumerics
# comment   : last (maybe)


CONVENTION = {
    "rnd"    : "s010_shotName" + TASK["lighting"] + "_v001_ar_comment",
    "shots"  : "s010_shotName" + TASK["lighting"] + "_v001_ar_comment",
    "assets" : "name_" + TASK["shading"] + "_v001_ar_comment"
}


#************************
# REPORT
#************************
REPORT_LIST = {
    "report"    : ["Bug", "Suggestion"],
    "maya"      : ["arSave", "arLoad", "Reference SHD_SCENE", "Combine SHD and Model", "arAlembicExport", "Alembic Import", "arReport", "other"],
    "nuke"      : ["arSave", "arLoad", "arWrite", "rrSubmit", "Renderthreads", "arReport", "other"],
    "houdini"   : ["arSave", "arLoad", "arReport", "other"],
    "other"     : ["arSave", "arLoad", "arReport", "other"]
}


#************************
# LINK
#************************
LINK = {
    "website"   : "https://www.richteralexander.com",

    "pipeline"  : "https://www.filmakademie.de/wiki/display/AISPD/arPipeline", 
    "software"  : "https://www.filmakademie.de/wiki/display/AISPD/arPipeline+%7C+Basics",
    
    "maya"      : "https://www.filmakademie.de/wiki/display/AISPD/arPipeline+%7C+Maya",
    "nuke"      : "https://www.filmakademie.de/wiki/display/AISPD/arPipeline+%7C+Nuke",
    "houdini"   : "https://www.filmakademie.de/wiki/display/AISPD/arPipeline+%7C+Houdini",
    
    "nope"      : "https://www.youtube.com/watch?v=p2NJH8VTDOg"
}