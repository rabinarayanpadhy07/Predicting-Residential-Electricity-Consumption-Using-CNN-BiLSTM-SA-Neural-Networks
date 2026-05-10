import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"
ARTIFACTS_DIR = BASE_DIR / "ml_artifacts"

TRAINING_DATA_PATH = DATASET_DIR / "household_power_consumption.csv"
DEFAULT_TEST_DATA_PATH = DATASET_DIR / "testData.csv"
FEATURE_SCALER_PATH = ARTIFACTS_DIR / "feature_scaler.pkl"
LABEL_SCALER_PATH = ARTIFACTS_DIR / "label_scaler.pkl"

REQUIRED_COLUMNS = [
    "Date",
    "Time",
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
]

NUMERIC_COLUMNS = [
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
]

TARGET_COMPONENT_COLUMNS = [
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3",
]

FEATURE_COLUMNS = [
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "second",
]

MODEL_REGISTRY = {
    "extension": {
        "label": "Extension CNN-BiGRU-SA Model",
        "weights": ARTIFACTS_DIR / "extension_weights.hdf5",
        "history": ARTIFACTS_DIR / "extension_hist.pckl",
        "recurrent": "gru",
    },
    "proposed": {
        "label": "Proposed CNN-BiLSTM-SA Model",
        "weights": ARTIFACTS_DIR / "propose_weights.hdf5",
        "history": ARTIFACTS_DIR / "propose_hist.pckl",
        "recurrent": "lstm",
    },
}

DEFAULT_MODEL_KEY = "extension"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-local-secret-replace-in-production")
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH
    PORT = int(os.environ.get("FLASK_PORT", "5000"))
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
