#*********************************************************************
# content   = SET default environment paths
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
import yaml

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG = ''

class Setup(object):

    def __init__(self):
        global LOG

        self.pipeline_env  = NewDict()
        this_path          = os.path.normpath(os.path.dirname(__file__))
        this_pipeline_path = os.path.normpath(os.path.dirname(this_path))
        data_project_path  = os.path.normpath(("/").join([this_path, "pipeline.yml"]))

        # OS & PYTHON_VERSION
        os.environ['OS'] = sys.platform
        os.environ['PYTHON_VERSION'] = sys.version[:3]

        # LOAD project data
        if os.path.exists(data_project_path):
            with open(data_project_path , 'r') as stream:
                try:
                    self.pipeline_data = yaml.load(stream)
                    if this_pipeline_path in self.pipeline_data['PATH']:
                        for index in range(0, self.pipeline_data["PATH"].index(this_pipeline_path)):
                            self.pipeline_data['PATH'].pop(0)
                        self.pipeline_env["PIPELINE_PATH"] = self.pipeline_data['PATH']
                    else:
                        print('STOP PROCESS\n\
                               Missing current PATH in {}\n\
                               GET:  {}\n\
                               NEED: {}'.format(pipeline_data_path, self.pipeline_data["PATH"], this_pipeline_path))
                        return
                except yaml.YAMLError as exc:
                    print('STOP PROCESS\n'\
                          'The DATA file is corrupted.\n\n{}'.format(exc))
                    return
        else:
            print("STOP PROCESS\nCANT load DATA file: {}".format(pipeline_data_path ))
            return

        # CREATE all pipeline env
        for eachPath in self.pipeline_data['PATH']:
            if not os.path.exists(eachPath):
                print('PIPELINE_PATH doesnt exist: {}\n'\
                      'SOURCE[PATH]: {}'.format(eachPath, data_project_path))
                continue

            self.pipeline_env.add("IMG_PATH",          eachPath + "/img")
            self.pipeline_env.add("LIB_PATH",          eachPath + "/lib")
            self.pipeline_env.add("SOFTWARE_PATH",     eachPath + "/software")
            self.pipeline_env.add("DATA_PATH",         eachPath + "/data")
            self.pipeline_env.add("DATA_USER_PATH",    eachPath + "/data/user/"    + os.getenv('username'))
            self.pipeline_env.add("DATA_PROJECT_PATH", eachPath + "/data/project/" + self.pipeline_data['project'])

            sys.path.append(eachPath)
            sys.path.append(self.pipeline_env['SOFTWARE_PATH'][-1])
            sys.path.append(self.pipeline_env['LIB_PATH'][-1])

        # ADD all pipeline env
        self.add_env_var("PIPELINE_PATH",     (";").join(self.pipeline_env["PIPELINE_PATH"]))
        self.add_env_var("IMG_PATH",          (";").join(self.pipeline_env["IMG_PATH"]))
        self.add_env_var("LIB_PATH",          (";").join(self.pipeline_env["LIB_PATH"]))
        self.add_env_var("SOFTWARE_PATH",     (";").join(self.pipeline_env["SOFTWARE_PATH"]))
        self.add_env_var("DATA_PATH",         (";").join(self.pipeline_env["DATA_PATH"]))
        self.add_env_var("DATA_PROJECT_PATH", (";").join(self.pipeline_env["DATA_PROJECT_PATH"]))

        # LOG
        import libLog
        LOG = libLog.init(script=TITLE)
        LOG.debug('')
        LOG.debug('______________________________SETUP______________________________')

        # CHECK if user overwrite is possible
        if not self.pipeline_data['user_data']:
            self.pipeline_env["DATA_USER_PATH"] = ''
            LOG.warning('USER DATA will be ignored.')

        self.add_env_var("DATA_USER_PATH", (";").join(self.pipeline_env["DATA_USER_PATH"]))

        import libData

        project_data = libData.get_data('project')["PROJECT"]
        os.environ["PROJECT_NAME"] = project_data["name"]

        if os.path.exists(project_data["path"]):
            os.environ["PROJECT_PATH"] = project_data["path"]
        else:
            LOG.warning('PROJECT PATH doesnt exist: {}'.format(project_data["path"]))

        self.__call__()


    def __call__(self):
        global LOG

        LOG.debug("PATH:{}".format('[%s]' % ', '.join(map(str, sys.path))))
        LOG.debug('ENV: {}'.format(self.pipeline_env))


    #************************
    # FUNCTIONS
    def add_env_var(self, var, content):
        content = os.path.normpath(content)
        if os.environ.__contains__(var):
            os.environ[var] += ("").join([";", content])
        else:
            os.environ[var] = content
        return os.environ[var]


#************************
# CLASS

# add or overwrite dict + normpath
class NewDict(dict):
    def __init__(self):
        super(dict)
        self = dict()

    def add(self, key, value):
        value = os.path.normpath(value)
        if self.has_key(key):
            self[key].append(value)
        else:
            self[key] = [value]


# DELETE
# a = Setup()
# import libData
# print libData.getProjectUserPath()
# import libRepo
# libRepo.make_github_issue(title='Login Test', body='Body text', milestone=None, labels=['bug'])

