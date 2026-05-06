@echo off
REM ============================================================
REM SmartDoc AI - Hybrid Launcher
REM SidecarManager handles Python processes (Flask, ds2api, etc.)
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   SmartDoc AI - Hybrid Launcher
echo ========================================
echo.

REM Kill existing Electron instances
echo [CLEANUP] Checking for existing processes...
taskkill /F /IM electron.exe 2>NUL
echo [OK] Cleanup completed
echo.

REM Check Python venv
echo [CHECK] Verifying Python environment...
set BACKEND_DIR=%~dp0backend
if exist "%BACKEND_DIR%\venv\Scripts\python.exe" (
    echo [OK] Python venv found
) else (
    echo [INSTALL] Creating Python venv...
    cd /d "%BACKEND_DIR%"
    python -m venv venv
    echo [INSTALL] Installing dependencies...
    venv\Scripts\pip install -r requirements.txt >nul 2>&1
    echo [OK] Python environment ready
)
echo.

REM Check Node.js
echo [CHECK] Verifying Node.js...
where node.exe >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found! Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)
echo [OK] Node.js is installed
echo.

REM Start Electron (SidecarManager handles Python processes internally)
echo [START] Launching SmartDoc AI...
cd /d "%~dp0frontend"
start "" npm start
echo [OK] Application starting...
echo.

echo ========================================
echo   SmartDoc AI Started
echo ========================================
echo.
echo Close Electron window to stop everything.
echo.

:wait_loop
timeout /t 2 /nobreak >nul
tasklist /FI "IMAGENAME eq electron.exe" 2>NUL | find /I /N "electron.exe">NUL
if "%ERRORLEVEL%"=="0" goto wait_loop

echo.
echo [SHUTDOWN] Application closed. SidecarManager handles cleanup.
echo.
timeout /t 2 /nobreak >nul
