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
from subclass import Singleton

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#************************
# CLASS
class Software(Singleton):

    def setup(self, software):
        self.software = software.lower()

        # GET data
        self.software_data = libData.get_data()['software'][self.software.upper()]

        self.ver = self.software_data['version']
        self.software_path = self.software_data['path']

        # RENDERER
        self.renderer      = self.software_data.get('renderer', '')
        self.renderer_path = self.software_data.get('renderer_path', '')

    def add_env(self):
        LOG.debug('______________________________{}'.format(self.software))
        new_software_path = []
        for each_path in os.environ['SOFTWARE_PATH'].split(';'):
            tmp_paths  = ('/').join([each_path, self.software])
            LOG.debug(tmp_paths)
            tmp_folder = libFileFolder.get_file_list(path=tmp_paths, exclude='.py')
            new_path   = []
            for folder in tmp_folder:
                new_path.append(os.path.normpath(('/').join([tmp_paths, folder])))
            new_software_path.extend(new_path)

        os.environ['SOFTWARE'] = self.software.upper()
        os.environ['SOFTWARE_PATH'] = ('/').join([each_path, self.software])
        os.environ['SOFTWARE_SUB_PATH'] = (';').join(new_software_path)

        # GET data
        self.software_data = libData.get_data()['software'][self.software.upper()]
        self.env = self.software_data.get('ENV', '')

        # ADD software ENV
        if(self.env):
            for env, content in self.env.iteritems():
                LOG.debug('{} _ {}'.format(env, content))
                if isinstance(content, list):
                    for each in content:
                        libData.add_env(env, each)
                else: libData.add_env(env, content)

            LOG.debug('{}_ENV: {}'.format(self.software.upper(), self.env))


    #************************
    # SOFTWARE
    def start(self, open_file=''):
        self.add_env()

        cmd = self.software_data['start'].format(open_file)
        LOG.debug(cmd)
        subprocess.Popen(cmd, shell=True, env=os.environ)

    def __call__(self):
        LOG.info('SOFTWARE: {} {} - {}\n\
                  ENV: {}'.format(self.software, self.ver, self.software_path,
                                  self.env))


    #************************
    # VARIABLES
    @property
    def id(self):
        return id(self)

    @property
    def name(self):
        return self.software

    @property
    def version(self):
        return self.ver

    @property
    def path(self):
        return self.software_path

    @property
    def software_env(self):
        return self.env

    # @property
    # def renderer(self):
    #     return self.renderer

    # @property
    # def renderer_path(self):
    #     return self.renderer_path


    #************************
    # STATIC
    @staticmethod
    def add_menu(menu_node, new_command):
        for keys, item in new_command.iteritems():
            if isinstance(item, dict):
                if os.getenv('SOFTWARE') == 'MAYA':
                    import maya.cmds as cmds
                    sub_menu = cmds.menuItem(p = menu_node, l = keys, sm = True)
                elif os.getenv('SOFTWARE') == 'NUKE':
                    sub_menu = menu_node.addMenu(keys)
                else:
                    LOG.debug('CANT find software: {}'.format(software))
                    continue
                Software.add_menu(sub_menu, item)
            else:
                eval('menu_node.{}'.format(item))

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
        print('  {} ON  - lib'.format(chr(254)))
        print('  {} ON  - data'.format(chr(254)))
        print('  {} ON  - lib/utils'.format(chr(254)))
        print('  {} ON  - lib/classes'.format(chr(254)))
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
