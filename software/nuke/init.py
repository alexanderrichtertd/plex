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
import libData
import libFunc
from software import Software

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#************************
# PIPELINE
all_data      = libData.get_data()
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
    try:
      os.makedirs( os_path )
    except OSError, e:
      if e.errno != errno.EEXIST:
        raise

#************************
# PIPELINE
Software().setup('nuke')
Software().print_header(software_data[os.getenv('SOFTWARE')]['MENU'])

print('SETTINGS')
# FPS ***********************************
try:
    nuke.knobDefault("nuke.Root()['fps'].setValue({})".format(project_data['fps']))
    print('  {} ON  - FPS: {}'.format(chr(254), project_data['fps']))
except:
    pass
    LOG.debug('  OFF - FPS: {}'.format(project_data['fps']))
    print('  {} OFF - FPS: {}'.format(chr(254), project_data['fps']))

# RESOLUTION ****************************
try:
    nuke.addFormat(RESOLUTION)
    nuke.knobDefault('Root.format', project_data['name'].replace(' ', ''))
    print('  {} ON  - RES: {}'.format(chr(254), RESOLUTION))
except:
    LOG.debug('  OFF - RES: {}'.format(RESOLUTION))
    print('  {} OFF - RES: {}'.format(chr(254), RESOLUTION))

# createFolder ****************************
try:
    nuke.addBeforeRender(createWriteDir)
    print('  {} ON  - BeR: createWriteDir'.format(chr(254)))
except:
    LOG.error('  OFF - BeR: createWriteDir'.format(chr(254)), exc_info=True)
    print('  {} OFF - BeR: createWriteDir'.format(chr(254)))


print('') # ********************
