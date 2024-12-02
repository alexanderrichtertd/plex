# content   = Maya: Light Linker
# date      = 2020-06-19
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import maya.cmds as cmds

from plex import Plex

LOG = Plex().log(script=__name__)


# LIGHT LINKER ***************************************************************
def start():
    cmds.window(title='Light Linker')
    cmds.columnLayout()
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label='Light', width=300, height=30)
    # cmds.text(label='Shadow', width=300, height=30)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Add Lights", annotation="Add link between objects and lights", width=300, c="light_linker.selection_light_linking()")
    # cmds.button(label="Add Shadows", annotation="Add link between objects and shadows", width=300, c="light_linker.selection_light_linking(shadow_link=True)")
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Break Lights", annotation="Break link between objects and lights", width=300, c="light_linker.selection_light_linking(break_light=True)")
    # cmds.button(label="Break Shadows", annotation="Break link between objects and shadows", width=300, c="light_linker.selection_light_linking(break_light=True, shadow_link=True)")
    cmds.setParent('..')
    cmds.separator(height=10)
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Objects exclusive to this lights", annotation="Objects will only linked to this lights", width=300, c="light_linker.selection_light_linking(exclusive='lights')")
    # cmds.button(label="Link (Shadow Exclusive)", annotation="Objects will only linked to this shadows", width=300, c="light_linker.selection_light_linking(exclusive='lights', shadow_link=True)")
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Lights exclusive to this objects", annotation="Lights will only be linked to this objects", width=300, c="light_linker.selection_light_linking(exclusive='meshes')")
    # cmds.button(label="Link (Object Exclusive)", annotation="Shadows will only be linked to this objects", width=300, c="light_linker.selection_light_linking(exclusive='meshes', shadow_link=True)")
    cmds.setParent('..')
    cmds.separator(height=10)
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Select Linked Lights/Objects", annotation="Select the linked lights/meshes", width=300, c="light_linker.select_attached()")
    # cmds.button(label="Select Linked Shadows", annotation="Select the linked lights/meshes", width=300, c="light_linker.select_attached(shadow_link=True)")
    cmds.setParent('..')
    cmds.columnLayout()

    cmds.showWindow()


def selection_light_linking(break_light=False, exclusive="", shadow_link=False):
    selection = cmds.ls(dag=1,o=1,s=1,sl=1)
    lights    = cmds.ls(selection, type=["light"] + cmds.listNodeTypes("light"))
    meshes    = list(set(selection) - set(lights))

    if not selection or not lights: return "error:no_light_selection"

    if exclusive == "lights":
        scene_lights   = cmds.ls(type=["light"] + cmds.listNodeTypes("light"))
        exclude_lights = list(set(scene_lights) - set(lights))
        cmds.lightlink(light=exclude_lights, object=meshes, shadow=shadow_link, b=True)

        LOG.info(f"exclude_lights: {exclude_lights}")
    elif exclusive == "meshes":
        exclude_meshes = list(set(cmds.ls(dag=1,o=1,s=1)) - set(meshes))
        cmds.lightlink(light=lights, object=exclude_meshes, shadow=shadow_link, b=True)

        LOG.info(f"exclude_meshes: {exclude_meshes}")

    if not meshes:
        cmds.lightlink(light=lights, object=cmds.ls(dag=1,o=1,s=1), shadow=shadow_link)
        LOG.info(f"LightLinking: Default for {lights}")
        return

    cmds.lightlink(light=lights, object=meshes, shadow=shadow_link, b=break_light)
    LOG.debug(f"LightLinking - break:{break_light} - shadow:{shadow_link}: {lights} with {meshes}")


def select_attached(shadow_link=False):
    selection = cmds.ls(dag=1,o=1,s=1,sl=1)
    lights    = cmds.ls(selection, type=["light"] + cmds.listNodeTypes("light"))
    selection = cmds.pickWalk(direction='down')

    if not selection and not lights:
        return "error:no_light_selection"

    attached_objs = []

    if lights:
        for sel in selection:
            attached_objs += cmds.lightlink(query=True, shadow=shadow_link, light=sel)
        select_nodes = cmds.ls(attached_objs, type=['mesh', 'nurbsSurface'])
    else: # MESHES
        for sel in selection:
            attached_objs += cmds.lightlink(query=True, shadow=shadow_link, object=selection)
        select_nodes = cmds.ls(attached_objs, type=["light"] + cmds.listNodeTypes("light"))

    if not select_nodes: return

    cmds.select(select_nodes)
    cmds.pickWalk(direction='up')
