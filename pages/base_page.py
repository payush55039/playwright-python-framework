"""
base_page.py

Every page object in this framework inherits from BasePage. It provides
the common, logged, exception-safe primitives (click, fill, get_text, etc.)
so individual page objects only need to define locators and business-level
methods (login(), add_to_cart(), etc.) rather than re-implementing wait
and error-handling logic repeatedly. This is the cornerstone of the
Page Object Model layer and keeps tests free of raw Playwright calls.
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page

from config.config_manager import ConfigManager
from utilities.exceptions import ElementNotInteractableError
from utilities.logger import get_logger
from utilities.wait_helper import WaitHelper

logger = get_logger(__name__)


class BasePage:
    """Common functionality shared by every page object."""

    def __init__(self, page: Page, config: ConfigManager | None = None) -> None:
        self.page = page
        self.config = config or ConfigManager()
        self.wait = WaitHelper(page, self.config)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def navigate(self, path: str = "/") -> None:
        """Navigate to ``path`` relative to the configured base URL."""
        url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
        logger.info("Navigating to: %s", url)
        self.page.goto(url)
        self.wait.wait_for_load_state("load")

    @property
    def current_url(self) -> str:
        return self.page.url

    @property
    def title(self) -> str:
        return self.page.title()

    # ------------------------------------------------------------------
    # Interaction primitives (all explicit-wait backed)
    # ------------------------------------------------------------------
    def click(self, locator: Locator, description: str = "") -> None:
        label = description or str(locator)
        try:
            self.wait.wait_for_visible(locator)
            locator.click()
            logger.info("Clicked: %s", label)
        except Exception as exc:  # noqa: BLE001
            raise ElementNotInteractableError(f"Failed to click {label}: {exc}") from exc

    def fill(self, locator: Locator, text: str, description: str = "") -> None:
        label = description or str(locator)
        try:
            self.wait.wait_for_visible(locator)
            locator.fill(text)
            masked = "*" * len(text) if "password" in label.lower() else text
            logger.info("Filled '%s' into: %s", masked, label)
        except Exception as exc:  # noqa: BLE001
            raise ElementNotInteractableError(f"Failed to fill {label}: {exc}") from exc

    def get_text(self, locator: Locator) -> str:
        self.wait.wait_for_visible(locator)
        return (locator.text_content() or "").strip()

    def get_all_texts(self, locator: Locator) -> list[str]:
        self.wait.wait_for_visible(locator.first)
        return [text.strip() for text in locator.all_text_contents()]

    def is_visible(self, locator: Locator) -> bool:
        return locator.is_visible()

    def select_option(self, locator: Locator, value: str, description: str = "") -> None:
        label = description or str(locator)
        self.wait.wait_for_visible(locator)
        locator.select_option(value)
        logger.info("Selected option '%s' on: %s", value, label)

    def count(self, locator: Locator) -> int:
        return locator.count()
