#*********************************************************************
# content   = common functions
# version   = 0.0.1
# date      = 2018-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import glob
import time
import webbrowser

try:
    import libLog
    import libData
    import arNotice

    TITLE = os.path.splitext(os.path.basename(__file__))[0]
    LOG   = libLog.init(script=TITLE)
except: pass

#*********************************************************************
# FUNCTIONS
def get_help(name=''):
    project_data = libData.get_data('project')['HELP']
    if not name: name = os.getenv('SOFTWARE').lower()

    note = arNotice.Notice(title = name,
                           msg   = 'get help & solve issues here',
                           func  = 'HELP',
                           img   = 'lbl/lbl{}131'.format(name.title()),
                           img_link = '')
    arNotice.ArNotice(note)

    if name in project_data:
        webbrowser.open(project_data[name])
    else:
        webbrowser.open(project_data['main'])


# GET all (sub) keys in dict
def get_all_keys(key_list, dictonary=[]):
    for key, items in key_list.iteritems():
        dictonary.append(key)
        if isinstance(items, dict):
            get_all_keys(items, dictonary)

    return dictonary


# decorator: return function duration time
def get_duration(func):
    def timed(*args, **kw):
        startTime  = time.time()
        resultTime = func(*args, **kw)
        endTime    = time.time()

        printResult = '%r (%r, %r) %2.2f sec' % (func.__name__, args, kw, endTime-startTime)
        LOG.debug(printResult)
        return resultTime

    return timed


def find_inbetween(text, first, last):
    try:
        start = text.index(first) + len(first)
        end   = text.index(last, start)
    except ValueError: return ""
    return text[start:end]


#************************
# FOLDER
# @BRIEF  creates a folder, checks if it already exists,
#         creates the folder above if the path is a file
def create_folder(path):
    if len(path.split('.')) > 1: path = os.path.dirname(path)
    if not os.path.exists(path):
        try:    os.makedirs(path)
        except: LOG.warning('CANT create folder: {}'.format(path))

# @BRIEF  opens folder even if file is given
def open_folder(path):
    path = os.path.normpath(path)
    if os.path.exists(path):
        if len(path.split('.')) > 1: path = os.path.dirname(path)
        webbrowser.open(path)
    else: LOG.warning('UNVALID path: {}'.format(path))
    return path


#************************
# FILES
# @BRIEF  get a file/folder list with specifics
#
# @PARAM  path string.
#         file_type string/string[]. '*.py'
#         extension bool. True:[name.py] False:[name]
#         exclude string /string[]. '__init__.py' | '__init__' | ['btnReport48', 'btnHelp48']
#
# @RETURN strint[].
def get_file_list(path, file_type='*', extension=False, exclude='*', add_path=False):
    if(os.path.exists(path)):
        getFile = []
        try:    os.chdir(path)
        except: LOG.warning('Invalid dir: {}'.format(path))
        for file_name in glob.glob(file_type):
            if exclude in file_name: continue
            if add_path:  file_name = os.path.normpath(('/').join([path,file_name]))
            if extension: getFile.append(file_name)
            else:         getFile.append((file_name.split('.')[0]))
        return getFile

##
# @BRIEF  GET ALL subfolders in the path
def get_deep_folder_list(path, add_path=False):
    if add_path: getFile = map(lambda x: x[0], os.walk(path))
    else:        getFile = map(lambda x: os.path.basename(x[0]), os.walk(path))

    try:    getFile.pop(0)
    except: LOG.error('CANT pop file. Path: {}'.format(path), exc_info=True)

    return getFile
