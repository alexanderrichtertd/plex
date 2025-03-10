# content   = Nuke
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os

import nuke

import plex
from software import Software


# VARIABLE ***************************************************************
LOG = plex.log(script=__name__)
DEFAULT_PATH = os.path.normpath(plex.get_config('config_user') + '/tmp_img.jpg')


class Nuke(Software):

    _NAME = 'nuke'

    @property
    def scene_path(self):
        return nuke.root().knob('name').value()

    def scene_save(self):
        return nuke.scriptSave()

    def scene_save_as(self, file, setup_scene=False):
        nuke.scriptSaveAs(file)

    def scene_open(self, file):
        return nuke.scriptOpen(file)

    def scene_import(self, file):
        pass


    # SNAPSHOT ***************************************************************
    def viewport_snapshot(img_path=DEFAULT_PATH):
        viewer   = nuke.activeViewer()
        viewNode = nuke.activeViewer().node()

        actInput = nuke.ViewerWindow.activeInput(viewer)
        if actInput < 0: return False

        selInput = nuke.Node.input(viewNode, actInput)

        # look up filename based on top read node
        topName ="[file tail [knob [topnode].file]]"

        # create writes and define render format
        write1 = nuke.nodes.Write( file=img_path.replace("\\", "/"), name='writeNode1' , file_type=plex.config['project']['EXTENSION']['thumnail'])
        write1.setInput(0, selInput)

        # look up current frame
        curFrame = int(nuke.knob("frame"))
        # start the render
        nuke.execute( write1.name(), curFrame, curFrame )
        # clean up
        for n in [write1]: nuke.delete(n)

        LOG.info("nuke_viewer_snapshot")
