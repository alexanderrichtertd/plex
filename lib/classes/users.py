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
import libFunc

from subclass import Singleton

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

class User(Singleton):
    def setup(self, user_id=os.getenv('username')):
        self.create()

        if os.path.exists(os.path.dirname(self.user_path)):
            libFunc.create_folder(self.user_path)

    def create(self, user_id=os.getenv('username'), name=os.getenv('username'), settings = {}, rights = 'artist'):
        self._id       = user_id         # arichter
        self._initial  = self.id[0:2]    #  ar
        self._name     = name            # Alexander Richter

        self._settings = settings        # {'arLoad': []}
        self._rights   = rights          # admin, artist

        # self._task     = task            # {'LIGHT': [110, 120]}
        # self._position = position        # Pipeline


    def __call__(self):
        return (self.id, ': ',  self.name,
                '\nBirth: ',    self.birth,
                '\nTask: ',     self.task,
                '\nPosition: ', self.position,
                '\nSettings: ', self.settings)


    #*********************************************************************
    # VARIABLES
    @property
    def id(self):
        return self._id

    @property
    def initial(self):
        return self._initial

    @property
    def name(self):
        return self._name

    @property
    def rights(self):
        return self._rights

    @property
    def is_admin(self):
        return True if self._rights == 'admin' else False

    @property
    def data_path(self):
        return os.getenv('DATA_USER_PATH')

    @property
    def user_path(self):
        return libData.get_data('project')['PATH']['user'] + '/' + self._id


    #*********************************************************************
    # FUNCTIONS
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
