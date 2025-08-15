import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


class Config:
  # Flask
  ENV = os.getenv("FLASK_ENV", "production")
  DEBUG = ENV == "development"
  SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

  # DB (MySQL)
  DB_USER = os.getenv("DB_USER", "root")
  DB_PASS = os.getenv("DB_PASS", "root")
  DB_HOST = os.getenv("DB_HOST", "localhost")
  DB_PORT = os.getenv("DB_PORT", "3306")
  DB_NAME = os.getenv("DB_NAME", "flask_api")

  user = quote_plus(DB_USER)
  pwd = quote_plus(DB_PASS)

  SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{user}:{pwd}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
  )
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # Logs
  LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
  GRAYLOG_HOST = os.getenv("GRAYLOG_HOST", "")
  GRAYLOG_PORT = int(os.getenv("GRAYLOG_PORT", "12201"))

  # OpenAPI / Swagger
  OPENAPI_TITLE = os.getenv("OPENAPI_TITLE", "Sentiment Analysis API")
  OPENAPI_VERSION = os.getenv("OPENAPI_VERSION", "1.0.0")
  OPENAPI_URL_PREFIX = os.getenv("OPENAPI_URL_PREFIX", "/")
  OPENAPI_SWAGGER_UI_PATH = os.getenv("OPENAPI_SWAGGER_UI_PATH", "/")
