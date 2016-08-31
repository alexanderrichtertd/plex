#*************************************************************
# title:        uniteShaderGroup
#
# content:      sets the name of all shader groups as the shader (+SG)
#
# dependencies: 
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import os
import logging

from pymel.core import *

import maya.cmds as cmds
import maya.mel as mel

import settings as s

sys.path.append(s.PATH['lib'])
import libLog


#**********************
# VARIABLE
#**********************
TITLE       = os.path.splitext(os.path.basename(__file__))[0]


#**********************
# FUNCTIONS
#**********************
def getSGFromMaterial(mat):
    mat = PyNode(mat)
    return mat.shadingGroups()


def start(shaderTypes = ["alSurface", "alLayer"]): 

    LOG = libLog.initLog(script=TITLE, level=logging.INFO, logger=logging.getLogger(TITLE))
    LOG.info("START")

    shaderList = []
    
    for shaderType in shaderTypes:
        shaderList += cmds.ls(type = shaderType)

    for shader in shaderList:
        shaderGroupLst = getSGFromMaterial(shader)
        
        if len(shaderGroupLst) == 0:
            continue
        
        #START: ADDING
        shaderGroup = shaderGroupLst[0]          
        ownShaderGroups = []
        conns = connectionInfo(PyNode(shader).outColor, destinationFromSource = True)
        
        for conn in conns:
            connNode = PyNode(conn).node()
            
            if PyNode(connNode).nodeType() != "shadingEngine":
                continue
            else:
                ownShaderGroups.append(str(connNode))
                
        if not (shaderGroup in ownShaderGroups):
            continue
        # END: ADDING
        
        if (shaderGroup != shader + "SG"):       
            try:
                mel.eval('rename ' + shaderGroup + ' ' + shader + 'SG;')
            except:
                print ("** FAIL | Unite Shader and Shader Group: Shader has no shading group or is a reference - " + shader + " **")

    LOG.info("END : Unite Shader and Shader Group")
    # print ("** DONE | Unite Shader and Shader Group **")