"""
data_loader.py

Loads structured test data from the ``data/`` directory. Currently backed by
JSON, but the public API (``DataLoader.load``) is format-agnostic by design:
adding CSV or Excel support later only requires adding a private
``_load_csv`` / ``_load_excel`` method and dispatching on file suffix, with
zero changes required in any test module that already calls ``load()``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config.config_manager import ConfigManager
from utilities.exceptions import DataLoadError
from utilities.logger import get_logger

logger = get_logger(__name__)


class DataLoader:
    """Loads and caches JSON test-data fixtures from the ``data/`` directory."""

    def __init__(self, config: ConfigManager | None = None) -> None:
        self._config = config or ConfigManager()
        self._data_dir = self._config.project_root / "data"
        self._cache: dict[str, Any] = {}

    def load(self, file_name: str) -> Any:
        """Load and return the parsed contents of ``data/<file_name>``.

        Args:
            file_name: File name including extension, e.g. 'login_data.json'.

        Returns:
            The parsed JSON content (list or dict).

        Raises:
            DataLoadError: If the file is missing or contains invalid JSON.
        """
        if file_name in self._cache:
            return self._cache[file_name]

        file_path = self._data_dir / file_name
        if not file_path.exists():
            raise DataLoadError(f"Test data file not found: {file_path}")

        suffix = file_path.suffix.lower()
        if suffix == ".json":
            data = self._load_json(file_path)
        else:
            raise DataLoadError(
                f"Unsupported test data format '{suffix}'. "
                "Only .json is currently supported; extend DataLoader to add more."
            )

        self._cache[file_name] = data
        return data

    @staticmethod
    def _load_json(file_path: Path) -> Any:
        try:
            with open(file_path, encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError as exc:
            raise DataLoadError(f"Invalid JSON in {file_path}: {exc}") from exc

    def get_case(self, file_name: str, case_id: str) -> dict[str, Any]:
        """Convenience accessor for data files structured as a list of
        dicts each containing an 'id' key."""
        records = self.load(file_name)
        for record in records:
            if record.get("id") == case_id:
                return record
        raise DataLoadError(f"No record with id '{case_id}' found in {file_name}")
