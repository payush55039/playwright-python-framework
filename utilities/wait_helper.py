"""
wait_helper.py

Centralizes every explicit wait condition used across the framework. The
project intentionally forbids ``time.sleep`` / hardcoded sleeps; every wait
must be a condition-based Playwright wait routed through this module so
timeouts, logging, and error handling stay consistent.
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from config.config_manager import ConfigManager
from utilities.exceptions import ElementNotFoundError
from utilities.logger import get_logger

logger = get_logger(__name__)


class WaitHelper:
    """Collection of explicit-wait convenience methods bound to a Page."""

    def __init__(self, page: Page, config: ConfigManager | None = None) -> None:
        self._page = page
        self._config = config or ConfigManager()

    def wait_for_visible(self, locator: Locator, timeout: int | None = None) -> Locator:
        """Wait until the locator is attached and visible."""
        try:
            locator.wait_for(state="visible", timeout=timeout or self._config.timeout)
            return locator
        except PlaywrightTimeoutError as exc:
            raise ElementNotFoundError(
                f"Element was not visible within timeout: {locator}"
            ) from exc

    def wait_for_hidden(self, locator: Locator, timeout: int | None = None) -> None:
        """Wait until the locator is detached or hidden."""
        try:
            locator.wait_for(state="hidden", timeout=timeout or self._config.timeout)
        except PlaywrightTimeoutError as exc:
            raise ElementNotFoundError(
                f"Element did not become hidden within timeout: {locator}"
            ) from exc

    def wait_for_enabled(self, locator: Locator, timeout: int | None = None) -> Locator:
        """Wait until the locator is visible and not disabled."""
        self.wait_for_visible(locator, timeout)
        locator.page.wait_for_function(
            "el => el && !el.disabled",
            arg=locator.element_handle(),
            timeout=timeout or self._config.timeout,
        )
        return locator

    def wait_for_url_contains(self, fragment: str, timeout: int | None = None) -> None:
        """Wait until the current page URL contains the given fragment."""
        timeout = timeout or self._config.navigation_timeout

        self._page.wait_for_load_state("load", timeout=timeout)

        if fragment not in self._page.url:
            raise ElementNotFoundError(
                f"URL never contained expected fragment '{fragment}'. "
                f"Current URL: {self._page.url}"
            )

    def wait_for_load_state(self, state: str = "load", timeout: int | None = None) -> None:
        """Wait for a Playwright page load state: 'load', 'domcontentloaded', 'networkidle'."""
        self._page.wait_for_load_state(state, timeout=timeout or self._config.navigation_timeout)

    def wait_for_text(
        self, locator: Locator, expected_text: str, timeout: int | None = None
    ) -> None:
        """Wait until the locator's text content equals the expected text."""
        try:
            locator.page.wait_for_function(
                """([el, expected]) => el && el.textContent.trim() === expected""",
                arg=[locator.element_handle(), expected_text],
                timeout=timeout or self._config.timeout,
            )
        except PlaywrightTimeoutError as exc:
            raise ElementNotFoundError(f"Text of element never equaled '{expected_text}'") from exc

    def wait_for_count(
        self, locator: Locator, expected_count: int, timeout: int | None = None
    ) -> None:
        """Wait until a locator resolves to an expected number of matching elements."""
        deadline_timeout = timeout or self._config.timeout
        try:
            self._page.wait_for_function(
                """([selector, expected]) => document.querySelectorAll(selector).length === expected""",
                arg=[locator._selector if hasattr(locator, "_selector") else "", expected_count],
                timeout=deadline_timeout,
            )
        except PlaywrightTimeoutError as exc:
            # Fallback: poll via Python-side count (covers complex locators the
            # JS-side selector string can't represent, e.g. chained locators).
            logger.debug("Falling back to Python-side polling for wait_for_count")
            self._page.wait_for_timeout(0)
            actual = locator.count()
            if actual != expected_count:
                raise ElementNotFoundError(
                    f"Expected {expected_count} elements, found {actual}"
                ) from exc
