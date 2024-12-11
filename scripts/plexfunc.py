# content   = plexfunc
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import glob
import time
import webbrowser

from extern import yaml

# define & register custom tag handler
# combine var with strings
def join(loader, node):
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])

yaml.add_constructor('!join', join)


# SINGLETON ***************************************************************
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


# YAML ***************************************************************
def set_yaml_content(path, content):
    if not os.path.exists(path):
        return False

    try:
        def format_value(value):
            if isinstance(value, (list, dict)):
                return value
            value_str = str(value).strip()
            return f'"{value_str}"' if any(c in value_str for c in '{}') else value_str

        with open(path, 'r') as f:
            lines = f.readlines()

        updates = {}
        sections = set()
        def flatten_dict(d, prefix=''):
            for k, v in d.items():
                full_key = f"{prefix}{k}" if prefix else k
                if isinstance(v, dict):
                    sections.add(full_key)
                    flatten_dict(v, f"{full_key}/")
                else:
                    updates[full_key] = v

        flatten_dict(content)

        output = []
        section_stack = []
        last_line_empty = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.lstrip()
            indent = len(line) - len(stripped)

            if not stripped or stripped.startswith('#'):
                if stripped or not last_line_empty:
                    output.append(line)
                    last_line_empty = not stripped
                i += 1
                continue

            if ':' in stripped:
                key = stripped.split(':', 1)[0].strip()

                while section_stack and len(section_stack[-1][1]) >= indent:
                    section_stack.pop()
                
                current_path = '/'.join([s[0] for s in section_stack] + [key])
                section_stack.append((key, ' ' * indent))

                if '&' in line or '*' in line or '!join' in line:
                    output.append(line)
                    last_line_empty = False
                    i += 1
                    continue

                if current_path in sections:
                    output.append(line)
                    last_line_empty = False
                elif current_path in updates:
                    value = updates[current_path]
                    if isinstance(value, list):
                        output.append(f"{' ' * indent}{key}:\n")
                        for item in value:
                            item_str = format_value(item)
                            output.append(f"{' ' * (indent + 4)}- {item_str}\n")
                        last_line_empty = False
                        i += 1
                        while i < len(lines) and (lines[i].strip().startswith('-') or not lines[i].strip()):
                            i += 1
                        continue
                    else:
                        value_str = format_value(value)
                        output.append(f"{' ' * indent}{key}: {value_str}\n")
                        last_line_empty = False
                        i += 1
                        continue

            i += 1

        if output and not output[-1].endswith('\n'):
            output.append('\n')

        with open(path, 'w') as f:
            f.writelines(output)
        return True

    except Exception as exc:
        print(f"Failed to write YAML: {exc}")
        return False


def get_yaml_content(path, yaml_variables={}):
    try:
        with open(path, 'r') as stream:
            # Load YAML and convert None to empty string
            yaml_content = yaml.load(stream, Loader=yaml.Loader)
            
            def convert_none_to_empty(d):
                if isinstance(d, dict):
                    return {k: convert_none_to_empty(v) for k, v in d.items()}
                elif isinstance(d, list):
                    return [convert_none_to_empty(x) for x in d]
                else:
                    return '' if d is None else d

            yaml_content = convert_none_to_empty(yaml_content)

            if yaml_variables:
                content_str = str(yaml_content)
                for key, value in yaml_variables.items():
                    if isinstance(value, bool): continue
                    content_str = content_str.replace(f'${key}', f'{value}')
                yaml_content = yaml.safe_load(content_str)

            return yaml_content or {}

    except yaml.YAMLError as exc:
        print(exc)
        return {}


# TIME ***************************************************************
def get_duration(func):
    """ decorator: return function duration time """
    def timed(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time

        print(f"{func.__name__} ({args}, {kwargs}) {duration:.2f} sec")
        return result

    return timed


# ENV ***************************************************************
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
    

# DIRECTORY ***************************************************************
def create_dir(path):
    # Ensure the path is a directory, even if a file is given
    path = os.path.dirname(path) if '.' in os.path.basename(path) else path
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f'create_dir: {path}')
        except Exception as e:
            print(f"Failed to create dir: {path}. Error: {e}")

def open_dir(path):
    path = os.path.normpath(path)

    if os.path.exists(path):
        # Open dir if the path points to a file
        if '.' in os.path.basename(path):
            path = os.path.dirname(path)
        webbrowser.open(path)
    else:
        print(f"Invalid path: {path}")

    return path

def get_sub_dirs(path, exclude=['__pycache__'], sort=True, full_path=False):
    sub_dirs = [f.path if full_path else f.name
                    for f in os.scandir(path)
                    if f.is_dir() and os.path.basename(f.path) not in exclude]
    return sorted(sub_dirs) if sort else sub_dirs


# FILES ***************************************************************
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