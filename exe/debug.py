#*********************************************************************
# content   = Testing environment
# date      = 2024-12-01
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys

plex_path = f'{os.path.dirname(os.path.dirname(__file__))}/scripts'
sys.path.append(plex_path)

# SETUP pipeline
from plex import Plex
Plex().setup()