#*********************************************************************
# content   = main hub
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import getpass

import yaml
from Qt import QtGui

import pipefunc


#*********************************************************************
# SINGLETON
class Singleton(object):
    def __new__(cls, *args, **kwds):

        self = "__self__"
        if not hasattr(cls, self):
            instance = object.__new__(cls)
            instance.init(*args, **kwds)
            setattr(cls, self, instance)
        return getattr(cls, self)

    def init(self, *args, **kwds):
        pass


#*********************************************************************
# CLASS
class Tank(Singleton):
    _software = ''

    def init_software(self, software=''):
        if not software: software = os.getenv('SOFTWARE')

        if not self._software:
            if software == 'maya':
                from maya_dcc import Maya
                self._software = Maya()
            elif software == 'max':
                from max_dcc import Max
                self._software = Max()
            elif software == 'nuke':
                from nuke_dcc import Nuke
                self._software = Nuke()
            elif software == 'houdini':
                from houdini_dcc import Houdini
                self._software = Houdini()
            else:
                from software import Software
                self._software = Software()

        return self._software


    def start_software(self, software, open_file=''):
        from software import Software

        self._software = Software()
        self._software.setup()
        self._software.start(software, open_file)
        self._software.print_header()


    @property
    def software(self):
        return self.init_software()

    @property
    def context(self):
        return self.software.context

    @property
    def log(self):
        import pipelog
        return pipelog


    #*********************************************************************
    # CONFIG
    @property
    def config(self):
        return self.get_config()

    @property
    def config_project(self):
        return self.get_config('project')
    
    @property
    def config_pipeline(self):
        return self.get_config(file_name='pipeline', file_dir=self.plex_paths['config'])

    @property
    def config_software(self):
        return self.get_config(f'software/{self.software.name}')

    @property
    def config_notice(self):
        return self.get_config('notice')

    @property
    def config_announcement(self):
        return self.config_pipeline['announcement'] if self.config_project['announcement'] == 'None' or self.config_pipeline['announcement_overwrite'] else self.config_project['announcement']
        # return self.config_pipeline['announcement_overwrite'] and self.config_pipeline['announcement'] or self.config_project['announcement']
    

    #*********************************************************************
    # PLEX
    @property
    def plex_paths(self):
        return eval(os.environ['PLEX_PATHS'])
    
    @property
    def plex_context(self):
        return eval(os.environ['PLEX_CONTEXT'])

    @property
    def admin(self):
        return eval(os.environ['PLEX_CONTEXT'])['admin']
   
   
    #*********************************************************************
    # PROJECT    
    @property
    def project_names(self):
        projects_path = Tank().plex_paths['config_projects']
        return [os.path.basename(f.path) for f in os.scandir(projects_path) if f.is_dir()]

    @property
    def user_id(self):
        return getpass.getuser()
    
    @property    
    def user_sandbox(self):
        return f'{self.config_project["PATH"]["sandbox"]}/{self.user_id}'
    

    #*********************************************************************
    # GET AND SET CONFIG
    def get_config(self, file_name='', file_dir='', user_id=getpass.getuser()):
        if not file_dir: file_dir = self.plex_paths['config_project']
        file_dir = file_dir.split('.')[0]

        def get_all_config():
            configs = {}
            config_project_files = pipefunc.get_file_list(path=file_dir, file_type='*' + '.yml')

            for each_file in config_project_files:
                configs.update({each_file : self.get_config(each_file, file_dir, user_id)})
                
            return configs

        if not file_name: return get_all_config()

        file_name = file_name.split('.')[0].lower()
        file_path = os.path.normpath(f'{file_dir}/{file_name}.yml')

        # OPEN config path
        if os.path.exists(file_path):
            return self.get_yaml_file(file_path)
        else: 
            print(f"CAN'T find file: {file_path}")
        
        return ''


    def set_config(self, path, key, value):
        if os.path.exists(path):
            tmp_content = self.get_yaml_file(path)
        else:
            tmp_content = {}
            pipefunc.create_folder(path)

        tmp_content[key] = value
        self.set_yaml_file(path, tmp_content)


    def get_img_path(self, end_path='btn/default'):
        img_format = '' if '.' in end_path else '.png'

        path = f'{self.plex_paths["pipeline"]}/img/{end_path}{img_format}' or \
               f'{self.plex_paths["pipeline"]}/img/{os.path.dirname(end_path)}/default{img_format}' or \
               f'{self.plex_paths["pipeline"]}/img/btn/default{img_format}'

        return path


    #*********************************************************************
    # YAML
    def set_yaml_file(self, path, content):
        with open(path, 'w') as outfile:
            try:
                yaml.dump(content, outfile, default_flow_style=False)
            except yaml.YAMLError as exc:
                print(exc)


    def get_yaml_file(self, path):
        try:
            with open(path, 'r') as stream:
                # STRING into DICT
                yaml_content = str(yaml.load(stream, Loader=yaml.Loader))

                for key, value in self.plex_paths.items():
                    yaml_content = yaml_content.replace(f'${key}', value)
                yaml_content = yaml.safe_load(yaml_content)

                if yaml_content:
                    return yaml_content
                else:
                    print(f"CAN'T load file: {path}")

        except yaml.YAMLError as exc:
            print(exc)


    # define & register custom tag handler
    # combine var with strings
    def join(loader, node):
        seq = loader.construct_sequence(node)
        return ''.join([str(i) for i in seq])


    # replace (multiple) ENV var
    def env(loader, node):
        seq  = loader.construct_sequence(node)
        path = os.getenv(seq[0])
        seq.pop(0)

        if not path: return ''
        path = path.split(';')

        new_env = ''
        for env in path:
            if new_env: new_env += ';'
            new_env += env
            if seq: new_env += ''.join([str(os.path.normpath(i)) for i in seq])

        return new_env


    # replace (multiple) with first ENV var
    def env_first(loader, node):
        seq  = loader.construct_sequence(node)
        path = os.getenv(seq[0])

        if ';' in path: path = path.split(';')[0]
        seq.pop(0)

        if seq: path += ''.join([str(os.path.normpath(i)) for i in seq])
        return path

    yaml.add_constructor('!env', env)
    yaml.add_constructor('!env_first', env_first)
    yaml.add_constructor('!join', join)


    #*********************************************************************
    # ENV
    def add_env(self, var, content):
        if not content: return

        # CHECK for list
        if isinstance(content, list):
            for item in content:
                self.add_env(var, item)
        else:
            content = str(content)

            # CHECK empty
            if os.environ.__contains__(var):
                os.environ[var] += ''.join([';', content])
            else:
                os.environ[var] = ''.join([content])

            return os.environ[var]
