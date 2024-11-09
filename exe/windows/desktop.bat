:: arDESKTOP

:: Hide Commands
@echo off

CALL "%~dp0\setup_env.bat"

start "" "pythonw %newDir%\pipeline.py" %1 --software desktop

exit
