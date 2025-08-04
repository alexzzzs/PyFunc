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

3. **API Tokens**: Generate API tokens for secure authentication:
   - Go to PyPI Account Settings → API tokens
   - Create a token with "Entire account" scope
   - Save the token securely (you'll need it later)

## 🚀 Step-by-Step Publishing Process

### Step 1: Clean Previous Builds
```bash
# Remove old build artifacts
rm -rf dist/ build/ *.egg-info/
```

### Step 2: Build the Package
```bash
# Build source distribution and wheel
python -m build
```

This creates:
- `dist/pyfunc-0.2.0.tar.gz` (source distribution)
- `dist/pyfunc-0.2.0-py3-none-any.whl` (wheel)

### Step 3: Test on TestPyPI (Recommended)
```bash
# Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*
```

When prompted:
- Username: `__token__`
- Password: Your TestPyPI API token (starts with `pypi-`)

### Step 4: Test Installation from TestPyPI
```bash
# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ pyfunc
```

### Step 5: Publish to PyPI
```bash
# Upload to production PyPI
python -m twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: Your PyPI API token

### Step 6: Verify Publication
```bash
# Install from PyPI
pip install pyfunc

# Test the installation
python -c "from pyfunc import pipe, _; print(pipe([1,2,3]).map(_ * 2).to_list())"
```

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

## 🎉 Success!

Once published, your package will be available at:
- **PyPI**: https://pypi.org/project/pyfunc/
- **Installation**: `pip install pyfunc`

Users can then use your library:
```python
from pyfunc import pipe, _

result = pipe([1, 2, 3, 4]).filter(_ > 2).map(_ * 10).to_list()
print(result)  # [30, 40]
```