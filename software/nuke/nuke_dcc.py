#*********************************************************************
# content   = Nuke
# version   = 0.1.0
# date      = 2019-10-06
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
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


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
