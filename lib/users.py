#*********************************************************************
# content   = set und get user config
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

# WHY 'users' and not 'user'?
# 'user' is already taken by Python

import os
import sys
import getpass

import pipefunc

import tank
from tank import Tank


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)
USER = getpass.getuser()


#*********************************************************************
# USER
class User(tank.Singleton):
    def setup(self, user_id=USER):
        self.create()

        if os.path.exists(os.path.dirname(self.sandbox_path)):
            pipefunc.create_folder(self.sandbox_path)

    def create(self, user_id=USER, name=USER, settings = {}, rights = 'artist'):
        self._id       = user_id         # arichter
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
    def name(self):
        return self._name

    @property
    def rights(self):
        return self._rights

    @property
    def is_admin(self):
        return True if self._rights == 'admin' else False

    @property
    def config_path(self):
        return os.getenv('CONFIG_USER_PATH')

    @property
    def config_user_path(self):
        config_user_path = f'{self.config_path}/{self.name}.yml'
        if not os.path.exists(config_user_path):
            config_user_path = ''
        return config_user_path

    @property
    def stats_path(self):
        return f'{self.config_path}/{self.name}.stats'

    @property
    def log_path(self):
        return f'{self.config_path}/{self.name}.log'

    @property
    def sandbox_path(self):
        return Tank().config_project['PATH']['sandbox'] + '/' + self._id


    #*********************************************************************
    # FUNCTIONS
    def write_config(self, scriptSettings):
        currentChange = self.read_user()
        currentChange.__dict__["settings"].update(scriptSettings)
        setUser(currentChange)

    def delete_config(self):
        deletePath = os.path.join(Tank.PATH['config_user'], self.id)
        if os.path.exists(deletePath):
            LOG.info("DONE : " + self.id + " removed")
            os.remove(deletePath)
        else:
            LOG.info("FAIL : " + self.id + " - user doesn\'t exists")
