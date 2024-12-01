:: MAYA

:: Hide Commands
@echo off

CALL %~dp0\setup_env.bat

pythonw %newDir%\plex.py %1 --software maya

exit
