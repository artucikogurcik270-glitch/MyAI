@echo off
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║     TUMARIS AI CLUSTER - COMPLETE INSTALLATION        ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo This script will verify your setup and prepare the cluster
echo.
pause

echo.
echo [1/4] Checking prerequisites...
echo.

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
) else (
    echo [OK] Node.js found
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
) else (
    echo [OK] Python found
)

echo.
echo [2/4] Running diagnostics...
python diagnostics.py
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Some issues detected. Continue anyway? (Y/N)
    set /p continue=
    if /i not "%continue%"=="Y" exit /b 1
)

echo.
echo [3/4] Installing dependencies...
call install.bat
if %errorlevel% neq 0 (
    echo [ERROR] Installation failed!
    pause
    exit /b 1
)

echo.
echo [4/4] Starting cluster for the first time...
echo.
echo This will open 5 console windows.
echo Wait for all services to load (60-90 seconds)
echo.
pause

start_cluster.bat

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo [FINAL] Running quick test...
timeout /t 50 /nobreak >nul
python quick_test.py

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║            SETUP COMPLETE!                            ║
echo ╠════════════════════════════════════════════════════════╣
echo ║  Cluster is running on:                               ║
echo ║  http://localhost:3000                                ║
echo ║                                                        ║
echo ║  Try the interactive client:                          ║
echo ║  run_client.bat                                       ║
echo ╚════════════════════════════════════════════════════════╝
echo.
pause
