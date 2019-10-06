#*********************************************************************
# content   = maya utils
# version   = 0.6.0
# date      = 2019-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import maya.mel as mel
import maya.cmds as cmds
from pymel.core import *

from functools import wraps

import pipelog


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = pipelog.init(script=TITLE)


#*********************************************************************
def position_selected():
	selectedObj = ls( selection=True )

	if len(selectedObj) > 1:
	    origin = selectedObj[0]
	    selectedObj.pop(0)

	    for sObj in selectedObj:
	        cam_new = general.PyNode(sObj)
	        cam_origin = general.PyNode(origin)

	        cam_new.translate.set(cam_origin.translate.get())
	        cam_new.rotate.set(cam_origin.rotate.get())
	        cam_new.scale.set(cam_origin.scale.get())
	else:
	    LOG.warning("FAIL : Need at least 2 selections to set everything on the first selection position.")


#*********************************************************************
# DECORATOR
def viewport_off(func):
    @wraps(func)
    def viewport(*args, **kwargs):
        try:
            # viewport OFF
            mel.eval("paneLayout -e -manage false $gMainPane")
            return func(*args, **kwargs)
        except Exception:
    	    LOG.error("FAIL : Viewport off", exc_info=True)
            raise
        finally:
            # viewport ON
            mel.eval("paneLayout -e -manage true $gMainPane")

    return viewport



