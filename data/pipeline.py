#*********************************************************************
# content   = SET default environment paths
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

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = ''

try: import yaml
except:
    sys.path.append('C:/Python27/Lib/site-packages')
    import yaml

class Setup(object):

    def __init__(self):
        global LOG

        self.data_pipeline_path = []

        self.pipeline_env  = SmartDict()
        this_path          = os.path.normpath(os.path.dirname(__file__))
        this_pipeline_path = os.path.normpath(os.path.dirname(this_path))
        data_project_path  = os.path.normpath(('/').join([this_path, 'pipeline.yml']))

        # OS & PYTHON_VERSION
        os.environ['OS'] = sys.platform
        os.environ['PYTHON_VERSION'] = sys.version[:3]

        # LOAD project data
        if os.path.exists(data_project_path):
            with open(data_project_path , 'r') as stream:
                try:
                    self.pipeline_data = yaml.load(stream)
                except yaml.YAMLError as exc:
                    print('STOP PROCESS\n'\
                          'The DATA file is corrupted.\n\n{}'.format(exc))
                    return

                # SEARCH and ADD current and sub paths
                sub_paths = False
                for paths in self.pipeline_data['PATH']:
                    if this_pipeline_path in paths.values() or sub_paths:
                        if not sub_paths: self.pipeline_env['PIPELINE_STATUS'] = paths.keys()[0]
                        self.data_pipeline_path.append(paths.values())
                        sub_paths = True
                    else:
                        continue
        else:
            print('STOP PROCESS\n\
                   CANT find current path in {}'.format(data_project_path))
            return

        self.set_pipeline_env()
        self.__call__()

    def set_pipeline_env(self):
        global LOG

        if not self.data_pipeline_path:
            print('data/pipeline/PATH doesnt exist')
            return

        for eachPath in self.data_pipeline_path:
            eachPath = eachPath[0]

            if not os.path.exists(eachPath):
                print('PIPELINE_PATH doesnt exist: {}\n'\
                      'SOURCE[PATH]: {}'.format(eachPath, data_project_path))
                continue

            self.pipeline_env.add('PIPELINE_PATH',     eachPath)

            self.pipeline_env.add('IMG_PATH',          eachPath + '/img')
            self.pipeline_env.add('SOFTWARE_PATH',     eachPath + '/software')

            self.pipeline_env.add('LIB_PATH',          eachPath + '/lib')
            self.pipeline_env.add('UTILS_PATH',        eachPath + '/lib/utils')
            self.pipeline_env.add('CLASSES_PATH',      eachPath + '/lib/classes')

            self.pipeline_env.add('DATA_PATH',         eachPath + '/data')
            self.pipeline_env.add('DATA_USER_PATH',    eachPath + '/data/user/'    + os.getenv('username'))
            self.pipeline_env.add('DATA_PROJECT_PATH', eachPath + '/data/project/' + self.pipeline_data['project'])

        # ADD all pipeline env
        self.add_env('PIPELINE_PATH',     (';').join(self.pipeline_env['PIPELINE_PATH']))
        self.add_env('IMG_PATH',          (';').join(self.pipeline_env['IMG_PATH']))
        self.add_env('LIB_PATH',          (';').join(self.pipeline_env['LIB_PATH']))
        self.add_env('UTILS_PATH',        (';').join(self.pipeline_env['UTILS_PATH']))
        self.add_env('CLASSES_PATH',      (';').join(self.pipeline_env['CLASSES_PATH']))
        self.add_env('SOFTWARE_PATH',     (';').join(self.pipeline_env['SOFTWARE_PATH']))
        self.add_env('DATA_PATH',         (';').join(self.pipeline_env['DATA_PATH']))
        self.add_env('DATA_PROJECT_PATH', (';').join(self.pipeline_env['DATA_PROJECT_PATH']))

        sys.path.append(os.environ['PIPELINE_PATH'])
        sys.path.append(os.environ['IMG_PATH'] )
        sys.path.append(os.environ['LIB_PATH'])
        sys.path.append(os.environ['UTILS_PATH'])
        sys.path.append(os.environ['CLASSES_PATH'])
        sys.path.append(os.environ['SOFTWARE_PATH'] )
        sys.path.append(os.environ['DATA_PATH'])
        sys.path.append(os.environ['DATA_PROJECT_PATH'])

        self.add_env('PYTHONPATH', os.environ['LIB_PATH'])
        self.add_env('PYTHONPATH', os.environ['IMG_PATH'])
        self.add_env('PYTHONPATH', os.environ['UTILS_PATH'])
        self.add_env('PYTHONPATH', os.environ['CLASSES_PATH'])
        self.add_env('PYTHONPATH', os.environ['SOFTWARE_PATH'] )

        import libLog
        LOG = libLog.init(script=TITLE)
        LOG.debug('')
        LOG.debug('______________________________SETUP______________________________')

        # CHECK if user overwrite is active
        if self.pipeline_data['user_data']:
            self.add_env('DATA_USER_PATH', (';').join(self.pipeline_env['DATA_USER_PATH']))
            sys.path.append(os.environ['DATA_USER_PATH'])
        else:
            os.getenv['DATA_USER_PATH'] = ''
            LOG.warning('USER DATA will be ignored.')

        # SET project Data
        import libData
        project_data = libData.get_data('project')
        os.environ['PROJECT_NAME'] = project_data['name']

        if os.path.exists(project_data['path']):
            os.environ['PROJECT_PATH'] = os.path.normpath(project_data['path'])
        else:
            # ALT: PROJECT_PATH = '../pipeline'
            LOG.critical('PROJECT PATH doesnt exist: {}'.format(project_data['path']))


    def __call__(self):
        global LOG
        LOG.debug('PATH:   {}'.format('[%s]' % ', '.join(map(str, sys.path))))
        LOG.debug('OS_ENV: {}'.format(self.pipeline_env))


    #************************
    # FUNCTIONS
    def add_env(self, var, content):
        content = os.path.normpath(content)
        if os.environ.__contains__(var):
            os.environ[var] += ('').join([';', content])
        else:
            os.environ[var] = content
        return os.getenv(var)


#************************
# CLASS
class SmartDict(dict):
    global LOG
    def __init__(self):
        super(dict)
        self = dict()

    def add(self, key, value):
        value = os.path.normpath(value)
        if self.has_key(key):
            self[key].append(value)
        else:
            self[key] = [value]

    def __missing__(self, key):
        LOG.debug('MISSING Key: {}'.format(key))
        return key


#************************
# START
import argparse

parser = argparse.ArgumentParser(description='Setup your pipeline and start scripts.')
parser.add_argument('-s','--script', help='add script: software')
parser.add_argument('-so','--software', help='add software: nuke')
parser.add_argument('-p', '--proxy', action='store_true')
args = parser.parse_args()

if args.script:
    Setup()
    if args.script == 'software':
        import software
        software.Software(args.software).start_software()
    elif args.script == 'desktop':
        import arDesktop
        arDesktop.main()



