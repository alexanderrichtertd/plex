#*********************************************************************
# content   = Houdini
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os

from tank import Tank
from software import Software


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)


#*********************************************************************
# CLASS
class Houdini(Software):

    _NAME = 'houdini'
