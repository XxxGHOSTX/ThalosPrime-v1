@echo off
REM © 2026 Tony Ray Macier III. All rights reserved.
REM
REM Thalos Prime v2.0 - Automatic Web Deployment (Windows)
REM One-click web interface launcher

echo.
echo ========================================================================
echo.
echo     ████████╗██╗  ██╗ █████╗ ██╗      ██████╗ ███████╗
echo     ╚══██╔══╝██║  ██║██╔══██╗██║     ██╔═══██╗██╔════╝
echo        ██║   ███████║███████║██║     ██║   ██║███████╗
echo        ██║   ██╔══██║██╔══██║██║     ██║   ██║╚════██║
echo        ██║   ██║  ██║██║  ██║███████╗╚██████╔╝███████║
echo        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
echo.
echo        SYNTHETIC BIOLOGICAL INTELLIGENCE v2.0
echo            AUTOMATIC WEB DEPLOYMENT
echo.
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

REM Run the Python deployment script
echo [INFO] Launching Python deployment script...
echo.

python auto_web_deploy.py

REM Exit with the same code as the Python script
exit /b %errorlevel%
