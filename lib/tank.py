#*********************************************************************
# content   = main hub
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import glob
import time
import yaml
import getpass
import webbrowser


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

    def init_software(self, name=''):
        name = name or os.getenv('SOFTWARE') or 'software'

        if not self._software:
            # e.g. maya_dcc Maya
            module_name = f'{name}_dcc' if name != 'software' else 'software'
            class_name = name.title() 

            module = __import__(module_name, fromlist=[class_name])
            self._software = getattr(module, class_name)()

        return self._software


    def start_software(self, software, open_file=''):
        from software import Software
        self._software = Software()
        self._software.start(software, open_file)

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
    
    @property
    def LOG(self):
        return self.log.init(script=__name__)


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
        projects_path = self.plex_paths['config_projects']
        return [os.path.basename(f.path) for f in os.scandir(projects_path) if f.is_dir()]

    @property
    def user_id(self):
        return getpass.getuser()
    
    @property    
    def user_sandbox(self):
        user_sandbox_path = f'{self.config_project["PATH"]["sandbox"]}/{self.user_id}'
        if not os.path.exists(user_sandbox_path): os.makedirs(user_sandbox_path)
        return user_sandbox_path
    

    #*********************************************************************
    # GET AND SET CONFIG
    def get_config(self, file_name='', file_dir='', user_id=getpass.getuser()):
        if not file_dir: file_dir = self.plex_paths['config_project']
        file_dir = file_dir.split('.')[0]

        def get_all_config():
            configs = {}
            config_project_files = self.get_file_list(path=file_dir, file_type='*' + '.yml')

            for each_file in config_project_files:
                configs.update({each_file : self.get_config(each_file, file_dir, user_id)})
                
            return configs

        if not file_name: return get_all_config()

        file_name = file_name.split('.')[0].lower()
        file_path = os.path.normpath(f'{file_dir}/{file_name}.yml')

        # OPEN config path
        if os.path.exists(file_path):
            # print(self.get_yaml_content(file_path))
            return self.get_yaml_content(file_path)
        else: 
            print(f"CAN'T find file: {file_path}")
        
        return ''


    def set_config(self, path, key, value):
        if os.path.exists(path):
            tmp_content = self.get_yaml_content(path)
        else:
            tmp_content = {}
            self.create_folder(path)

        tmp_content[key] = value
        self.set_yaml_content(path, tmp_content)


    def get_img_path(self, end_path='btn/default'):
        img_format = '' if '.' in end_path else '.png'

        path = f'{self.plex_paths["pipeline"]}/img/{end_path}{img_format}' or \
               f'{self.plex_paths["pipeline"]}/img/{os.path.dirname(end_path)}/default{img_format}' or \
               f'{self.plex_paths["pipeline"]}/img/btn/default{img_format}'

        return path


    #*********************************************************************
    # YAML
    def set_yaml_content(self, path, content):
        with open(path, 'w') as outfile:
            try:
                yaml.dump(content, outfile, default_flow_style=False)
            except yaml.YAMLError as exc:
                print(exc)


    def get_yaml_content(self, path):
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

    yaml.add_constructor('!join', join)


    #*********************************************************************
    # ENV
    def add_env(self, var, content):
        if not content:
            return

        # Handle lists by recursively adding each item
        if isinstance(content, list):
            for item in content:
                self.add_env(var, item)
            return

        content = str(content)
        os.environ[var] = os.environ.get(var, '') + (';' + content if var in os.environ else content)
        return os.environ[var]


    def report(self):
        self.help('report')


    def help(self, name=''):
        name = name or os.getenv('SOFTWARE', name)
        project_help = self.config_project['URL']
        webbrowser.open(project_help.get(name, project_help['default']))


    # GET all (sub) keys in dict
    def get_all_keys(self, key_list, dictonary=[]):
        for key, items in key_list.items():
            dictonary.append(key)
            if isinstance(items, dict):
                self.get_all_keys(items, dictonary)

        return dictonary


    # decorator: return function duration time
    def get_duration(self, func):
        def timed(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start_time

            print(f"{func.__name__} ({args}, {kwargs}) {duration:.2f} sec")
            return result

        return timed


    #*********************************************************************
    # creates a folder, checks if it already exists,
    def create_folder(self, path):
        # Ensure the path is a directory, even if a file is given
        path = os.path.dirname(path) if '.' in os.path.basename(path) else path
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                print(f"Failed to create folder: {path}. Error: {e}")

    def open_folder(self, path):
        path = os.path.normpath(path)

        if os.path.exists(path):
            # Open folder if the path points to a file
            if '.' in os.path.basename(path):
                path = os.path.dirname(path)
            webbrowser.open(path)
        else:
            print(f"Invalid path: {path}")

        return path


    #*********************************************************************
    # FILES
    # @BRIEF  get a file/folder list with specifics
    #
    # @PARAM  path string.
    #         file_type string/string[]. '*.py'
    #         extension bool. True:[name.py] False:[name]
    #         exclude string /string[]. '__init__.py' | '__init__' | ['btnReport48', 'btnHelp48']
    #
    # @RETURN strint[].
    def get_file_list(self, path, file_type='*', extension=False, exclude='*', add_path=False):
        if os.path.exists(path):
            get_file = []
            try:    os.chdir(path)
            except: print(f'Invalid dir: {path}')

            for file_name in glob.glob(file_type):
                if exclude in file_name: continue
                if add_path:  file_name = os.path.normpath('/'.join([path, file_name]))

                if extension: get_file.append(file_name)
                else:         get_file.append((file_name.split('.')[0]))

            return get_file


    # GET all subfolders in the path
    def get_deep_dirs(self, path, full_path=False):
        if full_path: get_file = map(lambda x: x[0], os.walk(path))
        else:         get_file = map(lambda x: os.path.basename(x[0]), os.walk(path))

        try:    get_file.pop(0)
        except: print(f"CAN'T pop file. Path: {path}")

        return get_file

    def get_sub_dirs(self, path, exclude=['__pycache__'], sort=True, full_path=False):
        sub_dirs = [f.path if full_path else f.name
                     for f in os.scandir(path)
                     if f.is_dir() and os.path.basename(f.path) not in exclude]
        return sorted(sub_dirs) if sort else sub_dirs