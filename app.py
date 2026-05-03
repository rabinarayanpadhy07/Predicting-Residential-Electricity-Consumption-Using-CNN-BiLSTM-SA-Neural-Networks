import os
import threading
import webbrowser
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, render_template, request
from keras.callbacks import ModelCheckpoint
from keras.layers import (
    GRU,
    Bidirectional,
    Convolution2D,
    Dense,
    Dropout,
    Flatten,
    Input,
    MaxPooling2D,
    RepeatVector,
)
from keras.models import Sequential
from keras.layers import Layer
from sklearn.preprocessing import MinMaxScaler


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "Dataset" / "household_power_consumption.csv"
DEFAULT_TEST_DATA = BASE_DIR / "Dataset" / "testData.csv"
WEIGHTS_PATH = BASE_DIR / "model" / "extension_weights.hdf5"
HISTORY_PATH = BASE_DIR / "model" / "extension_hist.pckl"


class attention(Layer):
    def __init__(self, return_sequences=True, name=None, **kwargs):
        super(attention, self).__init__(name=name, **kwargs)
        self.return_sequences = return_sequences

    def build(self, input_shape):
        self.W = self.add_weight(name="att_weight", shape=(input_shape[-1], 1), initializer="normal")
        self.b = self.add_weight(name="att_bias", shape=(input_shape[1], 1), initializer="zeros")
        super(attention, self).build(input_shape)

    def call(self, x):
        e = tf.math.tanh(tf.matmul(x, self.W) + self.b)
        a = tf.nn.softmax(e, axis=1)
        output = x * a
        if self.return_sequences:
            return output
        return tf.reduce_sum(output, axis=1)

    def compute_output_shape(self, input_shape):
        if self.return_sequences:
            return input_shape
        return (input_shape[0], input_shape[-1])


def preprocess_training_data(path=DATASET_PATH, rows=10000):
    dataset = pd.read_csv(path, sep=";", nrows=rows)
    dataset = dataset.replace("?", 0)
    for column in [
        "Global_active_power",
        "Global_reactive_power",
        "Voltage",
        "Global_intensity",
        "Sub_metering_1",
        "Sub_metering_2",
        "Sub_metering_3",
    ]:
        dataset[column] = dataset[column].astype(float)

    dataset["Date"] = pd.to_datetime(dataset["Date"], format="%d/%m/%Y", dayfirst=True)
    dataset["year"] = dataset["Date"].dt.year
    dataset["month"] = dataset["Date"].dt.month
    dataset["day"] = dataset["Date"].dt.day
    dataset["Time"] = pd.to_datetime(dataset["Time"], format="%H:%M:%S")
    dataset["hour"] = dataset["Time"].dt.hour
    dataset["minute"] = dataset["Time"].dt.minute
    dataset["second"] = dataset["Time"].dt.second
    dataset["label"] = (
        dataset["Sub_metering_1"] + dataset["Sub_metering_2"] + dataset["Sub_metering_3"]
    )
    dataset.drop(
        ["Date", "Time", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"],
        axis=1,
        inplace=True,
    )
    dataset.fillna(0, inplace=True)

    y = dataset["label"].to_numpy().reshape(-1, 1)
    x = dataset.drop(["label"], axis=1).values

    feature_scaler = MinMaxScaler((0, 1))
    label_scaler = MinMaxScaler((0, 1))
    feature_scaler.fit(x)
    label_scaler.fit(y)
    return feature_scaler, label_scaler


def preprocess_prediction_data(file_storage=None):
    if file_storage and file_storage.filename:
        filename = file_storage.filename.lower()
        if filename.endswith((".xls", ".xlsx")):
            data = pd.read_excel(file_storage)
        else:
            data = pd.read_csv(file_storage, sep=";")
    else:
        data = pd.read_csv(DEFAULT_TEST_DATA, sep=";")

    original = data.values
    data = data.replace("?", 0)
    data.fillna(0, inplace=True)

    numeric_columns = ["Global_active_power", "Global_reactive_power", "Voltage", "Global_intensity"]
    for column in numeric_columns:
        data[column] = data[column].astype(float)

    data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y", dayfirst=True)
    data["year"] = data["Date"].dt.year
    data["month"] = data["Date"].dt.month
    data["day"] = data["Date"].dt.day
    data["Time"] = pd.to_datetime(data["Time"], format="%H:%M:%S")
    data["hour"] = data["Time"].dt.hour
    data["minute"] = data["Time"].dt.minute
    data["second"] = data["Time"].dt.second
    data.drop(["Date", "Time"], axis=1, inplace=True)
    data.fillna(0, inplace=True)
    return original, data.values


def build_extension_model(input_shape=(10, 1, 1)):
    model = Sequential()
    model.add(Input(shape=input_shape))
    model.add(Convolution2D(32, (1, 1), activation="relu"))
    model.add(MaxPooling2D(pool_size=(1, 1)))
    model.add(Convolution2D(32, (1, 1), activation="relu"))
    model.add(MaxPooling2D(pool_size=(1, 1)))
    model.add(Flatten())
    model.add(RepeatVector(3))
    model.add(attention(return_sequences=True, name="attention"))
    model.add(Bidirectional(GRU(64, activation="relu", reset_after=False)))
    model.add(RepeatVector(3))
    model.add(Bidirectional(GRU(64, activation="relu", reset_after=False)))
    model.add(Dense(units=256, activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(units=1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model


def load_model():
    model = build_extension_model()
    if not WEIGHTS_PATH.exists():
        raise FileNotFoundError(
            f"Missing saved weights: {WEIGHTS_PATH}. Run the notebook training cells first."
        )
    model.load_weights(WEIGHTS_PATH)
    return model


feature_scaler, label_scaler = preprocess_training_data()
extension_model = load_model()

app = Flask(__name__)
app.secret_key = "welcome"


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html", msg="")


@app.route("/AdminLogin", methods=["GET", "POST"])
def admin_login():
    return render_template("AdminLogin.html", msg="")


@app.route("/AdminLoginAction", methods=["GET", "POST"])
def admin_login_action():
    if request.method == "POST" and "t1" in request.form and "t2" in request.form:
        user = request.form["t1"]
        password = request.form["t2"]
        if user == "admin" and password == "admin":
            return render_template("AdminScreen.html", msg=f"Welcome {user}")
    return render_template("AdminLogin.html", msg="Invalid login details")


@app.route("/Logout")
def logout():
    return render_template("index.html", msg="")


@app.route("/Predict", methods=["GET", "POST"])
def predict_view():
    return render_template("Predict.html", msg="")


@app.route("/PredictAction", methods=["GET", "POST"])
def predict_action():
    if request.method != "POST":
        return render_template("Predict.html", msg="")

    uploaded_file = request.files.get("t1")
    try:
        original_rows, processed = preprocess_prediction_data(uploaded_file)
        scaled = feature_scaler.transform(processed)
        model_input = np.reshape(scaled, (scaled.shape[0], scaled.shape[1], 1, 1))
        predictions = extension_model.predict(model_input, verbose=0).reshape(-1, 1)
        predictions = label_scaler.inverse_transform(predictions)
    except Exception as exc:
        return render_template("Predict.html", msg=f"Prediction failed: {exc}")

    output = []
    for row, prediction in zip(original_rows, predictions):
        output.append(
            f"Test Data = {row} Predicted Electricity Consumption ===> {abs(float(prediction[0])):.4f}"
        )
    return render_template("Predict.html", msg="<br/><br/>".join(output))


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/index")


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        threading.Timer(1.0, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
