@echo off
 rem HOUDINI

 rem --- Path ---
set "PROJECT_ROOT=//bigfoot/revierkampf"
set "PIPELINE_PATH=%PROJECT_ROOT%/_pipeline/PUBLISH/software"
set "PLUGINS_PATH=%PIPELINE_PATH%/houdini/plugins"
set "HOUDINI_VERSION=Houdini 14.0.474"


 rem Set RR_ROOT

set "RR_ROOT=//smaug/Renderfarm/_RR6"

 rem Houdini Variables
 
set "PATH=%PLUGINS_PATH%/htoa-1.5.3_r1364_houdini-14.0.361/htoa-1.5.3_r1364_houdini-14.0.361/scripts/bin"
set "HOUDINI_PATH=%PIPELINE_PATH%/_sandbox/houdini/setup;%PLUGINS_PATH%/htoa-1.5.3_r1364_houdini-14.0.361/htoa-1.5.3_r1364_houdini-14.0.361;&"
set "HOUDINI_OTLSCAN_PATH=%PLUGINS_PATH%/qLib-dev/otls/experimental;%PLUGINS_PATH%/qLib-dev/otls/base;%PLUGINS_PATH%/houdini/qLib-dev/otls/future;%PIPELINE_PATH%/otl/publish;&"
 rem set "JOB=%PIPELINE_PATH%/_sandbox/houdini"
set "HOUDINI_BUFFEREDSAVE=1"
set "HOUDINI_USER_PREF_DIR=%PIPELINE_PATH%/_sandbox/houdini/setup/pref__HVER__"

 rem --- SplashScreen ---
 rem File: houdinisplash.png
set "HOUDINI_SPLASH_FILE=%PIPELINE_PATH%\img\logo\houdinisplash_sandbox.png"
set "HOUDINI_SPLASH_MESSAGE=BP SANDBOX HOUDINI"

 rem --- Call Houdini ---
set "HOUDINI=C:\Program Files\Side Effects Software\%HOUDINI_VERSION%\bin"
set "PATH=%PATH%;%HOUDINI%"
houdinifx %PYSETUP%

exit