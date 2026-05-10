# Residential Electricity Consumption Forecasting

Flask web application and research notebook for predicting residential electricity consumption with trained CNN-BiLSTM-SA and CNN-BiGRU-SA neural-network models.

## Features

- Upload CSV or Excel files and generate electricity-consumption predictions.
- Select between the Proposed CNN-BiLSTM-SA model and Extension CNN-BiGRU-SA model.
- View prediction summary cards, prediction records, model comparison, and an Actual vs Predicted graph.
- Use optional actual-value columns to calculate MAE, RMSE, R2 Score, and MAPE.
- Run predictions from the browser or through the `/api/predict` API.
- Open the training/research notebook from a shortcut.

## Project Structure

```text
app/                  Flask application package
dataset/              Input datasets and sample prediction file
ml_artifacts/         Trained model weights, histories, and scalers
research/             Jupyter notebook and helper code
.env.example          Example environment configuration
requirements.txt      Python dependencies
setup_project.bat     One-time Windows setup script
Run Project.bat       Shortcut to start the web app
Open Notebook.bat     Shortcut to open the notebook
run.py                Flask entry point
```

## Requirements

- Windows
- Python 3.12 or compatible Python 3
- Internet connection for first-time dependency installation

When installing Python, enable:

```text
Add Python to PATH
```

## First-Time Setup

Double-click:

```text
setup_project.bat
```

The setup script will:

- create a virtual environment
- install all packages from `requirements.txt`
- create `.env` from `.env.example` if `.env` does not exist

The virtual environment is created here:

```text
%LOCALAPPDATA%\ResElecForecasting\.venv
```

This short path avoids Windows long-path problems with TensorFlow and Jupyter.

## Run The Web App

Double-click:

```text
Run Project.bat
```

Then open:

```text
http://127.0.0.1:5000/predict
```

## Open The Notebook

Double-click:

```text
Open Notebook.bat
```

The notebook file is:

```text
research/ResElec-Pred (CNN-BiLSTM-SA).ipynb
```

## Input File Format

CSV files must use semicolon separation.

Required columns:

```text
Date;Time;Global_active_power;Global_reactive_power;Voltage;Global_intensity
```

Example:

```text
16/12/2006;17:59:00;2.472;0.058;236.940;10.400
```

Optional columns for actual-vs-predicted evaluation:

```text
Sub_metering_1;Sub_metering_2;Sub_metering_3
```

When these optional columns exist, the app calculates actual consumption as:

```text
Sub_metering_1 + Sub_metering_2 + Sub_metering_3
```

The dashboard then shows the Actual vs Predicted graph and evaluation metrics.

## API Usage

```powershell
curl -X POST http://127.0.0.1:5000/api/predict `
  -F "model_key=extension" `
  -F "file=@dataset/testData.csv"
```

Valid model keys:

```text
extension
proposed
```

## Manual Setup

Use this only if you do not want to use `setup_project.bat`.

```powershell
python -m venv "$env:LOCALAPPDATA\ResElecForecasting\.venv"
& "$env:LOCALAPPDATA\ResElecForecasting\.venv\Scripts\activate.ps1"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
python run.py
```

## Important Files

Do not delete these folders if you want the app to run:

```text
app/
dataset/
ml_artifacts/
research/
```

`ml_artifacts/` contains the trained model weights and scalers required for inference.

## Troubleshooting

If `python` is not recognized, reinstall Python and enable `Add Python to PATH`.

If dependency installation fails because of long paths, use `setup_project.bat`. It creates the virtual environment outside the project folder.

If the notebook shows an old cached page, close the notebook tab and reopen it using `Open Notebook.bat`.

If the web app is already running on port `5000`, stop the old Python process or change `FLASK_PORT` in `.env`.
