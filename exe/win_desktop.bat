:: arDESKTOP

:: Hide Commands
@echo off

set "newDir=%~dp0\..\data"
start "" pythonw %newDir%\pipeline.py %1 --software desktop

exit
