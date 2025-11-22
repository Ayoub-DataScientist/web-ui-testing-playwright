"""
Checkout Page Object Model.
"""

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page object for the checkout page."""

    # Locators
    FIRST_NAME_INPUT = "input[name='first_name']"
    LAST_NAME_INPUT = "input[name='last_name']"
    EMAIL_INPUT = "input[name='email']"
    PHONE_INPUT = "input[name='phone']"
    ADDRESS_INPUT = "input[name='address']"
    CITY_INPUT = "input[name='city']"
    STATE_INPUT = "input[name='state']"
    ZIP_INPUT = "input[name='zip']"
    COUNTRY_INPUT = "select[name='country']"
    CARD_NUMBER_INPUT = "input[name='card_number']"
    CARD_EXPIRY_INPUT = "input[name='expiry']"
    CARD_CVV_INPUT = "input[name='cvv']"
    PLACE_ORDER_BUTTON = "button:has-text('Place Order')"
    BACK_TO_CART_BUTTON = "button:has-text('Back to Cart')"
    ORDER_SUMMARY = ".order-summary"
    SHIPPING_METHOD = "select[name='shipping_method']"
    ERROR_MESSAGE = ".alert-danger"
    SUCCESS_MESSAGE = ".alert-success"

    def navigate(self):
        """Navigate to the checkout page."""
        super().navigate("/checkout")

    def fill_shipping_address(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        country: str = "US",
    ) -> None:
        """Fill in the shipping address form."""
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PHONE_INPUT, phone)
        self.fill(self.ADDRESS_INPUT, address)
        self.fill(self.CITY_INPUT, city)
        self.fill(self.STATE_INPUT, state)
        self.fill(self.ZIP_INPUT, zip_code)
        self.select_option(self.COUNTRY_INPUT, country)

    def fill_payment_info(self, card_number: str, expiry: str, cvv: str) -> None:
        """Fill in the payment information."""
        self.fill(self.CARD_NUMBER_INPUT, card_number)
        self.fill(self.CARD_EXPIRY_INPUT, expiry)
        self.fill(self.CARD_CVV_INPUT, cvv)

    def select_shipping_method(self, method: str) -> None:
        """Select a shipping method."""
        self.select_option(self.SHIPPING_METHOD, method)

    def place_order(self) -> None:
        """Click the place order button."""
        self.click(self.PLACE_ORDER_BUTTON)
        self.wait_for_navigation()

    def click_back_to_cart(self) -> None:
        """Click the back to cart button."""
        self.click(self.BACK_TO_CART_BUTTON)
        self.wait_for_navigation()

    def get_error_message(self) -> str:
        """Get error message if checkout fails."""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def get_success_message(self) -> str:
        """Get success message after order placement."""
        if self.is_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""

    def is_order_summary_visible(self) -> bool:
        """Check if the order summary is visible."""
        return self.is_visible(self.ORDER_SUMMARY)

    def complete_checkout(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        card_number: str,
        expiry: str,
        cvv: str,
        shipping_method: str = "standard",
    ) -> None:
        """Complete the entire checkout process."""
        self.fill_shipping_address(
            first_name, last_name, email, phone, address, city, state, zip_code
        )
        self.select_shipping_method(shipping_method)
        self.fill_payment_info(card_number, expiry, cvv)
        self.place_order()
