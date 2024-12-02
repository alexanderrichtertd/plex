# content   = plexfunc
# date      = 2024-11-25
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import glob
import time
import webbrowser

from extern import yaml


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
# YAML
def set_yaml_content(path, content):
    with open(path, 'w') as outfile:
        try:
            yaml.dump(content, outfile, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)


def get_yaml_content(path, yaml_variables={}):
    try:
        with open(path, 'r') as stream:
            # STRING into DICT
            yaml_content = str(yaml.load(stream, Loader=yaml.Loader))

            for key, value in yaml_variables.items():
                # Ignore boolean since it breaks
                if isinstance(value, bool): continue
                yaml_content = yaml_content.replace(f'${key}', f'{value}')
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
# TIME
def get_duration(func):
    """ decorator: return function duration time """
    def timed(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time

        print(f"{func.__name__} ({args}, {kwargs}) {duration:.2f} sec")
        return result

    return timed


#*********************************************************************
# ENV
def add_env(var, content):
    if not content:
        return

    # Handle lists by recursively adding each item
    if isinstance(content, list):
        for item in content:
            add_env(var, item)
        return

    content = str(content)
    os.environ[var] = os.environ.get(var, '') + (';' + content if var in os.environ else content)
    return os.environ[var]
    

#*********************************************************************
# FOLDER
def create_folder(path):
    # Ensure the path is a directory, even if a file is given
    path = os.path.dirname(path) if '.' in os.path.basename(path) else path
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f'create_folder: {path}')
        except Exception as e:
            print(f"Failed to create folder: {path}. Error: {e}")

def open_folder(path):
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
#   file_type string/string[]. '*.py'
#   extension bool. True:[name.py] False:[name]
#   exclude string /string[]. '__init__.py' | '__init__' | ['btnReport48', 'btnHelp48']
def get_files(path, file_type='*', extension=False, exclude='*', add_path=False):
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


def get_sub_dirs(path, exclude=['__pycache__'], sort=True, full_path=False):
    sub_dirs = [f.path if full_path else f.name
                    for f in os.scandir(path)
                    if f.is_dir() and os.path.basename(f.path) not in exclude]
    return sorted(sub_dirs) if sort else sub_dirs