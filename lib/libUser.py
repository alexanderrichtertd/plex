#*********************************************************************
# content   = set und get user data
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
import json

import libLog

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.initLog(script=TITLE)

#************************
# USER
class User:
    def __init__(self, userId, name = '', birth = '', task = {}, position = '', settings = {}):
        self.userId     = userId    # arichter
        self.name       = name      # Alexander Richter
        self.birth      = birth     # 06.10.1986
        self.task       = task      # {'LIGHT': [110, 120]}
        self.position   = position  # Pipeline
        self.settings   = settings  # {'arLoad': []}

    def __call__(self):
        return (self.userId, ': ', self.name,
                '\nBirth: ',    self.birth,
                '\nTask: ',     self.task,
                '\nPosition: ', self.position,
                '\nSettings: ', self.settings)


#************************
# USER FUNCTIONS
def setUser(user):
    path = DATA.PATH["data_user"] + "/" + user.userId + DATA.FILE_FORMAT["data"]
    with open(path, 'w') as outfile:
        json.dump(user.__dict__, outfile)
    return user.__dict__

def getUser(userId):
    tmpDict  = {}
    userPath = DATA.PATH["data_user"] + "/" + userId + DATA.FILE_FORMAT["data"]

    if not os.path.exists(userPath):
        setUser(User(userId = userId))

    try:
        with open(userPath, 'r') as outfile:
            tmpDict = json.load(outfile)
    except:
        LOG.info("User was not found")

    tempUser =  User(userId = userId)
    tempUser.__dict__ = tmpDict
    return tempUser
    # return User(userId = tmpDict["userId"],   name = tmpDict["name"], task = tmpDict["task"], position = tmpDict["position"], settings = tmpDict["settings"])

def setUserSettings(userId, scriptSettings):
    currentChange = getUser(userId)
    currentChange.__dict__["settings"].update(scriptSettings)
    setUser(currentChange)

def getUserSettings(userId, scriptName):
    return getUser(userId).settings.values()

def getCurrentUser():
    #user = getUser(os.getenv('username'))
    # if user.name:
    #     return user.name
    return os.getenv('username')

def getUserInitials(user = os.getenv('username')):
    return user[0:2]

def getUserList():
    with open(DATA.PATH["data_user"] + DATA.FILE_FORMAT["data"], 'r') as outfile:
        return json.load(outfile).keys()

def isUserAdmin():
    return getCurrentUser() in DATA.TEAM["admin"]

def deleteUser(userId):
    deletePath = os.path.join(DATA.PATH['data_user'], userId)
    if os.path.exists(deletePath):
        LOG.info("DONE : " + userId + " removed")
        os.remove(deletePath)
    else:
        LOG.info("FAIL : " + userId + " - user doesnt exists")

def setTeam():
    setUser(User(userId = 'arichter',     name = 'Alexander Richter', task = {}, position = 'Pipeline', settings = {}))
    setUser(User(userId = 'mlange',       name = 'Michael Lange', task = {}, position = 'Director', settings = {}))
    setUser(User(userId = 'nmaderthoner', name = 'Nikolai Maderthoner', task = {}, position = 'Muscle', settings = {}))
    setUser(User(userId = 'joberbeck',    name = 'Julian Oberbeck', task = {"RIG" : [010, 020]}, position = 'Rigging', settings = {}))

def getRights():
    return "user"
