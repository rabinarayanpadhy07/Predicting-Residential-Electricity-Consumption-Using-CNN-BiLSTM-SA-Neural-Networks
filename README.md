# Residential Electricity Consumption Prediction

This project predicts household electricity consumption from historical power-consumption data. It compares baseline machine-learning models with deep-learning models:

- Support Vector Regression
- Linear Regression
- CNN-BiLSTM with self-attention
- CNN-BiGRU with self-attention

The Flask web UI is separated into `app.py`, while the notebook is kept for data exploration, model comparison, and retraining.

## Project Structure

```text
Dataset/
  household_power_consumption.csv   Training/evaluation data
  testData.csv                      Sample prediction input
model/
  propose_weights.hdf5              Saved CNN-BiLSTM-SA weights
  extension_weights.hdf5            Saved CNN-BiGRU-SA weights
  propose_hist.pckl                 Saved training history
  extension_hist.pckl               Saved training history
static/
  default.css
  images/
templates/
  Flask HTML templates
app.py                              Standalone Flask web app
ResElec-Pred (CNN-BiLSTM-SA).ipynb  Notebook for model work
minepy.py                           Local compatibility fallback for MINE
requirements.txt                    Python dependencies
run.bat                             Starts the Flask UI on Windows
```

## Requirements

Use Python 3.12. The project has been updated to run with modern TensorFlow/Keras:

- TensorFlow 2.21+
- Keras 3.14+
- pandas 3+
- scikit-learn 1.8+

The original `minepy` package does not build reliably on current Python/NumPy versions, so this project includes a local `minepy.py` compatibility module that provides the `MINE` API used by the notebook.

## Setup

Open a terminal in the project folder:

```powershell
cd B:\ECP
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name ecp-python --display-name "ECP Python"
```

If Python is not available as `python`, install Python 3.12 and make sure it is added to PATH.

## Running The Flask UI

After setup, start the web app from the project folder:

```powershell
python app.py
```

On Windows, you can also double-click:

```text
run.bat
```

The app opens the browser automatically. If it does not, open:

```text
http://127.0.0.1:5000/index
```

Default login:

```text
username: admin
password: admin
```

Use the Forecasting Tool page to upload a CSV or Excel file. The expected input columns are:

```text
Date;Time;Global_active_power;Global_reactive_power;Voltage;Global_intensity
```

The included sample file is:

```text
Dataset/testData.csv
```

## Running The Notebook

Start Jupyter:

```powershell
jupyter notebook
```

Open:

```text
ResElec-Pred (CNN-BiLSTM-SA).ipynb
```

In Jupyter, select the correct kernel:

```text
Kernel -> Change Kernel -> ECP Python
```

Then run all cells from the top.

The notebook is now only for data exploration, model comparison, and retraining. The Flask UI code lives in `app.py`.

## Notes

- The saved model weights in `model/` are used if present. If weight files are removed, the notebook will retrain the neural models.
- The standalone Flask app uses `model/extension_weights.hdf5`.
- The dataset is loaded from `Dataset/household_power_consumption.csv`.
- The notebook uses inline Matplotlib plotting so graphs render inside Jupyter.
- TensorFlow may print CPU/GPU informational messages on Windows. Those messages are normal and are not project errors.
