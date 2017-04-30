#*********************************************************************
# content   = common functions
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import time
import webbrowser

import libData

def get_help(name = ''):
    project_data = libData.get_data('project')['HELP']
    if not name:
        name = os.getenv('SOFTWARE')
    if name in project_data:
        webbrowser.open(project_data[name])
    else:
        webbrowser.open(project_data['main'])


# GET all (sub) keys in dict
def get_all_keys(key_list, dictonary=[]):
    for key, items in key_list.iteritems():
        dictonary.append(key)
        if isinstance(items, dict):
            get_all_keys(items, dictonary)
    return dictonary

#************************
# TIME
# @BRIEF  count time of functions for optimazation
def get_duration(method):
    def timed(*args, **kw):
        startTime  = time.time()
        resultTime = method(*args, **kw)
        endTime    = time.time()

        printResult = '%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, endTime-startTime)
        LOG.debug(printResult)
        return resultTime
    return timed
