import numpy as np

from app.config import DEFAULT_MODEL_KEY, MODEL_REGISTRY
from app.services.evaluation_service import (
    evaluation_metrics,
    model_comparison_summary,
    prediction_statistics,
)
from app.services.model_service import load_model, load_scalers
from app.services.preprocessing import prepare_features, read_prediction_dataframe
from app.validators.upload_validator import validate_model_key


def build_prediction_response(file_storage=None, json_payload=None, model_key=DEFAULT_MODEL_KEY):
    selected_model = model_key or DEFAULT_MODEL_KEY
    model_validation = validate_model_key(selected_model, MODEL_REGISTRY.keys())
    if not model_validation.is_valid:
        return {"ok": False, "errors": model_validation.errors}, 400

    dataframe, source_name = read_prediction_dataframe(file_storage=file_storage, json_payload=json_payload)
    original, features, timestamps, actual = prepare_features(dataframe)
    feature_scaler, label_scaler = load_scalers()
    model = load_model(selected_model)

    scaled = feature_scaler.transform(features.to_numpy())
    model_input = np.reshape(scaled, (scaled.shape[0], scaled.shape[1], 1, 1))
    scaled_predictions = model.predict(model_input, verbose=0).reshape(-1, 1)
    predictions = np.abs(label_scaler.inverse_transform(scaled_predictions).reshape(-1))

    records = []
    for index, prediction in enumerate(predictions):
        row = original.iloc[index]
        records.append(
            {
                "timestamp": timestamps[index],
                "Date": str(row["Date"]),
                "Time": str(row["Time"]),
                "Global_active_power": float(row["Global_active_power"]),
                "Global_reactive_power": float(row["Global_reactive_power"]),
                "Voltage": float(row["Voltage"]),
                "Global_intensity": float(row["Global_intensity"]),
                "predicted_consumption": float(prediction),
                "actual_consumption": float(actual[index]) if actual is not None else None,
            }
        )

    metrics = evaluation_metrics(actual, predictions)
    response = {
        "ok": True,
        "selected_model": selected_model,
        "model_label": MODEL_REGISTRY[selected_model]["label"],
        "metadata": {
            "source": source_name,
            "rows": len(records),
            "features": list(features.columns),
            "scalers": ["ml_artifacts/feature_scaler.pkl", "ml_artifacts/label_scaler.pkl"],
        },
        "predictions": records,
        "statistics": prediction_statistics(predictions),
        "metrics": metrics,
        "model_comparison": model_comparison_summary(),
        "errors": [],
    }
    return response, 200
