#*********************************************************************
# content   = SET default environment paths
# version   = 1.0.0
# date      = 2019-12-01
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os
import sys

import yaml


#*********************************************************************
class Setup(object):

    def __init__(self):
        this_path = os.path.normpath(os.path.dirname(__file__))
        self.data_pipeline_path = []
        self.data_project_path  = os.path.normpath(('/').join([this_path, 'pipeline.yml']))

        self.pipeline_env  = SmartDict()
        self.this_pipeline = os.path.normpath(os.path.dirname(this_path))

        # LOAD pipeline data
        if os.path.exists(self.data_project_path):
            with open(self.data_project_path , 'r') as stream:
                try:   self.pipeline_data = yaml.load(stream)
                except yaml.YAMLError as exc: raise OSError ('STOP PROCESS', 'DATA file is corrupted', exc)
        else: raise OSError ('STOP PROCESS', 'PATH doesnt exist', self.data_project_path)

        # SEARCH and ADD current and sub paths
        for pipe in self.pipeline_data['PATH']:

            for status, path in pipe.items():
                # REPLACE $this with current_path
                if path == '$this': path = self.this_pipeline

                if path and self.this_pipeline == path or self.data_pipeline_path:
                    if os.path.exists(path):
                        self.data_pipeline_path.append(path)
                        self.pipeline_status = status
                    else: print('PIPELINE_PATH doesnt exist: {}\nSOURCE[PATH]: {}'.format(path, self.data_project_path))

        if not self.data_pipeline_path:
            raise OSError ('STOP PROCESS', 'PATH doesnt exist in data/pipeline.yml', self.this_pipeline)

        self.set_pipeline_env()
        self.__call__()


    def set_pipeline_env(self):

        # SET STATUS
        os.environ['PIPELINE_STATUS'] = self.pipeline_status

        # ADD sub ENV
        for eachPath in self.data_pipeline_path:
            self.pipeline_env.add('PIPELINE_PATH', eachPath)

            if os.path.exists(eachPath + '/img'):        self.pipeline_env.add('IMG_PATH', eachPath + '/img')
            if os.path.exists(eachPath + '/software'):   self.pipeline_env.add('SOFTWARE_PATH', eachPath + '/software')
            if os.path.exists(eachPath + '/lib'):        self.pipeline_env.add('LIB_PATH', eachPath + '/lib')

            if os.path.exists(eachPath + '/lib/apps'):  self.pipeline_env.add('APPS_PATH', eachPath + '/lib/apps')
            if os.path.exists(eachPath + '/lib/extern'): self.pipeline_env.add('EXTERN_PATH', eachPath + '/lib/extern')

        os.environ['DATA_PATH'] = self.data_pipeline_path[0] + '/data'
        os.environ['DATA_PROJECT_PATH'] = self.data_pipeline_path[0] + '/data/project/' + self.pipeline_data['project']

        # ADD all pipeline env
        self.add_env('PIPELINE_PATH', (';').join(self.pipeline_env['PIPELINE_PATH']))
        try:
            self.add_env('IMG_PATH',       (';').join(self.pipeline_env['IMG_PATH']))
            self.add_env('LIB_PATH',       (';').join(self.pipeline_env['LIB_PATH']))
            self.add_env('APPS_PATH',      (';').join(self.pipeline_env['APPS_PATH']))
            self.add_env('EXTERN_PATH',    (';').join(self.pipeline_env['EXTERN_PATH']))

            self.add_env('SOFTWARE_PATH',     (';').join(self.pipeline_env['SOFTWARE_PATH']))
            self.add_env('SOFTWARE_SRC_PATH', (';').join(self.pipeline_env['SOFTWARE_PATH']))
        except: raise OSError ('STOP PROCESS', 'PATH doesnt exist in data/pipeline.yml', self.this_pipeline)

        sys.path.append(os.environ['PIPELINE_PATH'])
        sys.path.append(os.environ['IMG_PATH'] )
        sys.path.append(os.environ['LIB_PATH'])
        sys.path.append(os.environ['APPS_PATH'])
        sys.path.append(os.environ['SOFTWARE_PATH'] )
        sys.path.append(os.environ['DATA_PATH'])
        sys.path.append(os.environ['DATA_PROJECT_PATH'])

        self.add_env('PYTHONPATH', os.environ['IMG_PATH'])
        self.add_env('PYTHONPATH', os.environ['LIB_PATH'])
        self.add_env('PYTHONPATH', os.environ['APPS_PATH'])
        self.add_env('PYTHONPATH', os.environ['EXTERN_PATH'])

        # DATA ENV
        os.environ['DATA_USER_PATH']      = self.data_pipeline_path[0] + '/data/user/' + os.getenv('username')
        os.environ['DATA_USER_OVERWRITE'] = str(self.pipeline_data['user_data'])
        sys.path.append(os.environ['DATA_USER_PATH'])

        # SET project Data
        from tank import Tank

        self.project_data = Tank().data_project
        os.environ['PROJECT_NAME'] = self.project_data['name']

        # ADD project path
        if os.path.exists(self.project_data['path']):
            os.environ['PROJECT_PATH'] = os.path.normpath(self.project_data['path'])
        else: os.environ['PROJECT_PATH'] = ''

        # OS & PYTHON_VERSION
        os.environ['OS'] = sys.platform
        os.environ['PYTHON_VERSION'] = sys.version[:3]


    def add_env(self, var, content):
        content = os.path.normpath(content)
        if     os.environ.__contains__(var): os.environ[var] += ('').join([';', content])
        else:  os.environ[var] = content
        return os.getenv(var)


    def __call__(self):
        from tank import Tank
        TITLE = os.path.splitext(os.path.basename(__file__))[0]
        LOG   = Tank().log.init(script=TITLE)

        LOG.debug('____________________________________________________________')
        LOG.debug('PIPELINE: {} [{}, {}, {}] {}'.format(self.pipeline_data['PIPELINE']['name'],
                           self.pipeline_data['PIPELINE']['version'],
                           os.environ['PIPELINE_STATUS'],
                           'user overwrite' if os.environ['DATA_USER_PATH'] else 'NO user overwrite',
                           self.data_pipeline_path))

        LOG.debug('PROJECT:  {} [{}, {}] [{}{}]'.format(self.project_data['name'],
                            '{} x {}'.format(Tank().data_project['resolution'][0], Tank().data_project['resolution'][1]),
                            Tank().data_project['fps'],
                            '' if os.path.exists(self.project_data['path']) else 'NOT existing: ',
                            os.path.normpath(self.project_data['path'])))

        LOG.debug('------------------------------------------------------------')
        LOG.debug('SYS_PATH: {}'.format('[%s]' % ', '.join(map(str, sys.path))))
        LOG.debug('ADD_ENV:  {}'.format(self.pipeline_env))




#*********************************************************************
# CLASS
class SmartDict(dict):
    def __init__(self):
        super(dict)
        self = dict()

    def add(self, key, value):
        value = os.path.normpath(value)
        if self.has_key(key): self[key].append(value)
        else:                 self[key] = [value]

    def __missing__(self, key):
        return key



#*********************************************************************
# START
import argparse

parser = argparse.ArgumentParser(description='Setup your pipeline and start scripts.')
parser.add_argument('-so','--software', help='add software: nuke')
parser.add_argument('-p', '--proxy', action='store_true')

args = parser.parse_args()

if args.software:
    Setup()

    from tank import Tank
    if args.software == 'desktop':
        # Tank().start_software(args.software)
        import arDesktop
        arDesktop.start()
    else:
        Tank().start_software(args.software)

