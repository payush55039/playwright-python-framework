"""login_page.py - Page object for https://www.saucedemo.com/ (the login screen)."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Encapsulates all interactions with the Sauce Demo login page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator('[data-test="error"]')
        self.logo = page.locator(".login_logo")

    def open(self) -> LoginPage:
        logger.info("Opening Login Page")
        self.navigate("/")
        return self

    def login(self, username: str, password: str) -> None:
        logger.info("Entering Username")
        self.fill(self.username_input, username, "Username field")
        logger.info("Entering Password")
        self.fill(self.password_input, password, "Password field")
        logger.info("Clicking Login")
        self.click(self.login_button, "Login button")

    def get_error_message(self) -> str:
        return self.get_text(self.error_message)

    def has_error(self) -> bool:
        return self.is_visible(self.error_message)

    def is_loaded(self) -> bool:
        return self.is_visible(self.logo)
