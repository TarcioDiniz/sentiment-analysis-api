import logging
import sys

from ..config import Config


def setup_logging(app):
  app.logger.setLevel(Config.LOG_LEVEL)

  stream = logging.StreamHandler(sys.stdout)
  stream.setLevel(Config.LOG_LEVEL)
  stream.setFormatter(logging.Formatter(
    "[%(asctime)s] %(levelname)s %(name)s %(message)s"
  ))
  app.logger.addHandler(stream)

  if Config.GRAYLOG_HOST:
    try:
      from graypy import GELFUDPHandler
      gelf = GELFUDPHandler(Config.GRAYLOG_HOST, Config.GRAYLOG_PORT)
      gelf.setLevel(Config.LOG_LEVEL)
      app.logger.addHandler(gelf)
    except Exception as e:
      app.logger.warning(f"Graylog não configurado: {e}")
