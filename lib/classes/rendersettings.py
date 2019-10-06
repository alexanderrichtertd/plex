#*********************************************************************
# content   = sets rendersettings
# version   = 0.1.0
# date      = 2019-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os

import libLog
import libLogstats
import arNotice


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#*********************************************************************
# RENDERSETTINGS
class Rendersettings(object):

    def __init__(self):
        self.states = ["final", "preview", "lgt", "custom"]


    def default(self):
        LOG.info("RENDERSETTINGS:default")


    @libLogstats.notice_func("rendersettings:lgt")
    def lgt(self):
        LOG.info("RENDERSETTINGS:default")


    @libLogstats.notice_func("rendersettings:preview")
    def preview(self):
        LOG.info("RENDERSETTINGS:default")


    @libLogstats.notice_func("rendersettings:final")
    def final(self):
        LOG.info("RENDERSETTINGS:default")


    @libLogstats.notice_func("rendersettings:custom")
    def custom(self):
        pass


    def lowest(self):
        self.lgt()

    def highest(self):
        self.final()

    def default_string(self):
        return "preview"


    def setup(self, state = "final"):
        try:
            if state != "custom": self.default()
            getattr(self, state, self.custom)()
        except:
            arNotice.create_default_notice("error:no_renderer")

