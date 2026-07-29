"""
assertion_helper.py

Wraps Playwright's built-in expect() assertions and adds a lightweight
"soft assertion" collector, so a test can gather several assertion
failures and report them together at the end rather than stopping at the
first one, which is invaluable when validating many fields on one page
(e.g. verifying every product's name/price/image in a single pass).
"""

from __future__ import annotations

from typing import Any

from playwright.sync_api import Locator, Page, expect

from utilities.exceptions import AssertionHelperError
from utilities.logger import get_logger

logger = get_logger(__name__)


class AssertionHelper:
    """Hard assertions (fail fast) plus an accumulating soft-assertion mode."""

    def __init__(self) -> None:
        self._soft_failures: list[str] = []

    # ------------------------------------------------------------------
    # Hard assertions - raise immediately
    # ------------------------------------------------------------------
    @staticmethod
    def assert_visible(locator: Locator, message: str = "") -> None:
        expect(locator, message).to_be_visible()

    @staticmethod
    def assert_hidden(locator: Locator, message: str = "") -> None:
        expect(locator, message).to_be_hidden()

    @staticmethod
    def assert_text_equals(locator: Locator, expected: str, message: str = "") -> None:
        expect(locator, message).to_have_text(expected)

    @staticmethod
    def assert_text_contains(locator: Locator, expected: str, message: str = "") -> None:
        expect(locator, message).to_contain_text(expected)

    @staticmethod
    def assert_count(locator: Locator, expected: int, message: str = "") -> None:
        expect(locator, message).to_have_count(expected)

    @staticmethod
    def assert_url_contains(page: Page, expected_fragment: str) -> None:
        if expected_fragment not in page.url:
            raise AssertionHelperError(
                f"Expected URL to contain '{expected_fragment}', got '{page.url}'"
            )

    @staticmethod
    def assert_equals(actual: Any, expected: Any, message: str = "") -> None:
        if actual != expected:
            raise AssertionHelperError(message or f"Expected '{expected}', got '{actual}'")

    # ------------------------------------------------------------------
    # Soft assertions - collected and raised together via assert_all()
    # ------------------------------------------------------------------
    def soft_assert_equals(self, actual: Any, expected: Any, message: str = "") -> None:
        if actual != expected:
            failure = message or f"Expected '{expected}', got '{actual}'"
            logger.warning("Soft assertion failed: %s", failure)
            self._soft_failures.append(failure)

    def soft_assert_true(self, condition: bool, message: str) -> None:
        if not condition:
            logger.warning("Soft assertion failed: %s", message)
            self._soft_failures.append(message)

    def assert_all(self) -> None:
        """Raise a single AssertionHelperError summarizing all soft failures."""
        if self._soft_failures:
            summary = "\n".join(f"- {failure}" for failure in self._soft_failures)
            failures = list(self._soft_failures)
            self._soft_failures.clear()
            raise AssertionHelperError(f"{len(failures)} soft assertion(s) failed:\n{summary}")
