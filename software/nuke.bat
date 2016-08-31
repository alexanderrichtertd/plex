@echo off
 rem NUKE

 rem --- Path ---
set "PROJECT_ROOT=//bigfoot/revierkampf"
set "PROJECT_ROOT=K:"
set "PIPELINE_PATH=%PROJECT_ROOT%/_pipeline"
set "STATUS_PATH=%PIPELINE_PATH%/WORK"
set "SOFTWARE_PATH=%STATUS_PATH%/software/nuke"

set "NUKE_VERSION=Nuke10.0v1"


 rem --- Settings & Lib ---
set "NUKE_PATH=%STATUS_PATH%;%NUKE_PATH%"
set "NUKE_PATH=%SOFTWARE_PATH%;%NUKE_PATH%"
set "NUKE_PATH=%PIPELINE_PATH%;%NUKE_PATH%"
set "NUKE_PATH=%PLUGIN_PATH%;%NUKE_PATH%"


 rem --- Init & Menu ---
set "NUKE_INIT_PATH=%SOFTWARE_PATH%;%NUKE_INIT_PATH%"
set "NUKE_MENU_PATH=%SOFTWARE_PATH%;%NUKE_MENU_PATH%"


 rem --- Call Nuke ---
set "NUKE_DIR=C:/Program Files/%NUKE_VERSION%"
set "PATH=%NUKE_DIR%;%PATH%"
start Nuke10.0.exe --nukex %1

