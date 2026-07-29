"""test_navigation.py - Hamburger menu and general navigation test suite."""

from __future__ import annotations

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = [allure.feature("Navigation")]


@pytest.fixture
def authenticated_inventory(login_page: LoginPage, inventory_page: InventoryPage) -> InventoryPage:
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    assert inventory_page.is_loaded()
    return inventory_page


@allure.story("Hamburger Menu")
def test_hamburger_menu_opens_and_shows_all_links(authenticated_inventory: InventoryPage) -> None:
    authenticated_inventory.open_hamburger_menu()
    assert authenticated_inventory.is_visible(authenticated_inventory.logout_link)
    assert authenticated_inventory.is_visible(authenticated_inventory.about_link)
    assert authenticated_inventory.is_visible(authenticated_inventory.reset_app_state_link)


@allure.story("About Page")
def test_about_link_navigates_to_saucelabs_site(
    authenticated_inventory: InventoryPage, page
) -> None:
    authenticated_inventory.go_to_about_page()
    authenticated_inventory.wait.wait_for_url_contains("saucelabs.com")
    assert "saucelabs.com" in page.url


@allure.story("Logout")
def test_logout_clears_session_and_blocks_back_navigation(
    authenticated_inventory: InventoryPage, login_page: LoginPage, page
) -> None:
    authenticated_inventory.logout()
    assert login_page.is_loaded()
    page.go_back()
    assert login_page.is_loaded() or "inventory.html" not in page.url


@allure.story("Reset App State")
def test_reset_app_state_clears_cart_badge(authenticated_inventory: InventoryPage) -> None:
    authenticated_inventory.add_product_to_cart_by_name("Sauce Labs Backpack")
    assert authenticated_inventory.get_cart_badge_count() == 1
    authenticated_inventory.reset_app_state()
    assert authenticated_inventory.get_cart_badge_count() == 0


@allure.story("Continue Shopping")
def test_continue_shopping_from_cart_preserves_items(
    authenticated_inventory: InventoryPage, cart_page
) -> None:
    authenticated_inventory.add_product_to_cart_by_name("Sauce Labs Bike Light")
    authenticated_inventory.open_cart()
    cart_page.continue_shopping()
    assert authenticated_inventory.get_cart_badge_count() == 1
