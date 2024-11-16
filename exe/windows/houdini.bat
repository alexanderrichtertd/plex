:: HOUDINI

:: Hide Commands
@echo off

set "newDir=%~dp0/../../config"
set "PYTHONPATH=%~dp0/../../lib/extern"

pythonw "%newDir%\pipeline.py" %1 --software houdini

exit

