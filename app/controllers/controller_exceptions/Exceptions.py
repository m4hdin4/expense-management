from flask import Blueprint
from app.utils.JSONEncoder import JSONEncoder
from jsonschema.exceptions import ValidationError

app_exception = Blueprint("exception", __name__)


@app_exception.app_errorhandler(ValidationError)
def handle_validation_error(e):
    return JSONEncoder().encode({"error": e.schema}), 400


@app_exception.app_errorhandler(401)
def handle_authorization_error(e):
    return JSONEncoder().encode({"error": "you should login first"}), 401


@app_exception.app_errorhandler(Exception)
def handle_other_errors(e):
    return JSONEncoder().encode({"error": str(e)}), 400
