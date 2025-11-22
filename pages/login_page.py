"""
Login Page Object Model.
"""

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page."""

    # Locators
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button:has-text('Sign In')"
    REGISTER_LINK = "a:has-text('Create Account')"
    ERROR_MESSAGE = ".alert-danger"
    SUCCESS_MESSAGE = ".alert-success"
    FORGOT_PASSWORD_LINK = "a:has-text('Forgot Password')"

    def navigate(self):
        """Navigate to the login page."""
        super().navigate("/login")

    def login(self, email: str, password: str) -> None:
        """Perform login with given credentials."""
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.wait_for_navigation()

    def get_error_message(self) -> str:
        """Retrieve error message from login attempt."""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def get_success_message(self) -> str:
        """Retrieve success message after login."""
        if self.is_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""

    def click_register_link(self) -> None:
        """Click on the register link."""
        self.click(self.REGISTER_LINK)
        self.wait_for_navigation()

    def click_forgot_password(self) -> None:
        """Click on the forgot password link."""
        self.click(self.FORGOT_PASSWORD_LINK)
        self.wait_for_navigation()

    def is_login_button_enabled(self) -> bool:
        """Check if the login button is enabled."""
        return self.is_enabled(self.LOGIN_BUTTON)

    def is_email_field_visible(self) -> bool:
        """Check if email input field is visible."""
        return self.is_visible(self.EMAIL_INPUT)

    def is_password_field_visible(self) -> bool:
        """Check if password input field is visible."""
        return self.is_visible(self.PASSWORD_INPUT)
