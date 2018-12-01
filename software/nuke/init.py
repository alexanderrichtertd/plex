#*********************************************************************
# content   = init Nuke
# version   = 0.0.1
# date      = 2018-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import errno

import nuke

import libLog
import libFunc
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
    file_path = os.path.dirname(file_name)
    os_path   = nuke.callbacks.filenameFilter(file_path)

    # cope with the directory existing already by ignoring that exception
    try: os.makedirs(os_path)
    except OSError, e:
      if e.errno != errno.EEXIST:
        raise


def add_plugin_paths():
    # ADD all IMG paths
    for img in os.getenv('IMG_PATH').split(';'):
        for img_sub in libFunc.get_deep_folder_list(path=img, add_path=True):
            nuke.pluginAddPath(img_sub)

    # ADD sub software paths
    for paths in os.getenv('SOFTWARE_SUB_PATH').split(';'):
        nuke.pluginAddPath(paths)


#************************
# PIPELINE
Tank().init_software()
add_plugin_paths()


try:    from scripts import write_node
except: LOG.warning('FAILED loading write_node')

# LOAD paths
try:
    for paths in os.getenv('SOFTWARE_SUB_PATH').split(';'):
        nuke.pluginAddPath(paths)
except:
    LOG.warning('FAILED loading SOFTWARE_SUB_PATH')


print('SETTINGS')

# RESOLUTION ****************************
try:
    nuke.addFormat(RESOLUTION)
    nuke.knobDefault('Root.format', project_data['name'].replace(' ', ''))
    print('  {} ON  - {}'.format(chr(254), RESOLUTION))
except:
    LOG.error('  OFF - {}'.format(RESOLUTION), exc_info=True)
    print('  {} OFF - {}'.format(chr(254), RESOLUTION))

# FPS ***********************************
try:
    nuke.knobDefault("Root.fps", str(project_data['fps']))
    print('  {} ON  - {} fps'.format(chr(254), project_data['fps']))
except:
    LOG.error('  OFF - {} fps'.format(project_data['fps']), exc_info=True)
    print('  {} OFF - {} fps'.format(chr(254), project_data['fps']))

# createFolder ****************************
try:
    nuke.addBeforeRender(createWriteDir)
    print('  {} ON  - createWriteDir (before render)'.format(chr(254)))
except:
    LOG.error('  OFF - createWriteDir (before render)'.format(chr(254)), exc_info=True)
    print('  {} OFF - createWriteDir (before render)'.format(chr(254)))


print('') # ********************
