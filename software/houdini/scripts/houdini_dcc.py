#*********************************************************************
# content   = Houdini
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os

from plex import Plex
from software import Software


#*********************************************************************
# VARIABLE
LOG = Plex().log(script=__name__)


#*********************************************************************
# CLASS
class Houdini(Software):

    _NAME = 'houdini'
