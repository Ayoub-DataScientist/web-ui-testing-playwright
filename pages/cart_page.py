"""
Shopping Cart Page Object Model.
"""

from pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for the shopping cart page."""

    # Locators
    CART_ITEMS = ".cart-item"
    ITEM_QUANTITY = ".item-quantity"
    ITEM_PRICE = ".item-price"
    REMOVE_BUTTON = "button:has-text('Remove')"
    SUBTOTAL = ".subtotal"
    TAX = ".tax"
    TOTAL = ".total"
    CHECKOUT_BUTTON = "button:has-text('Proceed to Checkout')"
    CONTINUE_SHOPPING_BUTTON = "button:has-text('Continue Shopping')"
    EMPTY_CART_MESSAGE = ".empty-cart-message"
    QUANTITY_INPUT = "input[name='quantity']"
    UPDATE_QUANTITY_BUTTON = "button:has-text('Update')"

    def navigate(self):
        """Navigate to the cart page."""
        super().navigate("/cart")

    def get_cart_item_count(self) -> int:
        """Get the number of items in the cart."""
        return len(self.page.query_selector_all(self.CART_ITEMS))

    def get_subtotal(self) -> str:
        """Get the subtotal amount."""
        return self.get_text(self.SUBTOTAL)

    def get_tax(self) -> str:
        """Get the tax amount."""
        return self.get_text(self.TAX)

    def get_total(self) -> str:
        """Get the total amount."""
        return self.get_text(self.TOTAL)

    def remove_first_item(self) -> None:
        """Remove the first item from the cart."""
        items = self.page.query_selector_all(self.CART_ITEMS)
        if items:
            remove_button = items[0].query_selector(self.REMOVE_BUTTON)
            if remove_button:
                remove_button.click()

    def update_item_quantity(self, item_index: int, new_quantity: str) -> None:
        """Update the quantity of a specific item."""
        items = self.page.query_selector_all(self.CART_ITEMS)
        if item_index < len(items):
            quantity_input = items[item_index].query_selector(self.QUANTITY_INPUT)
            if quantity_input:
                quantity_input.fill(new_quantity)
                update_button = items[item_index].query_selector(self.UPDATE_QUANTITY_BUTTON)
                if update_button:
                    update_button.click()

    def is_cart_empty(self) -> bool:
        """Check if the cart is empty."""
        return self.is_visible(self.EMPTY_CART_MESSAGE)

    def click_checkout(self) -> None:
        """Click the checkout button."""
        self.click(self.CHECKOUT_BUTTON)
        self.wait_for_navigation()

    def click_continue_shopping(self) -> None:
        """Click the continue shopping button."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        self.wait_for_navigation()

    def get_first_item_price(self) -> str:
        """Get the price of the first item in the cart."""
        items = self.page.query_selector_all(self.CART_ITEMS)
        if items:
            price_element = items[0].query_selector(self.ITEM_PRICE)
            return price_element.text_content() or "" if price_element else ""
        return ""

    def get_first_item_quantity(self) -> str:
        """Get the quantity of the first item in the cart."""
        items = self.page.query_selector_all(self.CART_ITEMS)
        if items:
            quantity_element = items[0].query_selector(self.ITEM_QUANTITY)
            return quantity_element.text_content() or "" if quantity_element else ""
        return ""
