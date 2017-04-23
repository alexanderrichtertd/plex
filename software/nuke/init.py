#*********************************************************************
# content   = init Nuke
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
import errno

import nuke

import libLog
import libData
import libFunc

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
# PIPELINE
libFunc.console_header(project_data['name'])

# **********************************

LOG.debug(os.environ)

print('PATHS')
print('  {} ON  - libUtil'.format(chr(254)))
print('  {} ON  - libClass'.format(chr(254)))
print('  {} ON  - img'.format(chr(254)))
print('  {} ON  - utilities'.format(chr(254)))
print('')
print('  {} ON  - gizmos'.format(chr(254)))
print('  {} ON  - scripts'.format(chr(254)))
print('  {} ON  - plugins'.format(chr(254)))


print('') # ********************


#************************
print('SCRIPTS')
try:
    print('  {} ON  - {}'.format(chr(254), software_data['NUKE']['MENU']))
except:
    LOG.debug('  {} OFF - SCRIPTS: {}'.format(chr(254), software_data['NUKE']['MENU']))
    pass


print('') # ********************


#************************
print('SETTINGS')

# FPS ***********************************
try:
    nuke.knobDefault('Root.fps', project_data['fps'])
    print('  {} ON  - FPS: {}'.format(chr(254), project_data['fps']))
except:
    pass
    LOG.debug('  OFF - FPS: {}'.format(project_data['fps']))
    print('  {} OFF - FPS: {}'.format(chr(254), project_data['fps']))

# RESOLUTION ****************************
try:
    nuke.addFormat(RESOLUTION)
    nuke.knobDefault('Root.format', s.PROJECT_NAME.replace(' ', ''))
    print('  {} ON  - RES: {}'.format(chr(254), RESOLUTION))
except:
    LOG.debug('  OFF - RES: {}'.format(RESOLUTION))
    print('  {} OFF - RES: {}'.format(chr(254), RESOLUTION))

# createFolder ****************************
try:
    nuke.addBeforeRender(createWriteDir)
    print('  {} ON  - BeR: createWriteDir'.format(chr(254)))
except:
    LOG.debug('  OFF - BeR: createWriteDir'.format(chr(254)))
    print('  {} OFF - BeR: createWriteDir'.format(chr(254)))


print('') # ********************


#************************
# FOLDER CREATION
def createWriteDir():
  file  = nuke.filename(nuke.thisNode())
  dir   = os.path.dirname( file )
  osdir = nuke.callbacks.filenameFilter( dir )
  # cope with the directory existing already by ignoring that exception
  try:
    os.makedirs( osdir )
  except OSError, e:
    if e.errno != errno.EEXIST:
      raise

