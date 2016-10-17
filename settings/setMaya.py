#*************************************************************
# CONTENT       set maya environment variables
#
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
import sys

import setRenderer
from setEnv import SetEnv

class SetMaya(SetEnv):
    def __init__(self):
        super(SetMaya, self).__init__()

        from lib import libFunc

        os.environ["SOFTWARE"]         = "maya"
        os.environ["SOFTWARE_VERSION"] = "2015"
        os.environ["SOFTWARE_DIR"]     = ("/").join(["C:/Program Files/Autodesk", os.environ["SOFTWARE_VERSION"]])

        os.environ["RENDERER"]         = "arnold"
        os.environ["RENDERER_PATH"]    = ("/").join([os.environ["SOFTWARE_PATH"], "plugins", os.environ["RENDERER"], os.environ["SOFTWARE_VERSION"]])

        #add renderer
        # ACTIVATE RENDERER from os.environ["RENDERER"]
        setRenderer.setRenderer()

        # ------------------
        # PATH
        mayaPath   = ("/").join([os.environ["SOFTWARE_PATH"], "maya"])
        scriptPath = ("/").join([mayaPath, "scripts"])
        pluginPath = ("/").join([mayaPath, "plugins"])
        shelfPath  = ("/").join([mayaPath, "shelf"])    # just read rights
        externPath = ("/").join([mayaPath, "extern"])

        # ------------------
        # SCRIPT
        libFunc.addEnvnVar("MAYA_SCRIPT_PATH", ("/").join([pluginPath, "ANIM"]))

        # ------------------
        # PYTHON
        libFunc.addEnvnVar("PYTHONPATH", scriptPath)
        libFunc.addEnvnVar("PYTHONPATH", pluginPath)
        libFunc.addEnvnVar("PYTHONPATH", shelfPath)
        libFunc.addEnvnVar("PYTHONPATH", externPath)

        # ------------------
        # PLUGIN
        libFunc.addEnvnVar("MAYA_PLUG_IN_PATH", pluginPath)

        # ------------------
        # SHELF
        libFunc.addEnvnVar("MAYA_SHELF_PATH", ("/").join([os.environ["SOFTWARE_PATH"], "shelf;"]))

        # ------------------
        # DISABLE REPORT
        os.environ["MAYA_DISABLE_CIP"] = "1"
        os.environ["MAYA_DISABLE_CER"] = "1"

        # ------------------
        # --- MayaEnvVars ---
        # MAYA_PROJECT = PROJECT_ROOT/2_production
        # cd MAYA_PROJECT

        # ------------------
        # SPLASHSCREEN
        # File: MayaEDUStartupImage.png
        libFunc.addEnvnVar("XBMLANGPATH", os.environ["IMG_PATH"])

        # ------------------
        # CALL MAYA
        sys.path.append(("/").join([os.environ["SOFTWARE_DIR"], "bin;"]))
