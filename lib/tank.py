#*********************************************************************
# content   = main hub
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys
import getpass

import yaml
from Qt import QtGui

import pipefunc


#*********************************************************************
# VARIABLES
CONFIG_FORMAT = '.yml'


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

    def init_os(self):
        self.user.setup()


    def init_software(self, software=''):
        if not software:
            software = os.getenv('SOFTWARE')

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
        self.user.setup()
        self._software.start(software, open_file)
        self._software.print_header()


    @property
    def software(self):
        return self.init_software()

    @property
    def user(self):
        from users import User
        return User()

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
    def config_software(self):
        return self.get_config(f'dcc/{os.getenv("SOFTWARE")}')

    @property
    def config_script(self):
        return self.get_config('script')

    @property
    def config_notice(self):
        return self.get_config('notice')


    #*********************************************************************
    # GET AND SET CONFIG
    def get_config(self, file_name='', user_id=getpass.getuser()):

        def get_all_config():
            config_config = {}
            config_user_files    = pipefunc.get_file_list(path=self.get_env('CONFIG_USER_PATH'),    file_type='*' + CONFIG_FORMAT)
            config_project_files = pipefunc.get_file_list(path=self.get_env('CONFIG_PROJECT_PATH'), file_type='*' + CONFIG_FORMAT)

            config_project_files = list(set(config_user_files)|set(config_project_files))
            for each_file in config_project_files:
                config_config.update({each_file : self.get_config(each_file, user_id)})
                
            return config_config

        if not file_name: return get_all_config()

        file_name = file_name.split('.')[0]
        file_name = file_name.lower()
        file_path = ''

        if user_id and self.get_env('CONFIG_USER_OVERWRITE') == 'True':
            file_path = os.path.normpath(('/').join([self.get_env('CONFIG_USER_PATH'), file_name + CONFIG_FORMAT]))

        if not os.path.exists(file_path):
            file_path = os.path.normpath(('/').join([self.get_env('CONFIG_PROJECT_PATH'), file_name + CONFIG_FORMAT]))

        # OPEN config path
        if os.path.exists(file_path):
            return self.get_yml_file(file_path)
        else: print(f'CANT find file: {file_path}')
        
        return ''


    def set_config(self, path, key, value):
        if os.path.exists(path):
            tmp_content = self.get_yml_file(path)
        else:
            tmp_content = {}
            pipefunc.create_folder(path)

        tmp_content[key] = value
        self.set_yml_file(path, tmp_content)


    #*********************************************************************
    # PATH
    def get_pipeline_path(self, end_path):
        pipeline_path = os.getenv('PIPELINE_PATH')
        if not pipeline_path: return

        pipeline_path = pipeline_path.split(';')
        # find first fitting path
        for eachPath in pipeline_path:
            path = os.path.normpath(('/').join([eachPath,end_path]))

            if os.path.exists(path):
                return path

        return ''


    def get_img_path(self, end_path='btn/default', format=''):
        if '.' in end_path:
            img_format = ''
        else:
            img_format = self.config_project['EXTENSION']['icons']

        path = self.get_pipeline_path(f'img/{end_path}.{img_format}')
        if not path:
            path = self.get_pipeline_path(f'img/{os.path.dirname(end_path)}/default.{img_format}')
            if not path:
                path = self.get_pipeline_path(f'img/btn/default.{img_format}')

        if format == 'pixmap':
            return QtGui.QPixmap(QtGui.QImage(path))
        elif format == 'icon':
            return QtGui.QIcon(path)

        return path


    #*********************************************************************
    # YAML
    def set_yml_file(self, path, content):
        with open(path, 'w') as outfile:
            try:
                yaml.dump(content, outfile, default_flow_style=False)
            except yaml.YAMLError as exc:
                print(exc)


    def get_yml_file(self, path):
        try:
            with open(path, 'r') as stream:
                # STRING into DICT
                yml_content = yaml.load(stream, Loader=yaml.Loader)
                if yml_content:
                    return yml_content
                else:
                    print(f'CANT load file: {path}')

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
    #
    # @BRIEF  creates or add enviroment variable
    #
    # @PARAM  STRING var, STRING content
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
                os.environ[var] += ('').join([';', content])
            else:
                os.environ[var] = ('').join([content])

            return os.environ[var]


    # GET env or empty str & WARNING
    def get_env(self, var):
        if os.environ.__contains__(var):
            return os.environ[var].split(';')[0]
        print(f'ENV doesnt exist: {var}')

        return ''
