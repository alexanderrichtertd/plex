#*************************************************************
# CONTENT       SET default environment path
#
# DEPENDENCIES  MASTER pipeline path
#
# EMAIL         contact@richteralexander.com
#*************************************************************

import os
import sys
import logging

# ABSOLUTE PATH
MASTER_PATH = r"D:/Dropbox/arPipeline/v002/PUBLISH"

class SetEnv(object):
    def __init__(self):
        os.environ["SETTINGS_PATH"] = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

        os.environ["PIPELINE_PATH"] = os.path.dirname(os.environ["SETTINGS_PATH"])
        os.environ["PROJECT_PATH"]  = os.path.dirname(os.environ["PIPELINE_PATH"])

        os.environ["DATA_PATH"]     = os.environ["PIPELINE_PATH"] + "/data"
        os.environ["IMG_PATH"]      = os.environ["PIPELINE_PATH"] + "/img"
        os.environ["LIBRARY_PATH"]  = os.environ["PIPELINE_PATH"] + "/lib"
        os.environ["SOFTWARE_PATH"] = os.environ["PIPELINE_PATH"] + "/software"

        sys.path.append(os.environ["PIPELINE_PATH"])
        sys.path.append(os.environ["SOFTWARE_PATH"])

        self.pathMasterPipeline()

    def pathMasterPipeline(self):
        os.environ["PIPELINE_MASTER_PATH"] = MASTER_PATH

        os.environ["DATA_MASTER_PATH"]     = os.environ["DATA_PATH"].replace(os.environ["PIPELINE_PATH"], os.environ["PIPELINE_MASTER_PATH"])
        os.environ["IMG_MASTER_PATH"]      = os.environ["IMG_PATH"].replace(os.environ["PIPELINE_PATH"], os.environ["PIPELINE_MASTER_PATH"])
        os.environ["LIBRARY_MASTER_PATH"]  = os.environ["LIBRARY_PATH"].replace(os.environ["PIPELINE_PATH"], os.environ["PIPELINE_MASTER_PATH"])
        os.environ["SETTINGS_MASTER_PATH"] = os.environ["SETTINGS_PATH"].replace(os.environ["PIPELINE_PATH"], os.environ["PIPELINE_MASTER_PATH"])
        os.environ["SOFTWARE_MASTER_PATH"] = os.environ["SOFTWARE_PATH"].replace(os.environ["PIPELINE_PATH"], os.environ["PIPELINE_MASTER_PATH"])

        if os.path.exists(os.environ["PIPELINE_PATH"]):
            sys.path.append(os.environ["PIPELINE_MASTER_PATH"])
        else:
            print("PIPELINE_MASTER_PATH doesnt exist: %s"%os.environ["PIPELINE_MASTER_PATH"])

        if os.path.exists(os.environ["SOFTWARE_PATH"]):
            sys.path.append(os.environ["SOFTWARE_MASTER_PATH"])
        else:
            print("SOFTWARE_MASTER_PATH doesnt exist: %s"%os.environ["SOFTWARE_MASTER_PATH"])

