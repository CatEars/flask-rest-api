from flask import Flask
from loguru import logger
import sys


def configure_logging(app: Flask):
    if app.config.log_config:
        logger.configure(**app.config.log_config)
    app.logger = logger
