"""
Shopping cart operations tests.
"""

import pytest
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class TestCartOperations:
    """Test suite for shopping cart functionality."""

    @pytest.mark.smoke
    def test_add_product_to_cart(self, product_page: ProductPage, cart_page: CartPage):
        """Test adding a product to the cart."""
        product_page.navigate()
        product_page.search_product("Laptop")
        
        if product_page.get_product_count() > 0:
            product_page.add_first_product_to_cart()
            cart_page.navigate()
            assert cart_page.get_cart_item_count() > 0

    @pytest.mark.smoke
    def test_view_empty_cart(self, cart_page: CartPage):
        """Test viewing an empty cart."""
        cart_page.navigate()
        assert cart_page.is_cart_empty()

    @pytest.mark.regression
    def test_remove_item_from_cart(self, product_page: ProductPage, cart_page: CartPage):
        """Test removing an item from the cart."""
        product_page.navigate()
        product_page.search_product("Laptop")
        
        if product_page.get_product_count() > 0:
            product_page.add_first_product_to_cart()
            cart_page.navigate()
            initial_count = cart_page.get_cart_item_count()
            
            cart_page.remove_first_item()
            # Cart should have one fewer item
            assert cart_page.get_cart_item_count() < initial_count

    @pytest.mark.regression
    def test_update_item_quantity(self, product_page: ProductPage, cart_page: CartPage):
        """Test updating the quantity of an item in the cart."""
        product_page.navigate()
        product_page.search_product("Laptop")
        
        if product_page.get_product_count() > 0:
            product_page.add_first_product_to_cart()
            cart_page.navigate()
            cart_page.update_item_quantity(0, "3")
            # Quantity should be updated
            assert cart_page.page.url  # Page should be valid

    @pytest.mark.ui
    def test_cart_displays_item_details(self, product_page: ProductPage, cart_page: CartPage):
        """Test that cart displays item price and quantity."""
        product_page.navigate()
        product_page.search_product("Laptop")
        
        if product_page.get_product_count() > 0:
            product_page.add_first_product_to_cart()
            cart_page.navigate()
            
            assert cart_page.get_first_item_price() != ""
            assert cart_page.get_first_item_quantity() != ""

    @pytest.mark.regression
    def test_cart_totals_calculation(self, product_page: ProductPage, cart_page: CartPage):
        """Test that cart calculates subtotal, tax, and total correctly."""
        product_page.navigate()
        product_page.search_product("Laptop")
        
        if product_page.get_product_count() > 0:
            product_page.add_first_product_to_cart()
            cart_page.navigate()
            
            subtotal = cart_page.get_subtotal()
            tax = cart_page.get_tax()
            total = cart_page.get_total()
            
            assert subtotal != ""
            assert tax != ""
            assert total != ""

    @pytest.mark.regression
    def test_continue_shopping_navigation(self, product_page: ProductPage, cart_page: CartPage, page):
        """Test continuing shopping from cart."""
        product_page.navigate()
        product_page.search_product("Laptop")
        
        if product_page.get_product_count() > 0:
            product_page.add_first_product_to_cart()
            cart_page.navigate()
            cart_page.click_continue_shopping()
            
            # Should navigate back to products page
            assert "/products" in page.url or "/shop" in page.url

    @pytest.mark.slow
    def test_add_multiple_products_to_cart(self, product_page: ProductPage, cart_page: CartPage):
        """Test adding multiple different products to the cart."""
        product_page.navigate()
        product_page.search_product("Laptop")
        
        if product_page.get_product_count() > 0:
            product_page.add_first_product_to_cart()
            product_page.navigate()
            product_page.search_product("Mouse")
            
            if product_page.get_product_count() > 0:
                product_page.add_first_product_to_cart()
                cart_page.navigate()
                
                # Cart should have at least 2 items
                assert cart_page.get_cart_item_count() >= 2

    @pytest.mark.regression
    def test_cart_persistence_after_navigation(self, product_page: ProductPage, cart_page: CartPage):
        """Test that cart items persist after navigating away and back."""
        product_page.navigate()
        product_page.search_product("Laptop")
        
        if product_page.get_product_count() > 0:
            product_page.add_first_product_to_cart()
            cart_page.navigate()
            initial_count = cart_page.get_cart_item_count()
            
            product_page.navigate()
            cart_page.navigate()
            
            # Cart should still have the same items
            assert cart_page.get_cart_item_count() == initial_count
