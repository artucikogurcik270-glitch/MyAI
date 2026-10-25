@echo off
title Tumaris AI Cluster - Startup
color 0A

echo.
echo  ╔════════════════════════════════════════════════════════╗
echo  ║         TUMARIS AI CLUSTER - Starting Nodes           ║
echo  ╚════════════════════════════════════════════════════════╝
echo.

echo [SYSTEM] Checking prerequisites...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js
    pause
    exit /b 1
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python
    pause
    exit /b 1
)

echo [OK] Prerequisites found
echo.

echo [STARTUP] Launching Node 3 - Brain Service (Port 8002)...
start "Tumaris-Brain" cmd /k "cd /d D:\Project\Brain && python service.py"
timeout /t 3 /nobreak >nul

echo [STARTUP] Launching Node 2 - Ear Service (Port 8001)...
start "Tumaris-Ear" cmd /k "cd /d D:\Project\Ear && python service.py"
timeout /t 3 /nobreak >nul

echo [STARTUP] Launching Node 4.1 - Styler Service (Port 8003)...
start "Tumaris-Styler" cmd /k "cd /d D:\Project\Styler && python service.py"
timeout /t 3 /nobreak >nul

echo [STARTUP] Launching Node 4.2 - Voice Service (Port 8004)...
start "Tumaris-Voice" cmd /k "cd /d D:\Project\Voice && python service.py"
timeout /t 3 /nobreak >nul

echo [STARTUP] Launching Node 1 - Router Service (Port 3000)...
start "Tumaris-Router" cmd /k "cd /d D:\Project\Router && node server.js"
timeout /t 2 /nobreak >nul

echo.
echo  ╔════════════════════════════════════════════════════════╗
echo  ║              All Nodes Started Successfully            ║
echo  ╠════════════════════════════════════════════════════════╣
echo  ║  Node 1 (Router):  http://localhost:3000              ║
echo  ║  Node 2 (Ear):     http://localhost:8001              ║
echo  ║  Node 3 (Brain):   http://localhost:8002              ║
echo  ║  Node 4.1 (Styler): http://localhost:8003             ║
echo  ║  Node 4.2 (Voice):  http://localhost:8004             ║
echo  ╠════════════════════════════════════════════════════════╣
echo  ║  API Endpoint: http://localhost:3000/api/v1/process   ║
echo  ╚════════════════════════════════════════════════════════╝
echo.
echo [INFO] Press any key to view cluster status...
pause >nul

echo.
echo [STATUS] Checking node health...
timeout /t 5 /nobreak >nul

curl -s http://localhost:3000/health 2>nul
curl -s http://localhost:8001/health 2>nul
curl -s http://localhost:8002/health 2>nul
curl -s http://localhost:8003/health 2>nul
curl -s http://localhost:8004/health 2>nul

echo.
echo [SYSTEM] Cluster is running. Close this window to keep services active.
echo [SYSTEM] To stop all services, run: stop_cluster.bat
pause
