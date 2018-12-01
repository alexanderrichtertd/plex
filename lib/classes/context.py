#*********************************************************************
# content   = context
#             executes other scripts on PUBLISH (on task in file name)
# version   = 0.0.1
# date      = 2018-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import libLog
import libFunc

#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

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

        self.author     = author           # arichter
        self.comment    = comment          # "Broken scene"


    #*******************
    # VARIABLE
    @property
    def project(self):
        return self.project


    #*******************
    # FUNCTIONS
    def open_path(self):
        return libFunc.openFolder(self.file_path)
