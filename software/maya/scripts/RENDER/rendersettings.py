# ****************************************************
# content = setup render settings in maya scene
# version = 1.0.0
# date    = 2019-08-01
#
# license = MIT
# author  = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os

import maya.cmds as cmds

import pipelog


#*********************************************************************
# VAR
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = pipelog.init(script=TITLE)


#*********************************************************************
# CLASS
class Rendersettings(object):

    def __init__(self):
        self.states = ["work", "preview", "publish", "custom"]

    def default(self):
        pass

    def work(self):
        pass


    def preview(self):
        pass


    def publish(self):
       pass


    def custom(self):
        pass


    #*********************************************************************
    # CLASS
    def lowest(self):
        self.work()

    def highest(self):
        self.publish()


    #*********************************************************************
    # SETUP
    def setup(self, state="default"):
        if state != "custom": self.default()
        getattr(self, state, self.custom)()

