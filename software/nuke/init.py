#*********************************************************************
# content   = init Nuke
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import errno

import nuke

import libLog
from tank import Tank

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#************************
# PIPELINE
all_data      = Tank().data
project_data  = all_data['project']
software_data = all_data['software']
RESOLUTION    = (' ').join([str(project_data['resolution'][0]),
                            str(project_data['resolution'][1]),
                            project_data['name'].replace(' ', '')])


#************************
# FOLDER CREATION
def createWriteDir():
    file_name = nuke.filename(nuke.thisNode())
    file_path = os.path.dirname( file_name )
    os_path   = nuke.callbacks.filenameFilter(file_path)

    # cope with the directory existing already by ignoring that exception
    try: os.makedirs( os_path )
    except OSError, e:
      if e.errno != errno.EEXIST:
        raise

#************************
# PIPELINE
Tank().init_software()


try:    from scripts import write_node
except: LOG.warning('FAILED loading write_node')

# LOAD paths
try:
    for paths in os.getenv('SOFTWARE_SUB_PATH').split(';'):
        nuke.pluginAddPath(paths)
except:
    LOG.warning('FAILED loading SOFTWARE_SUB_PATH')


print('SETTINGS')
# FPS ***********************************
try:
    nuke.knobDefault("Root.fps", str(project_data['fps']))
    print('  {} ON  - FPS: {}'.format(chr(254), project_data['fps']))
except:
    LOG.error('  OFF - FPS: {}'.format(project_data['fps']), exc_info=True)
    print('  {} OFF - FPS: {}'.format(chr(254), project_data['fps']))

# RESOLUTION ****************************
try:
    nuke.addFormat(RESOLUTION)
    nuke.knobDefault('Root.format', project_data['name'].replace(' ', ''))
    print('  {} ON  - RES: {}'.format(chr(254), RESOLUTION))
except:
    LOG.error('  OFF - RES: {}'.format(RESOLUTION), exc_info=True)
    print('  {} OFF - RES: {}'.format(chr(254), RESOLUTION))

# createFolder ****************************
try:
    nuke.addBeforeRender(createWriteDir)
    print('  {} ON  - BeR: createWriteDir'.format(chr(254)))
except:
    LOG.error('  OFF - BeR: createWriteDir'.format(chr(254)), exc_info=True)
    print('  {} OFF - BeR: createWriteDir'.format(chr(254)))


print('') # ********************

