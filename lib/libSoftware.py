#*********************************************************************
# content   = setup software attributes
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <contact@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************


from setEnv import SetEnv

#************************
# SOFTWARE

class SetSoftware(setEnv)

    def __init__(self, software):
        super(self)

        if software == "maya":
            self.maya()
        elif software == "houdini":
            self.houdini()
        elif software == "nuke":
            self.nuke()

    def maya(self):
        from lib import libFunc

        os.environ["SOFTWARE"]         = "maya"
        os.environ["SOFTWARE_VERSION"] = "2015" # data
        os.environ["SOFTWARE_PATH"]     = ("/").join(["C:/Program Files/Autodesk", os.environ["SOFTWARE_VERSION"]]) # data

        os.environ["RENDERER"]         = "arnold" # data
        os.environ["RENDERER_PATH"]    = ("/").join([os.environ["SOFTWARE_PATH"], "plugins", os.environ["RENDERER"], os.environ["SOFTWARE_VERSION"]]) #data

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
        sys.path.append(("/").join([os.environ["SOFTWARE_PATH"], "bin;"]))


    def nuke(self):
        print('Nuke ENV')


    def houdini(self):
        print('Houdini ENV')
