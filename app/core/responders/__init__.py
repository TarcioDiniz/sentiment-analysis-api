from flask import jsonify, request
from werkzeug.exceptions import HTTPException


def ok(data=None, message="OK", meta=None, status=200):
  return jsonify({"message": message, "data": data, "meta": meta or {}}), status


def register_error_handlers(app):
  @app.errorhandler(HTTPException)
  def _http(ex: HTTPException):
    return ok(None, ex.description or ex.name, {"status_code": ex.code, "path": request.path}, ex.code)

  @app.errorhandler(Exception)
  def _ex(ex: Exception):
    app.logger.exception("Unhandled error")
    return ok(None, "Internal Server Error", {"status_code": 500, "path": request.path}, 500)
