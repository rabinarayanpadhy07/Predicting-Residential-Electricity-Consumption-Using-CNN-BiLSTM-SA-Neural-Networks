import logging
from flask import Blueprint, jsonify, render_template, request

from app.config import DEFAULT_MODEL_KEY
from app.services.model_service import available_models
from app.services.prediction_service import build_prediction_response

logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

def render_predict_page(result=None, errors=None, selected_model=DEFAULT_MODEL_KEY, status_code=200):
    return (
        render_template(
            "Predict.html",
            result=result,
            errors=errors or [],
            models=available_models(),
            selected_model=selected_model or DEFAULT_MODEL_KEY,
        ),
        status_code,
    )

@main.route("/")
@main.route("/index", methods=["GET"])
def index():
    return render_template("index.html")

@main.route("/predict", methods=["GET"])
@main.route("/Predict", methods=["GET"])
def predict_view():
    return render_predict_page()

@main.route("/PredictAction", methods=["POST"])
def predict_action():
    selected_model = request.form.get("model_key", DEFAULT_MODEL_KEY)
    uploaded_file = request.files.get("t1")
    try:
        result, status_code = build_prediction_response(
            file_storage=uploaded_file,
            model_key=selected_model,
        )
    except Exception as exc:
        logger.exception("Prediction failed")
        return render_predict_page(
            errors=[str(exc)],
            selected_model=selected_model,
            status_code=400,
        )

    if not result.get("ok"):
        return render_predict_page(
            errors=result.get("errors", ["Prediction failed."]),
            selected_model=selected_model,
            status_code=status_code,
        )
    return render_predict_page(result=result, selected_model=selected_model)

@main.route("/api/predict", methods=["POST"])
def api_predict():
    selected_model = request.form.get("model_key") or request.args.get("model") or DEFAULT_MODEL_KEY
    uploaded_file = request.files.get("file") or request.files.get("t1")
    json_payload = None

    if request.is_json:
        json_payload = request.get_json(silent=True)
        if isinstance(json_payload, dict):
            selected_model = json_payload.get("model_key", json_payload.get("model", selected_model))

    try:
        result, status_code = build_prediction_response(
            file_storage=uploaded_file,
            json_payload=json_payload,
            model_key=selected_model,
        )
    except Exception as exc:
        logger.exception("API prediction failed")
        return jsonify({"ok": False, "errors": [str(exc)]}), 400

    return jsonify(result), status_code

@main.app_errorhandler(413)
def request_entity_too_large(_error):
    message = "Uploaded file is too large. Maximum allowed size is 16 MB."
    if request.path.startswith("/api/"):
        return jsonify({"ok": False, "errors": [message]}), 413
    return render_predict_page(errors=[message], status_code=413)
