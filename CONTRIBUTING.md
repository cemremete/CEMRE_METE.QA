# Contributing to Insider Test Automation Project

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- VS Code (recommended) or any Python IDE
- Chrome, Firefox, or Safari browser

### Development Environment Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/cemremete/CEMRE_METE.QA.git
cd CEMRE_METE.QA
```

#### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Verify Installation
```bash
pytest --version
python -c "import selenium; print(f'Selenium version: {selenium.__version__}')"
```

## VS Code Configuration

### Required Extensions
- Python (Microsoft)
- Pylance
- Python Test Explorer (optional)
- GitLens (recommended)
- Python Docstring Generator (recommended)

### Settings Configuration
The project includes optimized VS Code settings in `.vscode/settings.json`:

#### Python Interpreter
- **Windows**: `${workspaceFolder}/venv/Scripts/python.exe`
- **Linux/macOS**: `${workspaceFolder}/venv/bin/python`

#### Code Quality Tools
- **Formatting**: Black (auto-format on save)
- **Linting**: Flake8 with Black-compatible rules
- **Import Sorting**: isort with Black profile
- **Type Checking**: Basic mode enabled

#### File Exclusions
Automatically excludes:
- `__pycache__/`, `*.pyc` (Python cache)
- `screenshots/`, `reports/` (Test artifacts)
- `.coverage`, `htmlcov/` (Coverage reports)
- `.tox/`, `.mypy_cache/` (Tool caches)

## Test Development

### Test Structure
```
tests/
├── popup/           # Popup functionality tests
├── cross_browser/   # Cross-browser compatibility
├── mobile/          # Mobile and responsive tests
├── unit/            # Unit tests
├── integration/     # Integration tests
├── utils/           # Test utilities
├── conftest.py      # Shared fixtures
└── README.md        # Test documentation
```

### Test Naming Conventions
- **Files**: `test_<feature>_<behavior>.py`
- **Functions**: `test_<expected_behavior>`
- **Classes**: `Test<FeatureName>`

### Example Test Structure
```python
import pytest
from pages.popup_page import PopupPage

class TestPopupFunctionality:
    """Test class for popup functionality validation."""
    
    @pytest.mark.critical
    @pytest.mark.popup
    def test_popup_displays_correctly(self, driver):
        """Test that popup displays with correct content."""
        # Arrange
        popup_page = PopupPage(driver)
        
        # Act
        popup_page.click_show_instantly_button()
        
        # Assert
        assert popup_page.is_popup_visible()
        assert popup_page.get_popup_content() == "Expected Content"
```

### Test Markers
Use appropriate markers for test categorization:

#### Priority Markers
- `@pytest.mark.critical` - P1 Critical tests
- `@pytest.mark.high` - P2 High priority tests
- `@pytest.mark.medium` - P3 Medium priority tests
- `@pytest.mark.low` - P4 Low priority tests

#### Functional Markers
- `@pytest.mark.smoke` - Smoke tests
- `@pytest.mark.regression` - Regression tests
- `@pytest.mark.performance` - Performance tests
- `@pytest.mark.cross_browser` - Cross-browser tests

#### Feature Markers
- `@pytest.mark.popup` - Popup functionality
- `@pytest.mark.mobile` - Mobile/responsive
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests

### Fixtures
Common fixtures are defined in `conftest.py`:
- `driver` - WebDriver instance
- `popup_page` - Popup page object
- `product_page` - Product page object

### Data-Driven Testing
Use `@pytest.mark.parametrize` for multiple test scenarios:

```python
@pytest.mark.parametrize("browser", ["chrome", "firefox", "safari"])
def test_cross_browser_compatibility(self, browser):
    """Test popup functionality across different browsers."""
    # Test implementation
    pass
```

## Code Style and Standards

### Python Standards
- Follow PEP 8 style guide
- Use Black for code formatting
- Maximum line length: 88 characters (Black default)
- Use type hints where appropriate
- Follow Google docstring format

### Import Organization
- Use isort with Black profile
- Group imports: standard library, third-party, local
- Auto-organize imports on save

### Documentation Requirements
- Use docstrings for all public functions and classes
- Follow Google docstring format
- Include parameter and return type documentation
- Provide usage examples for complex functions

### Code Quality Standards
- Maintain >90% test coverage
- Use meaningful variable and function names
- Avoid magic numbers and hard-coded values
- Implement proper error handling
- Use logging instead of print statements

## Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest tests/ -v

# Run specific test category
pytest tests/popup/ -v
pytest tests/cross_browser/ -v

# Run with markers
pytest -m critical
pytest -m "smoke and popup"
```

