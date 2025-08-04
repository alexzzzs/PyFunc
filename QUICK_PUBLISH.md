# Quick Publishing Reference

## 🚀 **Fast Publishing (Current Method)**

### 1. Set Environment Variables (Once)
```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-your-actual-token-here"
```

### 2. Update Version
Edit `pyproject.toml`:
```toml
version = "0.3.1"  # Update this
```

### 3. Publish
```bash
# Clean, build, and publish in one go
python simple_publish.py 0.3.1 prod
```

## 📋 **Manual Steps (If Script Fails)**

```bash
# 1. Clean
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue

# 2. Build
python -m build

# 3. Check
python -m twine check dist/*

# 4. Upload
python -m twine upload dist/* --non-interactive
```

## ✅ **Verify Publication**

```bash
# Install new version
pip install --upgrade --force-reinstall pyfunc-pipeline

# Test it works
python -c "from pyfunc import pipe, _; print('✅ Success!')"
```

## 🔗 **URLs**
- **PyPI**: https://pypi.org/project/pyfunc-pipeline/
- **TestPyPI**: https://test.pypi.org/project/pyfunc-pipeline/

## 📝 **Package Info**
- **Install**: `pip install pyfunc-pipeline`
- **Import**: `from pyfunc import pipe, _`
- **Current Version**: 0.3.0