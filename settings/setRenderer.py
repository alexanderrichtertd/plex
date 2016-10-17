#*************************************************************
# CONTENT       set renderer enviroment variable
#
# EMAIL         contact@richteralexander.com
#*************************************************************

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
