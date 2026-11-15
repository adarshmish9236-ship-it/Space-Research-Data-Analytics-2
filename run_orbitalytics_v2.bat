@echo off
setlocal
title ORBITALYTICS 2.0 - Space Research Big Data Platform

echo ======================================================================
echo    ORBITALYTICS 2.0 : Space Research Big Data Analytics & Forecasting
echo ======================================================================
echo.

set PYTHON_EXE=C:\Users\DELL\AppData\Local\Programs\Python\Python314\python.exe

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python not found at %PYTHON_EXE%
    echo Falling back to system python...
    set PYTHON_EXE=python
)

set SCRIPT_DIR=%~dp0
set APP_DIR=%SCRIPT_DIR%Orbitalytics_Generated\backend
set PYTHONPATH=%APP_DIR%

echo [1/3] Checking Medallion Lakehouse Storage...
if not exist "%SCRIPT_DIR%Orbitalytics_Generated\datasets\curated\fact_space_missions.parquet" (
    echo [INFO] Running Medallion Ingestion & ETL...
    "%PYTHON_EXE%" -c "from app.services.ingestion_service import IngestionService; IngestionService().run_full_medallion_pipeline()"
) else (
    echo [OK] Medallion Lakehouse data verified.
)

echo.
echo [2/3] Launching ORBITALYTICS 2.0 Dashboard and API on http://localhost:8000 ...
echo [INFO] Swagger Docs: http://localhost:8000/docs
echo [INFO] Health Check: http://localhost:8000/api/v1/health
echo.

echo [3/3] Opening browser...
timeout /t 2 /nobreak >nul
start "" "http://localhost:8000/"

"%PYTHON_EXE%" -m uvicorn app.main:app --app-dir "%APP_DIR%" --host 0.0.0.0 --port 8000

pause

