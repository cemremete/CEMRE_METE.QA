# Contributing to Insider Test Automation Project

Thank you for your interest in contributing to the Insider Test Automation Project! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)
- [Documentation](#documentation)

## 🤝 Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Chrome, Firefox, or Safari browser
- VS Code (recommended) or any Python IDE

### Quick Setup

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/test-automation-project.git
   cd test-automation-project
   ```
3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Verify installation:**
   ```bash
   pytest --version
   ```

## 🛠️ Development Setup

### VS Code Setup (Recommended)

1. **Install recommended extensions:**
   - Python (Microsoft)
   - Pylint
   - Python Docstring Generator
   - GitLens
   - Test Explorer

2. **Configure Python interpreter:**
   - Open Command Palette (Ctrl+Shift+P)
   - Select "Python: Select Interpreter"
   - Choose the virtual environment

3. **Enable testing:**
   - Open Test Explorer
   - Configure test settings for pytest

### Manual Setup

If you prefer other IDEs, ensure you have:
- Python interpreter configured
- Virtual environment activated
- Linting tools available
- Git integration

## 🏗️ Project Structure

```
insider_test_automation/
├── pages/                          # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py                # Base page with common methods
│   ├── popup_page.py               # Pop-up specific methods
│   └── product_page.py             # Product page methods
├── tests/                          # Test files
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration
│   ├── test_popup_functionality.py # Core functionality tests
│   ├── test_performance_responsive.py # Performance tests
│   └── test_cross_browser.py       # Browser compatibility tests
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── driver_manager.py           # WebDriver management
│   ├── screenshot_helper.py        # Screenshot utilities
│   └── test_data.py                # Test data management
├── screenshots/                    # Test screenshots
├── reports/                        # Test reports
├── comprehensive_test_matrix.md    # Test case matrix
├── bug_report_template.md          # Bug reporting template
├── requirements.txt                # Python dependencies
├── pytest.ini                     # Pytest configuration
├── conftest.py                     # Global test configuration
├── .gitignore                      # Git ignore rules
├── README.md                       # Project documentation
└── CONTRIBUTING.md                # This file
```

## 💻 Coding Standards

### Python Style Guide

This project follows PEP 8 with some modifications:

- **Line length:** 100 characters
- **Indentation:** 4 spaces
- **Naming conventions:**
  - Classes: `CamelCase`
  - Functions/methods: `snake_case`
  - Constants: `UPPER_CASE`
  - Private methods: `_private_method`

### Code Quality Tools

We use several tools to maintain code quality:

```bash
# Run linting
pylint pages/ tests/ utils/

# Format code
black --line-length 100 .

# Type checking (if using mypy)
mypy .

# Run tests with coverage
pytest --cov=pages --cov=utils --cov-report=html
```

### Docstring Standards

Use Google-style docstrings:

```python
def check_browser_compatibility(self, browser_name):
    """
    Check browser compatibility for popup functionality.

    Args:
        browser_name: Name of the browser being tested

    Returns:
        Dictionary with compatibility results

    Raises:
        ValueError: If browser_name is not supported
    """
```

## 🧪 Testing Guidelines

### Test Organization

- **Unit tests:** Test individual functions/methods
- **Integration tests:** Test component interactions
- **End-to-end tests:** Test complete user workflows
- **Performance tests:** Test speed and resource usage

### Test Naming Convention

```python
def test_tc001_popup_display_basic():
    """Test TC001: Basic popup display functionality."""
    pass

def test_tc004_popup_load_performance_detailed():
    """Test TC004: Detailed popup load performance analysis."""
    pass
```

### Test Markers

Use appropriate markers for test categorization:

```python
@pytest.mark.critical
def test_critical_functionality():
    """Critical priority test."""
    pass

@pytest.mark.smoke
def test_basic_smoke_test():
    """Quick smoke test."""
    pass

@pytest.mark.browser_chrome
def test_chrome_specific_feature():
    """Chrome-specific test."""
    pass
```

### Writing Effective Tests

1. **Arrange-Act-Assert pattern:**
   ```python
   def test_popup_display(self, driver):
       # Arrange
       popup_page = PopupPage(driver)

       # Act
       popup_page.click_show_instantly_button()

       # Assert
       assert popup_page.is_popup_visible()
   ```

2. **Use descriptive assertions:**
   ```python
   # Good
   assert popup_page.is_popup_visible(), "Popup should be visible after clicking trigger button"

   # Bad
   assert popup_page.is_popup_visible()
   ```

3. **Handle test data properly:**
   ```python
   @pytest.fixture
   def test_data():
       return {
           "expected_content": "Turkish",
           "timeout": 10
       }

   def test_content_validation(self, driver, test_data):
       popup_page = PopupPage(driver)
       content = popup_page.get_popup_content()
       assert test_data["expected_content"] in content
   ```

## 📝 Submitting Changes

### Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number-description
   ```

2. **Make your changes:**
   - Write tests first (TDD approach)
   - Follow coding standards
   - Add documentation
   - Test your changes

3. **Run quality checks:**
   ```bash
   # Run tests
   pytest tests/

   # Run linting
   pylint pages/ tests/ utils/

   # Format code
   black --line-length 100 .
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add new popup validation test

   - Add test for popup content validation
   - Update test data fixtures
   - Add screenshot capture on failure"
   ```

5. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Use conventional commit format:

```bash
# Feature
git commit -m "feat: add cross-browser compatibility tests"

# Bug fix
git commit -m "fix: resolve popup loading issue on Firefox"

# Documentation
git commit -m "docs: update installation instructions"

# Test
git commit -m "test: add performance regression tests"

# Refactor
git commit -m "refactor: simplify page object methods"
```

### Pull Request Guidelines

1. **Title:** Clear, descriptive title
2. **Description:** Detailed explanation of changes
3. **Testing:** How to test the changes
4. **Screenshots:** Before/after screenshots if UI changes
5. **Checklist:**
   - [ ] Tests pass
   - [ ] Code follows standards
   - [ ] Documentation updated
   - [ ] No breaking changes

## 🐛 Reporting Issues

### Bug Reports

Use the bug report template (`bug_report_template.md`):

1. **Clear title**
2. **Steps to reproduce**
3. **Expected vs actual behavior**
4. **Environment details**
5. **Screenshots/logs**
6. **Severity assessment**

### Feature Requests

1. **Clear description**
2. **Use case justification**
3. **Proposed implementation**
4. **Alternatives considered**

### Questions and Support

- Check existing issues first
- Use clear, descriptive titles
- Provide context and examples
- Be patient and respectful

## 📚 Documentation

### Documentation Standards

1. **README.md:** Project overview and setup
2. **Code comments:** Explain complex logic
3. **Docstrings:** Document all public methods
4. **Inline comments:** Explain non-obvious code

### Updating Documentation

When making changes:

1. Update relevant documentation
2. Add examples for new features
3. Update screenshots if UI changes
4. Review and update README if needed

## 🎯 Contribution Areas

### High Priority
- [ ] Performance optimization
- [ ] Cross-browser compatibility improvements
- [ ] Mobile responsiveness testing
- [ ] CI/CD pipeline enhancements

### Medium Priority
- [ ] Additional test scenarios
- [ ] Reporting improvements
- [ ] Documentation enhancements
- [ ] Code refactoring

### Good First Issues
- [ ] Test data improvements
- [ ] Screenshot organization
- [ ] Logging enhancements
- [ ] Configuration improvements

## 📞 Getting Help

- **Issues:** GitHub Issues for bugs and features
- **Discussions:** GitHub Discussions for questions
- **Documentation:** Check README and docs first
- **Community:** Be respectful and helpful

## 🙏 Recognition

Contributors will be recognized in:
- GitHub Contributors list
- CHANGELOG.md (future)
- Release notes
- Project documentation

Thank you for contributing to the Insider Test Automation Project! 🚀