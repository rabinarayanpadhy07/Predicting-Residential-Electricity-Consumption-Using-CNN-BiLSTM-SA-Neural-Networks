# Residential Electricity Consumption Prediction

This project predicts residential electricity consumption using historical household power consumption data and deep-learning models. It includes:

- A Flask web app for uploading test data and getting predictions
- A Jupyter notebook for model analysis, training, and comparison
- Saved model weights for running predictions without retraining

## Project Structure

```text
Dataset/
  household_power_consumption.csv   Main dataset used for scaler/model work
  testData.csv                      Sample input file for prediction

model/
  extension_weights.hdf5            Saved model weights used by Flask app
  propose_weights.hdf5              Saved CNN-BiLSTM-SA weights
  extension_hist.pckl               Saved training history
  propose_hist.pckl                 Saved training history

templates/                          Flask HTML pages
static/                             CSS and images
app.py                              Flask prediction web app
run.bat                             Shortcut to run the Flask app
open_jupyter.bat                    Shortcut to open the notebook
requirements.txt                    Python dependencies
ResElec-Pred (CNN-BiLSTM-SA).ipynb  Jupyter notebook
```

## Requirements

Use Windows with Python 3.12.

Install Python from:

```text
https://www.python.org/downloads/
```

During installation, select:

```text
Add python.exe to PATH
```

## First-Time Setup

Open Command Prompt or PowerShell in the project folder.

```powershell
cd "B:\Predicting-Residential-Electricity-Consumption-Using-CNN-BiLSTM-SA-Neural-Networks"
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Register the notebook kernel:

```powershell
python -m ipykernel install --user --name ecp-codex-python --display-name "ECP Python (fixed)"
```

## Run The Flask Web App

Option 1: double-click:

```text
run.bat
```

Option 2: run from terminal:

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000/index
```

Default login:

```text
username: admin
password: admin
```

Go to the Forecasting Tool page and upload a CSV or Excel file.

## Run The Jupyter Notebook

Option 1: double-click:

```text
open_jupyter.bat
```

Option 2: run from terminal:

```powershell
python -m jupyter notebook "ResElec-Pred (CNN-BiLSTM-SA).ipynb"
```

If Jupyter shows `Kernel Unknown`, select:

```text
Kernel -> Change Kernel -> ECP Python (fixed)
```

## Prediction Input Format

The uploaded prediction file should contain these columns:

```text
Date;Time;Global_active_power;Global_reactive_power;Voltage;Global_intensity
```

CSV files must use semicolon `;` separation.

Example:

```text
Date;Time;Global_active_power;Global_reactive_power;Voltage;Global_intensity
16/12/2006;17:59:00;2.472;0.058;236.940;10.400
```

You can test with:

```text
Dataset/testData.csv
```

## How Prediction Works

The Flask app loads the dataset and saved model when `app.py` starts.

1. It reads training data from `Dataset/household_power_consumption.csv`.
2. It converts `Date` into `year`, `month`, and `day`.
3. It converts `Time` into `hour`, `minute`, and `second`.
4. It creates the target label from:

```text
Sub_metering_1 + Sub_metering_2 + Sub_metering_3
```

5. It scales the input features and label using `MinMaxScaler`.
6. It loads saved model weights from `model/extension_weights.hdf5`.
7. When a test file is uploaded, the same date/time feature conversion and scaling are applied.
8. The neural network predicts electricity consumption.
9. The prediction is converted back to the original scale and shown on the web page.

The Flask app uses the saved extension model, which is CNN + self-attention + Bidirectional GRU. The notebook also contains the proposed CNN-BiLSTM-SA model and model-comparison work.

## Important Files

Do not delete these files if you want prediction to work:

```text
Dataset/household_power_consumption.csv
Dataset/testData.csv
model/extension_weights.hdf5
app.py
requirements.txt
templates/
static/
```

## Common Problems

If `python` is not recognized:

- Reinstall Python 3.12
- Make sure `Add python.exe to PATH` is selected
- Reopen Command Prompt or PowerShell

If `jupyter` is not recognized:

Use:

```powershell
python -m jupyter notebook
```

If `Kernel Unknown` appears:

Run:

```powershell
python -m ipykernel install --user --name ecp-codex-python --display-name "ECP Python (fixed)"
```

Then select:

```text
Kernel -> Change Kernel -> ECP Python (fixed)
```

If TensorFlow installation fails on Windows because of long paths, create the virtual environment in a short folder path, for example:

```powershell
python -m venv B:\ecpvenv
B:\ecpvenv\Scripts\activate
python -m pip install -r requirements.txt
```
