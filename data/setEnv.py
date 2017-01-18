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

class SetEnv(object):

    def __init__(self):
        self.pipeline_env  = newDict()
        this_path          = os.path.normpath(os.path.dirname(__file__))
        this_pipeline_path = os.path.normpath(os.path.dirname(this_path))
        data_project_path  = os.path.normpath(("/").join([this_path, "pipeline.yml"]))

        if os.path.exists(data_project_path):
            with open(data_project_path , 'r') as stream:
                try:
                    self.data_project = yaml.load(stream)

                    if this_pipeline_path in self.data_project['PATH']:
                        for index in range(0, self.data_project["PATH"].index(this_pipeline_path)):
                            self.data_project['PATH'].pop(0)
                        self.pipeline_env["PIPELINE_PATH"] = self.data_project['PATH']
                    else:
                        print('STOP PROCESS\n\
                               Missing this PATH in {}\n\
                               GET:  {}\n\
                               NEED: {}'.format(data_project_path, self.data_project["PATH"], this_pipeline_path))
                        return
                except yaml.YAMLError as exc:
                    print("STOP PROCESS\nThe DATA file is corrupted.\n\n{}".format(exc))
                    return
        else:
            print ("STOP PROCESS\nCANT load DATA file: {}".format(data_project_path ))
            return

        for eachPath in self.data_project['PATH']:
            if not os.path.exists(eachPath):
                print('PROJECT PATH doesnt exists: {}\nSOURCE[PATH]: {}'.format(eachPath, data_project_path))
                continue

            self.pipeline_env.add("IMG_PATH",          eachPath + "/img")
            self.pipeline_env.add("LIB_PATH",          eachPath + "/lib")
            self.pipeline_env.add("SOFTWARE_PATH",     eachPath + "/software")
            self.pipeline_env.add("DATA_PATH",         eachPath + "/data")
            self.pipeline_env.add("DATA_USER_PATH",    eachPath + "/data/user/"    + os.getenv('username'))
            self.pipeline_env.add("DATA_PROJECT_PATH", eachPath + "/data/project/" + self.data_project['project'])

            sys.path.append(eachPath)
            sys.path.append(self.pipeline_env['SOFTWARE_PATH'][-1])
            sys.path.append(self.pipeline_env['LIB_PATH'][-1])

        addEnvVar("PIPELINE_PATH",     (";").join(self.pipeline_env["PIPELINE_PATH"]))
        addEnvVar("IMG_PATH",          (";").join(self.pipeline_env["IMG_PATH"]))
        addEnvVar("LIB_PATH",          (";").join(self.pipeline_env["LIB_PATH"]))
        addEnvVar("SOFTWARE_PATH",     (";").join(self.pipeline_env["SOFTWARE_PATH"]))
        addEnvVar("DATA_PATH",         (";").join(self.pipeline_env["DATA_PATH"]))
        addEnvVar("DATA_PROJECT_PATH", (";").join(self.pipeline_env["DATA_PROJECT_PATH"]))

        if not self.data_project['user_data']:
            self.pipeline_env["DATA_USER_PATH"] = ''
            print('USER DATA will be ignored.')

        addEnvVar("DATA_USER_PATH", (";").join(self.pipeline_env["DATA_USER_PATH"]))

        import libData
        config_project = libData.getData('project')

        os.environ["PROJECT_NAME"] = config_project["PROJECT"]["name"]
        os.environ["PROJECT_PATH"] = config_project["PROJECT"]["path"]

        self.__call__()


    def __call__(self):
        import libLog

        LOG = libLog.initLog(script=TITLE)
        LOG.debug("PATH:\n{}".format('[%s]' % ', '.join(map(str, sys.path))))

        text = ''
        tmp  = self.pipeline_env
        while tmp:
            key, value = tmp.popitem()
            text += '{:17} - {}\n'.format(key,value[0])

        LOG.debug('ENV:\n{}'.format(text))


#************************
# CLASS
class newDict(dict):
    def __init__(self):
        super(dict)
        self = dict()

    def add(self, key, value):
        value = os.path.normpath(value)
        if self.has_key(key):
            self[key].append(value)
        else:
            self[key] = [value]

#************************
# FUNCTIONS
def addEnvVar(var, content):
    content = os.path.normpath(content)
    if os.environ.__contains__(var):
        os.environ[var] += ("").join([";", content])
    else:
        os.environ[var] = content
    return os.environ[var]


# DELETE
a = SetEnv()

# print os.environ["DATA_USER_PATH"]
# # import libData
# # config_project = libData.getData()
# # print "DATA: {}".format(config_project)

# import libData
# # # print libData.getEnv("DATA_PROJECT_PATH")

# print libData.getData()

# a.__call__()
