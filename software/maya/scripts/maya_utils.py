#*********************************************************************
# content   = maya utils
# version   = 0.6.0
# date      = 2017-07-10
#
# license   = MIT
# copyright = Copyright 2017 Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

from pymel.core import *
from functools import wraps
import maya.mel as mel

import libLog

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

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
	    LOG.warning("FAIL : Need at least 2 selections")


#************************
# Decorators
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
