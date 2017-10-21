
import os

import libData

from users import User
from software import Software

from subclass import Singleton


class Tank(Singleton):

    def init_os(self):
        self._user = User()
        self._user.setup()


    def init_software(self):
        self._software = Software()
        self._software.setup()
        self._software.print_header()

        self._user = User()
        self._user.setup()


    @property
    def software(self):
        return Software()

    @property
    def user(self):
        return self._user

    @property
    def context(self):
        return self._software.context

    @property
    def data(self):
        return libData.get_data()
