"""cart_page.py - Page object for the Shopping Cart page (/cart.html)."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    """Encapsulates the shopping cart page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page_title = page.locator(".title")
        self.cart_items = page.locator(".cart_item")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")
        self.remove_buttons = page.locator("button", has_text="Remove")
        self.continue_shopping_button = page.locator("#continue-shopping")
        self.checkout_button = page.locator("#checkout")

    def is_loaded(self) -> bool:
        return self.is_visible(self.page_title) and self.get_text(self.page_title) == "Your Cart"

    def get_item_names(self) -> list[str]:
        return self.get_all_texts(self.item_names)

    def get_item_count(self) -> int:
        return self.count(self.cart_items)

    def remove_product_by_name(self, product_name: str) -> None:
        item = self.page.locator(".cart_item").filter(has_text=product_name)
        button = item.locator("button", has_text="Remove")
        logger.info("Removing %s from Cart page", product_name)
        self.click(button, f"Remove button for {product_name}")

    def continue_shopping(self) -> None:
        logger.info("Clicking Continue Shopping")
        self.click(self.continue_shopping_button, "Continue Shopping button")

    def checkout(self) -> None:
        logger.info("Proceeding to Checkout")
        self.click(self.checkout_button, "Checkout button")
