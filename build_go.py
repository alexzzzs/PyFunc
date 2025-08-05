#!/usr/bin/env python3
"""
Build script for PyFunc Go backend.
"""

import os
import subprocess
import sys
import platform
from pathlib import Path

def check_go_installation():
    """Check if Go is installed and available."""
    try:
        result = subprocess.run(['go', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Go found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Go not found in PATH")
            return False
    except FileNotFoundError:
        print("❌ Go not installed")
        return False

def build_go_backend():
    """Build the Go backend shared library."""
    print("🔨 Building Go backend...")
    
    # Change to the Go directory
    go_dir = Path("pyfunc/native_go")
    if not go_dir.exists():
        print(f"❌ Go directory not found: {go_dir}")
        return False
    
    original_dir = os.getcwd()
    
    try:
        os.chdir(go_dir)
        
        # Determine output file name based on platform
        system = platform.system()
        if system == "Windows":
            output_name = "native_go.dll"
        elif system == "Darwin":
            output_name = "libnative_go.dylib"
        else:
            output_name = "libnative_go.so"
        
        # Build the shared library
        build_cmd = [
            'go', 'build',
            '-buildmode=c-shared',
            '-o', output_name,
            '.'
        ]
        
        print(f"Running: {' '.join(build_cmd)}")
        
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Go backend built successfully!")
            
            # Check if the library was created
            if os.path.exists(output_name):
                print(f"✅ Library created: {output_name}")
                return True
            else:
                print("❌ Library not found after build")
                return False
        else:
            print("❌ Go build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    finally:
        os.chdir(original_dir)

def test_go_backend():
    """Test the Go backend after building."""
    print("\n🧪 Testing Go backend...")
    
    try:
        from pyfunc.backends.go_backend import is_go_available, GoBackend
        
        if not is_go_available():
            print("❌ Go backend not available after build")
            return False
        
        # Test basic functionality
        backend = GoBackend()
        
        # Test bitwise AND
        test_data = [15, 31, 63, 127]
        result = backend.bitwise_and(test_data, 7)
        expected = [7, 7, 7, 7]  # All should result in 7
        
        if result == expected:
            print(f"✅ Bitwise AND test passed: {result}")
        else:
            print(f"❌ Bitwise AND test failed: expected {expected}, got {result}")
            return False
        
        # Test bitwise OR
        test_data = [1, 2, 4]
        result = backend.bitwise_or(test_data, 8)
        expected = [9, 10, 12]  # 1|8=9, 2|8=10, 4|8=12
        
        if result == expected:
            print(f"✅ Bitwise OR test passed: {result}")
        else:
            print(f"❌ Bitwise OR test failed: expected {expected}, got {result}")
            return False
        
        print("✅ All Go backend tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Go backend test failed: {e}")
        return False

def main():
    """Main build function."""
    print("🚀 PyFunc Go Backend Build Script")
    print("=" * 40)
    
    # Check if Go is installed
    if not check_go_installation():
        print("\n💡 To install Go:")
        print("• Visit: https://golang.org/dl/")
        print("• Or use package manager:")
        print("  - Windows: scoop install go")
        print("  - macOS: brew install go")
        print("  - Linux: sudo apt install golang-go")
        return 1
    
    # Build the backend
    if not build_go_backend():
        return 1
    
    # Test the backend
    if not test_go_backend():
        print("⚠️  Build succeeded but tests failed")
        return 1
    
    print("\n🎉 Go backend build completed successfully!")
    print("\n💡 Usage:")
    print("from pyfunc import pipe, set_go_threshold")
    print("set_go_threshold(500)  # Use Go for datasets >= 500")
    print("result = pipe([15, 31, 63]).bitwise_and(7).to_list()  # Auto-selects backend")
    print("result = pipe([15, 31, 63]).bitwise_and_go(7).to_list()  # Force Go")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())