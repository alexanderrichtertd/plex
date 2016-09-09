

import os
 # MAYA


class MayaPaths(default):
    def __init__(self):and
        super()
        
        os.environ["SOFTWARE"]     = maya
        os.environ["VERSION_MAYA"] = 2015
        
        # ------------------
        # PATH
        pathMaya         = PATH_SOFTWARE + "/maya"

        pathScript       = SOFTWARE_PATH + "/scripts"
        pathPlugins      = SOFTWARE_PATH + "/plugins"
        pathArnold       = PLUGINS_PATH + "/arnold"
        pathArnoldShader = ARNOLD_PATH + "/alShader"



        # ------------------
        # SCRIPT
        MAYA_SCRIPT_PATH = pathScript/ANIM;MAYA_SCRIPT_PATH
        MAYA_SCRIPT_PATH = PLUGINS_PATH/arctracker;MAYA_SCRIPT_PATH
        MAYA_SCRIPT_PATH = PLUGINS_PATH/tweenmachine;MAYA_SCRIPT_PATH


        # ------------------
        # PYTHON
        PYTHONPATH = STATUS_PATH;PYTHONPATH
        PYTHONPATH = SOFTWARE_PATH;PYTHONPATH
        PYTHONPATH = PIPELINE_PATH;PYTHONPATH
        PYTHONPATH = LIBRARY_PATH;PYTHONPATH
        PYTHONPATH = PLUGINS_PATH + "/ngskintools/scripts;PYTHONPATH"


        # ------------------
        # PLUGIN
        MAYA_PLUG_IN_PATH = PLUGINS_PATH;MAYA_PLUG_IN_PATH;
        MAYA_PLUG_IN_PATH = PLUGINS_PATH/ngskintools/plug-ins;MAYA_PLUG_IN_PATH;
        # MAYA_PLUG_IN_PATH = PLUGINS_PATH/SOuP/plug-ins/win_maya2015;MAYA_PLUG_IN_PATH


        # ------------------
        # SHELF
        # --- MAYA_SHELF_PATH = PLUGINS_PATH/SOuP/shelves;MAYA_SHELF_PATH
        MAYA_SHELF_PATH = SOFTWARE_PATH/shelf;MAYA_SHELF_PATH


        # ------------------
        # ICON
        XBMLANGPATH = PLUGINS_PATH/SOuP/icons;BXBMLANGPATH


        # ------------------
        # ARNOLD
        MtoA = ARNOLD_PATH/MAYA_VERSION
        MAYA_MODULE_PATH = MtoA;MAYA_MODULE_PATH
        PATH = MtoA/bin;PATH
        ARNOLD_PLUGIN_PATH  = MtoA/shaders;ARNOLD_PLUGIN_PATH;ARNOLD_PLUGIN_PATH
        ARNOLD_PLUGIN_PATH  = ARNOLD_PATH/bin;ARNOLD_PLUGIN_PATH;ARNOLD_PLUGIN_PATH
        ARNOLD_PLUGIN_PATH  = ARNOLD_SHADER_PATH/bin;ARNOLD_PLUGIN_PATH
        MTOA_TEMPLATES_PATH = ARNOLD_SHADER_PATH/ae;MTOA_TEMPLATES_PATH

        ARNOLD_LICENSE_HOST = blue


        # ------------------
        # RENDERMAN
        RM = "PLUGINS_PATH/renderman/RenderManStudio-20.9-maya" + os.environ["VERSION_MAYA"]
        MAYA_MODULE_PATH = "RM/etc;MAYA_MODULE_PATH"
        RMSTREE = RM
        PATH = RM/bin;PATH


        # ------------------
        # DISABLE REPORT
        MAYA_DISABLE_CIP = 1
        MAYA_DISABLE_CER = 1


        # ------------------
        # --- MayaEnvVars ---
        # MAYA_PROJECT = PROJECT_ROOT/2_production
        # cd MAYA_PROJECT


        # ------------------
        # SPLASHSCREEN
        # File: MayaEDUStartupImage.png
        XBMLANGPATH = IMG_PATH;XBMLANGPATH


        # ------------------
        # CALL MAYA
        MAYA_DIR = C:/Program Files/Autodesk/os.environ["VERSION_MAYA"]
        PATH = MAYA_DIR/bin;PATH
