"""
trace_utility.py

Manages Playwright trace viewer (.zip) files. Tracing is started on the
BrowserContext by BrowserFactory; this module stops tracing and decides
whether to keep or discard the trace based on ``trace_mode`` and the
outcome of the test, mirroring VideoUtility's retention behaviour.
"""

from __future__ import annotations

import re
from pathlib import Path

from playwright.sync_api import BrowserContext

from config.config_manager import ConfigManager
from utilities.logger import get_logger

logger = get_logger(__name__)


class TraceUtility:
    """Stops and stores Playwright traces for failed (or all) tests."""

    def __init__(self, config: ConfigManager | None = None) -> None:
        self._config = config or ConfigManager()
        self.output_dir = self._config.reports_dir / "traces"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _sanitize(name: str) -> str:
        return re.sub(r"[^A-Za-z0-9_.-]", "_", name)

    def finalize(self, context: BrowserContext, test_name: str, test_passed: bool) -> Path | None:
        """Stop tracing on ``context`` and persist the trace if warranted.

        Returns:
            Path to the saved trace .zip, or None if tracing was disabled
            or the trace was discarded because the test passed.
        """
        if self._config.trace_mode == "off":
            return None

        should_retain = self._config.trace_mode == "on" or (
            self._config.trace_mode == "retain-on-failure" and not test_passed
        )

        if not should_retain:
            context.tracing.stop()
            return None

        trace_path = self.output_dir / f"{self._sanitize(test_name)}_trace.zip"
        context.tracing.stop(path=str(trace_path))
        logger.info("Trace retained: %s", trace_path)
        return trace_path
