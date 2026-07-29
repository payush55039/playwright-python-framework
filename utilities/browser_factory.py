"""
browser_factory.py

Encapsulates all Playwright browser/context creation logic so that no test
or page object needs to know how a browser is launched. Centralizing this
here means switching from Chromium to Firefox/WebKit, adding proxy support,
or turning on tracing/video is a one-file change.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from playwright.sync_api import Browser, BrowserContext, Page, Playwright

from config.config_manager import ConfigManager
from utilities.exceptions import ConfigurationError
from utilities.logger import get_logger

logger = get_logger(__name__)

SupportedBrowser = Literal["chromium", "firefox", "webkit"]
_SUPPORTED_BROWSERS = {"chromium", "firefox", "webkit"}


class BrowserFactory:
    """Creates and configures Browser / BrowserContext / Page instances."""

    def __init__(self, playwright: Playwright, config: ConfigManager | None = None) -> None:
        self._playwright = playwright
        self._config = config or ConfigManager()

    def launch_browser(self, browser_name: str | None = None) -> Browser:
        """Launch the requested browser engine (defaults to config value)."""
        name = (browser_name or self._config.browser).lower()
        if name not in _SUPPORTED_BROWSERS:
            raise ConfigurationError(
                f"Unsupported browser '{name}'. Expected one of {sorted(_SUPPORTED_BROWSERS)}."
            )

        logger.info("Launching Browser: %s (headless=%s)", name, self._config.headless)
        engine = getattr(self._playwright, name)
        browser = engine.launch(
            headless=self._config.headless,
            slow_mo=self._config.slow_mo,
        )
        return browser

    def create_context(self, browser: Browser, video_dir: Path | None = None) -> BrowserContext:
        """Create a BrowserContext with viewport, tracing, and video config applied."""
        record_video_dir = None
        if self._config.video_mode != "off" and video_dir is not None:
            video_dir.mkdir(parents=True, exist_ok=True)
            record_video_dir = str(video_dir)

        context = browser.new_context(
            viewport={
                "width": self._config.viewport_width,
                "height": self._config.viewport_height,
            },
            record_video_dir=record_video_dir,
            base_url=self._config.base_url,
        )
        context.set_default_timeout(self._config.timeout)
        context.set_default_navigation_timeout(self._config.navigation_timeout)

        if self._config.trace_mode != "off":
            context.tracing.start(screenshots=True, snapshots=True, sources=True)

        return context

    @staticmethod
    def create_page(context: BrowserContext) -> Page:
        """Open a new page/tab within the given context."""
        page = context.new_page()
        return page
