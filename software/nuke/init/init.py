# content   = init Nuke
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import errno

import nuke

import plexfunc
import plex


# VARIABLE ***************************************************************
LOG = plex.log(script=__name__)

PROJECT_CONFIG = plex.config['project']
RESOLUTION   = ' '.join([str(PROJECT_CONFIG['resolution'][0]),
                            str(PROJECT_CONFIG['resolution'][1]),
                            PROJECT_CONFIG['name'].replace(' ', '')])


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
        for img_sub in plexfunc.get_sub_dirs(path=img, full_path=True):
            nuke.pluginAddPath(img_sub)

    # ADD sub software paths
    for path in os.getenv('SOFTWARE_PATH').split(';'):
        nuke.pluginAddPath(path)



# PIPELINE ***************************************************************
plex.init_software()
add_plugin_paths()

try:    from scripts import write_node
except: LOG.warning('FAILED loading write_node')

# LOAD paths
try:
    for paths in os.getenv('SOFTWARE_PATH').split(';'):
        nuke.pluginAddPath(paths)
except:
    LOG.warning('FAILED loading SOFTWARE_PATH')



print('SETTINGS')

# RESOLUTIONs
try:
    nuke.addFormat(RESOLUTION)
    nuke.knobDefault('Root.format', PROJECT_CONFIG['name'].replace(' ', ''))
    print(f'  {chr(254)} ON  - {RESOLUTION}')
except:
    LOG.error(f'  OFF - {RESOLUTION}', exc_info=True)
    print(f'  {chr(254)} OFF - {RESOLUTION}')


# FPS
try:
    nuke.knobDefault("Root.fps", str(PROJECT_CONFIG['fps']))
    print(f'  {chr(254)} ON  - {PROJECT_CONFIG['fps']} fps')
except:
    LOG.error(f'  OFF - {PROJECT_CONFIG['fps']} fps', exc_info=True)
    print(f'  {chr(254)} OFF - {PROJECT_CONFIG['fps']} fps')


# createFolder
try:
    nuke.addBeforeRender(create_write_dir)
    print(f'  {chr(254)} ON  - create_write_dir (before render)')
except:
    LOG.error('  OFF - create_write_dir (before render)', exc_info=True)
    print(f'  {chr(254)} OFF - create_write_dir (before render)')

print('')