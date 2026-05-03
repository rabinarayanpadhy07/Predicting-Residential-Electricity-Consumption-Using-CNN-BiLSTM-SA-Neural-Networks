@echo off
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else if exist "C:\Users\padhy\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    set "PYTHON=C:\Users\padhy\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
) else (
    set "PYTHON=python"
)

echo Starting Residential Electricity Consumption Prediction UI...
%PYTHON% app.py
pause
