# content   = main hub
# date      = 2024-11-25
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import sys
import getpass
import pathlib
import webbrowser

import plexfunc


class Plex(plexfunc.Singleton):
   
    # SETUP **************************************************************
    def setup(self, project_id='default'):
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
                        'apps'    : scripts_path + '/apps/',
                        'extern'  : scripts_path + '/extern/',

                      'software' : plex_path + '/software/',
                      }
        
        plex_context = {'project_id'   : project_id,                            # default
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

        # COMMENT: Avoids circular import with arDesktop
        from plex import Plex
        self.plex_print()

    def plex_print(self):
        LOG = self.log(script=__name__)

        LOG.debug('')
        LOG.debug(200 * '_')
        LOG.debug(f'PLEX:     {os.environ["PLEX_PATHS"]}')
        LOG.debug(f'CONTEXT:  {os.environ["PLEX_CONTEXT"]}')
        LOG.debug(f"SYS_PATH: {'[%s]' % ', '.join(map(str, sys.path))}")
        LOG.debug(200 * '-')


    # SOFTWARE ************************************************************
    @property
    def software(self):
        """ Get the current software object based on the environment variable.
            RETURN: software class e.g. maya_dcc.Maya()
        """
        module_name = f"{self.software_name}_dcc" if self.software_name else 'software'
        class_name = self.software_name.title() or 'Software'

        try:
            module = __import__(module_name, fromlist=[class_name])
            return getattr(module, class_name)()
        except ImportError:
            from software import Software
            return Software()

    @property
    def software_name(self):
        return self.context['software']

    @property
    def software_context(self):
        return self.software.context

    @property
    def log(self):
        import plexlog
        return plexlog.init
   
    @property
    def announcement(self):
        # announcement order: overwrite than plex or project 
        return self.config_plex['announcement'] if self.config_project['announcement'] == 'None' or self.config_plex['announcement_overwrite'] else self.config_project['announcement']
    

    # CONFIG *************************************************************
    @property
    def config(self):
        return self.get_config()

    @property
    def config_project(self):
        return self.get_config('project')
    
    @property
    def config_meta(self):
        return self.get_config('meta')
    
    @property
    def config_plex(self):
        return self.get_config(file_name='plex', file_dir=self.paths['config'])

    @property
    def config_software(self):
        return self.get_config(f'software/{self.software_name}')


    # CONFIG: Get & Set **************************************************
    def get_config(self, file_name='', file_dir='', user_id=getpass.getuser()):
        if not file_dir: file_dir = self.paths['config_project']
        file_dir = file_dir.split('.')[0]

        def get_all_config():
            configs = {}
            config_project_files = plexfunc.get_files(path=file_dir, file_type='*' + '.yml')

            for each_file in config_project_files:
                configs.update({each_file : self.get_config(each_file, file_dir, user_id)})
                
            return configs

        if not file_name: return get_all_config()

        file_name = file_name.split('.')[0].lower()
        file_path = os.path.normpath(f'{file_dir}/{file_name}.yml')

        # OPEN config path
        if os.path.exists(file_path):
            # self.LOG.debug(plexfunc.get_yaml_content(file_path, self.paths))
            return plexfunc.get_yaml_content(file_path, (self.paths | self.context))
        else: 
            print(f"CAN'T find file: {file_path}")
        
        return ''


    def set_config(self, path, key, value):
        if os.path.exists(path):
            tmp_content = plexfunc.get_yaml_content(path, self.paths)
        else:
            tmp_content = {}
            plexfunc.create_dir(path)

        tmp_content[key] = value
        plexfunc.set_yaml_content(path, tmp_content)


    def get_img_path(self, end_path='btn/default'):
        img_format = '' if '.' in end_path else '.png'

        path = f'{self.paths["plex"]}/img/{end_path}{img_format}' or \
               f'{self.paths["plex"]}/img/{os.path.dirname(end_path)}/default{img_format}' or \
               f'{self.paths["plex"]}/img/btn/default{img_format}'

        return path


    # PLEX ***************************************************************
    @property
    def paths(self):
        return eval(os.environ['PLEX_PATHS'])
    
    @property
    def context(self):
        return eval(os.environ['PLEX_CONTEXT'])
    
    def set_context(self, key, value):
        context = eval(os.environ['PLEX_CONTEXT'])
        context[key] = value
        os.environ['PLEX_CONTEXT'] = str(context)


    # PROJECT ************************************************************    
    @property
    def project_names(self):
        projects_path = self.paths['config_projects']
        return [os.path.basename(f.path) for f in os.scandir(projects_path) if f.is_dir()]
    
    
    # USER ***************************************************************  
    @property
    def user_id(self):
        return getpass.getuser()
    
    @property
    def admin(self):
        return eval(os.environ['PLEX_CONTEXT'])['admin']
   
    @property    
    def user_sandbox(self):
        user_sandbox_path = f'{self.config_project["PATH"]["sandbox"]}/{self.user_id}'
        plexfunc.create_dir(user_sandbox_path)
        return user_sandbox_path


    # BUTTON **************************************************************
    def report(self):
        self.help('report')

    def help(self, name=''):
        name = name or self.software_name
        webbrowser.open(self.config_project['URL'].get(name, self.config_project['URL']['default']))


# START **************************************************************
import argparse

parser = argparse.ArgumentParser(description='Setup your plex and start scripts.')
parser.add_argument('-s','--software', help='add software: nuke/max/maya/houdini')
args = parser.parse_args()

if args.software:
    Plex().setup()

    if args.software == 'desktop':
        import arDesktop
        arDesktop.start()
    else:
        Plex().software.start(name=args.software)