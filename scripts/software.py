#*********************************************************************
# content   = setup software attributes
# date      = 2024-11-23
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys
import getpass
import subprocess

import pipefunc
from tank import Tank

LOG = Tank().log(script=__name__)


#*********************************************************************
# CLASS
class Software(pipefunc.Singleton):
    def start(self, name='', open_file=''):
        os.environ['SOFTWARE'] = name

        # SETUP env
        software_dirs = pipefunc.get_sub_dirs(self.path, full_path=True)

        os.environ['SOFTWARE_PATH'] = ';'.join(software_dirs)
        # PYTHONPATH important for software imports
        os.environ['PYTHONPATH'] = ';'.join([
            os.environ.get('PYTHONPATH', ''),
            *software_dirs,
            f'{Tank().paths["software"]}/{self.name}',
            Tank().paths["scripts"],
            Tank().paths["apps"],
            Tank().paths["extern"],
            # Tank().paths["software"]
            ])        

        sys.path.extend(software_dirs)

        # GET software config
        self.env = Tank().config_software.get('ENV', '')

        # ADD software ENV
        for env, content in self.env.items():
            if isinstance(content, list):
                [pipefunc.add_env(env, each) for each in content]
            else:
                pipefunc.add_env(env, content)

        if open_file: open_file = f'"{open_file}"'
        cmd = Tank().config_software['start'].format(open_file)
        subprocess.Popen(cmd, shell=True, env=os.environ)

        LOG.debug(f'{self.name.upper()}{20 * "-"}')
        LOG.debug(cmd)
        self.print_header()


    #*********************************************************************
    # VARIABLES
    @property
    def id(self):
        return id(self)
    
    @property
    def name(self):
        return os.environ.get('SOFTWARE', 'software')
   
    @property
    def path(self):        
        return f'{Tank().paths["software"]}/{self.name}'

    @property
    def config(self):
        return Tank().config_software

    @property
    def extension(self):
        return Tank().config_project['EXTENSION'][self.name]

    @property
    def menu(self):
        return Tank().config_software['MENU']
    
    @property
    def version(self):
        return Tank().config_software['version']
    
    @property
    def renderer(self):
        return Tank().config_software.get('renderer', '')
        
    @property
    def renderer_path(self):        
        return Tank().config_software.get('renderer_path', '')


    #*********************************************************************
    # FUNCTION
    def is_software(self, software_name):
        return self.name == software_name
    
    def create_menu(self):
        print('NO menu create')

    def delete_menu(self):
        print('NO menu deleted')


    @property
    def scene_path(self):
        print('NO scene_path software override found')

    def scene_save(self):
        print('NO scene_save software override found')

    def scene_save_as(self, file):
        print('NO scene_save_as software override found')

    def scene_open(self, file):
        print('NO scene_open software override found')

    def scene_import(self, file):
        print('NO scene_import software override found')


    #*********************************************************************
    # PRINT
    def print_header(self):
        if self.is_software('max'): return

        project_len = len(Tank().context['project_name'])
        space = (20-int(project_len/2)) - 1

        # project name
        print('')
        print(chr(124) + '-' * (2 * space + project_len) + chr(124))
        print(chr(124) + ' ' * space + Tank().context['project_name'] + ' ' * space + chr(124))
        print(chr(124) + '-' * (2 * space + project_len) + chr(124))

        # user name & software
        space = (21-int(len('Welcome ' + getpass.getuser())/2)) - 1
        print(' ' * space + 'Welcome ' + getpass.getuser())
        print('')
        space = (20-int(len(f'{self.name} {self.version}')/2)) - 1
        print(' ' * space + f'{self.name.title()} {self.version}')

        print(f'\n\n{Tank().paths["pipeline"]}')
        print('\n• img')
        print('• lib')
        print(r'• lib\apps')
        print(r'• lib\extern')

        print(f'\n• config\\projects\\{Tank().context["project_id"]}\n')

        print(fr'• software\{self.name}')
        for sub_dir in pipefunc.get_sub_dirs(self.path):
            print(fr'• software\{self.name}\{sub_dir}')

        print('')

        LOG.debug(f'SOFTWARE: {self.name} {self.version} - {self.path}\nENV: {self.env}')
        LOG.debug(f'PYTHONPATH: {os.environ["PYTHONPATH"]}')
