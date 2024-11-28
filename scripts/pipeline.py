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

try:
    import yaml
except: # use included yaml: plex/lib/extern/yaml
    sys.path.append(f'{os.path.dirname(os.path.dirname(__file__))}/scripts/extern')
    import yaml

# yaml !join combines variables and strings
def join(loader, node):
        seq = loader.construct_sequence(node)
        return ''.join([str(i) for i in seq])

yaml.add_constructor('!join', join)


#*********************************************************************
class Setup(object):

    def __init__(self):
        self.scripts_path = str(pathlib.Path(os.path.dirname(__file__)).resolve())
        self.config_path = f'{os.path.dirname(self.scripts_path)}/config'
        self.pipeline_path = str(pathlib.Path(os.path.dirname(os.path.dirname(__file__))).resolve())

        # LOAD pipeline config
        self.pipeline_config = self.get_yaml_content(f'{self.config_path}/pipeline.yml')
        self.set_pipeline_env()


    def set_pipeline_env(self, project_id='default'):
        project_yaml_path = f'{self.config_path}/projects/{project_id}/project.yml'

        if not os.path.exists(project_yaml_path):
            print(f'WARNING: Set to default project. Project config doesn\'t exist: {project_yaml_path}')
            project_yaml_path = f'{self.config_path}/projects/default/project.yml'

        self.project_config = self.get_yaml_content(project_yaml_path)

        plex_paths = {'pipeline' : os.path.dirname(self.config_path),
                      
                      'config'          : f'{self.config_path}/',
                        'config_users'    : f'{self.config_path}/users/',
                        'config_user'     : f'{self.config_path}/users/{getpass.getuser()}/',
                        'config_projects' : f'{self.config_path}/projects/',
                        'config_project'  : f'{os.path.dirname(project_yaml_path)}/',

                      'img' : self.pipeline_path + '/img/',

                      'scripts' : self.scripts_path,
                        'apps'    : self.scripts_path + '/apps/',
                        'extern'  : self.scripts_path + '/extern/',

                      'software' : self.pipeline_path + '/software/',
                      }
        
        plex_context = {'project_id'   : project_id,
                        'project_name' : self.project_config['name'],
                        'admin'        : True if getpass.getuser() in self.pipeline_config['admin'] else False}

        
        os.environ['PLEX_PATHS'] = str(plex_paths)
        os.environ['PLEX_CONTEXT'] = str(plex_context)
        os.environ['SOFTWARE'] = 'software'
    
        # PATH env: Add all plex_paths
        sys.path.extend(plex_paths.values())
        # os.environ['PYTHONPATH'] += f';{path}' 

        self.__call__(plex_paths)


    def get_yaml_content(self, path):
        if os.path.exists(path):
            with open(path, 'r') as stream:
                try:   return yaml.load(stream, Loader=yaml.Loader)
                except yaml.YAMLError as exc: raise OSError ('STOP PROCESS', 'CONFIG file is corrupted', exc)
        else: 
            raise OSError ('STOP PROCESS', 'PATH doesn\'t exist', path)


    def __call__(self, plex_paths):
        from plex import Plex

        LOG = Plex().log(script=__name__)

        LOG.debug('')
        LOG.debug(200 * '_')
        LOG.debug(f"PIPELINE: {self.pipeline_config['name']} {self.pipeline_config['ver']} | PIPELINE PATHS: {plex_paths['pipeline']}")

        LOG.debug(f"PROJECT:  {self.project_config['name']} " + 
                  f"[{Plex().config_project['SETTING']['resolution'][0]} x {Plex().config_project['SETTING']['resolution'][1]} | {Plex().config_project['SETTING']['fps']}] " +
                  f"{Plex().config_project['PATH']['project']}")

        LOG.debug(200 * '-')
        LOG.debug(f"SYS_PATH: {'[%s]' % ', '.join(map(str, sys.path))}")

        plex_paths_print = ' | '.join([f'{name.upper()}_PATH: {path}' for name, path in plex_paths.items()])
        LOG.debug(plex_paths_print)


#*********************************************************************
# START
import argparse

parser = argparse.ArgumentParser(description='Setup your pipeline and start scripts.')
parser.add_argument('-so','--software', help='add software: nuke/max/maya/houdini')
parser.add_argument('-p', '--proxy', action='store_true')

args = parser.parse_args()

if args.software:
    Setup()

    if args.software == 'desktop':
        import arDesktop
        arDesktop.start()
    else:
        from plex import Plex
        Plex().start_software(args.software)
