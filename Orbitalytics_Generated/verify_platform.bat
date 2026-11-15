@echo off
setlocal enabledelayedexpansion
title Orbitalytics 2.0 - Platform Integration Verification
echo ==============================================================================
echo       ORBITALYTICS 2.0: FULL INTEGRATION & QUALITY VERIFICATION SUITE
echo ==============================================================================
echo.

set SCRIPT_DIR=%~dp0
set PYTHON_EXE=C:\Users\DELL\AppData\Local\Programs\Python\Python314\python.exe

if not exist "!PYTHON_EXE!" (
    for /f "tokens=*" %%i in ('where python 2^>nul') do (
        set PYTHON_EXE=%%i
        goto :FoundPython
    )
    echo [ERROR] Python not found.
    pause
    exit /b 1
)

:FoundPython
set PYTHONPATH=%SCRIPT_DIR%backend
"!PYTHON_EXE!" "%SCRIPT_DIR%scripts\verify_orbitalytics_v2.py"

pause

