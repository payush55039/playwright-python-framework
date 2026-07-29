"""inventory_page.py - Page object for the Products / Inventory page."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class InventoryPage(BasePage):
    """Encapsulates the product listing page (/inventory.html)."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page_title = page.locator(".title")
        self.inventory_items = page.locator(".inventory_item")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")
        self.item_images = page.locator(".inventory_item_img img")
        self.item_descriptions = page.locator(".inventory_item_desc")
        self.sort_dropdown = page.locator(".product_sort_container")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.hamburger_menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")
        self.about_link = page.locator("#about_sidebar_link")
        self.reset_app_state_link = page.locator("#reset_sidebar_link")
        self.close_menu_button = page.locator("#react-burger-cross-btn")

    def is_loaded(self) -> bool:
        logger.info("Waiting for Inventory Page")
        loaded = self.is_visible(self.page_title) and self.get_text(self.page_title) == "Products"
        if loaded:
            logger.info("Inventory Page Loaded Successfully")
        return loaded

    def get_product_names(self) -> list[str]:
        return self.get_all_texts(self.item_names)

    def get_product_prices(self) -> list[float]:
        raw_prices = self.get_all_texts(self.item_prices)
        return [float(price.replace("$", "")) for price in raw_prices]

    def get_product_count(self) -> int:
        return self.count(self.inventory_items)

    def add_product_to_cart_by_name(self, product_name: str) -> None:
        item = self.page.locator(".inventory_item").filter(has_text=product_name)
        button = item.locator("button", has_text="Add to cart")
        logger.info("Adding %s to Cart", product_name)
        self.click(button, f"Add to cart button for {product_name}")

    def remove_product_from_cart_by_name(self, product_name: str) -> None:
        item = self.page.locator(".inventory_item").filter(has_text=product_name)
        button = item.locator("button", has_text="Remove")
        logger.info("Removing %s from Cart", product_name)
        self.click(button, f"Remove button for {product_name}")

    def open_product_details(self, product_name: str) -> None:
        link = self.page.locator(".inventory_item_name", has_text=product_name)
        self.click(link, f"Product link for {product_name}")

    def get_cart_badge_count(self) -> int:
        if not self.is_visible(self.cart_badge):
            return 0
        return int(self.get_text(self.cart_badge))

    def open_cart(self) -> None:
        self.click(self.cart_link, "Cart icon")

    def sort_by(self, option_value: str) -> None:
        logger.info("Sorting products by: %s", option_value)
        self.select_option(self.sort_dropdown, option_value, "Sort dropdown")

    def open_hamburger_menu(self) -> None:
        logger.info("Opening Hamburger Menu")
        self.click(self.hamburger_menu_button, "Hamburger menu button")
        self.wait.wait_for_visible(self.logout_link)

    def logout(self) -> None:
        self.open_hamburger_menu()
        logger.info("Clicking Logout")
        self.click(self.logout_link, "Logout link")

    def go_to_about_page(self) -> None:
        self.open_hamburger_menu()
        self.click(self.about_link, "About link")

    def reset_app_state(self) -> None:
        self.open_hamburger_menu()
        logger.info("Resetting App State")
        self.click(self.reset_app_state_link, "Reset App State link")
        self.click(self.close_menu_button, "Close menu button")
