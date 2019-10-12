#*********************************************************************
# content   = set und get user data
# version   = 0.1.0
# date      = 2019-10-06
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

# why users? because user is already taken by python

import os
import sys

import pipefunc

import tank
from tank import Tank


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = Tank().log.init(script=TITLE)


#*********************************************************************
# USER
class User(tank.Singleton):
    def setup(self, user_id=os.getenv('username')):
        self.create()

        if os.path.exists(os.path.dirname(self.sandbox_path)):
            pipefunc.create_folder(self.sandbox_path)

    def create(self, user_id=os.getenv('username'), name=os.getenv('username'), settings = {}, rights = 'artist'):
        self._id       = user_id         # arichter
        self._initial  = self.id[0:2]    # ar
        self._name     = name            # Alexander Richter

        self._settings = settings        # {'arLoad': []}
        self._rights   = rights          # admin, artist

        # self._task     = task          # {'LIGHT': [110, 120]}
        # self._position = position      # Pipeline


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
    def data_user_path(self):
        data_user_path = '{}/{}.yml'.format(self.data_path, self.name)
        if not os.path.exists(data_user_path):
            data_user_path = ''
        return data_user_path

    @property
    def stats_path(self):
        return '{}/{}.stats'.format(self.data_path, self.name)

    @property
    def log_path(self):
        return '{}/{}.log'.format(self.data_path, self.name)

    @property
    def sandbox_path(self):
        return Tank().data_project['PATH']['sandbox'] + '/' + self._id


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
