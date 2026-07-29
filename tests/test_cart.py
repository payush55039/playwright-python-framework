"""test_cart.py - Shopping cart test suite."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = [allure.feature("Cart")]


@pytest.fixture
def authenticated_inventory(login_page: LoginPage, inventory_page: InventoryPage) -> InventoryPage:
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    assert inventory_page.is_loaded()
    return inventory_page


@allure.story("Add To Cart")
def test_add_single_product_to_cart(authenticated_inventory: InventoryPage) -> None:
    authenticated_inventory.add_product_to_cart_by_name("Sauce Labs Backpack")
    assert authenticated_inventory.get_cart_badge_count() == 1


@allure.story("Add To Cart")
def test_add_multiple_products_to_cart(authenticated_inventory: InventoryPage) -> None:
    for product in ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Onesie"]:
        authenticated_inventory.add_product_to_cart_by_name(product)
    assert authenticated_inventory.get_cart_badge_count() == 3


@allure.story("Remove From Cart")
def test_remove_single_product_from_inventory_page(authenticated_inventory: InventoryPage) -> None:
    authenticated_inventory.add_product_to_cart_by_name("Sauce Labs Backpack")
    assert authenticated_inventory.get_cart_badge_count() == 1
    authenticated_inventory.remove_product_from_cart_by_name("Sauce Labs Backpack")
    assert authenticated_inventory.get_cart_badge_count() == 0


@allure.story("Remove From Cart")
def test_remove_multiple_products_from_cart_page(
    authenticated_inventory: InventoryPage, cart_page: CartPage
) -> None:
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    for product in products:
        authenticated_inventory.add_product_to_cart_by_name(product)
    authenticated_inventory.open_cart()
    assert cart_page.is_loaded()
    for product in products:
        cart_page.remove_product_by_name(product)
    assert cart_page.get_item_count() == 0


@allure.story("Verify Cart Badge")
def test_cart_badge_reflects_item_count_accurately(authenticated_inventory: InventoryPage) -> None:
    assert authenticated_inventory.get_cart_badge_count() == 0
    authenticated_inventory.add_product_to_cart_by_name("Sauce Labs Fleece Jacket")
    assert authenticated_inventory.get_cart_badge_count() == 1
    authenticated_inventory.add_product_to_cart_by_name("Sauce Labs Bolt T-Shirt")
    assert authenticated_inventory.get_cart_badge_count() == 2


@allure.story("Verify Cart Contents")
def test_cart_contents_match_added_products(
    authenticated_inventory: InventoryPage, cart_page: CartPage
) -> None:
    products = ["Sauce Labs Backpack", "Sauce Labs Onesie"]
    for product in products:
        authenticated_inventory.add_product_to_cart_by_name(product)
    authenticated_inventory.open_cart()
    assert set(cart_page.get_item_names()) == set(products)


@allure.story("Continue Shopping")
def test_continue_shopping_returns_to_inventory(
    authenticated_inventory: InventoryPage, cart_page: CartPage
) -> None:
    authenticated_inventory.open_cart()
    assert cart_page.is_loaded()
    cart_page.continue_shopping()
    assert authenticated_inventory.is_loaded()
