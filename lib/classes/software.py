#*********************************************************************
# content   = setup software attributes
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys
import getpass
import subprocess

import libLog
import libData
import libFunc
import libFileFolder
from subclass import SingletonType

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#************************
# CLASS
class Software(object):
    __metaclass__ = SingletonType

    def __init__(self, software, open_file=''):
        print id(self)
        self.software  = software
        self.open_file = open_file

        LOG.debug('______________________________{}'.format(self.software))

        # RENEW SOFTWARE_PATH & add sub paths
        new_software_path = []
        for each_path in os.environ['SOFTWARE_PATH'].split(';'):
            tmp_paths  = [('/').join([each_path, self.software.lower()])]
            tmp_folder = libFileFolder.getFileList(path=tmp_paths[0], exclude='.py')
            for folder in tmp_folder:
                tmp_paths.append(os.path.normpath(('/').join([tmp_paths[0], folder])))
            new_software_path.extend(tmp_paths)

        os.environ['SOFTWARE'] = self.software.upper()
        os.environ['SOFTWARE_PATH'] = (';').join(new_software_path)

        # GET data
        self.software_data = libData.get_data()['software'][self.software.upper()]

        # SOFTWARE
        self.version = self.software_data['version']
        self.path    = self.software_data['path']
        self.env     = self.software_data.get('ENV', '')

        # RENDERER
        if(self.software_data.get('renderer_path', '')):
            self.renderer      = self.software_data['renderer']
            self.renderer_path = self.software_data['renderer_path']
        else:
            self.renderer      = ''
            self.renderer_path = ''

        # ADD software ENV
        if(self.env):
            for env, content in self.env.iteritems():
                if isinstance(content, list):
                    for each in content:
                        libData.add_env(env, each)
                else: libData.add_env(env, content)

            LOG.debug('{}_ENV: {}'.format(self.software.upper(), self.env))


    # SOFTWARE specific behaviour
    def start_software(self):
        if(self.software == 'maya'):
            self.maya()
        elif(self.software == 'nuke'):
            self.nuke()
        elif(self.software == 'houdini'):
            self.houdini()
        else:
            raise LOG.warning('Software was not found')

    #************************
    # SOFTWARE
    def maya(self):
        cmd = 'start {} -file "{}"'.format(self.software_data['path'], self.open_file)
        LOG.debug(cmd)
        subproces

    def nuke(self):
        cmd = 'start Nuke{}.exe --nukex "{}"'.format(self.software_data['version'], self.open_file)
        LOG.debug(cmd)
        subprocess.check_output(cmd, shell=True)

    def houdini(self):
        print('Houdini')

    def __call__(self):
        LOG.info('SOFTWARE: {} {} - {}\n\
                  ENV: {}'.format(self.software, self.version, self.path,
                                  self.env))

    def id(self):
        return id(self)

    # @property
    # def software(self):
    #     return self.software

    # @property
    # def version(self):
    #     return self.version

    # @property
    # def path(self):
    #     return self.path

    # @property
    # def env(self):
    #     return self.env

    # @property
    # def renderer(self):
    #     return self.renderer

    # @property
    # def renderer_path(self):
    #     return self.renderer_path


    @staticmethod
    def print_header(menu_data):
        space = (20-int(len(os.getenv('PROJECT_NAME'))/2)) - 1

        # project name & user namse
        print('')
        print(chr(218) + chr(196)*38 + chr(191))
        print(chr(179) + ' '*space + os.getenv('PROJECT_NAME') + ' '*space + chr(179))
        print(chr(192) + chr(196)*38 + chr(217))

        print ('\n' + ' '*12 + 'Welcome ' + getpass.getuser() + '\n')

        print('PATHS')
        print('  {} ON  - img'.format(chr(254)))
        print('  {} ON  - data'.format(chr(254)))
        print('  {} ON  - lib'.format(chr(254)))
        print('  {} ON  - lib/classes'.format(chr(254)))
        print('  {} ON  - lib/utils'.format(chr(254)))
        print('  {} ON  - software/{}'.format(chr(254), os.getenv('SOFTWARE').lower()))
        print('  {} ON  - software/{}/scripts'.format(chr(254), os.getenv('SOFTWARE').lower()))
        print('  {} ON  - software/{}/plugins'.format(chr(254), os.getenv('SOFTWARE').lower()))
        # print('  {} ON  - software/{}/gizmos'.format(chr(254), os.getenv('SOFTWARE')))

        print('') # ********************

        print('SCRIPTS')
        # scripts from software/MENU
        for menu_item in menu_data:
            for key in menu_item:
                if key == 'break': continue
                print('  {} ON  - {}'.format(chr(254), key))

        print('') # ********************

    @staticmethod
    def print_checked_header(text, content, func):
        try:
            func
            print('  {} ON  - {}: {}'.format(chr(254), text, content))
        except:
            LOG.debug('  OFF - {}: {}'.format(content))
            print('  {} OFF - {}: {}'.format(chr(254), text, content))

    @staticmethod
    def add_menu(menu_node, new_command):
        for keys, item in new_command.iteritems():
            if isinstance(item, dict):
                sub_menu = menu_node.addMenu(keys)
                Software.add_menu(sub_menu, item)
            else:
                eval('menu_node.{}'.format(item))

# Software('nuke')
