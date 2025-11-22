"""
Base Page class containing common methods for all page objects.
"""

from playwright.sync_api import Page
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://demo.ecommerce.local")


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page):
        """Initialize the page object with a Playwright Page instance."""
        self.page = page
        self.base_url = BASE_URL

    def navigate(self, path: str = ""):
        """Navigate to a specific path on the application."""
        url = f"{self.base_url}{path}"
        self.page.goto(url, wait_until="networkidle")

    def fill(self, selector: str, text: str) -> None:
        """Fill a text input field."""
        self.page.fill(selector, text)

    def click(self, selector: str) -> None:
        """Click on an element."""
        self.page.click(selector)

    def get_text(self, selector: str) -> str:
        """Get text content of an element."""
        return self.page.text_content(selector) or ""

    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        return self.page.is_visible(selector)

    def is_enabled(self, selector: str) -> bool:
        """Check if an element is enabled."""
        return self.page.is_enabled(selector)

    def wait_for_element(self, selector: str, timeout: int = 5000) -> None:
        """Wait for an element to be visible."""
        self.page.wait_for_selector(selector, timeout=timeout)

    def get_attribute(self, selector: str, attribute: str) -> str:
        """Get an attribute value from an element."""
        return self.page.get_attribute(selector, attribute) or ""

    def select_option(self, selector: str, value: str) -> None:
        """Select an option from a dropdown."""
        self.page.select_option(selector, value)

    def get_url(self) -> str:
        """Get the current page URL."""
        return self.page.url

    def wait_for_navigation(self) -> None:
        """Wait for page navigation to complete."""
        self.page.wait_for_load_state("networkidle")

    def take_screenshot(self, filename: str) -> None:
        """Take a screenshot of the current page."""
        self.page.screenshot(path=f"screenshots/{filename}.png")

    def refresh(self) -> None:
        """Refresh the current page."""
        self.page.reload()

    def go_back(self) -> None:
        """Navigate back to the previous page."""
        self.page.go_back()

    def get_title(self) -> str:
        """Get the page title."""
        return self.page.title()

    def accept_alert(self) -> None:
        """Accept a JavaScript alert."""
        self.page.on("dialog", lambda dialog: dialog.accept())

    def dismiss_alert(self) -> None:
        """Dismiss a JavaScript alert."""
        self.page.on("dialog", lambda dialog: dialog.dismiss())
