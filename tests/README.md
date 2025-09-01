# Test Suite Documentation

## 🏗️ Test Structure

This test suite follows a feature-based organization pattern for better maintainability and scalability.

```
tests/
├── unit/                    # Unit tests for individual components
├── integration/             # Integration tests for component interactions
├── popup/                   # Popup functionality tests
│   ├── test_popup_functionality.py
│   ├── test_popup_display.py
│   └── test_popup_performance.py
├── cross_browser/           # Cross-browser compatibility tests
│   └── test_cross_browser.py
├── mobile/                  # Mobile and tablet responsive tests
│   └── test_performance_responsive.py
├── utils/                   # Test utilities and helpers
├── conftest.py             # Centralized pytest fixtures
└── README.md               # This file
```

## 🧪 Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest tests/ -v

# Run specific test category
pytest tests/popup/ -v
pytest tests/cross_browser/ -v
pytest tests/mobile/ -v

# Run with markers
pytest -m critical
pytest -m smoke
pytest -m regression
```

### Test Categories

- **Popup Tests** (`tests/popup/`): Core popup functionality validation
- **Cross-Browser Tests** (`tests/cross_browser/`): Browser compatibility testing
- **Mobile Tests** (`tests/mobile/`): Responsive design and mobile functionality
- **Unit Tests** (`tests/unit/`): Individual component testing
- **Integration Tests** (`tests/integration/`): Component interaction testing

## 📊 Test Markers

### Priority Markers
- `@pytest.mark.critical` - P1 Critical tests
- `@pytest.mark.high` - P2 High priority tests
- `@pytest.mark.medium` - P3 Medium priority tests
- `@pytest.mark.low` - P4 Low priority tests

### Functional Markers
- `@pytest.mark.smoke` - Smoke tests
- `@pytest.mark.regression` - Regression tests
- `@pytest.mark.performance` - Performance tests
- `@pytest.mark.cross_browser` - Cross-browser tests

### Browser Markers
- `@pytest.mark.browser_chrome` - Chrome-specific tests
- `@pytest.mark.browser_firefox` - Firefox-specific tests
- `@pytest.mark.browser_safari` - Safari-specific tests

## 🔧 Test Conventions

### Naming Conventions
- **Test Files**: `test_<feature>.py` (e.g., `test_popup_functionality.py`)
- **Test Functions**: `test_<expected_behavior>` (e.g., `test_popup_displays_correctly`)

### Test Structure
```python
def test_feature_behavior():
    """Test description explaining what is being tested."""
    # Arrange
    # Act
    # Assert
```

### Fixtures
Common fixtures are defined in `conftest.py`:
- `driver` - WebDriver instance
- `popup_page` - Popup page object
- `product_page` - Product page object

## 📸 Screenshots & Evidence

Screenshots are automatically captured:
- **Failed tests**: `screenshots/failed/`
- **Passed tests**: `screenshots/passed/`
- **Evidence**: `screenshots/evidence/`

## 🚀 CI/CD Integration

Tests run automatically on:
- **Push to main branch**
- **Pull requests**
- **Scheduled runs** (if configured)

## 🆘 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure you're in the project root
cd /path/to/project

# Install dependencies
pip install -r requirements.txt
```

**WebDriver Issues:**
```bash
# Update WebDriver
pip install --upgrade webdriver-manager

# Clear cache
rm -rf ~/.wdm
```

**Test Discovery Issues:**
```bash
# Run with explicit path
pytest tests/popup/test_popup_functionality.py -v

# Check test discovery
pytest --collect-only
```

## 📝 Adding New Tests

1. **Create test file** in appropriate category folder
2. **Follow naming conventions** for files and functions
3. **Use appropriate markers** for categorization
4. **Include docstrings** with test descriptions
5. **Add to this README** if creating new categories

## 🔍 Test Utilities

Common test utilities are available in `tests/utils/`:
- Screenshot helpers
- Test data generators
- Custom assertions
- Performance monitoring tools

---

**Last Updated**: September 1, 2025  
**Maintainer**: QA Automation Team  
**Version**: 2.0.0
