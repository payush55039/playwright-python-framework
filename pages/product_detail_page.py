"""product_detail_page.py - Page object for a single product's detail view."""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class ProductDetailPage(BasePage):
    """Encapsulates the individual product detail page (/inventory-item.html)."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.product_name = page.locator(".inventory_details_name")
        self.product_description = page.locator(".inventory_details_desc")
        self.product_price = page.locator(".inventory_details_price")
        self.product_image = page.locator(".inventory_details_img")
        self.add_to_cart_button = page.locator("button", has_text="Add to cart")
        self.back_to_products_button = page.locator("#back-to-products")

    def get_name(self) -> str:
        return self.get_text(self.product_name)

    def get_description(self) -> str:
        return self.get_text(self.product_description)

    def get_price(self) -> float:
        return float(self.get_text(self.product_price).replace("$", ""))

    def is_image_visible(self) -> bool:
        return self.is_visible(self.product_image)

    def add_to_cart(self) -> None:
        self.click(self.add_to_cart_button, "Add to cart button")

    def back_to_products(self) -> None:
        logger.info("Navigating back to Products page")
        self.click(self.back_to_products_button, "Back to products button")
