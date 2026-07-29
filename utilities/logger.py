"""
logger.py

Provides a single ``get_logger`` factory that produces a consistently
configured, structured logger shared across the entire framework. Logs are
written both to the console and to a rotating file inside
``reports/logs/``, so every action taken during a test run (browser launch,
navigation, clicks, assertions, teardown) is recoverable after the fact for
debugging flaky or failed runs.
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.config_manager import ConfigManager

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_configured_loggers: dict[str, logging.Logger] = {}


def _build_file_handler(log_dir: Path) -> RotatingFileHandler:
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        filename=log_dir / "automation.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
    return handler


def _build_console_handler() -> logging.StreamHandler:
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
    return handler


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for the given module name.

    Loggers are cached by name so repeated calls (e.g. from every page
    object) do not attach duplicate handlers.
    """
    if name in _configured_loggers:
        return _configured_loggers[name]

    config = ConfigManager()
    logger = logging.getLogger(name)
    logger.setLevel(config.log_level)
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(_build_console_handler())
        logger.addHandler(_build_file_handler(config.reports_dir / "logs"))

    _configured_loggers[name] = logger
    return logger
