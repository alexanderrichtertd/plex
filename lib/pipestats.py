#*********************************************************************
# content   = popups and statistic loggings
# date      = 2024-11-09
#
# license   = MIT <https://github.com/alexanderrichtertd>
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import io
import yaml
import time
from datetime import datetime

import arNotice
from tank import Tank


#*********************************************************************
# VARIABLE
LOG = Tank().log.init(script=__name__)


#*********************************************************************
# FUNC
def notice(script_string, meta=False, notice=True):
    def decorator(function):
        def wrapper(*args, **kwargs):

            # NO Qt on the FARM
            if check_ui(): note = notice
            else: note = True

            start_time  = datetime.now()
            result_func = function(*args, **kwargs)
            result_time = (datetime.now() - start_time).total_seconds()

            if note:
                if ":" in str(result_func):
                    arNotice.create_default_notice(result_func)
                elif type(result_func) == str:
                    arNotice.create_default_notice("common:fail", result_func)
                else:
                    arNotice.create_default_notice(script_string)

            root, script_name = script_string.split(":")

            if ':' in script_string:
                if meta: LOG.info(f'{script_name} {"#" * 50} START')
                else: LOG.info(f'DONE - {script_name}')

                try:    set_exe_file(root, script_name, Tank().user_sandbox, result_time)
                except: LOG.error(f'STATS are broken: {root} {script_name} {Tank().user_sandbox} {result_time}', exc_info=True)

                hours, remainder = divmod(result_time, 3600)
                minutes, seconds = divmod(remainder, 60)

                if meta: LOG.info("{} {} {:02}:{:02}:{:02} END".format(script_name, "#" * 37, int(hours), int(minutes), int(seconds)))

            return result_func
        return wrapper
    return decorator


def check_ui():
    try:
        import maya.OpenMaya
        return maya.OpenMaya.MGlobal.mayaState() != maya.OpenMaya.MGlobal.kBatch
    except:
        return os.getenv("UID")


def set_exe_file(root, script_name, stats_path, result_time):
    user_config = {}

    if os.path.exists(stats_path):
        # READ YAML file
        with open(stats_path, 'r') as stream:
            user_config = yaml.load(stream)

    # CREATE entry if not existing
    if not user_config or not root in user_config:
        user_config[root] = {}
    if not script_name in user_config[root]:
        user_config[root][script_name]= { "count"    : 0,
                                        "time avg" : 0,
                                        "time min" : 0,
                                        "time max" : 0 }

    # FILL content
    user_config[root][script_name]["count"] += 1

    if user_config[root][script_name]["count"] == 1:
        user_config[root][script_name]["time avg"] = result_time
    else:
        avg_time = ((user_config[root][script_name]["time avg"] * (user_config[root][script_name]["count"] - 1))
                    + result_time) / user_config[root][script_name]["count"]
        user_config[root][script_name]["time avg"] = avg_time

    if result_time < user_config[root][script_name]["time min"] or user_config[root][script_name]["time min"] == 0:
        user_config[root][script_name]["time min"] = result_time
    if result_time > user_config[root][script_name]["time max"]:
        user_config[root][script_name]["time max"] = result_time

    # WRITE YAML file
    try:
        with io.open(stats_path, 'w', encoding='utf8') as outfile:
            yaml.dump(user_config, outfile, default_flow_style=False, allow_unicode=True)
    except:
        LOG.error(f"CAN'T write stats info into: {stats_path}", exc_info=True)



#*********************************************************************
# START
def example():
    @notice("common:open_folder", True)
    def echo(foo):
        time.sleep(0.2)
        print("DONE     - echo")

    echo('123456')

# example()
