#*********************************************************************
# content   = Testing environment
# date      = 2024-11-22
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys

pipeline_path = f'{os.path.dirname(os.path.dirname(__file__))}/scripts'
sys.path.append(pipeline_path)

# SETUP pipeline
import pipeline
pipeline.Setup()

# MOST important module
from plex import Plex
# Plex().software.name = 'maya'
# print(Plex().config_software)


#*********************************************************************
# TESTING

# START software
software_name = 'maya'
# from software import Software
# Plex().software.start(software_name)
# import arConfig
# arConfig.start()


open_path = r'G:\My Drive\3 RESOURCES\github\plex\project\4_assets\assetName\GEO\WORK/assetName_GEO_v002.ma'
# Plex().start_software(dcc_name, open_path)


print(Plex().software)