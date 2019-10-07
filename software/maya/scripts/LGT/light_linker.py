#*********************************************************************
# content   = Maya: Light Linker
# version   = 0.1.0
# date      = 2019-08-01
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import maya.cmds as cmds

import pipestats


#*********************************************************************
# LIGHT LINKER
@pipestats.notice('apps:light_linker')
def start():
    cmds.window(title='Light & Shadow Linker')
    cmds.columnLayout()
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label='Light', width=250,)
    cmds.text(label='Shadow', width=250, height=30)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Add Link", annotation="Add light linking between objects and lights", width=250, c="light_linker.selection_light_linking()")
    cmds.button(label="Add Link", annotation="Add light linking between objects and lights", width=250, c="light_linker.selection_light_linking(shadow_link=True)")
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Break Link", annotation="Break light linking between objects and lights", width=250, c="light_linker.selection_light_linking(break_light=True)")
    cmds.button(label="Break Link", annotation="Break light linking between objects and lights", width=250, c="light_linker.selection_light_linking(break_light=True, shadow_link=True)")
    cmds.setParent('..')
    cmds.separator(height=10)
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Link (Light Exclusive)", annotation="Objects will only linked to this lights", width=250, c="light_linker.selection_light_linking(exclusive='lights')")
    cmds.button(label="Link (Light Exclusive)", annotation="Objects will only linked to this lights", width=250, c="light_linker.selection_light_linking(exclusive='lights', shadow_link=True)")
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Link (Object Exclusive)", annotation="Lights will only be linked to this objects", width=250, c="light_linker.selection_light_linking(exclusive='meshes')")
    cmds.button(label="Link (Object Exclusive)", annotation="Lights will only be linked to this objects", width=250, c="light_linker.selection_light_linking(exclusive='meshes', shadow_link=True)")
    cmds.setParent('..')
    cmds.separator(height=10)
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Select Linking", annotation="Select the linked lights/meshes", width=250, c="light_linker.select_attached()")
    cmds.button(label="Select Linking", annotation="Select the linked lights/meshes", width=250, c="light_linker.select_attached(shadow_link=True)")
    cmds.setParent('..')
    cmds.columnLayout()

    cmds.showWindow()


@pipestats.notice('apps:light_linker', meta=False)
def selection_light_linking(break_light=False, exclusive="", shadow_link=False):
    selection = cmds.ls(dag=1,o=1,s=1,sl=1)
    lights    = cmds.ls(selection, type=["light"] + cmds.listNodeTypes("light"))
    meshes    = list(set(selection) - set(lights))

    if not selection or not lights: return "error:no_light_selection"

    if exclusive == "lights":
        scene_lights   = cmds.ls(type=["light"] + cmds.listNodeTypes("light"))
        exclude_lights = list(set(scene_lights) - set(lights))
        cmds.lightlink(light=exclude_lights, object=meshes, shadow=shadow_link, b=True)

        LOG.info("exclude_lights: {}".format(exclude_lights))
    elif exclusive == "meshes":
        exclude_meshes = list(set(cmds.ls(dag=1,o=1,s=1)) - set(meshes))
        cmds.lightlink(light=lights, object=exclude_meshes, shadow=shadow_link, b=True)

        LOG.info("exclude_meshes: {}".format(exclude_meshes))

    if not meshes:
        cmds.lightlink(light=lights, object=cmds.ls(dag=1,o=1,s=1), shadow=shadow_link)
        LOG.info("LightLinking: Default for {}".format(lights))
        return

    LOG.info("selection: {}".format(selection))

    cmds.lightlink(light=lights, object=meshes, shadow=shadow_link, b=break_light)
    LOG.info("LightLinking - break:{} - shadow:{}: {} with {}".format(break_light, shadow_link, lights, meshes))


@pipestats.notice('apps:light_linker', meta=False)
def select_attached(shadow_link=False):
    selection = cmds.ls(dag=1,o=1,s=1,sl=1)
    if not selection or not lights: return "error:no_light_selection"

    lights    = cmds.ls(selection, type=["light"] + cmds.listNodeTypes("light"))
    selection = cmds.pickWalk(direction='down')

    attached_objs = []

    if lights:
        for sel in selection:
            attached_objs += cmds.lightlink(query=True, shadow=shadow_link, light=sel)
        select_nodes = cmds.ls(attached_objs, type=['mesh', 'nurbsSurface', 'pgYetiMaya'])
    else: # MESHES
        for sel in selection:
            attached_objs += cmds.lightlink(query=True, shadow=shadow_link, object=selection)
        select_nodes = cmds.ls(attached_objs, type=["light"] + cmds.listNodeTypes("light"))

    if not select_nodes: return
    cmds.select(select_nodes)
    cmds.pickWalk(direction='up')

