# Web UI Testing with Playwright & Pytest

##  Project Overview

This repository demonstrates **professional automated UI testing** using **Playwright** and **Pytest**. It tests a demo ecommerce website and showcases industry-standard practices including the **Page Object Model (POM)**, **Pytest fixtures**, **parallel execution**, and **comprehensive test strategy design**.

**QA Skills Demonstrated:**
- Writing maintainable, scalable UI tests using Playwright
- Implementing the Page Object Model for code reusability
- Designing and executing test strategies
- Using Pytest fixtures for test setup and teardown
- Running tests in parallel for faster feedback
- Professional test reporting and logging

---

##  Test Strategy

### Scope
This test suite covers critical user journeys on a demo ecommerce platform:
- User registration and login
- Product search and filtering
- Adding/removing items from cart
- Checkout process (happy path)
- User profile management

### Test Levels
- **Functional Tests:** Verify core features work as expected
- **UI/UX Tests:** Validate proper rendering and user interactions
- **Negative Tests:** Ensure proper error handling and validation

### Test Environment
- **Target Application:** [Demo Ecommerce Site](https://demo.ecommerce.local)
- **Browser Coverage:** Chromium, Firefox, WebKit
- **Execution:** Parallel execution for faster feedback

### Risk Assessment
- **High Priority:** Login, checkout, payment processing
- **Medium Priority:** Search, filtering, product details
- **Low Priority:** UI cosmetics, animations

---

##  Tech Stack

| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | 3.9+ | Test scripting language |
| **Playwright** | Latest | Cross-browser automation |
| **Pytest** | Latest | Test framework and runner |
| **Pytest-Xdist** | Latest | Parallel test execution |
| **Pytest-HTML** | Latest | HTML test reports |

---

##  Project Structure

```
web-ui-testing-playwright/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── pytest.ini                         # Pytest configuration
├── conftest.py                        # Pytest fixtures and configuration
├── pages/                             # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py                   # Base page class with common methods
│   ├── login_page.py                  # Login page object
│   ├── product_page.py                # Product listing and details page
│   ├── cart_page.py                   # Shopping cart page
│   └── checkout_page.py               # Checkout page
├── tests/                             # Test files
│   ├── __init__.py
│   ├── test_authentication.py         # Login/registration tests
│   ├── test_product_search.py         # Product search and filtering tests
│   ├── test_cart_operations.py        # Add/remove from cart tests
│   └── test_checkout.py               # Checkout process tests
├── fixtures/                          # Test data and fixtures
│   ├── test_users.json                # User credentials for testing
│   └── test_products.json             # Product data
└── reports/                           # Test execution reports (generated)
    └── index.html                     # HTML test report
```

---

##  Getting Started

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ayoub-DataScientist/web-ui-testing-playwright.git
   cd web-ui-testing-playwright
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

---

##  Running Tests

### Run all tests
```bash
pytest tests/
```

### Run tests in parallel (4 workers)
```bash
pytest tests/ -n 4
```

### Run specific test file
```bash
pytest tests/test_authentication.py
```

### Run tests with verbose output
```bash
pytest tests/ -v
```

### Run tests and generate HTML report
```bash
pytest tests/ --html=reports/index.html --self-contained-html
```

### Run tests with specific marker
```bash
pytest tests/ -m "smoke"
```

---

##  Page Object Model (POM)

The Page Object Model is a design pattern that improves test maintainability by abstracting page elements and interactions into reusable classes.

### Example: Login Page Object

```python
# pages/login_page.py
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button:has-text('Sign In')"
    ERROR_MESSAGE = ".error-message"

    def login(self, email: str, password: str):
        """Perform login with given credentials."""
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Retrieve error message from login attempt."""
        return self.get_text(self.ERROR_MESSAGE)
```

### Example: Test Using POM

```python
# tests/test_authentication.py
def test_valid_login(page, login_page):
    """Test successful login with valid credentials."""
    login_page.navigate()
    login_page.login("user@example.com", "password123")
    assert page.url.endswith("/dashboard")

def test_invalid_login(page, login_page):
    """Test login failure with invalid credentials."""
    login_page.navigate()
    login_page.login("user@example.com", "wrongpassword")
    error = login_page.get_error_message()
    assert "Invalid credentials" in error
```

---

##  Fixtures

Pytest fixtures provide reusable setup and teardown logic for tests.

### Example: Browser and Page Fixtures

```python
# conftest.py
@pytest.fixture
def browser():
    """Provide a Playwright browser instance."""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()
    playwright.stop()

@pytest.fixture
def page(browser):
    """Provide a browser page for each test."""
    page = browser.new_page()
    yield page
    page.close()

@pytest.fixture
def login_page(page):
    """Provide a LoginPage instance."""
    return LoginPage(page)
```

---

##  Parallel Execution

Tests are configured to run in parallel using `pytest-xdist` for faster feedback:

```bash
pytest tests/ -n auto  # Uses all available CPU cores
```

**Benefits:**
- Significantly faster test execution
- Better utilization of system resources
- Ideal for CI/CD pipelines

---

##  Test Reporting

Tests generate HTML reports for easy review:

```bash
pytest tests/ --html=reports/index.html --self-contained-html
```

The report includes:
- Test execution summary
- Pass/fail status for each test
- Execution time
- Error details and stack traces

---

##  Key Learnings

This project demonstrates:
1. **Page Object Model:** Separating test logic from page interactions
2. **Pytest Fixtures:** Reusable setup and teardown
3. **Parallel Execution:** Running tests concurrently for speed
4. **Test Strategy:** Designing comprehensive test coverage
5. **Professional Practices:** Clean code, documentation, and reporting

---

##  Related Repositories

- [qa-portfolio-overview](https://github.com/Ayoub-DataScientist/qa-portfolio-overview) - Portfolio map and overview
- [api-testing-automation](https://github.com/Ayoub-DataScientist/api-testing-automation) - API testing examples
- [test-automation-framework-from-scratch](https://github.com/Ayoub-DataScientist/test-automation-framework-from-scratch) - Advanced framework

---

##  License

This project is open source and available under the MIT License.
