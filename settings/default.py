#*************************************************************
# CONTENT       SET default environment path
#
# DEPENDENCIES  MASTER pipeline path
#
# SOFTWARE      default + software (maya | nuke | houdini ...)
#
# AUTHOR        contact@richteralexander.com
#*************************************************************

import os
import sys

class PathDefault():
    def __init__ (self):
        pathSettings = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

        os.environ["PATH_PIPELINE"] = os.path.dirname(pathSettings)
        os.environ["PATH_PROJECT"]  = os.path.dirname(os.environ["PATH_PIPELINE"])

        os.environ["PATH_DATA"]     = os.environ["PATH_PIPELINE"] + "/data"
        os.environ["PATH_IMG"]      = os.environ["PATH_PIPELINE"] + "/img"
        os.environ["PATH_LIBRARY"]  = os.environ["PATH_PIPELINE"] + "/lib"
        os.environ["PATH_SETTINGS"] = pathSettings
        os.environ["PATH_SOFTWARE"] = os.environ["PATH_PIPELINE"] + "/software"

        sys.path.append(os.environ["PATH_PIPELINE"])
        sys.path.append(os.environ["PATH_SOFTWARE"])


    def pathMasterPipeline(self):
        # RELATIVE PATH
        os.environ["PATH_MASTER_PIPELINE"] = r"D:/Dropbox/arPipeline/v002/PUBLISH"

        os.environ["PATH_MASTER_DATA"]     = os.environ["PATH_DATA"].replace(os.environ["PATH_PIPELINE"], os.environ["PATH_MASTER_PIPELINE"])
        os.environ["PATH_MASTER_IMG"]      = os.environ["PATH_IMG"].replace(os.environ["PATH_PIPELINE"], os.environ["PATH_MASTER_PIPELINE"])
        os.environ["PATH_MASTER_LIBRARY"]  = os.environ["PATH_LIBRARY"].replace(os.environ["PATH_PIPELINE"], os.environ["PATH_MASTER_PIPELINE"])
        os.environ["PATH_MASTER_SETTINGS"] = os.environ["PATH_SETTINGS"].replace(os.environ["PATH_PIPELINE"], os.environ["PATH_MASTER_PIPELINE"])
        os.environ["PATH_MASTER_SOFTWARE"] = os.environ["PATH_SOFTWARE"].replace(os.environ["PATH_PIPELINE"], os.environ["PATH_MASTER_PIPELINE"])

        sys.path.append(os.environ["PATH_MASTER_PIPELINE"])
        sys.path.append(os.environ["PATH_MASTER_SOFTWARE"])


    def __call__(self):
        print os.environ["PATH_PROJECT"] 
        print os.environ["PATH_PIPELINE"]

        print os.environ["PATH_DATA"]    
        print os.environ["PATH_IMG"]     
        print os.environ["PATH_LIBRARY"] 
        print os.environ["PATH_SETTINGS"]
        print os.environ["PATH_SOFTWARE"]

        print ""

        print os.environ["PATH_MASTER_PIPELINE"]

        print os.environ["PATH_MASTER_DATA"]    
        print os.environ["PATH_MASTER_IMG"]     
        print os.environ["PATH_MASTER_LIBRARY"] 
        print os.environ["PATH_MASTER_SETTINGS"]
        print os.environ["PATH_MASTER_SOFTWARE"]


kDefault = PathDefault()
kDefault.pathMasterPipeline()
kDefault.__call__()