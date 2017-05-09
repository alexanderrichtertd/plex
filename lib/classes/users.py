#*********************************************************************
# content   = set und get user data
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

# why users? because user is already taken by python

import os
import sys

import libLog
import libData
from subclass import Singleton

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

class User(Singleton):
    def setup(self, user_id=os.getenv('username'), name=os.getenv('username'), settings = {}, rights = 'artist'):
        self.id       = user_id         # arichter
        self.initial  = self.id[0:2]    #  ar
        self.name     = name            # Alexander Richter

        self.settings = settings        # {'arLoad': []}
        self.rights   = rights          # admin, artist

        # self.birth    = birth           # 06.10.1986
        # self.task     = task            # {'LIGHT': [110, 120]}

        # self.position = position        # Pipeline

    def __call__(self):
        return (self.id, ': ',  self.name,
                '\nBirth: ',    self.birth,
                '\nTask: ',     self.task,
                '\nPosition: ', self.position,
                '\nSettings: ', self.settings)


    #************************
    # VARIABLES
    @property
    def id(self):
        return self.id

    @property
    def initial(self):
        return self.initial

    @property
    def name(self):
        return self.name

    @property
    def rights(self):
        return self.rights

    @property
    def get_project_user_path(user = os.getenv('username')):
        project_user_path = get_data('Path')['PROJECT_PATH']['user']
        return project_user_path + '/' + user

    #************************
    # EXTRAS
    @property
    def data_path(self):
        return "data_path"

    @property
    def user_path(self):
        return "user_path"

    @property
    def local_path(self):
        return "local_path"

    @property
    def is_admin(self):
        return False # True if self.rights == 'admin' else False


    #************************
    # FUNCTIONS
    def read_data(self):
        libData.get_data()

    def write_data(self, scriptSettings):
        currentChange = self.read_user()
        currentChange.__dict__["settings"].update(scriptSettings)
        setUser(currentChange)

    def delete_data(self):
        deletePath = os.path.join(DATA.PATH['data_user'], self.id)
        if os.path.exists(deletePath):
            LOG.info("DONE : " + self.id + " removed")
            os.remove(deletePath)
        else:
            LOG.info("FAIL : " + self.id + " - user doesnt exists")
