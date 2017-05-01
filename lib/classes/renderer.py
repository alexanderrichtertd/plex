#*********************************************************************
# content   = renderer
#             executes other scripts on PUBLISH (on task in file name)
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys

def setRenderer():
    from lib import libFunc

    # ------------------
    # ARNOLD
    if os.environ["RENDERER"] == "arnold":
        libFunc.addEnvnVar("MtoA", os.environ["RENDERER_PATH"])
        libFunc.addEnvnVar("MAYA_MODULE_PATH", os.environ["MtoA"])
        sys.path.append(os.environ["MtoA"] + "/bin;")

        # WRONG
        os.environ["ARNOLD_SHADER_PATH"] = os.environ["RENDERER_PATH"] + "/alShader"

        libFunc.addEnvnVar("ARNOLD_PLUGIN_PATH", os.environ["MtoA"] + "/shaders")
        libFunc.addEnvnVar("ARNOLD_PLUGIN_PATH", os.environ["RENDERER_PATH"] + "/bin")
        libFunc.addEnvnVar("ARNOLD_PLUGIN_PATH", os.environ["ARNOLD_SHADER_PATH"] + "/bin")
        libFunc.addEnvnVar("MTOA_TEMPLATES_PATH", os.environ["ARNOLD_SHADER_PATH"] + "/ae")

        # AI LICENCE
        libFunc.addEnvnVar("ARNOLD_LICENSE_HOST", "blue")

    # ------------------
    # RENDERMAN
    if os.environ["RENDERER"] == "renderman":
        os.environ["RM"] = os.environ["RENDERER_PATH"]
        libFunc.addEnvnVar("MAYA_MODULE_PATH", os.environ["RM"] + "/etc")
        os.environ["RMSTREE"] = os.environ["RM"]
        sys.path.append(os.environ["RM"] + "/bin;")


#************************
# RENDER SETTINGS
def setRenderSettings(renderStatus):
    LOG.info("setRenderSettings")

    # LOG.info(s.MAYA_RENDERER
    # if os.environ["SOFTWARE"] == "maya":
    #     if renderStatus:
    #         LOG.info("Render Settings : " + SOFTWARE + " : Low")
    #     else:
    #         LOG.info("Render Settings : " + SOFTWARE + " : High")


    # if os.environ["SOFTWARE"] == "nuke":
    #     if renderStatus:
    #         LOG.info("Render Settings : " + SOFTWARE + " : Low")
    #     else:
    #         LOG.info("Render Settings : " + SOFTWARE + " : High")


    # if os.environ["SOFTWARE"] == "houdini":
    #     if renderStatus:
    #         LOG.info("Render Settings : " + SOFTWARE + " : Low")
    #     else:
    #         LOG.info("Render Settings : " + SOFTWARE + " : High")
