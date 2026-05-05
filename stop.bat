@echo off
REM ============================================================
REM SmartDoc AI - Stop Script
REM One-click stopper for Windows
REM ============================================================

echo.
echo ========================================
echo   SmartDoc AI - Stopping Application
echo ========================================
echo.

echo [STOP] Stopping Electron Frontend...
taskkill /F /IM electron.exe 2>NUL
echo [OK] Frontend stopped

echo.
echo [STOP] Stopping Python Backend...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq SmartDoc Backend*" 2>NUL
echo [OK] Backend stopped

echo.
echo [STOP] Stopping Ollama...
taskkill /F /IM ollama.exe 2>NUL
echo [OK] Ollama stopped

echo.
echo ========================================
echo   Application Stopped Successfully!
echo ========================================
echo.
timeout /t 2 /nobreak >nul