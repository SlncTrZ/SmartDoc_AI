@echo off
REM ============================================================
REM SmartDoc AI - Startup Script
REM One-click launcher for Windows
REM ============================================================

echo.
echo ========================================
echo   SmartDoc AI - Starting Application
echo ========================================
echo.

REM Check if Ollama is running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Ollama is already running
) else (
    echo [START] Starting Ollama...
    start "" "ollama.exe" serve
    timeout /t 3 /nobreak >nul
    echo [OK] Ollama started
)

echo.
echo [START] Starting Python Backend...
cd /d "%~dp0backend"
start "SmartDoc Backend" /min python app.py
timeout /t 3 /nobreak >nul
echo [OK] Backend started

echo.
echo [START] Starting Electron Frontend...
cd /d "%~dp0frontend"
start "" npm start
echo [OK] Frontend started

echo.
echo ========================================
echo   Application Started Successfully!
echo ========================================
echo.
echo NOTE: Keep all terminal windows open!
echo   - Ollama window (backend for AI)
echo   - Python Backend window (port 5000)
echo   - Electron window (main application)
echo.
echo Press any key to close this window...
pause >nul