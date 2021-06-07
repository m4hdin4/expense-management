from app import app
from app.utils.JSONEncoder import JSONEncoder
from jsonschema.exceptions import ValidationError


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return JSONEncoder().encode({"error": e.schema}), 400


@app.errorhandler(401)
def handle_authorization_error(e):
    return JSONEncoder().encode({"error": "you should login first"}), 401


@app.errorhandler(Exception)
def handle_other_errors(e):
    return JSONEncoder().encode({"error": str(e)}), 400
