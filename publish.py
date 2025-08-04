#!/usr/bin/env python3
"""
PyFunc Publishing Script - Environment Variable Method

This script publishes PyFunc to PyPI using environment variables for authentication.
This is the method we successfully used for publishing v0.2.0 and v0.3.0.

Prerequisites:
1. Set environment variables:
   $env:TWINE_USERNAME = "__token__"
   $env:TWINE_PASSWORD = "your-pypi-token-here"

Usage: python publish.py [test|prod]
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
        if result.stdout.strip():
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        if e.stderr:
            print(e.stderr)
        return False

def check_environment():
    """Check if required environment variables are set."""
    username = os.getenv('TWINE_USERNAME')
    password = os.getenv('TWINE_PASSWORD')
    
    if not username:
        print("❌ TWINE_USERNAME environment variable not set")
        print("Run: $env:TWINE_USERNAME = \"__token__\"")
        return False
    
    if not password:
        print("❌ TWINE_PASSWORD environment variable not set")
        print("Run: $env:TWINE_PASSWORD = \"your-pypi-token-here\"")
        return False
    
    if username != "__token__":
        print("❌ TWINE_USERNAME should be \"__token__\"")
        return False
    
    if not password.startswith("pypi-"):
        print("❌ TWINE_PASSWORD should start with \"pypi-\"")
        return False
    
    print("✅ Environment variables are properly configured")
    return True

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['test', 'prod']:
        print("Usage: python publish.py [test|prod]")
        print("  test - Upload to TestPyPI")
        print("  prod - Upload to production PyPI")
        print("\nPrerequisites:")
        print("  $env:TWINE_USERNAME = \"__token__\"")
        print("  $env:TWINE_PASSWORD = \"your-pypi-token-here\"")
        sys.exit(1)
    
    target = sys.argv[1]
    
    print("🚀 PyFunc Publishing Script (Environment Variable Method)")
    print("=" * 60)
    
    # Step 1: Check environment variables
    if not check_environment():
        sys.exit(1)
    
    # Step 2: Clean old builds
    print("\n🧹 Cleaning old builds...")
    if os.path.exists('dist'):
        import shutil
        shutil.rmtree('dist')
        print("✅ Cleaned dist/ directory")
    
    # Step 3: Run tests
    if not run_command("python -m unittest discover tests", "Running tests"):
        print("❌ Tests failed. Please fix before publishing.")
        sys.exit(1)
    
    # Step 4: Build package
    if not run_command("python -m build", "Building package"):
        sys.exit(1)
    
    # Step 5: Validate package
    if not run_command("python -m twine check dist/*", "Validating package"):
        sys.exit(1)
    
    # Step 6: Upload using environment variables
    if target == 'test':
        print("\n🧪 Uploading to TestPyPI...")
        upload_cmd = "python -m twine upload --repository testpypi dist/* --non-interactive"
    else:
        print("\n🚀 Uploading to PyPI...")
        upload_cmd = "python -m twine upload dist/* --non-interactive"
    
    try:
        result = subprocess.run(upload_cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Successfully published to {'TestPyPI' if target == 'test' else 'PyPI'}!")
        
        if result.stdout:
            print(result.stdout)
        
        if target == 'test':
            print("\n🧪 Test installation:")
            print("pip install --index-url https://test.pypi.org/simple/ pyfunc-pipeline")
            print("\n🔗 TestPyPI URL:")
            print("https://test.pypi.org/project/pyfunc-pipeline/")
        else:
            print("\n📦 Installation:")
            print("pip install --upgrade pyfunc-pipeline")
            print("\n🔗 PyPI URL:")
            print("https://pypi.org/project/pyfunc-pipeline/")
        
        print("\n✅ Next steps:")
        print("1. Test the installation")
        print("2. Commit version changes to GitHub")
        print("3. Create a GitHub release tag")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Upload to {'TestPyPI' if target == 'test' else 'PyPI'} failed.")
        if e.stderr:
            print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()