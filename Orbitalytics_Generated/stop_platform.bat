@echo off
title Stop Orbitalytics Platform
echo Stopping Orbitalytics backend server on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo Terminating PID: %%a
    taskkill /F /PID %%a 2>nul
)
echo Orbitalytics server stopped.
pause

