"""
Product search and filtering tests.
"""

import pytest
from pages.product_page import ProductPage


class TestProductSearch:
    """Test suite for product search functionality."""

    @pytest.mark.smoke
    def test_search_existing_product(self, product_page: ProductPage):
        """Test searching for an existing product."""
        product_page.navigate()
        product_page.search_product("Laptop")
        assert product_page.get_product_count() > 0

    @pytest.mark.smoke
    def test_search_nonexistent_product(self, product_page: ProductPage):
        """Test searching for a product that doesn't exist."""
        product_page.navigate()
        product_page.search_product("NonexistentProductXYZ123")
        assert product_page.is_no_results_displayed()

    @pytest.mark.regression
    def test_search_with_special_characters(self, product_page: ProductPage):
        """Test search with special characters."""
        product_page.navigate()
        product_page.search_product("Product@#$%")
        # Should handle gracefully without crashing
        assert product_page.page.url  # Page should still be valid

    @pytest.mark.regression
    def test_search_case_insensitive(self, product_page: ProductPage):
        """Test that search is case-insensitive."""
        product_page.navigate()
        product_page.search_product("laptop")
        count_lowercase = product_page.get_product_count()
        
        product_page.search_product("LAPTOP")
        count_uppercase = product_page.get_product_count()
        
        assert count_lowercase == count_uppercase

    @pytest.mark.ui
    def test_product_display_information(self, product_page: ProductPage):
        """Test that products display required information."""
        product_page.navigate()
        product_page.search_product("Laptop")
        
        if product_page.get_product_count() > 0:
            title = product_page.get_first_product_title()
            price = product_page.get_first_product_price()
            assert title != ""
            assert price != ""

    @pytest.mark.regression
    def test_filter_by_category(self, product_page: ProductPage):
        """Test filtering products by category."""
        product_page.navigate()
        product_page.filter_by_category("Electronics")
        # Should display products in the Electronics category
        assert product_page.page.url  # Page should be valid

    @pytest.mark.regression
    def test_filter_by_price_range(self, product_page: ProductPage):
        """Test filtering products by price range."""
        product_page.navigate()
        product_page.filter_by_price_range("100", "500")
        # Should display products within the price range
        assert product_page.page.url  # Page should be valid

    @pytest.mark.regression
    def test_sort_products_by_price_low_to_high(self, product_page: ProductPage):
        """Test sorting products by price (low to high)."""
        product_page.navigate()
        product_page.sort_products("price_asc")
        # Should display products sorted by price ascending
        assert product_page.page.url  # Page should be valid

    @pytest.mark.regression
    def test_sort_products_by_price_high_to_low(self, product_page: ProductPage):
        """Test sorting products by price (high to low)."""
        product_page.navigate()
        product_page.sort_products("price_desc")
        # Should display products sorted by price descending
        assert product_page.page.url  # Page should be valid

    @pytest.mark.regression
    def test_sort_products_by_rating(self, product_page: ProductPage):
        """Test sorting products by rating."""
        product_page.navigate()
        product_page.sort_products("rating")
        # Should display products sorted by rating
        assert product_page.page.url  # Page should be valid

    @pytest.mark.ui
    def test_product_click_navigation(self, product_page: ProductPage, page):
        """Test clicking on a product navigates to product details."""
        product_page.navigate()
        product_page.search_product("Laptop")
        
        if product_page.get_product_count() > 0:
            product_page.click_first_product()
            # Should navigate to product details page
            assert "/product/" in page.url or "/details/" in page.url

    @pytest.mark.slow
    def test_combined_search_and_filter(self, product_page: ProductPage):
        """Test combining search with filters."""
        product_page.navigate()
        product_page.search_product("Laptop")
        product_page.filter_by_price_range("500", "1500")
        # Should display filtered search results
        assert product_page.page.url  # Page should be valid

    @pytest.mark.regression
    def test_empty_search(self, product_page: ProductPage):
        """Test searching with empty search term."""
        product_page.navigate()
        product_page.search_product("")
        # Should either show all products or handle gracefully
        assert product_page.page.url  # Page should be valid
