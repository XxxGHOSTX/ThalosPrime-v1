@echo off
REM ############################################################################
REM Thalos Prime v3.0 - Auto Deploy & Launch Script for Windows
REM 
REM This script automatically sets up and runs Thalos Prime after extraction
REM ############################################################################

setlocal enabledelayedexpansion

REM Colors (using ANSI escape codes if supported)
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "CYAN=[96m"
set "NC=[0m"

:BANNER
echo.
echo ============================================================================
echo.
echo     TTTTTTT  H     H   AAAAA   L        OOOOO    SSSSS
echo        T     H     H  A     A  L       O     O  S
echo        T     HHHHHHH  AAAAAAA  L       O     O   SSSSS
echo        T     H     H  A     A  L       O     O        S
echo        T     H     H  A     A  LLLLLLL  OOOOO   SSSSS
echo.
echo          SYNTHETIC BIOLOGICAL INTELLIGENCE v3.0
echo                 AUTO DEPLOYMENT SYSTEM
echo.
echo ============================================================================
echo.

:CHECK_PYTHON
echo [STEP] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.12 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python %PYTHON_VERSION% detected
echo.

:SETUP_VENV
echo [STEP] Setting up virtual environment...
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [INFO] Virtual environment already exists
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
echo [SUCCESS] Virtual environment activated
echo.

:INSTALL_DEPS
echo [STEP] Installing dependencies...
if exist "requirements.txt" (
    echo [INFO] Installing Python packages...
    python -m pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    echo [SUCCESS] Dependencies installed
) else (
    echo [WARN] requirements.txt not found
)
echo.

:SETUP_ENV
echo [STEP] Setting up environment configuration...
if not exist ".env" (
    if exist ".env.example" (
        echo [INFO] Creating .env file from template...
        copy .env.example .env
        echo [SUCCESS] .env file created
        echo [WARN] Remember to update .env with your settings
    )
) else (
    echo [INFO] .env file already exists
)
echo.

:ASK_TEST
set /p RUN_TEST="Run system tests before launch? (y/n): "
if /i "%RUN_TEST%"=="y" (
    echo [STEP] Running system tests...
    if exist "test_system.py" (
        python test_system.py
    ) else (
        echo [WARN] test_system.py not found
    )
    echo.
)

:LAUNCH_MENU
cls
echo.
echo ============================================================================
echo                          LAUNCH OPTIONS
echo ============================================================================
echo.
echo 1) Web Interface (Matrix Chatbot) [RECOMMENDED]
echo    - Matrix code rain background
echo    - Interactive chatbot interface
echo    - Real-time neural visualization
echo    URL: http://localhost:8000
echo.
echo 2) Command Line Interface (CLI)
echo    - Terminal-based interaction
echo    - Direct system access
echo.
echo 3) System Status
echo    - View comprehensive system status
echo    - Check all components
echo.
echo 4) Run Tests
echo    - Verify system integrity
echo    - Test all components
echo.
echo 5) Exit
echo.

set /p CHOICE="Enter your choice (1-5): "

if "%CHOICE%"=="1" goto LAUNCH_WEB
if "%CHOICE%"=="2" goto LAUNCH_CLI
if "%CHOICE%"=="3" goto SHOW_STATUS
if "%CHOICE%"=="4" goto RUN_TESTS
if "%CHOICE%"=="5" goto EXIT
echo [ERROR] Invalid choice. Please select 1-5.
timeout /t 2 >nul
goto LAUNCH_MENU

:LAUNCH_WEB
echo.
echo [STEP] Launching Web Interface...
echo [INFO] Starting server on http://localhost:8000
echo [INFO] Press Ctrl+C to stop
echo.
python thalos_prime.py web
goto EXIT

:LAUNCH_CLI
echo.
echo [STEP] Launching CLI Interface...
python thalos_prime.py cli --help
echo.
set /p CLI_CMD="Enter CLI command (or 'exit'): "
if not "%CLI_CMD%"=="exit" (
    python thalos_prime.py cli %CLI_CMD%
)
pause
goto LAUNCH_MENU

:SHOW_STATUS
echo.
echo [STEP] Getting System Status...
python thalos_prime.py status
pause
goto LAUNCH_MENU

:RUN_TESTS
echo.
echo [STEP] Running system tests...
python test_system.py
pause
goto LAUNCH_MENU

:EXIT
echo.
echo [SUCCESS] Thalos Prime deployment finished
echo.
pause
exit /b 0
