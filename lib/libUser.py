#*************************************************************
# title        libUser
#
# content      create user & save all informations 
#              of the person & his work
#
# author       Alexander Richter 
# email        contact@richteralexander.com
#*************************************************************

import os
import sys
import json

import settings as s
import libFileService


#************************
# USER
#************************
class User:
    def __init__(self, userId, name = '', birth = '', task = {}, position = '', settings = {}):       
        self.userId     = userId    # arichter
        self.name       = name      # Alexander Richter
        self.birth      = birth     # 06.10.1986
        self.task       = task      # {'LIGHT': [110, 120]}
        self.position   = position  # Pipeline
        self.settings   = settings  # {'arLoad': []}

    def __call__(self):
        return (self.userId, ': ', self.name, '\nBirth: ', self.birth, '\nTask: ', self.task, \
            '\nPosition: ', self.position, '\nSettings: ', self.settings)


#************************
# USER FUNCTIONS
#************************
def setUser(user):
    tmpDict = {}
    path    = s.PATH["data_user"] + "/" + user.userId + ".json"

    with open(path, 'w') as outfile:
        json.dump(user.__dict__, outfile)

    return user.__dict__


def getUser(userId):
    tmpDict  = {}
    userPath = s.PATH["data_user"] + "/" + userId + ".json"

    if not os.path.exists(userPath):
        setUser(User(userId = userId))

    try:
        with open(userPath, 'r') as outfile:
            tmpDict = json.load(outfile)
    except:
        print "libUser|getUser : User was not found"

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
    user = getUser(os.getenv('username'))

    if user.name:
        return user.name
    return os.getenv('username')


def getUserInitials(user = os.getenv('username')):
    return user[0:2]


def getUserList():
    with open(s.PATH["data_user"] + ".json", 'r') as outfile:
        return json.load(outfile).keys()


def deleteUser(userId):
    deletePath = os.path.join(s.PATH['data_user'], userId)

    if os.path.exists(deletePath):
        print ("DONE : " + userId + " removed")
        os.remove(deletePath)
    else:
        print ("FAIL : " + userId + " - user doesnt exists")


def setTeam():
    setUser(User(userId = 'arichter',   name = 'Alexander Richter', task = {}, position = 'Pipeline', settings = {}))
    setUser(User(userId = 'mlange',     name = 'Michael Lange', task = {}, position = 'Director', settings = {}))
    setUser(User(userId = 'mkuelkoeylue',  name = 'Manolya Kuelkoeylue', task = {}, position = 'Animation', settings = {}))
    setUser(User(userId = 'jtegethoff',  name = 'Jessica Tegethoff', task = {}, position = 'Animation', settings = {}))
    setUser(User(userId = 'nmaderthoner',  name = 'Nikolai Maderthoner', task = {}, position = 'Muscle', settings = {}))
    setUser(User(userId = 'joberbeck',  name = 'Julian Oberbeck', task = {"RIG" : [010, 020]}, position = 'Rigging', settings = {}))


# setTeam()