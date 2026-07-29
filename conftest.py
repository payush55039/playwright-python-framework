"""
conftest.py (root)

Registers the fixture modules living under fixtures/ as pytest plugins and
implements the ``pytest_runtest_makereport`` hook that powers automatic
screenshot / video / trace capture on failure, plus Allure attachment of
that evidence. Kept at the repository root (rather than inside tests/) so
that ``pytest_plugins`` registration is honored regardless of which
directory pytest is invoked from.
"""

from __future__ import annotations

from collections.abc import Generator

import allure
import pytest
from playwright.sync_api import BrowserContext, Page

from config.config_manager import ConfigManager
from utilities.logger import get_logger
from utilities.screenshot_utility import ScreenshotUtility
from utilities.trace_utility import TraceUtility
from utilities.video_utility import VideoUtility

pytest_plugins = [
    "fixtures.browser_fixtures",
    "fixtures.page_fixtures",
]

logger = get_logger(__name__)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register CLI options so browser/headless can be overridden without
    touching config.yaml or .env, e.g.:
        pytest --browser-engine=firefox --run-headed

    Note: this framework ships its own browser/context/page fixtures (see
    fixtures/browser_fixtures.py and fixtures/page_fixtures.py) rather than
    relying on the pytest-playwright plugin's fixtures, so these options are
    deliberately named to avoid colliding with that plugin's built-in
    ``--browser`` / ``--headed`` flags, which remain available if you choose
    to use pytest-playwright's fixtures directly instead.
    """
    parser.addoption(
        "--browser-engine",
        action="store",
        default=None,
        help="Override the browser engine: chromium, firefox, webkit",
    )
    parser.addoption(
        "--run-headed",
        action="store_true",
        default=False,
        help="Run browsers in headed mode instead of headless",
    )


@pytest.fixture(scope="session", autouse=True)
def _apply_cli_overrides(request: pytest.FixtureRequest) -> None:
    """Push --browser-engine / --headed CLI flags into environment variables
    before ConfigManager is first instantiated, so they take effect via the
    standard environment-variable override mechanism."""
    import os

    browser_engine = request.config.getoption("--browser-engine")
    if browser_engine:
        os.environ["BROWSER"] = browser_engine

    if request.config.getoption("--run-headed"):
        os.environ["HEADLESS"] = "false"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator:
    """Capture screenshot/video/trace evidence and attach it to Allure
    whenever a test fails, and always finalize video/trace retention.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    page: Page | None = item.funcargs.get("page")
    context: BrowserContext | None = item.funcargs.get("context")
    config = ConfigManager()
    test_passed = report.passed

    if page is not None and report.failed and config.screenshot_on_failure:
        try:
            screenshot_path = ScreenshotUtility(config).capture(page, item.name, "failure")
            allure.attach.file(
                str(screenshot_path),
                name="screenshot-on-failure",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not capture failure screenshot: %s", exc)

    if page is not None:
        try:
            video_path = VideoUtility(config).finalize(page, item.name, test_passed)
            if video_path:
                allure.attach.file(
                    str(video_path), name="video", attachment_type=allure.attachment_type.WEBM
                )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not finalize video: %s", exc)

    if context is not None:
        try:
            trace_path = TraceUtility(config).finalize(context, item.name, test_passed)
            if trace_path:
                allure.attach.file(str(trace_path), name="trace", attachment_type="application/zip")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not finalize trace: %s", exc)
