"""
environment_manager.py

Small companion to ConfigManager that exposes environment-specific
convenience helpers (e.g. deciding which base URL/tag to use for
'qa', 'staging', or 'prod' test runs). Kept separate from ConfigManager
to respect the Single Responsibility Principle: ConfigManager loads and
resolves configuration values, EnvironmentManager reasons about *which*
environment is active and what that implies for test execution.
"""

from __future__ import annotations

from config.config_manager import ConfigManager


class EnvironmentManager:
    """Provides environment-aware helpers built on top of ConfigManager."""

    VALID_ENVIRONMENTS = {"qa", "staging", "prod"}

    def __init__(self, config: ConfigManager | None = None) -> None:
        self._config = config or ConfigManager()

    @property
    def current(self) -> str:
        return self._config.active_environment

    def is_production(self) -> bool:
        return self.current == "prod"

    def is_qa(self) -> bool:
        return self.current == "qa"

    def validate(self) -> None:
        """Raise if the configured environment is not recognized."""
        if self.current not in self.VALID_ENVIRONMENTS:
            raise ValueError(
                f"Unknown environment '{self.current}'. "
                f"Expected one of {sorted(self.VALID_ENVIRONMENTS)}."
            )

    def describe(self) -> str:
        return (
            f"Environment={self.current} | "
            f"BaseURL={self._config.base_url} | "
            f"Browser={self._config.browser} | "
            f"Headless={self._config.headless}"
        )
