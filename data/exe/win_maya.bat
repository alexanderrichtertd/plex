:: MAYA

:: Hide Commands
@echo off

set "newDir=%~dp0\.."
python %newDir%\pipeline.py %1 --script software --software maya

::exit
