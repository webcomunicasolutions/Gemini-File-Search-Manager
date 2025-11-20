# Contributing to Gemini File Search Manager

## 🌍 Available Languages

- [English](CONTRIBUTING.md)
- [Español](CONTRIBUTING_ES.md)

---

Thank you for your interest in contributing to Gemini File Search Manager! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Trolling, insulting comments, or personal attacks
- Public or private harassment
- Publishing others' private information
- Other conduct that could reasonably be considered inappropriate

---

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Google Gemini API key
- Text editor or IDE

### Fork and Clone

1. **Fork the repository** on GitHub

2. **Clone your fork**:
```bash
git clone https://github.com/your-username/gemini-file-search-manager.git
cd gemini-file-search-manager
```

3. **Add upstream remote**:
```bash
git remote add upstream https://github.com/original-owner/gemini-file-search-manager.git
```

4. **Verify remotes**:
```bash
git remote -v
# origin    https://github.com/your-username/gemini-file-search-manager.git (fetch)
# origin    https://github.com/your-username/gemini-file-search-manager.git (push)
# upstream  https://github.com/original-owner/gemini-file-search-manager.git (fetch)
# upstream  https://github.com/original-owner/gemini-file-search-manager.git (push)
```

### Development Setup

1. **Create virtual environment**:
```bash
cd web_app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install flask flask-cors google-genai python-dotenv werkzeug
pip install pytest pytest-cov  # For testing
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your API key
```

4. **Run application**:
```bash
python app.py
```

---

## Development Workflow

### Branch Strategy

We use the following branch naming conventions:

- `main` - Stable production code
- `develop` - Integration branch for features
- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes
- `hotfix/critical-fix` - Critical production fixes
- `docs/documentation-topic` - Documentation updates

### Workflow Steps

1. **Sync with upstream**:
```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

2. **Create feature branch**:
```bash
git checkout -b feature/amazing-feature
```

3. **Make changes**:
- Write code
- Add tests
- Update documentation

4. **Commit changes**:
```bash
git add .
git commit -m "Add amazing feature"
```

5. **Push to your fork**:
```bash
git push origin feature/amazing-feature
```

6. **Create Pull Request** on GitHub

---

## Code Style

### Python Code Style

Follow **PEP 8** guidelines:

**Good**:
```python
def upload_document(file_path, metadata=None):
    """
    Upload document to File Search Store.

    Args:
        file_path (str): Path to document file
        metadata (dict, optional): Custom metadata

    Returns:
        dict: Upload result with document ID
    """
    if metadata is None:
        metadata = {}

    # Implementation
    return {'success': True}
```

**Bad**:
```python
def uploadDoc(fp, m):
    if m == None:
        m = {}
    return {'success':True}
```

### Python Best Practices

**1. Naming Conventions**:
```python
# Variables and functions: snake_case
user_message = "Hello"
def get_store_info():
    pass

# Classes: PascalCase
class FileSearchManager:
    pass

# Constants: UPPER_CASE
MAX_FILE_SIZE = 100 * 1024 * 1024
```

**2. Docstrings** (required for all functions):
```python
def suggest_metadata(file_content):
    """
    Analyze document and suggest metadata using Gemini AI.

    Args:
        file_content (bytes): Document binary content

    Returns:
        dict: Suggested metadata fields

    Raises:
        ValueError: If file cannot be read
        APIError: If Gemini API fails

    Example:
        >>> metadata = suggest_metadata(file_content)
        >>> print(metadata['titulo'])
        'Contract for Services'
    """
    pass
```

**3. Type Hints** (recommended):
```python
from typing import Dict, List, Optional

def upload_file(
    file_path: str,
    metadata: Optional[Dict[str, str]] = None
) -> Dict[str, any]:
    """Upload file with optional metadata."""
    pass
```

**4. Error Handling**:
```python
# Good - Specific exceptions
try:
    result = api_call()
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    raise
except TimeoutError as e:
    logger.warning(f"Timeout: {e}")
    return None

# Bad - Catch all
try:
    result = api_call()
except:
    pass
```

**5. Logging**:
```python
# Good - Use logging module
import logging
logger = logging.getLogger(__name__)

logger.info("Starting upload")
logger.warning("Retrying failed request")
logger.error("Upload failed", exc_info=True)

# Bad - Use print
print("Starting upload")
```

### JavaScript Code Style

**1. Modern ES6+ Syntax**:
```javascript
// Good - const/let, arrow functions
const uploadDocument = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    return await response.json();
};

