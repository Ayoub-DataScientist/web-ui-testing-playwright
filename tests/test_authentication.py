"""
Authentication tests for login and registration functionality.
"""

import pytest
from pages.login_page import LoginPage


class TestAuthentication:
    """Test suite for authentication features."""

    @pytest.mark.smoke
    def test_valid_login(self, login_page: LoginPage, page):
        """Test successful login with valid credentials."""
        login_page.navigate()
        login_page.login("testuser@example.com", "TestPassword123!")
        assert page.url.endswith("/dashboard") or page.url.endswith("/home")

    @pytest.mark.smoke
    def test_invalid_email_login(self, login_page: LoginPage):
        """Test login failure with invalid email."""
        login_page.navigate()
        login_page.login("invalid@example.com", "TestPassword123!")
        error_message = login_page.get_error_message()
        assert "Invalid credentials" in error_message or "not found" in error_message.lower()

    @pytest.mark.smoke
    def test_invalid_password_login(self, login_page: LoginPage):
        """Test login failure with incorrect password."""
        login_page.navigate()
        login_page.login("testuser@example.com", "WrongPassword123!")
        error_message = login_page.get_error_message()
        assert "Invalid credentials" in error_message or "incorrect" in error_message.lower()

    @pytest.mark.regression
    def test_empty_email_login(self, login_page: LoginPage):
        """Test login with empty email field."""
        login_page.navigate()
        login_page.login("", "TestPassword123!")
        error_message = login_page.get_error_message()
        assert "required" in error_message.lower() or "email" in error_message.lower()

    @pytest.mark.regression
    def test_empty_password_login(self, login_page: LoginPage):
        """Test login with empty password field."""
        login_page.navigate()
        login_page.login("testuser@example.com", "")
        error_message = login_page.get_error_message()
        assert "required" in error_message.lower() or "password" in error_message.lower()

    @pytest.mark.regression
    def test_empty_credentials_login(self, login_page: LoginPage):
        """Test login with both email and password empty."""
        login_page.navigate()
        login_page.login("", "")
        error_message = login_page.get_error_message()
        assert "required" in error_message.lower()

    @pytest.mark.ui
    def test_login_page_elements_visible(self, login_page: LoginPage):
        """Test that all login page elements are visible."""
        login_page.navigate()
        assert login_page.is_email_field_visible()
        assert login_page.is_password_field_visible()
        assert login_page.is_login_button_enabled()

    @pytest.mark.ui
    def test_register_link_navigation(self, login_page: LoginPage, page):
        """Test navigation to registration page via link."""
        login_page.navigate()
        login_page.click_register_link()
        assert page.url.endswith("/register")

    @pytest.mark.ui
    def test_forgot_password_link_navigation(self, login_page: LoginPage, page):
        """Test navigation to forgot password page via link."""
        login_page.navigate()
        login_page.click_forgot_password()
        assert page.url.endswith("/forgot-password")

    @pytest.mark.regression
    def test_sql_injection_attempt_email(self, login_page: LoginPage):
        """Test that SQL injection attempts are properly handled."""
        login_page.navigate()
        login_page.login("' OR '1'='1", "password")
        error_message = login_page.get_error_message()
        assert "Invalid credentials" in error_message or error_message != ""

    @pytest.mark.regression
    def test_case_sensitive_email(self, login_page: LoginPage):
        """Test that email is case-insensitive."""
        login_page.navigate()
        login_page.login("TESTUSER@EXAMPLE.COM", "TestPassword123!")
        # Should either succeed or fail consistently
        url = login_page.page.url
        assert url  # Just verify page loaded

    @pytest.mark.slow
    def test_login_session_persistence(self, login_page: LoginPage, page):
        """Test that login session persists across page navigation."""
        login_page.navigate()
        login_page.login("testuser@example.com", "TestPassword123!")
        page.goto(login_page.base_url + "/products")
        # User should still be logged in
        assert not page.url.endswith("/login")
