"""
page_fixtures.py

Function-scoped fixtures exposing a fresh Playwright Page and all Sauce
Demo page objects to every test, so test modules can simply request e.g.
``login_page`` as a parameter instead of manually wiring up
``LoginPage(page)`` in every test.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from playwright.sync_api import BrowserContext, Page

from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletePage,
    CheckoutInformationPage,
    CheckoutOverviewPage,
)
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_detail_page import ProductDetailPage


@pytest.fixture
def page(context: BrowserContext) -> Iterator[Page]:
    new_page = context.new_page()
    yield new_page
    new_page.close()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def product_detail_page(page: Page) -> ProductDetailPage:
    return ProductDetailPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_information_page(page: Page) -> CheckoutInformationPage:
    return CheckoutInformationPage(page)


@pytest.fixture
def checkout_overview_page(page: Page) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    return CheckoutCompletePage(page)


@pytest.fixture
def logged_in_page(page: Page, login_page: LoginPage, inventory_page: InventoryPage) -> Page:
    """A Page that is already authenticated as the standard_user.

    Saves every cart/checkout/navigation test from repeating the same
    three lines of login boilerplate.
    """
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.is_loaded()
    return page
