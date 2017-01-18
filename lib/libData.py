#*********************************************************************
# content   = get and set data files for project and user
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
import json
import yaml

import libLog
import libUser
import libFileFolder

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.initLog(script=TITLE)

DATA_FORMAT = ".yml"
IMG_FORMAT  = ".png"


#************************
# CONFIG
def getData(file_name = '', user_id = libUser.getCurrentUser()):
    if not file_name:
        return getAllData(user_id)

    file_name = file_name.split('.')[0]
    file_path = ''

    if user_id:
        file_path = os.path.normpath(('/').join([getEnv('DATA_USER_PATH'), file_name + DATA_FORMAT]))

    if not os.path.exists(file_path):
        file_path = os.path.normpath(('/').join([getEnv('DATA_PROJECT_PATH'), file_name + DATA_FORMAT]))

    # OPEN data path
    if os.path.exists(file_path):
        LOG.debug(file_path)
        return getYmlFile(file_path)
    else:
        LOG.warning("CANT find {} file : {}".format(DATA_FORMAT, file_path))
    return ""


def getAllData(user_id = libUser.getCurrentUser()):
    config_data        = {}
    data_user_files    = libFileFolder.getFileList(path = getEnv('DATA_USER_PATH'),    file_type = '*' + DATA_FORMAT)
    data_project_files = libFileFolder.getFileList(path = getEnv('DATA_PROJECT_PATH'), file_type = '*' + DATA_FORMAT)

    data_project_files = list(set(data_user_files)|set(data_project_files))
    for each_file in data_project_files: config_data.update({each_file : getData(each_file, user_id)})
    return config_data


def setData(file_name, var, data):
    print("setData")
    # setYmlFile


#************************
# YAML
def setYmlFile(path, content):
    print "set YAML file"


def getYmlFile(path):
    with open(path, 'r') as stream:
        try:
            pipelinePath = yaml.load(stream)
            return pipelinePath
        except yaml.YAMLError as exc:
            LOG.error(exc)




def getPipelinePath(endPath):
    pipelinePath = os.environ.get("PIPELINE_PATH", "")
    if pipelinePath:
        pipelinePath = pipelinePath.split(";")
        # find first fitting path
        for eachPath in pipelinePath:
            path = os.path.normpath(("/").join([eachPath,endPath]))

            if os.path.exists(path):
                # LOG.debug("PATH exists: {0}".format(path))
                return path

        LOG.warning("PATH doesnt exists: {}".format(path))
    else:
        LOG.critical('PIPELINE_PATH doesnt exists.')

    return ""

def getImgPath(name = "btn/default"):
    path = getPipelinePath("img/" + name + IMG_FORMAT)
    if not path:
        path = getImgPath(("/").join([os.path.dirname(name), "default"]))
    return path


#************************
# TEMP IMAGE
def rmTmpImg():
    tmpImgPath = DATA.PATH_EXTRA["img_tmp"]  #temp user place (os independent)
    if os.path.exists(tmpImgPath):
        try:
            os.remove(tmpImgPath)
        except:
            LOG.error('FAIL : cant delete tmpFile : ' + tmpImgPath)
    return tmpImgPath


# @BRIEF  creates or add enviroment variable
#
# @PARAM  STRING var, STRING content
def addEnv(var, content):
    if os.environ.__contains__(var):
        os.environ[var] += ("").join([content, ";"])
    else:
        os.environ[var] = ("").join([content, ";"])
    return os.environ[var]

def getEnv(var):
    if os.environ.__contains__(var):
        return os.environ[var].split(';')[0]
    LOG.warning('ENV doesnt exist: {}'.format(var))
    return ""




# import sys
# sys.path.append("D:/Dropbox/arPipeline/2000/data")
# import setEnv
# setEnv.SetEnv()

# print getPipelinePath("img")
# print os.environ.get("PIPELINE_PATH", "")

# print getImgPath("btn/btnReport4")
