#*********************************************************************
# content   = get and set data files for project and user
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

import libLog
import libFileFolder

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

try: import yaml
except:
    path = 'C:/Python27/Lib/site-packages'
    sys.path.append(path)
    LOG.debug('SYS_PATH added YAML: {}'.format(path))
    import yaml

DATA_FORMAT = '.yml'
IMG_FORMAT  = '.png'

# TODO: user_id with user class - see also below
# GET data from files
# Specific file or all files
def get_data(file_name='', user_id=os.getenv('username')):

    def get_all_data():
        config_data        = {}
        data_user_files    = libFileFolder.get_file_list(path=get_env('DATA_USER_PATH'),    file_type='*' + DATA_FORMAT)
        data_project_files = libFileFolder.get_file_list(path=get_env('DATA_PROJECT_PATH'), file_type='*' + DATA_FORMAT)

        data_project_files = list(set(data_user_files)|set(data_project_files))
        for each_file in data_project_files: config_data.update({each_file : get_data(each_file, user_id)})
        return config_data

    if not file_name:
        return get_all_data()

    file_name = file_name.split('.')[0]
    file_path = ''

    if user_id:
        file_path = os.path.normpath(('/').join([get_env('DATA_USER_PATH'), file_name + DATA_FORMAT]))

    if not os.path.exists(file_path):
        file_path = os.path.normpath(('/').join([get_env('DATA_PROJECT_PATH'), file_name + DATA_FORMAT]))

    # OPEN data path
    if os.path.exists(file_path):
        # LOG.debug(file_path)
        return get_yml_file(file_path)
    else:
        LOG.warning('CANT find file: {}'.format(file_path))
    return ''

def set_data(file_name, var, data):
    print('set_data')
    # set_yml_file


#************************
# GET PATH
def get_pipeline_path(end_path):
    pipeline_path = os.getenv('PIPELINE_PATH')
    if pipeline_path:
        pipeline_path = pipeline_path.split(';')
        # find first fitting path
        for eachPath in pipeline_path:
            path = os.path.normpath(('/').join([eachPath,end_path]))

            if os.path.exists(path):
                # LOG.debug('PATH exists: {0}'.format(path))
                return path

    LOG.warning('PATH doesnt exists: {}'.format(path))
    return ''

def get_img_path(end_path='btn/default'):
    if '.' in end_path: img_format = ''
    else: img_format = IMG_FORMAT
    path = get_pipeline_path('img/{}{}'.format(end_path, img_format))
    if not path:
        path = get_pipeline_path('img/btn/default{}'.format(IMG_FORMAT))
    return path


#************************
# YAML
def set_yml_file(path, content):
    print 'set YAML file'

def get_yml_file(path):
    with open(path, 'r') as stream:
        try:
            # STRING into DICT
            pipeline_path = yaml.load(stream)
            if pipeline_path:
                return pipeline_path
            else:
                LOG.warning('CANT load file: {}'.format(path))
        except yaml.YAMLError as exc:
            LOG.error(exc, exc_info=True)

# define & register custom tag handler
# combine var with strings
def join(loader, node):
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])

# replace (multiple) ENV var
def env(loader, node):
    seq  = loader.construct_sequence(node)
    path = os.getenv(seq[0])
    seq.pop(0)

    if ';' in path: path = path.split(';')
    else: path = [path]

    new_env = ''
    for env in path:
        if new_env: new_env += ';'
        new_env += env
        if seq: new_env += ''.join([str(os.path.normpath(i)) for i in seq])
    return new_env

# replace (multiple) with first ENV var
def env_first(loader, node):
    seq  = loader.construct_sequence(node)
    path = os.getenv(seq[0])
    seq.pop(0)

    if ';' in path: path = path.split(';')[0]
    else: path = path

    if seq: path += ''.join([str(os.path.normpath(i)) for i in seq])
    return path

yaml.add_constructor('!env', env)
yaml.add_constructor('!env_first', env_first)
yaml.add_constructor('!join', join)


# @BRIEF  creates or add enviroment variable
#
# @PARAM  STRING var, STRING content
def add_env(var, content):
    if os.environ.__contains__(var):
        os.environ[var] += ('').join([';', content])
    else:
        os.environ[var] = ('').join([content])
    return os.environ[var]

# GET env or empty str & WARNING
def get_env(var):
    if os.environ.__contains__(var):
        return os.environ[var].split(';')[0]
    LOG.warning('ENV doesnt exist: {}'.format(var))
    return ''

