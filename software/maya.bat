@echo off
 rem MAYA

 rem --- Path ---
set "PROJECT_ROOT=//bigfoot/revierkampf"
set "PIPELINE_PATH=%PROJECT_ROOT%/_pipeline"
set "STATUS_PATH=%PIPELINE_PATH%/WORK"
set "LIBRARY_PATH=%STATUS_PATH%/lib"
set "SOFTWARE_PATH=%STATUS_PATH%/software/maya"
set "IMG_PATH=%STATUS_PATH%/img/software/maya"

set "SCRIPT_PATH=%SOFTWARE_PATH%/scripts"
set "PLUGINS_PATH=%SOFTWARE_PATH%/plugins"
set "ARNOLD_PATH=%PLUGINS_PATH%/arnold"
set "ARNOLD_SHADER_PATH=%ARNOLD_PATH%/alShader"

set "MAYA_VERSION=2015"


 rem --- SCRIPT ---
set "MAYA_SCRIPT_PATH=%SCRIPT_PATH%/ANIM;%MAYA_SCRIPT_PATH%"
set "MAYA_SCRIPT_PATH=%PLUGINS_PATH%/arctracker;%MAYA_SCRIPT_PATH%"
set "MAYA_SCRIPT_PATH=%PLUGINS_PATH%/tweenmachine;%MAYA_SCRIPT_PATH%"


 rem --- Python ---
set "PYTHONPATH=%STATUS_PATH%;%PYTHONPATH%"
set "PYTHONPATH=%SOFTWARE_PATH%;%PYTHONPATH%"
set "PYTHONPATH=%PIPELINE_PATH%;%PYTHONPATH%"
set "PYTHONPATH=%LIBRARY_PATH%;%PYTHONPATH%"
set "PYTHONPATH=%PLUGINS_PATH%/ngskintools/scripts;%PYTHONPATH%"


 rem --- Plugin ---
set "MAYA_PLUG_IN_PATH=%PLUGINS_PATH%;%MAYA_PLUG_IN_PATH%;"
set "MAYA_PLUG_IN_PATH=%PLUGINS_PATH%/ngskintools/plug-ins;%MAYA_PLUG_IN_PATH%;"
 rem set "MAYA_PLUG_IN_PATH=%PLUGINS_PATH%/SOuP/plug-ins/win_maya2015;%MAYA_PLUG_IN_PATH%"


 rem --- Shelf ---
 rem --- set "MAYA_SHELF_PATH=%PLUGINS_PATH%/SOuP/shelves;%MAYA_SHELF_PATH%"
set "MAYA_SHELF_PATH=%SOFTWARE_PATH%/shelf;%MAYA_SHELF_PATH%"


 rem --- Icon ---
set "XBMLANGPATH=%PLUGINS_PATH%/SOuP/icons;%B%XBMLANGPATH%"


 rem --- Arnold ---
set "MtoA=%ARNOLD_PATH%/%MAYA_VERSION%"
set "MAYA_MODULE_PATH=%MtoA%;%MAYA_MODULE_PATH%"
set "PATH=%MtoA%/bin;%PATH%"
set "ARNOLD_PLUGIN_PATH=%MtoA%/shaders;%ARNOLD_PLUGIN_PATH%;%ARNOLD_PLUGIN_PATH%"
set "ARNOLD_PLUGIN_PATH=%ARNOLD_PATH%/bin;%ARNOLD_PLUGIN_PATH%;%ARNOLD_PLUGIN_PATH%"
set "ARNOLD_PLUGIN_PATH=%ARNOLD_SHADER_PATH%/bin;%ARNOLD_PLUGIN_PATH%"
set "MTOA_TEMPLATES_PATH=%ARNOLD_SHADER_PATH%/ae;%MTOA_TEMPLATES_PATH%"

set "ARNOLD_LICENSE_HOST=blue"


 rem --- RenderMan ---
set "RM=%PLUGINS_PATH%/renderman/RenderManStudio-20.9-maya2015"
set "MAYA_MODULE_PATH=%RM%/etc;%MAYA_MODULE_PATH%"
set "RMSTREE=%RM%"
set "PATH=%RM%/bin;%PATH%"


 rem --- Disable Report ---
set "MAYA_DISABLE_CIP=1"
set "MAYA_DISABLE_CER=1"


 rem --- MayaEnvVars ---
 rem set "MAYA_PROJECT=%PROJECT_ROOT%/2_production"
 rem cd %MAYA_PROJECT%


 rem --- SplashScreen ---
 rem File: MayaEDUStartupImage.png
set "XBMLANGPATH=%IMG_PATH%;%XBMLANGPATH%"


 rem --- Call Maya ---
set "MAYA_DIR=C:/Program Files/Autodesk/Maya%MAYA_VERSION%"
set "PATH=%MAYA_DIR%/bin;%PATH%"

if "%1"=="" (
  start "" "%MAYA_DIR%\bin\maya.exe"
) else (
  start "" "%MAYA_DIR%\bin\maya.exe" -file "%1"
) 

exit