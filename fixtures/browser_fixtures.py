"""
browser_fixtures.py

Session/function scoped fixtures that manage the Playwright lifecycle:
one Playwright driver per test session, one Browser per test session
(reused across tests for speed), and a fresh, isolated BrowserContext for
every single test function so tests never leak cookies/localStorage/state
into one another - a common source of hard-to-reproduce flaky failures.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from playwright.sync_api import Browser, BrowserContext, Playwright, sync_playwright

from config.config_manager import ConfigManager
from utilities.browser_factory import BrowserFactory
from utilities.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def playwright_instance() -> Iterator[Playwright]:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Iterator[Browser]:
    config = ConfigManager()
    factory = BrowserFactory(playwright_instance, config)
    browser_instance = factory.launch_browser()
    yield browser_instance
    logger.info("Closing Browser")
    browser_instance.close()


@pytest.fixture
def context(browser: Browser) -> Iterator[BrowserContext]:
    """Provide a fresh, isolated BrowserContext for each test function.

    Context creation only needs the already-launched Browser (not the
    Playwright driver), so it is built directly here rather than through
    BrowserFactory.launch_browser(), keeping this fixture simple and fast.
    """
    config = ConfigManager()
    video_dir = config.reports_dir / "videos" / "_raw"
    record_video_dir = str(video_dir) if config.video_mode != "off" else None
    if record_video_dir:
        video_dir.mkdir(parents=True, exist_ok=True)

    new_context = browser.new_context(
        viewport={"width": config.viewport_width, "height": config.viewport_height},
        record_video_dir=record_video_dir,
        base_url=config.base_url,
    )
    new_context.set_default_timeout(config.timeout)
    new_context.set_default_navigation_timeout(config.navigation_timeout)

    if config.trace_mode != "off":
        new_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield new_context

    new_context.close()
