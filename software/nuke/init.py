#*********************************************************************
# content   = init Nuke
# version   = 0.1.0
# date      = 2022-01-01
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import errno

import nuke

import pipefunc
from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)

PROJECT_DATA = Tank().data_project
RESOLUTION   = (' ').join([str(PROJECT_DATA['resolution'][0]),
                            str(PROJECT_DATA['resolution'][1]),
                            PROJECT_DATA['name'].replace(' ', '')])


#*********************************************************************
# FOLDER CREATION
def create_write_dir():
    file_name = nuke.filename(nuke.thisNode())
    file_path = os.path.dirname(file_name)
    os_path   = nuke.callbacks.filenameFilter(file_path)

    # cope with the directory existing already by ignoring that exception
    try:
        os.makedirs(os_path)
    except OSError(e):
      if e.errno != errno.EEXIST:
        raise


def add_plugin_paths():
    # ADD all IMG paths
    for img in os.getenv('IMG_PATH').split(';'):
        for img_sub in pipefunc.get_deep_folder_list(path=img, add_path=True):
            nuke.pluginAddPath(img_sub)

    # ADD sub software paths
    for paths in os.getenv('SOFTWARE_SUB_PATH').split(';'):
        nuke.pluginAddPath(paths)



#*********************************************************************
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

# RESOLUTION *********************************************************************
try:
    nuke.addFormat(RESOLUTION)
    nuke.knobDefault('Root.format', PROJECT_DATA['name'].replace(' ', ''))
    print('  {} ON  - {}'.format(chr(254), RESOLUTION))
except:
    LOG.error('  OFF - {}'.format(RESOLUTION), exc_info=True)
    print('  {} OFF - {}'.format(chr(254), RESOLUTION))

# FPS *********************************************************************
try:
    nuke.knobDefault("Root.fps", str(PROJECT_DATA['fps']))
    print('  {} ON  - {} fps'.format(chr(254), PROJECT_DATA['fps']))
except:
    LOG.error('  OFF - {} fps'.format(PROJECT_DATA['fps']), exc_info=True)
    print('  {} OFF - {} fps'.format(chr(254), PROJECT_DATA['fps']))

# createFolder *********************************************************************
try:
    nuke.addBeforeRender(create_write_dir)
    print('  {} ON  - create_write_dir (before render)'.format(chr(254)))
except:
    LOG.error('  OFF - create_write_dir (before render)'.format(chr(254)), exc_info=True)
    print('  {} OFF - create_write_dir (before render)'.format(chr(254)))

print('')

