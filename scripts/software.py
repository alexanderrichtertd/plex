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
from plex import Plex

LOG = Plex().log(script=__name__)


#*********************************************************************
# CLASS
class Software(pipefunc.Singleton):
    def start(self, name='', open_file=''):
        Plex().set_context('software', name)

        # SETUP env
        software_dirs = pipefunc.get_sub_dirs(self.path, full_path=True)

        os.environ['SOFTWARE_PATH'] = ';'.join(software_dirs)
        # PYTHONPATH important for software imports
        os.environ['PYTHONPATH'] = ';'.join([
            os.environ.get('PYTHONPATH', ''),
            *software_dirs,
            f'{Plex().paths["software"]}/{self.name}',
            Plex().paths["scripts"],
            Plex().paths["apps"],
            Plex().paths["extern"],
            ])        

        sys.path.extend(software_dirs)

        # GET software config
        self.env = Plex().config_software.get('ENV', '')

        # ADD software ENV
        for env, content in self.env.items():
            if isinstance(content, list):
                [pipefunc.add_env(env, each) for each in content]
            else:
                pipefunc.add_env(env, content)

        if open_file: open_file = f'"{open_file}"'
        cmd = Plex().config_software['start'].format(open_file)
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
        return Plex().context['software']
   
    @property
    def path(self):        
        return f'{Plex().paths["software"]}/{self.name}'

    @property
    def config(self):
        return Plex().config_software

    @property
    def extension(self):
        return Plex().config_project['EXTENSION'][self.name]

    @property
    def menu(self):
        return Plex().config_software['MENU']
    
    @property
    def version(self):
        return Plex().config_software['version']
    
    @property
    def renderer(self):
        return Plex().config_software.get('renderer', '')
        
    @property
    def renderer_path(self):        
        return Plex().config_software.get('renderer_path', '')


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

        project_len = len(Plex().context['project_name'])
        space = (20-int(project_len/2)) - 1

        # project name
        print('')
        print(chr(124) + '-' * (2 * space + project_len) + chr(124))
        print(chr(124) + ' ' * space + Plex().context['project_name'] + ' ' * space + chr(124))
        print(chr(124) + '-' * (2 * space + project_len) + chr(124))

        # user name & software
        space = (21-int(len('Welcome ' + getpass.getuser())/2)) - 1
        print(' ' * space + 'Welcome ' + getpass.getuser())
        print('')
        space = (20-int(len(f'{self.name} {self.version}')/2)) - 1
        print(' ' * space + f'{self.name.title()} {self.version}')

        print(f'\n\n{Plex().paths["pipeline"]}')
        print('\n• img')
        print('• scripts')
        print(r'• scripts\apps')
        print(r'• scripts\extern')

        print(f'\n• config\\projects\\{Plex().context["project_id"]}\n')

        print(fr'• software\{self.name}')
        for sub_dir in pipefunc.get_sub_dirs(self.path):
            print(fr'• software\{self.name}\{sub_dir}')

        print('')

        LOG.debug(f'SOFTWARE: {self.name} {self.version} - {self.path}\nENV: {self.env}')
        LOG.debug(f'PYTHONPATH: {os.environ["PYTHONPATH"]}')
