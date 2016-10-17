#*************************************************************
# CONTENT       SET default environment path
#
# DEPENDENCIES  MASTER pipeline path
#
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
# DELETE ******************
import sys
sys.path.append("..\settings")
import setEnv
setEnv.SetEnv()
class GetDefault(object):
    #************************
    # WORK & PUBLISH
    STATUS = {
        "work"    : "WORK",
        "publish" : "PUBLISH",

        "render"  : "images",
        "thumbs"  : "thumbs",
        "history" : "_history"
    }


    #************************
    # TYPE
    TYPE = {
        "assets" : "ASSETS",
        "shots"  : "SHOTS"
    }

    TYPE_ASSETS = {
        "character" : "char",
        "prop"      : "prop",
        "set"       : "set",
        "fx"        : "fx"
    }


    #************************
    # CONTROL GROUPS
    # no DIR in between: e.g. ASSETS/char
    TYPE_DIRECT  = [TYPE["assets"], TYPE["shots"]]
    ENVIRON_PATH = ["_PATH", "_MASTER_PATH"]


    #************************
    # TASK
    TASK_TYPE = {
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
    }

    TASK = {}
    TASK.update(TASK_TYPE[TYPE["assets"]])
    TASK.update(TASK_TYPE[TYPE["shots"]])

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

    TASK_FOLDER = {}

    TASK_FOLDER.update(TASK_ASSETS_FOLDER)
    TASK_FOLDER.update(TASK_SHOTS_FOLDER)

    FILE_FORMAT_LOAD = {
        "maya"      : [".mb", ".ma", ".abc"], #, ".fbx", ".obj"],
        "texture"   : [".ptx", ".tif", ".exr"]
    }

    FILE_FORMAT_REF = {
        "maya"      : [".abc", ".fbx", ".obj"],
        "texture"   : [".ptx", ".tif", ".exr"]
    }


    #************************
    # SOFTWARE
    # PROGRAM_FILES = os.environ["ProgramFiles"] # "C:/Program Files"

    # SOFTWARE = {
    #     "maya"      : PROGRAM_FILES + "/Autodesk/Maya" + MAYA_VERSION + "/bin/maya.exe",
    #     "nuke"      : PROGRAM_FILES + "/Nuke" + NUKE_VERSION + "/Nuke9.0.exe",
    #     "houdini"   : PROGRAM_FILES + "/Side Effects Software/Houdini " + HOUDINI_VERSION + "/bin/houdinifx.exe",
    #     "rv"        : PROGRAM_FILES + "/Tweak/RV/bin/rv.exe",
    #     "ptxview"   : PATH["maya_plugins_renderman"] + "/rmantree/bin/ptxview"
    # }


    #************************
    # FORMAT
    FILE_FORMAT = {
        "maya"      : ".mb",
        "nuke"      : ".nk",
        "texture"   : ".tiff",
        "rendering" : ".exr",
        "thumbs"    : ".jpg",
        "img"       : ".png",
        "data"      : ".yml",
        "playblast" : ".mov"
    }


    FILE_FORMAT_CODE = {
        ".ma"  : "mayaAscii",
        ".mb"  : "mayaBinary",
        ".obj" : "OBJ",
        ".abc" : "Alembic",
        ".nk"  : "nuke",
        ".tif" : "tiff",
        ".exr" : "openExr",
        ".avi" : "avi",
        ".jpg" : "jpeg"
    }


    #************************
    # NAMING CONVENTION
    # shot      : s000 - s + 3digits (first)
    # shotName  : shotName - after shotNr (maybe)
    # assets    : assetname (first)
    # taks      : task in TASK_TYPE[kategory].keys()
    # version   : v + 3 digits
    # user      : 2 alphanumerics
    # comment   : last (maybe)


    #************************
    # NAMING CONVENTION
    CONVENTION = {
        "shot"  : "<shotnr>_<name>_<task>_<version>_<artist>_<comment>",
        "asset" : "<name>_<task>_<version>_<artist>_<comment>"
    }

    CONVENTION_EXAMPLE = {
        "shot"  : "s010_shotName" + TASK["lighting"] + "_v001_ar_comment",
        "asset" : "name_" + TASK["shading"] + "_v001_ar_comment"
    }


    #************************
    # BATCH = {
    #     "maya_work"      : PATH["pipeline_work"]    + "/software/maya.bat",
    #     "maya_publish"   : PATH["pipeline_publish"] + "/software/maya.bat",
    #     "nuke_work"      : PATH["pipeline_work"]    + "/software/nuke.bat",
    #     "nuke_publish"   : PATH["pipeline_publish"] + "/software/nuke.bat",
    #     "houdini_work"   : PATH["pipeline_work"]    + "/software/houdini.bat",
    #     "houdini_publish": PATH["pipeline_publish"] + "/software/houdini.bat"
    # }

    PROJECT_PATH = ("\n").join([os.environ["PROJECT_PATH"],
        os.environ["PIPELINE_PATH"],

        os.environ["DATA_PATH"],
        os.environ["IMG_PATH"],
        os.environ["LIBRARY_PATH"],
        os.environ["SETTINGS_PATH"],
        os.environ["SOFTWARE_PATH"],

        os.environ["PIPELINE_MASTER_PATH"],

        os.environ["DATA_MASTER_PATH"],
        os.environ["IMG_MASTER_PATH"],
        os.environ["LIBRARY_MASTER_PATH"],
        os.environ["SETTINGS_MASTER_PATH"],
        os.environ["SOFTWARE_MASTER_PATH"]])


    #************************
    REPORT_LIST = {
        "report"    : ["Bug", "Suggestion"],
        "maya"      : ["arSave", "arLoad", "Reference SHD_SCENE", "Combine SHD and Model", "arAlembicExport", "Alembic Import", "arReport", "other"],
        "nuke"      : ["arSave", "arLoad", "arWrite", "rrSubmit", "Renderthreads", "arReport", "other"],
        "houdini"   : ["arSave", "arLoad", "arReport", "other"],
        "other"     : ["arSave", "arLoad", "arReport", "other"]
    }


    #************************
    LINK = {
        "pipeline"  : "https://www.filmakademie.de/wiki/display/AISPD/arPipeline",
        "software"  : "https://www.filmakademie.de/wiki/display/AISPD/arPipeline+%7C+Basics",

        "maya"      : "https://www.filmakademie.de/wiki/display/AISPD/arPipeline+%7C+Maya",
        "nuke"      : "https://www.filmakademie.de/wiki/display/AISPD/arPipeline+%7C+Nuke",
        "houdini"   : "https://www.filmakademie.de/wiki/display/AISPD/arPipeline+%7C+Houdini",

        "nope"      : "https://www.youtube.com/watch?v=p2NJH8VTDOg",

        "website"   : "www.richteralexander.com"
    }
