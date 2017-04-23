#*********************************************************************
# content   = SET default environment paths
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


from pymel.core import *

def positionSelected():
	selectedObj = ls( selection=True )

	if len(selectedObj) > 1:
	    origin = selectedObj[0]
	    selectedObj.pop(0)

	    for sObj in selectedObj:
	        camNew = general.PyNode(sObj)
	        camOrigin = general.PyNode(origin)

	        camNew.translate.set(camOrigin.translate.get())
	        camNew.rotate.set(camOrigin.rotate.get())
	        camNew.scale.set(camOrigin.scale.get())
	else:
	    print "FAIL : Need at least 2 selections"
