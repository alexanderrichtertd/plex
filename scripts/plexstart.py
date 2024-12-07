# content   = plex startup
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import sys
import pathlib
import getpass

import plex
import plexfunc

from extern.Qt import QtWidgets, QtCore
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)


# SETUP **************************************************************
def setup(project_id='default'):
    scripts_path = str(pathlib.Path(os.path.dirname(__file__)).resolve())
    config_path = f'{os.path.dirname(scripts_path)}/config'
    plex_path = str(pathlib.Path(os.path.dirname(os.path.dirname(__file__))).resolve())
    
    # LOAD plex config
    plex_config = plexfunc.get_yaml_content(f'{config_path}/plex.yml')
    project_yaml_path = f'{config_path}/projects/{project_id}/project.yml'

    if not os.path.exists(project_yaml_path):
        print(f'WARNING: Set to default project. Project config doesn\'t exist: {project_yaml_path}')
        project_yaml_path = f'{config_path}/projects/default/project.yml'
    
    project_config = plexfunc.get_yaml_content(project_yaml_path)

    plex_paths = {'plex' : os.path.dirname(config_path),
                    
                  'config'          : f'{config_path}/',
                    'config_users'    : f'{config_path}/users/',
                    'config_user'     : f'{config_path}/users/{getpass.getuser()}/',
                    'config_projects' : f'{config_path}/projects/',
                    'config_project'  : f'{os.path.dirname(project_yaml_path)}/',

                  'img' : plex_path + '/img/',

                  'scripts' : scripts_path,
                  'plugins' : scripts_path + '/plugins/',
                  'extern'  : scripts_path + '/extern/',

                  'software' : plex_path + '/software/',
                  }
    
    plex_context = {'name'         : plex_config['name'],           # Plex
                    'description'  : plex_config['description'],    # Open Source Pipeline
                    'version'      : plex_config['version'],        # 2.5.0.
                    'credit'       : plex_config['credit'],         # Alexander Richter

                    'announcement_overwrite' : plex_config['announcement_overwrite'],
                    'announcement' : plex_config['announcement'],
        
                    'project_id'   : project_id,                            # default
                    'project_name' : project_config['name'],                # Plex default
                    'project_path' : project_config['PATH']['project'],     # D:/project

                    'software'   : '',                                      # maya, max, nuke, houdini

                    'resolution' : project_config['SETTING']['resolution'], # [1920, 1080]
                    'fps'        : project_config['SETTING']['fps'],        # 24

                    'artist'     : getpass.getuser(),                       # arichter
                    'admin'      : True if getpass.getuser() in plex_config['admin'] else False,  # True or False

                    'file_name'       : '', # mike_RIG_v012
                    'file_path'       : '', # D:/project/asset/mike_RIG_v012.mb
                    'file_extension'  : '', # mb

                    'step'       : '',      # shots or assets or renders
                    'scene'      : '',      # s010 or mike
                    'task'       : '',      # ANIMATION
                    'status'     : '',      # WORK or PUBLISH
                    }

    
    os.environ['PLEX_PATHS'] = str(plex_paths)
    os.environ['PLEX_CONTEXT'] = str(plex_context)

    # PATH env: Add plex_paths
    sys.path.extend(plex_paths.values())

    plex_print()    


def plex_print():
    LOG = plex.log(script=__name__)

    LOG.debug('')
    LOG.debug(200 * '_')
    LOG.debug(f'PLEX:     {os.environ["PLEX_PATHS"]}')
    LOG.debug(f'CONTEXT:  {os.environ["PLEX_CONTEXT"]}')
    LOG.debug(f"SYS_PATH: {'[%s]' % ', '.join(map(str, sys.path))}")
    LOG.debug(200 * '-')


def show_splashscreen():
    app = QtWidgets.QApplication.instance()
    if not app:  
        app = QtWidgets.QApplication(sys.argv)

    import arSplash
    splash = arSplash.arSplash()
    
    # Process events until splash closes
    while splash.wgSplash.isVisible():
        app.processEvents()
        
    return app


# START **************************************************************
import argparse

parser = argparse.ArgumentParser(description='Setup your Plex and start software.')
parser.add_argument('-s','--software', help='start software: desktop/nuke/max/maya/houdini')
args = parser.parse_args()

if args.software:
    setup()
    app = show_splashscreen()
    
    if args.software == 'desktop':
        import arDesktop
        arDesktop.start()
    else:
        plex.software.start(name=args.software)
    
    sys.exit(0)