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

    def setup(self, software=os.getenv('SOFTWARE')):
        if not software: raise

        self._software = software.lower()

        # GET data
        self._software_data = libData.get_data()['software'][self._software.upper()]

        self._version = self._software_data['version']
        self._path = self._software_data['path']

        # RENDERER
        self._renderer      = self._software_data.get('renderer', '')
        self._renderer_path = self._software_data.get('renderer_path', '')

    def add_env(self):
        LOG.debug('------------------------------ {}'.format(self._software))

        new_path = []
        for each_path in os.environ['SOFTWARE_PATH'].split(';'):
            if not each_path.endswith('software'): each_path = os.path.dirname(each_path)
            tmp_paths  = ('/').join([each_path, self._software])
            tmp_folder = libFileFolder.get_file_list(path=tmp_paths, exclude='.py', add_path=True)
            new_path.extend(tmp_folder)

        os.environ['SOFTWARE'] = self._software.upper()
        os.environ['SOFTWARE_PATH'] = os.environ['SOFTWARE_PATH'].replace('software', 'software/' + self._software)
        os.environ['SOFTWARE_SUB_PATH'] = (';').join(new_path)

        LOG.debug("SOFTWARE_PATH: {}".format(os.environ['SOFTWARE_PATH']))

        # GET data
        self._software_data = libData.get_data()['software'][self._software.upper()]
        self._env = self._software_data.get('ENV', '')

        # ADD software ENV
        if(self._env):
            for env, content in self._env.iteritems():
                if isinstance(content, list):
                    for each in content:
                        libData.add_env(env, each)
                else: libData.add_env(env, content)

            LOG.debug('{}_ENV: {}'.format(self._software.upper(), self._env))


    #************************
    # SOFTWARE
    def start(self, software='', open_file=''):
        if software: self.setup(software)
        self.add_env()

        cmd = self._software_data['start'].format(open_file)
        if self._software == 'maya' and not open_file:
            cmd = cmd.split('-file')[0]
        LOG.debug(cmd)
        subprocess.Popen(cmd, shell=True, env=os.environ)

    def __call__(self):
        LOG.info('SOFTWARE: {} {} - {}\n\
                  ENV: {}'.format(self._software, self._version, self._path,
                                  self._env))


    #************************
    # VARIABLES
    @property
    def id(self):
        return id(self)

    @property
    def software(self):
        return self._software

    @property
    def version(self):
        return self._version

    @property
    def path(self):
        return self._path

    @property
    def env(self):
        return self._env

    @property
    def renderer(self):
        return self._renderer

    @property
    def renderer_path(self):
        return self._renderer_path


    #************************
    # STATIC
    def add_menu(self, menu_node, new_command):
        try:
            for keys, item in new_command.iteritems():
                if isinstance(item, dict):
                    if self._software == 'maya':
                        import maya.cmds as cmds
                        sub_menu = cmds.menuItem(p = menu_node, l = keys, sm = True)
                    elif self._software == 'nuke':
                        sub_menu = menu_node.addMenu(keys)
                    else:
                        LOG.debug('CANT find software: {}'.format(software))
                        continue
                    self.add_menu(sub_menu, item)
                else:
                    if self._software == 'maya':
                        import maya.cmds as cmds
                        cmd = ('cmds.{}'.format(item)).format(menu_node)
                        LOG.debug(cmd)
                        eval(cmd)
                    if self._software == 'nuke':
                        eval('menu_node.{}'.format(item))
        except:
              LOG.error('DATA Menu couldnt be created', exc_info=True)


    def print_header(self):
        space = (20-int(len(os.getenv('PROJECT_NAME'))/2)) - 1

        # project name
        print('')
        print(chr(218) + chr(196)*38 + chr(191))
        print(chr(179) + ' '*space + os.getenv('PROJECT_NAME') + ' '*space + chr(179))
        print(chr(192) + chr(196)*38 + chr(217))

        # user name
        print ('\n' + ' '*12 + 'Welcome ' + getpass.getuser() + '\n')

        print('PATHS')
        print('  {} ON  - img'.format(chr(254)))
        print('  {} ON  - lib'.format(chr(254)))
        print('  {} ON  - data'.format(chr(254)))
        print('  {} ON  - lib/utils'.format(chr(254)))
        print('  {} ON  - lib/classes'.format(chr(254)))
        print('  {} ON  - software/{}'.format(chr(254), self._software))
        print('  {} ON  - software/{}/scripts'.format(chr(254), self._software))
        print('  {} ON  - software/{}/plugins'.format(chr(254), self._software))
        if self._software == 'maya':
            print('  {} ON  - software/{}/shelf'.format(chr(254), self._software))
        if self._software == 'nuke':
            print('  {} ON  - software/{}/gizmos'.format(chr(254), self._software))

        print('') # ********************

        print('SCRIPTS')
        # scripts from software/MENU
        for menu_item in self._software_data['MENU']:
            for key in menu_item:
                if key == 'break': continue
                print('  {} ON  - {}'.format(chr(254), key))

        print('') # ********************

    def print_checked_header(self, text, content, func):
        try:
            func
            print('  {} ON  - {}: {}'.format(chr(254), text, content))
        except:
            LOG.debug('  OFF - {}: {}'.format(content))
            print('  {} OFF - {}: {}'.format(chr(254), text, content))
