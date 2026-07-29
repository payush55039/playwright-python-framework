"""
config_manager.py

Central configuration authority for the framework.

Reads defaults from ``config.yaml`` and allows every value to be overridden
by an environment variable of the same (upper-cased) name, which in turn may
be supplied via a ``.env`` file (loaded through ``python-dotenv``) or the CI
environment. This layered approach means the exact same codebase can be run
locally, in Docker, or in GitHub Actions without a single line of source
code being touched.

Precedence (highest wins):
    1. Explicit environment variable (``export BROWSER=firefox``)
    2. Value defined in ``.env``
    3. Value defined in ``config.yaml``
    4. Hard-coded fallback default in this module
"""

from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


class ConfigManager:
    """Thread-safe singleton responsible for all framework configuration.

    Example:
        >>> config = ConfigManager()
        >>> config.base_url
        'https://www.saucedemo.com'
        >>> config.browser
        'chromium'
    """

    _instance: ConfigManager | None = None
    _lock = threading.Lock()

    def __new__(cls, *args: Any, **kwargs: Any) -> ConfigManager:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._initialize()
                    cls._instance = instance
        return cls._instance

    def _initialize(self) -> None:
        """Load environment variables and the YAML configuration file once."""
        env_file = _PROJECT_ROOT / ".env"
        if env_file.exists():
            load_dotenv(dotenv_path=env_file, override=False)

        config_path = _PROJECT_ROOT / "config.yaml"
        self._raw_config: dict[str, Any] = {}
        if config_path.exists():
            with open(config_path, encoding="utf-8") as handle:
                self._raw_config = yaml.safe_load(handle) or {}

        active_env = self._env("ENV", self._raw_config.get("environment", "qa"))
        self._env_config: dict[str, Any] = self._raw_config.get("environments", {}).get(
            active_env, {}
        )
        self.active_environment = active_env

    @staticmethod
    def _env(key: str, default: Any) -> Any:
        return os.getenv(key, default)

    def _get(self, key: str, default: Any) -> Any:
        """Resolve a config value using the precedence rules described above."""
        env_value = os.getenv(key.upper())
        if env_value is not None:
            return env_value
        if key in self._env_config:
            return self._env_config[key]
        return self._raw_config.get(key, default)

    # ------------------------------------------------------------------
    # Typed configuration properties
    # ------------------------------------------------------------------
    @property
    def base_url(self) -> str:
        return str(self._get("base_url", "https://www.saucedemo.com"))

    @property
    def browser(self) -> str:
        return str(self._get("browser", "chromium")).lower()

    @property
    def headless(self) -> bool:
        value = self._get("headless", True)
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"1", "true", "yes"}

    @property
    def timeout(self) -> int:
        return int(self._get("timeout", 30_000))

    @property
    def navigation_timeout(self) -> int:
        return int(self._get("navigation_timeout", 30_000))

    @property
    def retry_count(self) -> int:
        return int(self._get("retry_count", 2))

    @property
    def slow_mo(self) -> int:
        return int(self._get("slow_mo", 0))

    @property
    def viewport_width(self) -> int:
        return int(self._get("viewport_width", 1920))

    @property
    def viewport_height(self) -> int:
        return int(self._get("viewport_height", 1080))

    @property
    def screenshot_on_failure(self) -> bool:
        value = self._get("screenshot_on_failure", True)
        return value if isinstance(value, bool) else str(value).lower() == "true"

    @property
    def video_mode(self) -> str:
        """One of: 'off', 'on', 'retain-on-failure'."""
        return str(self._get("video_mode", "retain-on-failure"))

    @property
    def trace_mode(self) -> str:
        """One of: 'off', 'on', 'retain-on-failure'."""
        return str(self._get("trace_mode", "retain-on-failure"))

    @property
    def log_level(self) -> str:
        return str(self._get("log_level", "INFO")).upper()

    @property
    def reports_dir(self) -> Path:
        return _PROJECT_ROOT / "reports"

    @property
    def project_root(self) -> Path:
        return _PROJECT_ROOT


config = ConfigManager()
