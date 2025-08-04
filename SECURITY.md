# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in PyFunc, please report it by emailing the maintainers directly rather than opening a public issue.

## Security Best Practices

### For Contributors

1. **Never commit sensitive information:**
   - API keys or tokens
   - Passwords or credentials
   - Private keys or certificates
   - Configuration files with secrets

2. **Use environment variables for secrets:**
   ```bash
   export TWINE_USERNAME="__token__"
   export TWINE_PASSWORD="your-api-token"
   ```

3. **Check your commits before pushing:**
   ```bash
   git diff --cached  # Review staged changes
   git log --oneline -5  # Check recent commits
   ```

### For Users

1. **Keep your dependencies updated:**
   ```bash
   pip install --upgrade pyfunc-pipeline
   ```

2. **Use virtual environments:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Validate input data when using PyFunc in production applications**

## Protected Files

The following files are automatically ignored by git to prevent accidental commits:

- `.pypirc` (contains PyPI API tokens)
- `.env` files (environment variables)
- `*secret*`, `*password*`, `*token*` files
- Build artifacts (`dist/`, `*.egg-info/`)
- IDE configuration files
- OS-specific files

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2   | :x:                |

## Security Updates

Security updates will be released as patch versions and announced in the [CHANGELOG.md](CHANGELOG.md).