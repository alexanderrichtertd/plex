#*********************************************************************
# content   = Nuke
# version   = 0.1.0
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os

import nuke

from tank import Tank
from software import Software


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)
DEFAULT_PATH = os.path.normpath(os.getenv('DATA_USER_PATH').split(';')[0] + '/tmp_img.jpg')


#*********************************************************************
# CLASS
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


    #******************************************************************************
    # SNAPSHOT
    def viewport_snapshot(img_path=DEFAULT_PATH):
        viewer   = nuke.activeViewer()
        viewNode = nuke.activeViewer().node()

        actInput = nuke.ViewerWindow.activeInput(viewer)
        if actInput < 0: return False

        selInput = nuke.Node.input(viewNode, actInput)

        # look up filename based on top read node
        topName ="[file tail [knob [topnode].file]]"

        # create writes and define render format
        write1 = nuke.nodes.Write( file=img_path.replace("\\", "/"), name='writeNode1' , file_type=Tank().data_project['EXTENSION']['thumnail'])
        write1.setInput(0, selInput)

        # look up current frame
        curFrame = int(nuke.knob("frame"))
        # start the render
        nuke.execute( write1.name(), curFrame, curFrame )
        # clean up
        for n in [write1]: nuke.delete(n)

        LOG.info("nuke_viewer_snapshot")
