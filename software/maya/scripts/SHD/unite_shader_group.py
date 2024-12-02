# content   = sets the name of all shader groups as the shader (+SG)
# date      = 2020-06-19

# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import maya.mel as mel
import maya.cmds as cmds
from pymel.core import *

from plex import Plex

LOG = Plex().log(script=__name__)


def start(shader_types=["alSurface", "alLayer"]):
    shaders = []

    for shader_type in shader_types:
        shaders += cmds.ls(type = shader_type)

    for shader in shaders:
        shader_groups = PyNode(shader).shadingGroups()

        if len(shader_groups) == 0: continue

        #START: ADDING
        shader_group = shader_groups[0]
        own_shader_roups = []
        conns = connectionInfo(PyNode(shader).outColor, destinationFromSource = True)

        for conn in conns:
            connNode = PyNode(conn).node()

            if PyNode(connNode).nodeType() != "shadingEngine":
                continue
            else:
                own_shader_roups.append(str(connNode))

        if not (shader_group in own_shader_roups): continue
        # END: ADDING

        if (shader_group != shader + "SG"):
            try:
                mel.eval('rename ' + shader_group + ' ' + shader + 'SG;')
            except:
                LOG.error("** FAIL | Unite Shader and Shader Group: Shader has no shading group or is a reference - " + shader + " **")

    LOG.info("DONE : Unite Shader and Shader Group")
