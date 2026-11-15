@echo off
setlocal
title ORBITALYTICS 2.0 - Space Research Big Data Platform

echo ======================================================================
echo    ORBITALYTICS 2.0 : Space Research Big Data Analytics & Forecasting
echo ======================================================================
echo.

set PYTHON_EXE=C:\Users\DELL\AppData\Local\Programs\Python\Python314\python.exe

if not exist "%PYTHON_EXE%" (
    set PYTHON_EXE=python
)

set SCRIPT_DIR=%~dp0
set APP_DIR=%SCRIPT_DIR%backend
set PYTHONPATH=%APP_DIR%

echo [1/2] Launching ORBITALYTICS 2.0 Dashboard and API on http://localhost:8000 ...
echo [INFO] Swagger Docs: http://localhost:8000/docs
echo [INFO] Health Check: http://localhost:8000/api/v1/health
echo.

echo [2/2] Opening browser...
timeout /t 2 /nobreak >nul
start "" "http://localhost:8000/"

"%PYTHON_EXE%" -m uvicorn app.main:app --app-dir "%APP_DIR%" --host 0.0.0.0 --port 8000

pause

