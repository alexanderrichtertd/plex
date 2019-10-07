#*********************************************************************
# content   = shader
# version   = 0.1.0
# date      = 2019-12-26
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import maya.cmds as cmds


#*********************************************************************
def create_simple_shd(name="BLACK_SHD", color=[0,0,0]):
    if cmds.objExists(name):
        print("CREATED - {}".format(name))
    else:
        shader = cmds.shadingNode("surfaceShader", name=name, asShader=True)
        cmds.setAttr(shader + '.outColor', color[0], color[1], color[2])
        print("EXISTS  - {}".format(name))

        return shader
