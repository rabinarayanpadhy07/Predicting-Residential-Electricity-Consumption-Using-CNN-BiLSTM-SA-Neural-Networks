@echo off
setlocal

cd /d "%~dp0"

if not defined APP_ENV_DIR set "APP_ENV_DIR=%LOCALAPPDATA%\ResElecForecasting\.venv"
set "PYTHON_CMD="

where py >nul 2>&1
if not errorlevel 1 (
    py -3.12 --version >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=py -3.12"
    if not defined PYTHON_CMD (
        py -3 --version >nul 2>&1
        if not errorlevel 1 set "PYTHON_CMD=py -3"
    )
)

if not defined PYTHON_CMD (
    where python >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo Python 3.12 or compatible Python 3 is required.
    echo Install Python from https://www.python.org/downloads/ and enable "Add Python to PATH".
    goto :fail
)

if not exist "%APP_ENV_DIR%\Scripts\python.exe" (
    echo Creating virtual environment at:
    echo %APP_ENV_DIR%
    %PYTHON_CMD% -m venv "%APP_ENV_DIR%"
    if errorlevel 1 goto :fail
)

call "%APP_ENV_DIR%\Scripts\activate.bat"

echo Installing project dependencies...
python -m pip install --upgrade pip
if errorlevel 1 goto :fail

python -m pip install -r requirements.txt
if errorlevel 1 goto :fail

if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo Created .env from .env.example
    )
)

echo.
echo Setup complete.
echo Virtual environment: %APP_ENV_DIR%
if /i "%~1"=="/nopause" exit /b 0
pause
exit /b 0

:fail
echo.
echo Setup failed. Check the error above and try again.
if /i "%~1"=="/nopause" exit /b 1
pause
exit /b 1
