#*********************************************************************
# content   = setup software attributes
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <contact@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import sys
import subprocess

# DELETE *************************
sys.path.append('D:/Dropbox/arPipeline/2000/data')
import setup
setup.Setup()
# ********************************

import libLog
import libData
from default import SingletonType

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#************************
# CLASS
class Software(object):
    __metaclass__ = SingletonType

    def __init__(self):
        print id(self)

    def setup(self, software, open_file=''):
        print ('new')
        # RENEW SOFTWARE_PATH
        new_software_path = []
        for each_path in os.environ['SOFTWARE_PATH'].split(';'):
            new_software_path.append(('/').join([each_path, software]))

        new_software_path = (';').join(new_software_path)
        os.environ['SOFTWARE_PATH'] = new_software_path

        # GET data
        self.software_data = libData.get_data()['software'][software.upper()]
        self.open_file = open_file

        # SOFTWARE
        self.software = software
        self.version  = self.software_data['version']
        self.path     = self.software_data['path']
        self.env      = self.software_data.get('ENV', '')

        # RENDERER
        if(self.software_data.get('renderer_path', '')):
            self.renderer      = self.software_data['renderer']
            self.renderer_path = self.software_data['renderer_path']
        else:
            self.renderer      = ''
            self.renderer_path = ''

        # ADD software ENV
        if self.env:
            for env, content in self.env.iteritems():
                if isinstance(content, list):
                    for each in content:
                        libData.add_env(env, each)
                else: libData.add_env(env, content)

            LOG.debug('{}_ENV: {}'.format(software.upper(), self.env))

        # SOFTWARE specific behaviour
        if software == 'maya':
            self.maya()
        elif software == 'nuke':
            self.nuke()
        elif software == 'houdini':
            self.houdini()
        else:
            raise LOG.warning('Software was not found')

    def id(self):
        return id(self)

    def __call__(self):
        LOG.info('SOFTWARE: {} {} - {}\n\
                  ENV: {}'.format(self.software, self.version, self.path,
                                  self.env))

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


    #************************
    # SOFTWARE
    def maya(self):
        print('Maya')


    def nuke(self):
        print('Nuke')
        cmd = 'start Nuke{}.exe --nukex "{}"'.format(self.software_data['version'], self.open_file)
        print cmd
        subprocess.check_output(cmd, shell=True)


    def houdini(self):
        print('Houdini')


soft = Software().setup('nuke')
# a1 = Software()
# print a1.id()
# a1.setup('nuke')

