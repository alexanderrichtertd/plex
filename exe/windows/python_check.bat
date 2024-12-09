@echo off
setlocal EnableDelayedExpansion

:: Check if Python is in the PATH
for /f "delims=" %%i in ('where python') do (
    echo %%i | findstr /I "Microsoft\\WindowsApps" >NUL
    if !errorlevel! equ 0 (
        echo Found invalid Python at: %%i
    ) else (
        set "PYTHON_PATH=%%i"
        goto :CheckVersion
    )
)

if not defined PYTHON_PATH (
    echo Python is not in the PATH.
    echo Please install Python and add it to the PATH.
    exit /b 1
)

:CheckVersion
:: Check if Python version is 3.6 or higher
for /f "delims=" %%v in ('"%PYTHON_PATH%" --version 2^>^&1') do (
    set "PYTHON_VERSION=%%v"
    goto :VersionFound
)

:VersionFound
echo !PYTHON_VERSION! | findstr /R "^Python 3\.\(6\|[7-9]\|\d{2,}\)" >NUL
if !errorlevel! neq 0 (
    echo Please install Python 3.6 or higher: www.python.org
    exit /b 1
)

echo !PYTHON_VERSION! is installed and meets requirements (Python 3.6+).
echo.

:: exit /b 0