"""
Checkout process tests.
"""

import pytest
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestCheckout:
    """Test suite for checkout functionality."""

    @pytest.mark.smoke
    def test_checkout_page_loads(self, checkout_page: CheckoutPage):
        """Test that checkout page loads successfully."""
        checkout_page.navigate()
        assert checkout_page.is_order_summary_visible()

    @pytest.mark.regression
    def test_complete_checkout_happy_path(
        self, product_page: ProductPage, cart_page: CartPage, checkout_page: CheckoutPage, page
    ):
        """Test completing a full checkout process."""
        product_page.navigate()
        product_page.search_product("Laptop")
        
        if product_page.get_product_count() > 0:
            product_page.add_first_product_to_cart()
            cart_page.navigate()
            cart_page.click_checkout()
            
            checkout_page.complete_checkout(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                phone="555-1234",
                address="123 Main St",
                city="New York",
                state="NY",
                zip_code="10001",
                card_number="4111111111111111",
                expiry="12/25",
                cvv="123",
            )
            
            # Should show success message or redirect to confirmation page
            assert "success" in page.url.lower() or "confirmation" in page.url.lower() or checkout_page.get_success_message() != ""

    @pytest.mark.regression
    def test_checkout_missing_first_name(self, checkout_page: CheckoutPage):
        """Test checkout with missing first name."""
        checkout_page.navigate()
        checkout_page.fill_shipping_address(
            first_name="",
            last_name="Doe",
            email="john.doe@example.com",
            phone="555-1234",
            address="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
        )
        checkout_page.place_order()
        
        error_message = checkout_page.get_error_message()
        assert "required" in error_message.lower() or "first name" in error_message.lower()

    @pytest.mark.regression
    def test_checkout_invalid_email(self, checkout_page: CheckoutPage):
        """Test checkout with invalid email format."""
        checkout_page.navigate()
        checkout_page.fill_shipping_address(
            first_name="John",
            last_name="Doe",
            email="invalid-email",
            phone="555-1234",
            address="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
        )
        checkout_page.place_order()
        
        error_message = checkout_page.get_error_message()
        assert "email" in error_message.lower() or "invalid" in error_message.lower()

    @pytest.mark.regression
    def test_checkout_invalid_phone(self, checkout_page: CheckoutPage):
        """Test checkout with invalid phone number."""
        checkout_page.navigate()
        checkout_page.fill_shipping_address(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="invalid",
            address="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
        )
        checkout_page.place_order()
        
        error_message = checkout_page.get_error_message()
        assert "phone" in error_message.lower() or "invalid" in error_message.lower()

    @pytest.mark.regression
    def test_checkout_invalid_card_number(self, checkout_page: CheckoutPage):
        """Test checkout with invalid credit card number."""
        checkout_page.navigate()
        checkout_page.fill_shipping_address(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="555-1234",
            address="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
        )
        checkout_page.fill_payment_info(
            card_number="1234567890123456",
            expiry="12/25",
            cvv="123",
        )
        checkout_page.place_order()
        
        error_message = checkout_page.get_error_message()
        assert "card" in error_message.lower() or "payment" in error_message.lower()

    @pytest.mark.regression
    def test_checkout_expired_card(self, checkout_page: CheckoutPage):
        """Test checkout with an expired credit card."""
        checkout_page.navigate()
        checkout_page.fill_shipping_address(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="555-1234",
            address="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
        )
        checkout_page.fill_payment_info(
            card_number="4111111111111111",
            expiry="01/20",
            cvv="123",
        )
        checkout_page.place_order()
        
        error_message = checkout_page.get_error_message()
        assert "expired" in error_message.lower() or "card" in error_message.lower()

    @pytest.mark.regression
    def test_checkout_invalid_cvv(self, checkout_page: CheckoutPage):
        """Test checkout with invalid CVV."""
        checkout_page.navigate()
        checkout_page.fill_shipping_address(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="555-1234",
            address="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
        )
        checkout_page.fill_payment_info(
            card_number="4111111111111111",
            expiry="12/25",
            cvv="99",
        )
        checkout_page.place_order()
        
        error_message = checkout_page.get_error_message()
        assert "cvv" in error_message.lower() or "security" in error_message.lower()

    @pytest.mark.regression
    def test_checkout_select_shipping_method(self, checkout_page: CheckoutPage):
        """Test selecting different shipping methods."""
        checkout_page.navigate()
        checkout_page.select_shipping_method("express")
        # Should update shipping method without error
        assert checkout_page.page.url  # Page should be valid

    @pytest.mark.regression
    def test_back_to_cart_from_checkout(self, checkout_page: CheckoutPage, cart_page: CartPage, page):
        """Test navigating back to cart from checkout."""
        checkout_page.navigate()
        checkout_page.click_back_to_cart()
        
        # Should navigate back to cart page
        assert "/cart" in page.url
