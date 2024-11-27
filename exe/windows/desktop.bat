:: arDESKTOP

:: Hide Commands
@echo off

set "newDir=%~dp0/../../scripts"
set "PYTHONPATH=%~dp0/../../scripts/extern"

start "" "pythonw %newDir%\pipeline.py" %1 --software desktop

exit
