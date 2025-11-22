"""
Pytest configuration and fixtures for Playwright tests.
"""

import pytest
from playwright.sync_api import sync_playwright, Page, Browser
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://demo.ecommerce.local")


@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context arguments."""
    return {
        "viewport": {"width": 1280, "height": 720},
        "locale": "en-US",
        "timezone_id": "America/New_York",
    }


@pytest.fixture
def playwright_instance():
    """Provide a Playwright instance."""
    playwright = sync_playwright().start()
    yield playwright
    playwright.stop()


@pytest.fixture
def browser(playwright_instance):
    """Provide a Playwright browser instance."""
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture
def page(browser):
    """Provide a browser page for each test."""
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Provide a LoginPage instance."""
    return LoginPage(page)


@pytest.fixture
def product_page(page: Page) -> ProductPage:
    """Provide a ProductPage instance."""
    return ProductPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    """Provide a CartPage instance."""
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    """Provide a CheckoutPage instance."""
    return CheckoutPage(page)


@pytest.fixture
def authenticated_page(page: Page, login_page: LoginPage) -> Page:
    """Provide an authenticated page (user already logged in)."""
    login_page.navigate()
    login_page.login("testuser@example.com", "TestPassword123!")
    return page


@pytest.fixture(autouse=True)
def reset_app(page: Page):
    """Reset application state before each test."""
    # Navigate to home page to ensure clean state
    page.goto(BASE_URL, wait_until="networkidle")
    yield
    # Cleanup after test (optional)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "smoke: Smoke tests for critical paths")
    config.addinivalue_line("markers", "regression: Full regression test suite")
    config.addinivalue_line("markers", "ui: UI-specific tests")
    config.addinivalue_line("markers", "slow: Tests that take longer to execute")
