 rem Set NukePath
set "NUKE_PATH=//bigfoot/breakingpoint/_pipeline/_sandbox/nuke/plugins/hive;%NUKE_PATH%"
set "HIVE=//bigfoot/breakingpoint/_pipeline/_sandbox/nuke/plugins/hive/HIVE"

 rem Start Nuke
set "NUKE_DIR=C:\Program Files\Nuke9.0v7"
set "PATH=%NUKE_DIR%;%PATH%"
start Nuke9.0.exe --nukex %1

