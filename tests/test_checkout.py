"""test_checkout.py - End-to-end checkout flow test suite."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletePage,
    CheckoutInformationPage,
    CheckoutOverviewPage,
)
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utilities.data_loader import DataLoader

pytestmark = [allure.feature("Checkout")]


@pytest.fixture
def cart_with_one_item(
    login_page: LoginPage, inventory_page: InventoryPage, cart_page: CartPage
) -> CartPage:
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    assert inventory_page.is_loaded()
    inventory_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    inventory_page.open_cart()
    assert cart_page.is_loaded()
    cart_page.checkout()
    return cart_page


@allure.story("Successful Checkout")
@pytest.mark.smoke
def test_successful_checkout_end_to_end(
    cart_with_one_item: CartPage,
    checkout_information_page: CheckoutInformationPage,
    checkout_overview_page: CheckoutOverviewPage,
    checkout_complete_page: CheckoutCompletePage,
) -> None:
    checkout_information_page.fill_information("Jane", "Doe", "94107")
    checkout_information_page.continue_to_overview()
    assert checkout_overview_page.is_loaded()

    checkout_overview_page.finish()
    assert checkout_complete_page.is_loaded()
    assert "Thank you for your order" in checkout_complete_page.get_confirmation_message()


@allure.story("Checkout Validation")
@pytest.mark.parametrize(
    "case",
    [c for c in DataLoader().load("checkout_data.json") if "expected_error" in c],
    ids=lambda c: c["id"],
)
def test_checkout_information_required_fields(
    cart_with_one_item: CartPage,
    checkout_information_page: CheckoutInformationPage,
    case: dict,
) -> None:
    checkout_information_page.fill_information(
        case["first_name"], case["last_name"], case["postal_code"]
    )
    checkout_information_page.continue_to_overview()
    assert checkout_information_page.has_error()
    assert case["expected_error"] in checkout_information_page.get_error_message()


@allure.story("Cancel Checkout")
def test_cancel_checkout_from_information_step_returns_to_cart(
    cart_with_one_item: CartPage,
    checkout_information_page: CheckoutInformationPage,
) -> None:
    checkout_information_page.cancel()
    assert cart_with_one_item.is_loaded()


@allure.story("Cancel Checkout")
def test_cancel_checkout_from_overview_step_returns_to_inventory(
    cart_with_one_item: CartPage,
    checkout_information_page: CheckoutInformationPage,
    checkout_overview_page: CheckoutOverviewPage,
    inventory_page: InventoryPage,
) -> None:
    checkout_information_page.fill_information("Jane", "Doe", "94107")
    checkout_information_page.continue_to_overview()
    assert checkout_overview_page.is_loaded()
    checkout_overview_page.cancel()
    assert inventory_page.is_loaded()


@allure.story("Checkout Overview")
def test_checkout_overview_shows_correct_item_count(
    cart_with_one_item: CartPage,
    checkout_information_page: CheckoutInformationPage,
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    checkout_information_page.fill_information("Jane", "Doe", "94107")
    checkout_information_page.continue_to_overview()
    assert checkout_overview_page.get_item_count() == 1


@allure.story("Checkout Overview")
def test_checkout_overview_total_includes_tax(
    cart_with_one_item: CartPage,
    checkout_information_page: CheckoutInformationPage,
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    checkout_information_page.fill_information("Jane", "Doe", "94107")
    checkout_information_page.continue_to_overview()
    total_text = checkout_overview_page.get_total()
    assert total_text.startswith("Total: $")
    total_value = float(total_text.replace("Total: $", ""))
    assert total_value > 29.99  # Backpack subtotal plus tax


@allure.story("Order Confirmation")
def test_order_confirmation_back_home_returns_to_inventory(
    cart_with_one_item: CartPage,
    checkout_information_page: CheckoutInformationPage,
    checkout_overview_page: CheckoutOverviewPage,
    checkout_complete_page: CheckoutCompletePage,
    inventory_page: InventoryPage,
) -> None:
    checkout_information_page.fill_information("Jane", "Doe", "94107")
    checkout_information_page.continue_to_overview()
    checkout_overview_page.finish()
    assert checkout_complete_page.is_loaded()
    checkout_complete_page.back_to_home()
    assert inventory_page.is_loaded()
