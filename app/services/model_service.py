import pickle

from app.config import FEATURE_SCALER_PATH, LABEL_SCALER_PATH, MODEL_REGISTRY
from app.models.model_factory import build_forecasting_model


class ArtifactError(RuntimeError):
    pass


_model_cache = {}
_scaler_cache = None


def available_models():
    return {
        key: {"label": config["label"]}
        for key, config in MODEL_REGISTRY.items()
    }


def get_model_config(model_key):
    if model_key not in MODEL_REGISTRY:
        raise ArtifactError(f"Unknown model '{model_key}'.")
    return MODEL_REGISTRY[model_key]


def load_scalers():
    global _scaler_cache
    if _scaler_cache is not None:
        return _scaler_cache

    missing = [
        str(path)
        for path in (FEATURE_SCALER_PATH, LABEL_SCALER_PATH)
        if not path.exists()
    ]
    if missing:
        raise ArtifactError(
            "Missing scaler artifact(s): "
            + ", ".join(missing)
            + ". Run the notebook training/scaler export cells first."
        )

    try:
        with FEATURE_SCALER_PATH.open("rb") as file:
            feature_scaler = pickle.load(file)
        with LABEL_SCALER_PATH.open("rb") as file:
            label_scaler = pickle.load(file)
    except Exception as exc:
        raise ArtifactError(f"Could not load scaler artifacts: {exc}") from exc

    _scaler_cache = (feature_scaler, label_scaler)
    return _scaler_cache


def load_model(model_key):
    if model_key in _model_cache:
        return _model_cache[model_key]

    config = get_model_config(model_key)
    weights_path = config["weights"]
    if not weights_path.exists():
        raise ArtifactError(
            f"Missing weights for {config['label']}: {weights_path}. Run notebook training first."
        )

    try:
        model = build_forecasting_model(recurrent=config["recurrent"])
        model.load_weights(weights_path)
    except Exception as exc:
        raise ArtifactError(f"Could not load {config['label']}: {exc}") from exc

    _model_cache[model_key] = model
    return model
