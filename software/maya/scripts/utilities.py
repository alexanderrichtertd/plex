#*************************************************************
# title         utilities
#
# software		maya
#
# content       translate & rotate all selected objects 
#               to the first selected
#
# author        Alexander Richter 
# email         alexander.richter@filmakademie.de
#*************************************************************


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