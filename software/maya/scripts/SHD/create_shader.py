#*********************************************************************
# content   = shader
# date      = 2020-06-19
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import maya.cmds as cmds


#*********************************************************************
# FUNCTIONS
def create_simple_shd(name="BLACK_SHD", color=[0,0,0]):
    if cmds.objExists(name):
        print(f"CREATED - {name}")
    else:
        shader = cmds.shadingNode("surfaceShader", name=name, asShader=True)
        cmds.setAttr(shader + '.outColor', color[0], color[1], color[2])
        print(f"EXISTS  - {name}")

        return shader
