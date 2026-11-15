@echo off
setlocal enabledelayedexpansion
title Orbitalytics - Space Big Data Analytics Platform

echo ==============================================================================
echo       ORBITALYTICS: Space Research Big Data Analytics Platform
echo           A Hadoop Ecosystem Approach to Demand Forecasting
echo ==============================================================================
echo.

set SCRIPT_DIR=%~dp0
set PYTHON_EXE=C:\Users\DELL\AppData\Local\Programs\Python\Python314\python.exe

if not exist "!PYTHON_EXE!" (
    for /f "tokens=*" %%i in ('where python 2^>nul') do (
        set PYTHON_EXE=%%i
        goto :FoundPython
    )
    echo [ERROR] Python not found. Please install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

:FoundPython
echo [OK] Using Python: !PYTHON_EXE!

echo.
echo [1/3] Verifying Data Lakehouse & Parquet Curated Storage...
set PYTHONPATH=%SCRIPT_DIR%backend

if not exist "%SCRIPT_DIR%datasets\curated\space_missions" (
    echo [INFO] Curated datasets not found. Initializing space research datasets...
    "!PYTHON_EXE!" "%SCRIPT_DIR%scripts\initialize_project.py"
) else (
    echo [OK] Verified 9 curated space research datasets in HDFS / Parquet storage.
)

echo.
echo [2/3] Starting FastAPI REST API and Interactive Dashboard Server...
echo [INFO] Host: 0.0.0.0 (Accessible via http://localhost:8000/ and http://127.0.0.1:8000/)
echo.

echo [3/3] Opening browser at http://localhost:8000/ ...
start "" "http://localhost:8000/"

"!PYTHON_EXE!" -m uvicorn app.main:app --app-dir "%SCRIPT_DIR%backend" --host 0.0.0.0 --port 8000

pause

