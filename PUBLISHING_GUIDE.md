# PyPI Publishing Guide for PyFunc

## 📋 Prerequisites

Before publishing to PyPI, ensure you have:

1. **PyPI Account**: Create accounts on both:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

2. **Required Tools**: Install the publishing tools:
   ```bash
   pip install --upgrade pip build twine
   ```



## 🚀 Streamlined Publishing Process (Current Method)

### Step 1: Update Version and Changelog
```bash
# Update version in pyproject.toml
# Update CHANGELOG.md with new features
```

### Step 2: Clean and Build
```bash
# Remove old build artifacts (Windows)
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue

# Build source distribution and wheel
python -m build
```

### Step 3: Validate Package
```bash
# Check package integrity
python -m twine check dist/*
```

### Step 4: Set Environment Variables (Recommended)
```powershell
# Set credentials as environment variables (Windows PowerShell)
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "your-pypi-token-here"
```

### Step 5: Publish to PyPI
```bash
# Upload to production PyPI using environment variables
python -m twine upload dist/* --non-interactive
```

### Step 6: Verify and Test
```bash
# Install the new version
pip install --upgrade --force-reinstall pyfunc-pipeline

# Test the installation
python -c "from pyfunc import pipe, _; print('✅ Success!')"
```

## 📝 **Current Package Details**
- **Package Name**: `pyfunc-pipeline` (PyPI name)
- **Import Name**: `pyfunc` (Python import)
- **Installation**: `pip install pyfunc-pipeline`
- **Usage**: `from pyfunc import pipe, _`

## 🚨 **Common Issues & Solutions**

### Issue 1: Package Name Already Taken
**Problem**: `The user 'username' isn't allowed to upload to project 'pyfunc'`
**Solution**: The original name `pyfunc` was already taken, so we use `pyfunc-pipeline`

### Issue 2: Authentication Problems
**Problem**: `Invalid or non-existent authentication information`
**Solutions**:
- Ensure token starts with `pypi-`
- Use `__token__` as username
- Set environment variables instead of typing tokens manually

### Issue 3: Terminal Won't Accept Token Paste
**Problem**: Can't paste API token in terminal
**Solution**: Use environment variables:
```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-your-actual-token-here"
python -m twine upload dist/* --non-interactive
```

### Issue 4: F-String Template Confusion
**Problem**: `TypeError: unsupported format string passed to Placeholder.__format__`
**Solution**: Don't use f-strings with template mapping:
```python
# ❌ Wrong (f-string)
.map(f"Order #{_['id']} for {_['customer']}")

# ✅ Correct (string template)
.map("Order #{id} for {customer}")
```

## 📊 **Publishing History**
- **v0.1.0**: Initial release (never published)
- **v0.2.0**: First successful PyPI release with core features
- **v0.3.0**: Template mapping features added

## 🔄 **Version Update Process**
1. Update `version = "x.x.x"` in `pyproject.toml`
2. Update `CHANGELOG.md` with new features
3. Clean, build, and publish
4. Test installation
5. Commit and push to GitHub

## 🔧 Alternative: Using GitHub Actions (Automated)

Create `.github/workflows/publish.yml` for automated publishing:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

## 📝 Pre-Publication Checklist

- [ ] Updated version number in `pyproject.toml`
- [ ] Updated `CHANGELOG.md` with new version
- [ ] All tests passing (`python -m unittest discover tests`)
- [ ] Documentation is up to date
- [ ] README.md has correct installation instructions
- [ ] License file is present
- [ ] Package builds successfully (`python -m build`)
- [ ] Tested on TestPyPI

## 🔍 Package Validation

Before publishing, validate your package:

```bash
# Check package metadata
python -m twine check dist/*

# Verify package contents
tar -tzf dist/pyfunc-0.2.0.tar.gz
```

## 🏷️ Version Management

For future releases:

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with new features
3. **Create git tag**:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```
4. **Build and publish** following the steps above

## 🛡️ Security Best Practices

1. **Use API tokens** instead of username/password
2. **Store tokens securely** (use environment variables or GitHub secrets)
3. **Test on TestPyPI first** before production
4. **Use 2FA** on your PyPI account

## 📊 Post-Publication

After publishing:

1. **Update README** with correct installation command:
   ```bash
   pip install pyfunc
   ```

2. **Create GitHub release** with changelog
3. **Monitor downloads** on PyPI dashboard
4. **Respond to issues** and user feedback

## 🚨 Troubleshooting

### Common Issues:

1. **Package name already exists**: Choose a different name or contact PyPI support
2. **Version already exists**: Increment version number
3. **Authentication failed**: Check API token and username (`__token__`)
4. **Build fails**: Check `pyproject.toml` syntax and dependencies

### Useful Commands:

```bash
# Check what will be included in package
python -m build --sdist --outdir temp_dist
tar -tzf temp_dist/pyfunc-0.2.0.tar.gz

# Validate package before upload
python -m twine check dist/*

# Upload with verbose output
python -m twine upload --verbose dist/*
```

