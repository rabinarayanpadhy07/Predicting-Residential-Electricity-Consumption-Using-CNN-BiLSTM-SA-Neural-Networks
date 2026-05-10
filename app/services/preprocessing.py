import io

import pandas as pd

from app.config import (
    DEFAULT_TEST_DATA_PATH,
    FEATURE_COLUMNS,
    NUMERIC_COLUMNS,
    TARGET_COMPONENT_COLUMNS,
)
from app.validators.upload_validator import validate_dataframe


class DataInputError(ValueError):
    def __init__(self, errors):
        self.errors = errors if isinstance(errors, list) else [str(errors)]
        super().__init__(" ".join(self.errors))


def read_prediction_dataframe(file_storage=None, json_payload=None):
    if json_payload is not None:
        records = json_payload.get("records", json_payload) if isinstance(json_payload, dict) else json_payload
        if isinstance(records, dict):
            records = [records]
        if not isinstance(records, list):
            raise DataInputError("JSON payload must be a record, a list of records, or {'records': [...]} .")
        return pd.DataFrame(records), "json-payload"

    if file_storage and file_storage.filename:
        filename = file_storage.filename.lower()
        try:
            if filename.endswith((".xls", ".xlsx")):
                return pd.read_excel(file_storage), file_storage.filename
            if filename.endswith(".csv"):
                raw = file_storage.read()
                file_storage.stream.seek(0)
                header = raw.splitlines()[0].decode("utf-8", errors="ignore") if raw else ""
                if ";" not in header:
                    raise DataInputError("CSV files must use semicolon ';' as the delimiter.")
                return pd.read_csv(io.BytesIO(raw), sep=";"), file_storage.filename
        except DataInputError:
            raise
        except Exception as exc:
            raise DataInputError(f"Could not read uploaded file: {exc}") from exc
        raise DataInputError("Unsupported file type. Upload CSV, XLS, or XLSX.")

    return pd.read_csv(DEFAULT_TEST_DATA_PATH, sep=";"), DEFAULT_TEST_DATA_PATH.name


def prepare_features(dataframe):
    validation = validate_dataframe(dataframe)
    if not validation.is_valid:
        raise DataInputError(validation.errors)

    working = dataframe.copy()
    original = working.copy()
    for column in NUMERIC_COLUMNS:
        working[column] = pd.to_numeric(working[column], errors="raise")

    dates = pd.to_datetime(working["Date"], format="%d/%m/%Y", dayfirst=True, errors="raise")
    times = pd.to_datetime(working["Time"], format="%H:%M:%S", errors="raise")

    working["year"] = dates.dt.year
    working["month"] = dates.dt.month
    working["day"] = dates.dt.day
    working["hour"] = times.dt.hour
    working["minute"] = times.dt.minute
    working["second"] = times.dt.second

    actual = None
    if all(column in working.columns for column in TARGET_COMPONENT_COLUMNS):
        for column in TARGET_COMPONENT_COLUMNS:
            working[column] = pd.to_numeric(working[column].replace("?", pd.NA), errors="coerce")
        if not working[TARGET_COMPONENT_COLUMNS].isna().any().any():
            actual = working[TARGET_COMPONENT_COLUMNS].sum(axis=1).astype(float).to_numpy()
    elif "Actual_consumption" in working.columns:
        actual_values = pd.to_numeric(working["Actual_consumption"], errors="coerce")
        if not actual_values.isna().any():
            actual = actual_values.astype(float).to_numpy()

    features = working[FEATURE_COLUMNS].astype(float)
    timestamps = original["Date"].astype(str) + " " + original["Time"].astype(str)
    return original, features, timestamps.tolist(), actual


def prepare_training_scaler_data(path, rows=10000):
    data = pd.read_csv(path, sep=";", nrows=rows).replace("?", 0)
    for column in NUMERIC_COLUMNS + TARGET_COMPONENT_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce").fillna(0)

    dates = pd.to_datetime(data["Date"], format="%d/%m/%Y", dayfirst=True, errors="coerce")
    times = pd.to_datetime(data["Time"], format="%H:%M:%S", errors="coerce")
    data["year"] = dates.dt.year.fillna(0).astype(int)
    data["month"] = dates.dt.month.fillna(0).astype(int)
    data["day"] = dates.dt.day.fillna(0).astype(int)
    data["hour"] = times.dt.hour.fillna(0).astype(int)
    data["minute"] = times.dt.minute.fillna(0).astype(int)
    data["second"] = times.dt.second.fillna(0).astype(int)
    label = data[TARGET_COMPONENT_COLUMNS].sum(axis=1).to_numpy().reshape(-1, 1)
    features = data[FEATURE_COLUMNS].astype(float).to_numpy()
    return features, label
