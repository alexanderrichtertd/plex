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

import libLog
import libData

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
    libData.setData()

def setUserSettings(userId, scriptSettings):
    currentChange = getUser(userId)
    currentChange.__dict__["settings"].update(scriptSettings)
    setUser(currentChange)

def getCurrentUser():
    #user = getUser(os.getenv('username'))
    # if user.name:
    #     return user.name
    return os.getenv('username')

def getUserInitials(user = os.getenv('username')):
    return user[0:2]

# DO
def isUserAdmin():
    return True # getCurrentUser() in DATA.TEAM["admin"]

def getRights():
    return "user"

def deleteUser(userId):
    deletePath = os.path.join(DATA.PATH['data_user'], userId)
    if os.path.exists(deletePath):
        LOG.info("DONE : " + userId + " removed")
        os.remove(deletePath)
    else:
        LOG.info("FAIL : " + userId + " - user doesnt exists")

