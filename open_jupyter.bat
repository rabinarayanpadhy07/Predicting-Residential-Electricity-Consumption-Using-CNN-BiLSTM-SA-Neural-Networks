@echo off
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else if exist "B:\ecpvenv\Scripts\python.exe" (
    set "PYTHON=B:\ecpvenv\Scripts\python.exe"
) else if exist "C:\Users\padhy\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    set "PYTHON=C:\Users\padhy\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
) else (
    set "PYTHON=python"
)

echo Opening Jupyter Notebook for Residential Electricity Consumption Prediction...
"%PYTHON%" -m jupyter notebook "ResElec-Pred (CNN-BiLSTM-SA).ipynb"
pause
