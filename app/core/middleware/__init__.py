import time
import uuid

from flask import g, request


def register_middleware(app):
  @app.before_request
  def _start():
    g.req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    g.start_time = time.time()

  @app.after_request
  def _finish(resp):
    duration = (time.time() - getattr(g, "start_time", time.time())) * 1000
    resp.headers["X-Request-ID"] = getattr(g, "req_id", "")
    resp.headers["X-Response-Time-ms"] = f"{duration:.2f}"
    return resp
