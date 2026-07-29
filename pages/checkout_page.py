"""
checkout_page.py

Groups the three-step Sauce Demo checkout flow into three cohesive page
objects: CheckoutInformationPage (step one - customer info form),
CheckoutOverviewPage (step two - order review), and
CheckoutCompletePage (step three - confirmation). They are kept in a single
module because they represent one logical workflow and are always used
together, while still respecting Separation of Concerns internally by
giving each step its own class.
"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class CheckoutInformationPage(BasePage):
    """Step one of checkout: first name / last name / postal code form."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        self.cancel_button = page.locator("#cancel")
        self.error_message = page.locator('[data-test="error"]')

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        logger.info("Filling Checkout Information")
        self.fill(self.first_name_input, first_name, "First name field")
        self.fill(self.last_name_input, last_name, "Last name field")
        self.fill(self.postal_code_input, postal_code, "Postal code field")

    def continue_to_overview(self) -> None:
        logger.info("Continuing to Checkout Overview")
        self.click(self.continue_button, "Continue button")

    def cancel(self) -> None:
        logger.info("Cancelling Checkout")
        self.click(self.cancel_button, "Cancel button")

    def get_error_message(self) -> str:
        return self.get_text(self.error_message)

    def has_error(self) -> bool:
        return self.is_visible(self.error_message)


class CheckoutOverviewPage(BasePage):
    """Step two of checkout: order review with item/price/tax/total summary."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page_title = page.locator(".title")
        self.cart_items = page.locator(".cart_item")
        self.item_total_label = page.locator(".summary_subtotal_label")
        self.tax_label = page.locator(".summary_tax_label")
        self.total_label = page.locator(".summary_total_label")
        self.finish_button = page.locator("#finish")
        self.cancel_button = page.locator("#cancel")

    def is_loaded(self) -> bool:
        return self.get_text(self.page_title) == "Checkout: Overview"

    def get_item_count(self) -> int:
        return self.count(self.cart_items)

    def get_total(self) -> str:
        return self.get_text(self.total_label)

    def finish(self) -> None:
        logger.info("Checkout Completed Successfully")
        self.click(self.finish_button, "Finish button")

    def cancel(self) -> None:
        self.click(self.cancel_button, "Cancel button")


class CheckoutCompletePage(BasePage):
    """Step three of checkout: order confirmation ('Thank you for your order!')."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.complete_header = page.locator(".complete-header")
        self.back_home_button = page.locator("#back-to-products")

    def is_loaded(self) -> bool:
        return self.is_visible(self.complete_header)

    def get_confirmation_message(self) -> str:
        return self.get_text(self.complete_header)

    def back_to_home(self) -> None:
        self.click(self.back_home_button, "Back Home button")
