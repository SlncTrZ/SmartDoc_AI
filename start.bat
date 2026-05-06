@echo off
REM ============================================================
REM SmartDoc AI - Launcher
REM Single window, auto-exit on app close
REM ============================================================

setlocal enabledelayedexpansion

title SmartDoc AI
echo.
echo ========================================
echo   SmartDoc AI
echo ========================================
echo.

REM Kill old Electron
taskkill /F /IM electron.exe 2>NUL

REM Check Python venv
set BACKEND_DIR=%~dp0backend
if not exist "%BACKEND_DIR%\venv\Scripts\python.exe" (
    echo [SETUP] Creating Python environment...
    cd /d "%BACKEND_DIR%"
    python -m venv venv
    venv\Scripts\pip install -r requirements.txt >nul
    echo [OK] Python ready
)

REM Check Node.js
where node.exe >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found
    pause
    exit /b 1
)

REM Launch Electron (this stays open until user closes app)
echo [START] Starting SmartDoc AI...
echo.
cd /d "%~dp0frontend"
call npm start

REM Cleanup on exit
echo.
echo App closed. Goodbye!
timeout /t 2 /nobreak >nul
exit /b 0
