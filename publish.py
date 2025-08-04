#!/usr/bin/env python3
"""
PyFunc Publishing Script

This script helps you publish PyFunc to PyPI.
Run with: python publish.py [test|prod]
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(e.stderr)
        return False

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['test', 'prod']:
        print("Usage: python publish.py [test|prod]")
        print("  test - Upload to TestPyPI")
        print("  prod - Upload to production PyPI")
        sys.exit(1)
    
    target = sys.argv[1]
    
    print("🚀 PyFunc Publishing Script")
    print("=" * 40)
    
    # Step 1: Clean old builds
    print("\n1. Cleaning old builds...")
    if os.path.exists('dist'):
        import shutil
        shutil.rmtree('dist')
        print("✅ Cleaned dist/ directory")
    
    # Step 2: Run tests
    if not run_command("python -m unittest discover tests", "Running tests"):
        print("❌ Tests failed. Please fix before publishing.")
        sys.exit(1)
    
    # Step 3: Build package
    if not run_command("python -m build", "Building package"):
        sys.exit(1)
    
    # Step 4: Validate package
    if not run_command("python -m twine check dist/*", "Validating package"):
        sys.exit(1)
    
    # Step 5: Upload
    if target == 'test':
        print("\n🧪 Uploading to TestPyPI...")
        print("Username: __token__")
        print("Password: [Your TestPyPI API token]")
        upload_cmd = "python -m twine upload --repository testpypi dist/*"
    else:
        print("\n🚀 Uploading to PyPI...")
        print("Username: __token__")
        print("Password: [Your PyPI API token]")
        upload_cmd = "python -m twine upload dist/*"
    
    print(f"\nRunning: {upload_cmd}")
    print("\nNote: You'll be prompted for your API token.")
    
    try:
        subprocess.run(upload_cmd, shell=True, check=True)
        print(f"\n🎉 Successfully published to {'TestPyPI' if target == 'test' else 'PyPI'}!")
        
        if target == 'test':
            print("\n📦 Test installation:")
            print("pip install --index-url https://test.pypi.org/simple/ pyfunc")
        else:
            print("\n📦 Installation:")
            print("pip install pyfunc")
            
        print("\n🔗 Package URL:")
        base_url = "https://test.pypi.org" if target == 'test' else "https://pypi.org"
        print(f"{base_url}/project/pyfunc/")
        
    except subprocess.CalledProcessError:
        print(f"\n❌ Upload to {'TestPyPI' if target == 'test' else 'PyPI'} failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()