#*********************************************************************
# content   = context
#             executes other scripts on PUBLISH (on task in file name)
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import plexfunc
from plex import Plex


#*********************************************************************
# VARIABLE
LOG = Plex().log(script=__name__)


#*********************************************************************
# CLASS
class Context():
    def setup(self):
        self.project_name = project_name   # project
        self.project_path = project_path   # /awesome/project

        self.path       = path             # D:/project/asset/mike_RIG_v012.mb

        self.step       = step             # shots or assets or renders
        self.scene      = scene            # s010 or mike
        self.task       = task             # ANIMATION

        self.resolution = resolution       # [1920, 1080]
        self.fps        = fps              # 24

        self.artist     = artist           # arichter
        self.comment    = comment          # Broken scene


    #*********************************************************************
    # VARIABLE
    @property
    def project(self):
        return self.project_name

    @property
    def project_path(self):
        return self.project_path

    @property
    def path(self):
        return self.path

    @property
    def step(self):
        return self.step

    @property
    def task(self):
        return self.task

    @property
    def resolution(self):
        return self.resolution

    @property
    def fps(self):
        return self.fps

    @property
    def artist(self):
        return self.artist

    @property
    def comment(self):
        return self.comment


    #*********************************************************************
    # FUNCTIONS
    def open_path(self):
        return plexfunc.open_folder(self.file_path)
