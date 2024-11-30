#*********************************************************************
# content   = SET default environment paths
# date      = 2024-11-16
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys
import getpass
import pathlib

sys.path.append(f'{os.path.dirname(__file__)}/extern')
import yaml

import plexfunc

# yaml !join combines variables and strings
def join(loader, node):
        seq = loader.construct_sequence(node)
        return ''.join([str(i) for i in seq])

yaml.add_constructor('!join', join)


def setup(project_id='default'):
    scripts_path = str(pathlib.Path(os.path.dirname(__file__)).resolve())
    config_path = f'{os.path.dirname(scripts_path)}/config'
    pipeline_path = str(pathlib.Path(os.path.dirname(os.path.dirname(__file__))).resolve())

    # LOAD pipeline config
    pipeline_config = plexfunc.get_yaml_content(f'{config_path}/pipeline.yml')
    project_yaml_path = f'{config_path}/projects/{project_id}/project.yml'

    if not os.path.exists(project_yaml_path):
        print(f'WARNING: Set to default project. Project config doesn\'t exist: {project_yaml_path}')
        project_yaml_path = f'{config_path}/projects/default/project.yml'

    project_config = plexfunc.get_yaml_content(project_yaml_path)

    plex_paths = {'pipeline' : os.path.dirname(config_path),
                    
                  'config'          : f'{config_path}/',
                    'config_users'    : f'{config_path}/users/',
                    'config_user'     : f'{config_path}/users/{getpass.getuser()}/',
                    'config_projects' : f'{config_path}/projects/',
                    'config_project'  : f'{os.path.dirname(project_yaml_path)}/',

                  'img' : pipeline_path + '/img/',

                  'scripts' : scripts_path,
                    'apps'    : scripts_path + '/apps/',
                    'extern'  : scripts_path + '/extern/',

                  'software' : pipeline_path + '/software/',
                  }
    
    plex_context = {'project_id'   : project_id,                                 # default
                    'project_name' : project_config['name'],                # Plex default
                    'project_path' : project_config['PATH']['project'],     # D:/project

                    'software'   : '',                                 # maya, max, nuke, houdini

                    'resolution' : project_config['SETTING']['resolution'], # [1920, 1080]
                    'fps'        : project_config['SETTING']['fps'],        # 24

                    'artist'     : getpass.getuser(),                            # arichter
                    'admin'      : True if getpass.getuser() in pipeline_config['admin'] else False,  # True or False

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

    # PATH env: Add all plex_paths
    sys.path.extend(plex_paths.values())

    from plex import Plex
    Plex().print_pipeline()


#*********************************************************************
# START
import argparse

parser = argparse.ArgumentParser(description='Setup your pipeline and start scripts.')
parser.add_argument('-so','--software', help='add software: nuke/max/maya/houdini')
parser.add_argument('-p', '--proxy', action='store_true')

args = parser.parse_args()

if args.software:
    setup()

    if args.software == 'desktop':
        import arDesktop
        arDesktop.start()
    else:
        from plex import Plex
        Plex().software.start(name=args.software)
