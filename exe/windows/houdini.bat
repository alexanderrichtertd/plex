:: HOUDINI

:: Hide Commands
@echo off

set "newDir=%~dp0/../../scripts"
set "PYTHONPATH=%~dp0/../../scripts/extern"

pythonw "%newDir%\pipeline.py" %1 --software houdini

exit

