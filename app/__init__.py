from flask import Flask

from app.modules.auth.controllers.routes import blp as auth_blp
from app.modules.users.controllers.routes import blp as users_blp
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
    JSON_SORT_KEYS=False,
  )

  app.json.sort_keys = False
  api.init_app(app)
  api.register_blueprint(auth_blp, url_prefix="/api/v1")
  api.register_blueprint(users_blp, url_prefix="/api/v1")
  api.spec.components.security_scheme(
    "bearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
  )

  api.spec.options.update({"security": [{"bearerAuth": []}]})

  # cross-cutting
  register_middleware(app)
  register_error_handlers(app)

  return app
