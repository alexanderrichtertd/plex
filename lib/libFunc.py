#*************************************************************
# CONTENT       common functions (open|crete folder, file, help)
#*********************************************************************
# content   = common functions (e.g.help)
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <contact@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import time
import webbrowser






#************************
# TIME
# @BRIEF  count time of functions for optimazation
def getDuration(method):
    def timed(*args, **kw):
        startTime  = time.time()
        resultTime = method(*args, **kw)
        endTime    = time.time()

        printResult = '%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, endTime-startTime)
        LOG.debug(printResult)
        return resultTime
    return timed
