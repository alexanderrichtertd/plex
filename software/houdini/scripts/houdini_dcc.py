# content   = Houdini
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>


from plex import Plex
from software import Software

LOG = Plex().log(script=__name__)


class Houdini(Software):

    _NAME = 'houdini'
