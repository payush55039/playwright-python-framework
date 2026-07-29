"""test_products.py - Product listing and detail page test suite."""

from __future__ import annotations

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_detail_page import ProductDetailPage
from utilities.assertion_helper import AssertionHelper
from utilities.data_loader import DataLoader

pytestmark = [allure.feature("Products")]

EXPECTED_PRODUCT_COUNT = 6


@pytest.fixture
def authenticated_inventory(login_page: LoginPage, inventory_page: InventoryPage) -> InventoryPage:
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    assert inventory_page.is_loaded()
    return inventory_page


@allure.story("Verify Products")
def test_verify_all_products_are_listed(authenticated_inventory: InventoryPage) -> None:
    assert authenticated_inventory.get_product_count() == EXPECTED_PRODUCT_COUNT


@allure.story("Verify Products")
def test_verify_product_names_match_expected_catalog(
    authenticated_inventory: InventoryPage,
) -> None:
    expected_names = {item["name"] for item in DataLoader().load("product_data.json")}
    actual_names = set(authenticated_inventory.get_product_names())
    assert actual_names == expected_names


@allure.story("Verify Product Details")
def test_verify_product_details_page(
    authenticated_inventory: InventoryPage, product_detail_page: ProductDetailPage
) -> None:
    authenticated_inventory.open_product_details("Sauce Labs Backpack")
    assert product_detail_page.get_name() == "Sauce Labs Backpack"
    assert product_detail_page.get_price() == 29.99
    assert len(product_detail_page.get_description()) > 0


@allure.story("Verify Images")
def test_verify_every_product_has_visible_image(authenticated_inventory: InventoryPage) -> None:
    images = authenticated_inventory.item_images
    assert images.count() == EXPECTED_PRODUCT_COUNT
    for index in range(images.count()):
        assert images.nth(index).is_visible()


def test_verify_every_product_has_non_empty_description(
    authenticated_inventory: InventoryPage,
) -> None:
    descriptions = authenticated_inventory.get_all_texts(authenticated_inventory.item_descriptions)
    assert len(descriptions) == EXPECTED_PRODUCT_COUNT
    assert all(len(description) > 0 for description in descriptions)


@allure.story("Verify Prices")
def test_verify_all_product_prices_are_positive(authenticated_inventory: InventoryPage) -> None:
    prices = authenticated_inventory.get_product_prices()
    assertion = AssertionHelper()
    for name, price in zip(authenticated_inventory.get_product_names(), prices, strict=False):
        assertion.soft_assert_true(price > 0, f"Price for '{name}' was not positive: {price}")
    assertion.assert_all()


@allure.story("Product Sorting")
def test_sort_products_name_a_to_z(authenticated_inventory: InventoryPage) -> None:
    authenticated_inventory.sort_by("az")
    names = authenticated_inventory.get_product_names()
    assert names == sorted(names)


@allure.story("Product Sorting")
def test_sort_products_name_z_to_a(authenticated_inventory: InventoryPage) -> None:
    authenticated_inventory.sort_by("za")
    names = authenticated_inventory.get_product_names()
    assert names == sorted(names, reverse=True)


@allure.story("Product Sorting")
def test_sort_products_price_low_to_high(authenticated_inventory: InventoryPage) -> None:
    authenticated_inventory.sort_by("lohi")
    prices = authenticated_inventory.get_product_prices()
    assert prices == sorted(prices)


@allure.story("Product Sorting")
def test_sort_products_price_high_to_low(authenticated_inventory: InventoryPage) -> None:
    authenticated_inventory.sort_by("hilo")
    prices = authenticated_inventory.get_product_prices()
    assert prices == sorted(prices, reverse=True)
