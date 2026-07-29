"""
video_utility.py

Helper for locating/organizing Playwright-recorded videos. Video *recording*
itself is configured on the BrowserContext (see BrowserFactory); this module
is responsible for post-processing: renaming the recorded file to something
human-readable and optionally discarding videos for passed tests when the
video_mode is 'retain-on-failure'.
"""

from __future__ import annotations

import re
from pathlib import Path

from playwright.sync_api import Page

from config.config_manager import ConfigManager
from utilities.logger import get_logger

logger = get_logger(__name__)


class VideoUtility:
    """Manages the lifecycle of per-test video recordings."""

    def __init__(self, config: ConfigManager | None = None) -> None:
        self._config = config or ConfigManager()
        self.output_dir = self._config.reports_dir / "videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _sanitize(name: str) -> str:
        return re.sub(r"[^A-Za-z0-9_.-]", "_", name)

    def finalize(self, page: Page, test_name: str, test_passed: bool) -> Path | None:
        """Rename the video for ``page`` and delete it if the test passed
        and ``video_mode`` is 'retain-on-failure'.

        Returns:
            The final path of the retained video, or None if it was discarded
            or no video was recorded.
        """
        video = page.video
        if video is None:
            return None

        should_retain = self._config.video_mode == "on" or (
            self._config.video_mode == "retain-on-failure" and not test_passed
        )

        try:
            original_path = Path(video.path())
        except Exception:  # noqa: BLE001 - video may not be flushed yet on some browsers
            logger.warning("Could not resolve recorded video path for %s", test_name)
            return None

        if not should_retain:
            original_path.unlink(missing_ok=True)
            return None

        final_path = self.output_dir / f"{self._sanitize(test_name)}{original_path.suffix}"
        original_path.replace(final_path)
        logger.info("Video retained: %s", final_path)
        return final_path