// Bad - var, old syntax
var uploadDocument = function(file) {
    var formData = new FormData();
    formData.append('file', file);
    // ...
};
```

**2. Naming Conventions**:
```javascript
// Variables and functions: camelCase
const userName = 'John';
function getUserInfo() {}

// Classes: PascalCase
class DocumentManager {}

// Constants: UPPER_CASE
const MAX_FILE_SIZE = 100 * 1024 * 1024;
```

**3. Comments**:
```javascript
/**
 * Upload document with metadata
 * @param {File} file - Document file
 * @param {Object} metadata - Custom metadata
 * @returns {Promise<Object>} Upload result
 */
async function uploadDocument(file, metadata) {
    // Implementation
}
```

### HTML/CSS Style

**HTML**:
```html
<!-- Good - Semantic, accessible -->
<section class="document-list">
    <h2>Documents</h2>
    <ul role="list">
        <li role="listitem">
            <button aria-label="Delete document">Delete</button>
        </li>
    </ul>
</section>

<!-- Bad - Non-semantic, inaccessible -->
<div class="docs">
    <div class="title">Documents</div>
    <div>
        <div onclick="delete()">Delete</div>
    </div>
</div>
```

**CSS**:
```css
/* Good - Clear, organized */
.document-card {
    padding: 1rem;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.document-card__title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #0f766e;
}

/* Bad - Unclear, disorganized */
.dc {
    padding: 16px;
    background: #fff;
}
```

---

## Testing

### Test Requirements

All new features and bug fixes should include tests.

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=web_app tests/

# Run specific test file
pytest tests/test_upload.py

# Run specific test
pytest tests/test_upload.py::test_upload_pdf
```

### Writing Tests

**Example Test**:
```python
# tests/test_upload.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_success(client):
    """Test successful document upload"""
    data = {
        'file': (open('test.pdf', 'rb'), 'test.pdf'),
        'metadata': '{"tipo":"test"}'
    }

    response = client.post('/upload', data=data)
    assert response.status_code == 200
    assert response.json['success'] == True

def test_upload_no_file(client):
    """Test upload with no file"""
    response = client.post('/upload', data={})
    assert response.status_code == 400
    assert 'error' in response.json
```

### Test Coverage

Aim for:
- **Minimum**: 70% coverage
- **Target**: 85% coverage
- **Ideal**: 95% coverage

Focus on:
- Core functionality
- Edge cases
- Error handling
- API endpoints

---

## Pull Request Process

### Before Submitting

1. **Update your branch**:
```bash
git fetch upstream
git rebase upstream/main
```

2. **Run tests**:
```bash
pytest tests/
```

3. **Check code style**:
```bash
flake8 web_app/
pylint web_app/
```

4. **Update documentation** if needed

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issue
Fixes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Tested locally
- [ ] Added unit tests
- [ ] All tests passing

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex sections
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests
- [ ] All tests pass
```

### Review Process

1. **Automated Checks**: CI/CD runs tests
2. **Code Review**: Maintainers review code
3. **Feedback**: Address review comments
4. **Approval**: Get approval from maintainer
5. **Merge**: Maintainer merges PR

### After Merge

1. **Delete branch**:
```bash
git branch -d feature/amazing-feature
git push origin --delete feature/amazing-feature
```

2. **Update local main**:
```bash
git checkout main
git pull upstream main
```

---

## Reporting Bugs

### Before Reporting

1. **Search existing issues** - May already be reported
2. **Try latest version** - May be fixed
3. **Reproduce** - Ensure it's consistent

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Screenshots
If applicable

## Environment
- OS: [e.g. Windows 10, macOS 12.0]
- Python Version: [e.g. 3.10.0]
- Flask Version: [e.g. 3.0.0]
- Browser: [e.g. Chrome 120]

## Additional Context
Any other information

## Logs
```
Paste relevant logs here
```
```

---

## Suggesting Features

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Problem It Solves
What problem does this feature address?

## Proposed Solution
How should this feature work?

## Alternatives Considered
Other approaches you've considered

## Use Cases
Real-world scenarios where this helps

## Implementation Ideas
Technical suggestions (optional)

## Additional Context
Any other information
```

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and ideas
- **Pull Requests**: Code contributions

### Getting Help

1. Check [documentation](README.md)
2. Search [existing issues](https://github.com/yourusername/gemini-file-search-manager/issues)
3. Create new issue with details

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in project documentation

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

Feel free to:
- Open an issue
- Start a discussion
- Contact maintainers

Thank you for contributing to Gemini File Search Manager! 🎉
