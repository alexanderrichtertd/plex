

rem  ###################  Arnold/MtoA environment variables ###################
rem  ###################  required if you have not installed Arnold/MtoA locally ###################
set "RR_MTOA_BASE=c:\solidangle\mtoadeploy\2016" 
echo MtoA is installed in %RR_MTOA_BASE%
set "PATH=%RR_MTOA_BASE%\bin;%PATH%"
set "MAYA_MODULE_PATH=%RR_MTOA_BASE%;%MAYA_MODULE_PATH%"
set "MAYA_RENDER_DESC_PATH=%RR_MTOA_BASE%;%MAYA_RENDER_DESC_PATH%"
set "MAYA_PLUG_IN_PATH=%RR_MTOA_BASE%\plug-ins;%MAYA_PLUG_IN_PATH%"
set "ARNOLD_PLUGIN_PATH=%RR_MTOA_BASE%\shaders;%ARNOLD_PLUGIN_PATH%"

start "" "C:\Program Files\Autodesk\Maya2016\bin\maya.exe"