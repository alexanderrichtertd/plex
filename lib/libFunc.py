#*************************************************************
# CONTENT       common functions (open|crete folder, file, help)
#
# AUTHOR        Alexander Richter
#*************************************************************

import os
import time
import webbrowser

# TEMP***************************
import sys
sys.path.append(r"..\settings")
#********************************
import getProject
DATA = getProject.GetProject()

# @BRIEF  creates or add enviroment variable
#
# @PARAM  STRING var, STRING content
def addEnvnVar(var, content):
    if os.environ.__contains__(var):
        os.environ[var] += ("").join([content, ";"])
    else:
        os.environ[var] = ("").join([content, ";"])
    return os.environ[var]

#************************
# HELP
# @BRIEF  gets the help link
#
# @PARAM  STRING title.
def getHelp(title=""):
    if title == "":
        title = os.getenv('SOFTWARE')
    if title in DATA.LINK:
        webbrowser.open(DATA.LINK[title])
    else:
        webbrowser.open(DATA.LINK.itervalues().next())


#************************
# TIME
# @BRIEF  gives back the time iterations of processes
#
# @PARAM  func func. tested function
#         iter int. iterations
#         data str. test parameter for func
def getProcessTime(func, iter, data):
    print func.__name__,
    r = xrange(iter)
    t1 = time.clock()
    for i in r:
        func(data)
        func(data)
        func(data)
        func(data)
        func(data)
        func(data)
        func(data)
        func(data)
        func(data)
        func(data)
    t2 = time.clock()
    roundUp = round(t2 - t1, 3)
    return roundUp
