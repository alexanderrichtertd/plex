# content   = setup software attributes
# date      = 03.12.2024
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>

import os
import sys
import getpass
import subprocess

import plexfunc
import plex

LOG = plex.log(script=__name__)


class Software(plexfunc.Singleton):
    def start(self, name='', open_file=''):
        plex.set_context('software', name)

        # SETUP env
        software_dirs = plexfunc.get_sub_dirs(self.path, full_path=True)

        os.environ['SOFTWARE_PATH'] = ';'.join(software_dirs)
        # PYTHONPATH important for software imports
        os.environ['PYTHONPATH'] = ';'.join([
            os.environ.get('PYTHONPATH', ''),
            *software_dirs,
            f'{plex.paths["software"]}/{self.name}',
            plex.paths["scripts"],
            plex.paths["apps"],
            plex.paths["extern"],
        ])        

        sys.path.extend(software_dirs)

        # GET software config
        self.env = plex.config['software'].get('ENV', '')

        # ADD software ENV
        for env, content in self.env.items():
            if isinstance(content, list):
                [plexfunc.add_env(env, each) for each in content]
            else:
                plexfunc.add_env(env, content)

        if open_file: open_file = f'"{open_file}"'
        cmd = plex.config['software']['start'].format(open_file)
        subprocess.Popen(cmd, shell=True, env=os.environ)

        LOG.debug(f'START : {self.name.upper()} : {cmd}')
        self.print_header()


    # VARIABLES ***********************************************************
    @property
    def id(self):
        return id(self)
    
    @property
    def name(self):
        return plex.context['software']
   
    @property
    def path(self):        
        return f'{plex.paths["software"]}/{self.name}'

    @property
    def config(self):
        return plex.config['software']

    @property
    def extension(self):
        return plex.config['project']['EXTENSION'][self.name]

    @property
    def menu(self):
        return plex.config['software']['MENU']
    
    @property
    def version(self):
        return plex.config['software']['version']
    
    @property
    def renderer(self):
        return plex.config['software'].get('renderer', '')
        
    @property
    def renderer_path(self):        
        return plex.config['software'].get('renderer_path', '')


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

        project_len = len(plex.context['project_name'])
        space = (20-int(project_len/2)) - 1

        # project name
        print('')
        print(chr(124) + '-' * (2 * space + project_len) + chr(124))
        print(chr(124) + ' ' * space + plex.context['project_name'] + ' ' * space + chr(124))
        print(chr(124) + '-' * (2 * space + project_len) + chr(124))

        # user name & software
        space = (21-int(len('Welcome ' + getpass.getuser())/2)) - 1
        print(' ' * space + 'Welcome ' + getpass.getuser())
        print('')
        space = (20-int(len(f'{self.name} {self.version}')/2)) - 1
        print(' ' * space + f'{self.name.title()} {self.version}')

        print(f'\n\n{plex.paths["plex"]}')
        print('\n• img')
        print('• scripts')
        print(r'• apps')
        print(r'• scripts\extern')

        print(f'\n• config\\projects\\{plex.context["project_id"]}\n')

        print(fr'• software\{self.name}')
        for sub_dir in plexfunc.get_sub_dirs(self.path):
            print(fr'• software\{self.name}\{sub_dir}')

        print('')

        LOG.debug(f'SOFTWARE: {self.name} {self.version} : {self.path} | ENV: {self.env}')
        LOG.debug(f'PYTHONPATH: {os.environ["PYTHONPATH"]}')
