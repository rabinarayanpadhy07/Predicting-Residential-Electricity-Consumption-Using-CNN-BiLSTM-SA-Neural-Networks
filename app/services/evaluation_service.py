import pickle

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.config import MODEL_REGISTRY


def prediction_statistics(predictions):
    values = np.asarray(predictions, dtype=float)
    return {
        "total_rows": int(values.size),
        "min_prediction": float(np.min(values)) if values.size else 0.0,
        "max_prediction": float(np.max(values)) if values.size else 0.0,
        "average_prediction": float(np.mean(values)) if values.size else 0.0,
    }


def evaluation_metrics(actual, predictions):
    if actual is None:
        return None
    actual_values = np.asarray(actual, dtype=float)
    predicted_values = np.asarray(predictions, dtype=float)
    if actual_values.size == 0 or actual_values.size != predicted_values.size:
        return None

    non_zero = actual_values != 0
    mape = None
    if np.any(non_zero):
        mape = float(np.mean(np.abs((actual_values[non_zero] - predicted_values[non_zero]) / actual_values[non_zero])) * 100)

    return {
        "MAE": float(mean_absolute_error(actual_values, predicted_values)),
        "RMSE": float(np.sqrt(mean_squared_error(actual_values, predicted_values))),
        "R2 Score": float(r2_score(actual_values, predicted_values)),
        "MAPE": mape,
    }


def model_comparison_summary():
    rows = []
    for key, config in MODEL_REGISTRY.items():
        history_path = config["history"]
        row = {
            "key": key,
            "label": config["label"],
            "best_val_loss": None,
            "final_train_loss": None,
            "epochs": 0,
        }
        if history_path.exists():
            with history_path.open("rb") as file:
                history = pickle.load(file)
            losses = [float(value) for value in history.get("loss", [])]
            val_losses = [float(value) for value in history.get("val_loss", [])]
            row["epochs"] = max(len(losses), len(val_losses))
            row["final_train_loss"] = losses[-1] if losses else None
            row["best_val_loss"] = min(val_losses) if val_losses else None
        rows.append(row)
    return rows
