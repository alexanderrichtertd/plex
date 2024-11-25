#*********************************************************************
# content   = Testing environment
# date      = 2024-11-22
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys

pipeline_path = f'{os.path.dirname(os.path.dirname(__file__))}/config'
sys.path.append(pipeline_path)

# SETUP pipeline
import pipeline
pipeline.Setup()

# MOST important module
from tank import Tank
from software import Software


#*********************************************************************
# TESTING

# START dcc
Software().name = 'maya'
# Tank().start_software(dcc_name)

open_path = r'G:\My Drive\3 RESOURCES\github\plex\project\4_assets\assetName\GEO\WORK/assetName_GEO_v002.ma'
# Tank().start_software(dcc_name, open_path)

# open_file = "G:\My Drive\3 RESOURCES\github\plex\\project/4_assets/assetName/GEO/WORK/assetName_GEO_v002.ma"
# cmd = f'{Tank().config_software["start"]}'
# print(cmd)
for menu_item in Tank().config_software['MENU']:
    # print(menu_item)
    for key, value in menu_item.items():
        print(key, value)
        if value == 'None':
            print(f'MENU: {key}')
        else:
            print(value)