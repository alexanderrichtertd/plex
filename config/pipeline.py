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

try:
    import yaml
except: # use included yaml: plex/lib/extern/yaml
    plex_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(plex_path + "/lib/extern")
    import yaml

# yaml !join combines variables and strings
def join(loader, node):
        seq = loader.construct_sequence(node)
        return ''.join([str(i) for i in seq])

yaml.add_constructor('!join', join)


#*********************************************************************
class Setup(object):

    def __init__(self):
        self.config_path = os.path.dirname(__file__)
        self.pipeline_path = os.path.dirname(os.path.dirname(__file__))

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
                      'img'      : self.pipeline_path + '/img/',
                      'lib'      : self.pipeline_path + '/lib/',
                      'apps'     : self.pipeline_path + '/lib/apps/',
                      'dcc'      : self.pipeline_path + '/lib/dcc/',
                      'extern'   : self.pipeline_path + '/lib/extern/',
                      'software' : self.pipeline_path + '/software/',

                      'config'          : f'{self.config_path}/',
                      'config_projects' : f'{os.path.dirname(os.path.dirname(project_yaml_path))}/',
                      'config_project'  : f'{os.path.dirname(project_yaml_path)}/',
                      'config_users'    : f'{self.config_path}/users/',
                      'config_user'     : f'{self.config_path}/users/{getpass.getuser()}/'}
        
        plex_context = {'project_id'   : project_id,
                        'project_name' : self.project_config['name'],
                        'project_path' : self.project_config['PATH']['project'],
                        'admin'        : True if getpass.getuser() in self.pipeline_config['admin'] else False}


        # SET project name
        os.environ['PROJECT_NAME'] = self.project_config['name']     # TODO: Replace and delete
        os.environ['SOFTWARE_SRC_PATH'] = plex_paths['software']     # TODO: Needed?
        
        os.environ['PLEX_PATHS'] = str(plex_paths)
        os.environ['PLEX_CONTEXT'] = str(plex_context)
    
        # ADD all plex_paths to PATH
        for key, path in plex_paths.items():
            sys.path.append(path)


        # TODO: Needed to add to PYTHONPATH?
        # self.add_env('PYTHONPATH', ';'.join(plex_paths['img']))

        self.__call__(plex_paths)


    def add_env(self, var, content):
        content = os.path.normpath(content)
        if os.environ.__contains__(var):
              os.environ[var] += ''.join([';', content])
        else: os.environ[var] = content

        return os.getenv(var)

    def get_yaml_content(self, path):
        if os.path.exists(path):
            with open(path, 'r') as stream:
                try:   return yaml.load(stream, Loader=yaml.Loader)
                except yaml.YAMLError as exc: raise OSError ('STOP PROCESS', 'CONFIG file is corrupted', exc)
        else: 
            raise OSError ('STOP PROCESS', 'PATH doesn\'t exist', path)

    def __call__(self, plex_paths):
        from tank import Tank

        LOG = Tank().log.init(script=__name__)

        LOG.debug('')
        LOG.debug(200 * '_')
        LOG.debug(f"PIPELINE: {self.pipeline_config['name']} {self.pipeline_config['version']} | PIPELINE PATHS{plex_paths['pipeline']} | \
user_config_overwrite[{plex_paths['config_user'] if plex_paths['config_user'] else 'NO user overwrite'}]")

        LOG.debug(f"PROJECT:  {self.project_config['name']} \
[{Tank().config_project['SETTING']['resolution'][0]} x {Tank().config_project['SETTING']['resolution'][1]} | {Tank().config_project['SETTING']['fps']}] \
[{self.project_config['PATH']['project'] if os.path.exists else 'NOT existing: '}{os.path.normpath(self.project_config['PATH']['project'])}]")

        LOG.debug(200 * '-')
        LOG.debug(f"SYS_PATH: {'[%s]' % ', '.join(map(str, sys.path))}")
        LOG.debug(f"PIPELINE_PATH: {plex_paths['pipeline']} | IMG_PATH: {plex_paths['img']} | LIB_PATH: {plex_paths['lib']} | " +
                  f"APPS_PATH: {plex_paths['lib']} | DCC_PATH: {plex_paths['dcc']} | SOFTWARE_PATH: {plex_paths['software']} | " +
                  f"CONFIG_PROJECT_PATH: {plex_paths['config_project']}")


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
        from tank import Tank
        Tank().start_software(args.software)
