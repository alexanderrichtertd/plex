:: HOUDINI

:: Hide Commands
@echo off

CALL "%~dp0\setup_env.bat"

pythonw "%newDir%\pipeline.py" %1 --software houdini

exit

