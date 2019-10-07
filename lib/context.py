#*********************************************************************
# content   = context
#             executes other scripts on PUBLISH (on task in file name)
# version   = 0.1.0
# date      = 2019-12-01
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import pipefunc
from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
# CLASS
class Context():
    def setup(self):
        self.project_name = project_name   # project
        self.project_path = project_path   # //awesome/project

        self.path       = path             # D:/project/asset/file.format

        self.step       = step             # shot or asset
        self.task       = task             # ANIMATION

        self.resolution = resolution       # [1920, 1080]
        self.fps        = fps              # 25

        self.artist     = artist           # arichter
        self.comment    = comment          # "Broken scene"


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
        return pipefunc.openFolder(self.file_path)
