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
sys.path.append("D:/Dropbox/arPipeline/2000/data")
import setup
setup.Setup()
# ********************************

import libLog
import libData

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)


#************************
# CLASS
class Software(object):

    def __init__(self, software, open_file=''):
        # GET data
        self.software_data = libData.get_data()['software'][software.upper()]
        self.open_file = open_file

        # SET DATA/project/$project/Software.yml/$software/ENV
        # TODO: REPLACE variables
        env_data = self.software_data['ENV']

        for env, content in env_data.iteritems():
            if  isinstance(content, list):
                for each in content:
                    os.environ[env] = each
            else: os.environ[env] = str(content)

        LOG.debug('{}_ENV: {}'.format(software.upper(), env_data))

        # SOFTWARE
        self.software   = software
        self.version    = self.software_data['version']
        self.path       = self.software_data['path']

        self.pipeline_path = ("/").join([os.environ["SOFTWARE_PATH"], self.software])
        libData.add_env("PYTHONPATH", self.pipeline_path)

        # RENDERER
        self.renderer      = self.software_data['renderer']
        self.renderer_path = self.software_data['renderer_path']

        if software == 'maya':
            self.maya()
        elif software == 'nuke':
            self.nuke()
        elif software == 'houdini':
            self.houdini()
        else:
            raise LOG.warning('Software was not found')


    def __call__(self):
        LOG.info('SOFTWARE:\n{} {}\n{}\n{}\n{}'.format(self.software, self.version,
                                                       self.path,
                                                       self.renderer,
                                                       self.renderer_path))

    #************************
    # SOFTWARE
    def maya(self):
        print('Maya')


    def nuke(self):
        print('Nuke')
        # subprocess.check_output('start "{}" --nukex {}'.format(self.software_data['path'], self.open_file), shell=True)
        subprocess.check_output('start "{}"'.format(self.software_data['path']), shell=True)


    def houdini(self):
        print('Houdini')


soft = Software('nuke')
# soft.__call__()
