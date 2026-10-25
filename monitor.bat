@echo off
title Tumaris Health Monitor
color 0A

:loop
cls
echo.
echo  ╔════════════════════════════════════════════════════════╗
echo  ║         TUMARIS CLUSTER - HEALTH MONITOR              ║
echo  ╚════════════════════════════════════════════════════════╝
echo.
echo  Current Time: %date% %time:~0,8%
echo.

echo  [Checking Services...]
echo.

curl -s http://localhost:3000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo  ✓ Node 1 - Router    [ONLINE]  Port: 3000
) else (
    echo  ✗ Node 1 - Router    [OFFLINE] Port: 3000
)

curl -s http://localhost:8001/health >nul 2>&1
if %errorlevel% equ 0 (
    echo  ✓ Node 2 - Ear       [ONLINE]  Port: 8001
) else (
    echo  ✗ Node 2 - Ear       [OFFLINE] Port: 8001
)

curl -s http://localhost:8002/health >nul 2>&1
if %errorlevel% equ 0 (
    echo  ✓ Node 3 - Brain     [ONLINE]  Port: 8002
) else (
    echo  ✗ Node 3 - Brain     [OFFLINE] Port: 8002
)

curl -s http://localhost:8003/health >nul 2>&1
if %errorlevel% equ 0 (
    echo  ✓ Node 4.1 - Styler  [ONLINE]  Port: 8003
) else (
    echo  ✗ Node 4.1 - Styler  [OFFLINE] Port: 8003
)

curl -s http://localhost:8004/health >nul 2>&1
if %errorlevel% equ 0 (
    echo  ✓ Node 4.2 - Voice   [ONLINE]  Port: 8004
) else (
    echo  ✗ Node 4.2 - Voice   [OFFLINE] Port: 8004
)

echo.
echo  ═══════════════════════════════════════════════════════
echo  Press Ctrl+C to exit or wait for next refresh...
echo.

timeout /t 5 /nobreak >nul
goto loop
