@echo off
setlocal
title Space Research Big Data Platform

echo ======================================================================
echo    Space Research Data Analytics: Hadoop Ecosystem Demand Forecasting
echo ======================================================================
echo.

set PYTHON_EXE=C:\Users\DELL\AppData\Local\Programs\Python\Python314\python.exe

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python 3.14 not found at %PYTHON_EXE%
    pause
    exit /b 1
)

set SCRIPT_DIR=%~dp0
set PYTHONPATH=%SCRIPT_DIR%backend

echo [1/3] Checking Big Data Curated Storage (HDFS/Parquet)...
if not exist "%SCRIPT_DIR%hadoop_ecosystem\hdfs\space_research\curated\space_missions" (
    echo [INFO] Curated datasets not found. Running PySpark / Parquet ETL pipeline...
    "%PYTHON_EXE%" "%SCRIPT_DIR%hadoop_ecosystem\spark\jobs\spark_etl_pipeline.py"
) else (
    echo [OK] Curated HDFS Lakehouse datasets found.
)

echo.
echo [2/3] Launching FastAPI REST API and Big Data Dashboard Server...
echo [INFO] Server running on http://127.0.0.1:8000
echo.
echo [3/3] Opening browser at http://127.0.0.1:8000/ ...
start "" "http://127.0.0.1:8000/"

"%PYTHON_EXE%" -m uvicorn app.main:app --app-dir "%SCRIPT_DIR%backend" --host 127.0.0.1 --port 8000

pause
