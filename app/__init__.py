from flask import Flask

from .core import config as cfg
from .core.extensions import db, migrate, jwt, api
from .core.logging import setup_logging
from .core.middleware import register_middleware
from .core.responders import register_error_handlers


def create_app() -> Flask:
  app = Flask(__name__)
  app.config.from_object(cfg.Config)
  setup_logging(app)

  # extensões
  db.init_app(app)
  migrate.init_app(app, db)
  jwt.init_app(app)

  app.config.update(
    API_TITLE=cfg.Config.OPENAPI_TITLE,
    API_VERSION=cfg.Config.OPENAPI_VERSION,
    OPENAPI_VERSION="3.0.3",
    OPENAPI_URL_PREFIX=cfg.Config.OPENAPI_URL_PREFIX,
    OPENAPI_SWAGGER_UI_PATH=cfg.Config.OPENAPI_SWAGGER_UI_PATH,
    OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
  )
  api.init_app(app)
  api.spec.components.security_scheme(
    "bearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
  )

  # cross-cutting
  register_middleware(app)
  register_error_handlers(app)

  return app
