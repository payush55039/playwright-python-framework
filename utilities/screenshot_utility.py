"""
screenshot_utility.py

Handles capture and storage of screenshots, primarily for on-failure
diagnostics but usable at any point in a test for extra evidence.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import Page

from config.config_manager import ConfigManager
from utilities.logger import get_logger

logger = get_logger(__name__)


class ScreenshotUtility:
    """Captures full-page screenshots into ``reports/screenshots/``."""

    def __init__(self, config: ConfigManager | None = None) -> None:
        self._config = config or ConfigManager()
        self._output_dir = self._config.reports_dir / "screenshots"
        self._output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _sanitize(name: str) -> str:
        return re.sub(r"[^A-Za-z0-9_.-]", "_", name)

    def capture(self, page: Page, test_name: str, suffix: str = "") -> Path:
        """Capture a full-page screenshot for the given test.

        Args:
            page: The active Playwright page.
            test_name: Name of the executing test (used in the filename).
            suffix: Optional suffix, e.g. 'failure' or 'step_3'.

        Returns:
            Path to the saved screenshot file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = self._sanitize(test_name)
        suffix_part = f"_{self._sanitize(suffix)}" if suffix else ""
        file_path = self._output_dir / f"{safe_name}{suffix_part}_{timestamp}.png"

        page.screenshot(path=str(file_path), full_page=True)
        logger.info("Screenshot captured: %s", file_path)
        return file_path
