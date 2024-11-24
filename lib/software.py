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

import tank
from tank import Tank


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)


#*********************************************************************
# CLASS
class Software(tank.Singleton):
    name = 'software'

    def start(self, name='', open_file=''):
        self.name = name or self.name

        # SETUP env
        LOG.debug(f'- {self.name.upper()} -----------------------------------------------------')

        self.software_path = '/'.join([Tank().plex_paths['software'], self.name])
        software_dirs = Tank().get_sub_dirs(self.software_path, full_path=True)

        os.environ['SOFTWARE_PATH'] = ';'.join(software_dirs)

        # PYTHONPATH important for the software imports
        os.environ['PYTHONPATH'] += ';' + ';'.join(software_dirs)
        os.environ['PYTHONPATH'] += ';' + Tank().plex_paths['lib']
        for software_dir in software_dirs:
            sys.path.append(software_dir)

        # GET config
        self.env = Tank().config_software.get('ENV', '')

        # ADD software ENV
        if(self.env):
            for env, content in self.env.items():
                if isinstance(content, list):
                    for each in content:
                        Tank().add_env(env, each)
                else: 
                    Tank().add_env(env, content)

        self.version = Tank().config_software['version']
        self.path = Tank().config_software['path']

        # RENDERER
        self.renderer = Tank().config_software.get('renderer', '')
        self.renderer_path = Tank().config_software.get('renderer_path', '')

        if open_file: open_file = f'"{open_file}"'
        cmd = Tank().config_software['start'].format(open_file)
        subprocess.Popen(cmd, shell=True, env=os.environ)
        LOG.debug(cmd)

        self.print_header()


    #*********************************************************************
    # VARIABLES
    @property
    def id(self):
        return id(self)

    @property
    def config(self):
        return Tank().config_software

    @property
    def extension(self):
        return Tank().config_project['EXTENSION'][self.name]

    @property
    def menu(self):
        return Tank().config_software['MENU']


    #*********************************************************************
    # IS DCC
    @property
    def is_maya(self):
        return self.name == 'maya'

    @property
    def is_nuke(self):
        return self.name == 'nuke'

    @property
    def is_houdini(self):
        return self.name == 'houdini'

    @property
    def is_max(self):
        return self.name == 'max'


    #*********************************************************************
    # FUNCTION
    @property
    def scene_path(self):
        LOG.warning('NO software override found')

    def scene_save(self):
        LOG.warning('NO software override found')

    def scene_save_as(self, file):
        LOG.warning('NO software override found')

    def scene_open(self, file):
        LOG.warning('NO software override found')

    def scene_import(self, file):
        LOG.warning('NO software override found')


    #*********************************************************************
    # PRINT
    def print_header(self):
        if self.name == 'max': return

        project_len = len(Tank().plex_context['project_name'])
        space = (20-int(project_len/2)) - 1

        # project name
        print('')
        print(chr(124) + '-' * (2 * space + project_len) + chr(124))
        print(chr(124) + ' ' * space + Tank().plex_context['project_name'] + ' ' * space + chr(124))
        print(chr(124) + '-' * (2 * space + project_len) + chr(124))

        # user name & software
        space = (20-int(len('Welcome ' + getpass.getuser())/2)) - 1
        print(' ' * space + 'Welcome ' + getpass.getuser())
        print('')
        space = (20-int(len(f'{self.name} {self.version}')/2)) - 1
        print(' ' * space + f'{self.name.title()} {self.version}')

        print(f'\nPATHS')
        print('• img')
        print('• lib')
        print('• lib/apps')
        print('• lib/extern')

        print('\n• config')

        for sub_dir in Tank().get_sub_dirs(self.software_path):
            if sub_dir == 'menu': sub_dir += f'/{Tank().config_software["menu"]}'
            print(f'• software/{self.name}/{sub_dir}')

        print('')

        LOG.debug(f'SOFTWARE: {self.name} {self.version} - {self.path}\nENV: {self.env}')
        LOG.debug(f'PYTHONPATH: {os.environ["PYTHONPATH"]}')
