:: arDESKTOP

:: Hide Commands
@echo off

:: Check Python version
call "%~dp0\python_check.bat"
if %errorlevel% neq 0 (exit /b %errorlevel%)

python "%~dp0/../../scripts/plexstart.py" %1 --software desktop

exit
