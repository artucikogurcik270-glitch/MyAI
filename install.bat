@echo off
echo ====================================
echo Tumaris AI Cluster - Installation
echo ====================================
echo.

echo [1/5] Installing Node 1 - Router (Node.js)...
cd /d D:\Project\Router
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Router installation failed
    pause
    exit /b 1
)
echo Router installed successfully
echo.

echo [2/5] Installing Node 2 - Ear Service (Python)...
cd /d D:\Project\Ear
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Ear service installation failed
    pause
    exit /b 1
)
echo Ear service installed successfully
echo.

echo [3/5] Installing Node 3 - Brain Service (Python)...
cd /d D:\Project\Brain
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Brain service installation failed
    pause
    exit /b 1
)
echo Brain service installed successfully
echo.

echo [4/5] Installing Node 4.1 - Styler Service (Python)...
cd /d D:\Project\Styler
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Styler service installation failed
    pause
    exit /b 1
)
echo Styler service installed successfully
echo.

echo [5/5] Installing Node 4.2 - Voice Service (Python)...
cd /d D:\Project\Voice
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Voice service installation failed
    pause
    exit /b 1
)
echo Voice service installed successfully
echo.

echo ====================================
echo All services installed successfully!
echo ====================================
echo.
echo To start the cluster, run: start_cluster.bat
pause