### Using the Test Runner
```bash
# Run popup tests
python run_tests.py --suite popup --browser chrome

# Run cross-browser tests
python run_tests.py --suite cross-browser --browser firefox

# Run all tests
python run_tests.py --suite all --browser chrome --headless
```

### Test Reports
- **HTML Reports**: `reports/html/`
- **JSON Reports**: `reports/json/`
- **Screenshots**: `screenshots/` (failed/passed/evidence)

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/new-test-suite
```

### 2. Make Changes
- Write tests following conventions
- Update documentation if needed
- Ensure all tests pass
- Run code quality checks

### 3. Test Your Changes
```bash
# Run your new tests
pytest tests/your_new_tests/ -v

# Run related test suites
pytest -m "related_marker" -v

# Run code quality checks
black --check .
flake8 .
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: Add new test suite for X functionality

- Added test cases for feature X
- Updated documentation
- Added new markers if needed"
```

### 5. Push and Create PR
```bash
git push origin feature/new-test-suite
# Create Pull Request on GitHub
```

## Pull Request Guidelines

### PR Requirements
- All tests must pass
- Code coverage should not decrease
- Follow coding standards
- Include appropriate documentation
- Add relevant test markers

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### WebDriver Issues
```bash
# Update WebDriver
pip install --upgrade webdriver-manager

# Clear cache
rm -rf ~/.wdm
```

#### VS Code Issues
- Ensure Python extension is installed
- Check interpreter path in settings
- Reload VS Code window if needed
- Verify workspace settings are applied

### Getting Help
1. Check existing issues in GitHub
2. Review this documentation
3. Check test logs and screenshots
4. Contact the QA team
5. Review project README.md

## Quality Standards

### Test Coverage
- Aim for >90% test coverage
- Include positive and negative test cases
- Test edge cases and error conditions
- Use coverage reports to identify gaps

### Performance
- Tests should complete within reasonable time
- Use `@pytest.mark.slow` for tests >30 seconds
- Optimize slow tests when possible
- Monitor test execution times

### Reliability
- Tests should be deterministic
- Avoid hard-coded waits
- Use proper assertions and error messages
- Implement retry mechanisms for flaky tests

## Best Practices

### Test Design
- One assertion per test when possible
- Use descriptive test names
- Group related tests in classes
- Keep tests independent
- Use AAA pattern (Arrange, Act, Assert)

### Page Object Model
- Encapsulate page interactions in page classes
- Use locators as class constants
- Implement wait strategies for elements
- Separate test logic from page logic

### Data Management
- Use fixtures for test data
- Avoid hard-coded test data
- Use factories for complex objects
- Implement data cleanup strategies

### Error Handling
- Capture screenshots on failure
- Log detailed error information
- Provide clear failure messages
- Implement proper exception handling

### Security Considerations
- Never commit sensitive data
- Use environment variables for credentials
- Implement secure test data management
- Follow security testing best practices

## Continuous Integration

### GitHub Actions
The project includes CI/CD pipeline configuration:
- Automated test execution
- Code quality checks
- Security scanning
- Dependency updates

### Pre-commit Hooks
Install pre-commit hooks for code quality:
```bash
pip install pre-commit
pre-commit install
```

## Documentation Standards

### Code Documentation
- Use clear, concise docstrings
- Include examples for complex functions
- Document parameters and return values
- Keep documentation up to date

### Test Documentation
- Document test scenarios and expected outcomes
- Include bug reproduction steps
- Maintain test case matrices
- Update documentation with changes

---

**Thank you for contributing to the Insider Test Automation Project!**

For questions or suggestions, please open an issue or contact the QA team.

**Maintainer:** QA Automation Engineer  
**Last Updated:** September 3, 2025  
**Version:** 2.0.0
