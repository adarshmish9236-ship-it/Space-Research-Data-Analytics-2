@echo off
REM ============================================================================
REM ORBITALYTICS 2.0 — Interactive Final System Demonstration Launcher
REM ============================================================================
title ORBITALYTICS 2.0 System Demonstration
color 0B
cls

echo ============================================================================
echo   ORBITALYTICS 2.0 - Space Research Big Data Platform Demonstration
echo ============================================================================
echo.

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
cd /d "%PROJECT_ROOT%"

REM Detect Python executable
set PYTHON_BIN=python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    set PYTHON_BIN=C:\Users\DELL\AppData\Local\Programs\Python\Python314\python.exe
)

echo [INFO] Using Python binary: %PYTHON_BIN%
echo [INFO] Launching full 13-stage interactive system showcase...
echo.

%PYTHON_BIN% demonstration\run_orbitalytics_demo.py

echo.
echo ============================================================================
echo   Demonstration Sequence Concluded. Press any key to exit.
echo ============================================================================
pause >nul
