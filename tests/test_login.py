"""test_login.py - Authentication test suite for the Sauce Demo login page."""

from __future__ import annotations

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utilities.assertion_helper import AssertionHelper
from utilities.data_loader import DataLoader

pytestmark = [allure.feature("Authentication")]


@allure.story("Valid Login")
@pytest.mark.smoke
def test_valid_login_standard_user(login_page: LoginPage, inventory_page: InventoryPage) -> None:
    """A standard_user with correct credentials should reach the inventory page."""
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    assert inventory_page.is_loaded(), "Inventory page did not load after valid login"


@allure.story("Valid Login")
@pytest.mark.parametrize("case", DataLoader().load("login_data.json"), ids=lambda c: c["id"])
def test_valid_login_data_driven(
    login_page: LoginPage, inventory_page: InventoryPage, case: dict
) -> None:
    """Every non-locked demo user should be able to log in successfully."""
    login_page.open()
    login_page.login(case["username"], case["password"])
    assert inventory_page.is_loaded(), f"Login failed for user '{case['username']}'"


@allure.story("Invalid Login")
@pytest.mark.parametrize(
    "case", DataLoader().load("invalid_login_data.json"), ids=lambda c: c["id"]
)
def test_invalid_login_data_driven(login_page: LoginPage, case: dict) -> None:
    """Invalid credential combinations should surface the expected error banner."""
    login_page.open()
    login_page.login(case["username"], case["password"])
    assert login_page.has_error(), "Expected an error message but none was shown"
    AssertionHelper.assert_text_contains(login_page.error_message, case["expected_error"])


@allure.story("Invalid Login")
def test_empty_username_shows_required_error(login_page: LoginPage) -> None:
    login_page.open()
    login_page.login("", "secret_sauce")
    assert "Username is required" in login_page.get_error_message()


@allure.story("Invalid Login")
def test_empty_password_shows_required_error(login_page: LoginPage) -> None:
    login_page.open()
    login_page.login("standard_user", "")
    assert "Password is required" in login_page.get_error_message()


@allure.story("Invalid Login")
def test_locked_out_user_cannot_login(login_page: LoginPage) -> None:
    login_page.open()
    login_page.login("locked_out_user", "secret_sauce")
    assert "locked out" in login_page.get_error_message().lower()


@allure.story("Valid Login")
@pytest.mark.slow
def test_performance_glitch_user_eventually_logs_in(
    login_page: LoginPage, inventory_page: InventoryPage
) -> None:
    """performance_glitch_user intentionally simulates a slow backend; the
    framework's explicit waits must tolerate that latency without a
    hardcoded sleep."""
    login_page.open()
    login_page.login("performance_glitch_user", "secret_sauce")
    assert inventory_page.is_loaded()


@allure.story("Logout")
def test_logout_returns_to_login_page(login_page: LoginPage, inventory_page: InventoryPage) -> None:
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    assert inventory_page.is_loaded()
    inventory_page.logout()
    assert login_page.is_loaded(), "Logout did not return the user to the login page"


@allure.story("Session Validation")
def test_direct_inventory_access_without_login_redirects_to_login(
    login_page: LoginPage, page
) -> None:
    """Sauce Demo blocks direct navigation to protected pages without an
    active session; the app should redirect back to '/' with an error."""
    login_page.navigate("/inventory.html")
    assert "inventory.html" not in page.url or login_page.has_error()
