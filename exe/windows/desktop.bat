:: arDESKTOP

:: Hide Commands
@echo off

set "newDir=%~dp0/../../data"
set "PYTHONPATH=%~dp0/../../lib/extern"

start "" "pythonw %newDir%\pipeline.py" %1 --software desktop

exit
