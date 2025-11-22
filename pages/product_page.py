"""
Product Page Object Model.
"""

from pages.base_page import BasePage


class ProductPage(BasePage):
    """Page object for the product listing and details page."""

    # Locators
    SEARCH_INPUT = "input[name='search']"
    SEARCH_BUTTON = "button:has-text('Search')"
    PRODUCT_ITEMS = ".product-item"
    PRODUCT_TITLE = ".product-title"
    PRODUCT_PRICE = ".product-price"
    ADD_TO_CART_BUTTON = "button:has-text('Add to Cart')"
    FILTER_CATEGORY = "select[name='category']"
    FILTER_PRICE_MIN = "input[name='price_min']"
    FILTER_PRICE_MAX = "input[name='price_max']"
    APPLY_FILTER_BUTTON = "button:has-text('Apply Filters')"
    SORT_DROPDOWN = "select[name='sort']"
    NO_RESULTS_MESSAGE = ".no-results"
    PRODUCT_RATING = ".product-rating"

    def navigate(self):
        """Navigate to the products page."""
        super().navigate("/products")

    def search_product(self, product_name: str) -> None:
        """Search for a product by name."""
        self.fill(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_navigation()

    def get_product_count(self) -> int:
        """Get the number of products displayed."""
        return len(self.page.query_selector_all(self.PRODUCT_ITEMS))

    def get_first_product_title(self) -> str:
        """Get the title of the first product."""
        products = self.page.query_selector_all(self.PRODUCT_ITEMS)
        if products:
            return self.page.query_selector(f"{self.PRODUCT_ITEMS} {self.PRODUCT_TITLE}").text_content() or ""
        return ""

    def get_first_product_price(self) -> str:
        """Get the price of the first product."""
        products = self.page.query_selector_all(self.PRODUCT_ITEMS)
        if products:
            price_element = self.page.query_selector(f"{self.PRODUCT_ITEMS} {self.PRODUCT_PRICE}")
            return price_element.text_content() or "" if price_element else ""
        return ""

    def click_first_product(self) -> None:
        """Click on the first product in the list."""
        products = self.page.query_selector_all(self.PRODUCT_ITEMS)
        if products:
            products[0].click()
            self.wait_for_navigation()

    def add_first_product_to_cart(self) -> None:
        """Add the first product to the cart."""
        self.click(self.ADD_TO_CART_BUTTON)

    def filter_by_category(self, category: str) -> None:
        """Filter products by category."""
        self.select_option(self.FILTER_CATEGORY, category)
        self.click(self.APPLY_FILTER_BUTTON)
        self.wait_for_navigation()

    def filter_by_price_range(self, min_price: str, max_price: str) -> None:
        """Filter products by price range."""
        self.fill(self.FILTER_PRICE_MIN, min_price)
        self.fill(self.FILTER_PRICE_MAX, max_price)
        self.click(self.APPLY_FILTER_BUTTON)
        self.wait_for_navigation()

    def sort_products(self, sort_option: str) -> None:
        """Sort products by the specified option."""
        self.select_option(self.SORT_DROPDOWN, sort_option)
        self.wait_for_navigation()

    def is_no_results_displayed(self) -> bool:
        """Check if no results message is displayed."""
        return self.is_visible(self.NO_RESULTS_MESSAGE)

    def get_first_product_rating(self) -> str:
        """Get the rating of the first product."""
        products = self.page.query_selector_all(self.PRODUCT_ITEMS)
        if products:
            rating_element = self.page.query_selector(f"{self.PRODUCT_ITEMS} {self.PRODUCT_RATING}")
            return rating_element.text_content() or "" if rating_element else ""
        return ""
