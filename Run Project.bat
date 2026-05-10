@echo off
setlocal

cd /d "%~dp0"

if not defined APP_ENV_DIR set "APP_ENV_DIR=%LOCALAPPDATA%\ResElecForecasting\.venv"

if not exist "%APP_ENV_DIR%\Scripts\python.exe" (
    call setup_project.bat /nopause
    if errorlevel 1 goto :fail
)

call "%APP_ENV_DIR%\Scripts\activate.bat"

python -m pip show Flask >nul 2>&1
if errorlevel 1 call setup_project.bat /nopause
if errorlevel 1 goto :fail

echo Starting Residential Electricity Forecasting app...
echo Open http://127.0.0.1:5000/predict
python run.py

pause
exit /b 0

:fail
echo Failed to prepare the project environment.
pause
exit /b 1
