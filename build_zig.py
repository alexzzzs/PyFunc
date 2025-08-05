#!/usr/bin/env python3
"""
Build script for PyFunc Zig backend.
"""

import os
import subprocess
import sys
import platform
from pathlib import Path

def check_zig_installation():
    """Check if Zig is installed and available."""
    try:
        result = subprocess.run(['zig', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Zig found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Zig not found in PATH")
            return False
    except FileNotFoundError:
        print("❌ Zig not installed")
        return False

def build_zig_backend():
    """Build the Zig backend shared library."""
    print("🔨 Building Zig backend...")
    
    # Change to the Zig directory
    zig_dir = Path("pyfunc/native_zig")
    if not zig_dir.exists():
        print(f"❌ Zig directory not found: {zig_dir}")
        return False
    
    original_dir = os.getcwd()
    
    try:
        os.chdir(zig_dir)
        
        # Build the shared library
        build_cmd = ['zig', 'build', '-Doptimize=ReleaseFast']
        print(f"Running: {' '.join(build_cmd)}")
        
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Zig backend built successfully!")
            
            # Check if the library was created
            lib_extensions = {
                'Windows': 'dll',
                'Darwin': 'dylib',
                'Linux': 'so'
            }
            
            system = platform.system()
            ext = lib_extensions.get(system, 'so')
            
            # Look for the built library
            possible_paths = [
                f"zig-out/lib/libpyfunc_zig.{ext}",
                f"zig-out/lib/pyfunc_zig.{ext}",
                f"libpyfunc_zig.{ext}",
                f"pyfunc_zig.{ext}"
            ]
            
            lib_found = False
            for lib_path in possible_paths:
                if os.path.exists(lib_path):
                    print(f"✅ Library found: {lib_path}")
                    lib_found = True
                    break
            
            if not lib_found:
                print("⚠️  Library built but not found in expected locations")
                print("Available files:")
                for root, dirs, files in os.walk("."):
                    for file in files:
                        if file.endswith(('.dll', '.so', '.dylib')):
                            print(f"  {os.path.join(root, file)}")
            
            return True
        else:
            print("❌ Zig build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    finally:
        os.chdir(original_dir)

def test_zig_backend():
    """Test the Zig backend after building."""
    print("\n🧪 Testing Zig backend...")
    
    try:
        from pyfunc.backends.zig_backend import is_zig_available, ZigBackend
        
        if not is_zig_available():
            print("❌ Zig backend not available after build")
            return False
        
        # Test basic functionality
        backend = ZigBackend()
        
        # Test sum
        test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = backend.sum(test_data)
        expected = 15.0
        
        if abs(result - expected) < 0.001:
            print(f"✅ Sum test passed: {result}")
        else:
            print(f"❌ Sum test failed: expected {expected}, got {result}")
            return False
        
        # Test mean
        result = backend.mean(test_data)
        expected = 3.0
        
        if abs(result - expected) < 0.001:
            print(f"✅ Mean test passed: {result}")
        else:
            print(f"❌ Mean test failed: expected {expected}, got {result}")
            return False
        
        print("✅ All Zig backend tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Zig backend test failed: {e}")
        return False

def main():
    """Main build function."""
    print("🚀 PyFunc Zig Backend Build Script")
    print("=" * 40)
    
    # Check if Zig is installed
    if not check_zig_installation():
        print("\n💡 To install Zig:")
        print("• Visit: https://ziglang.org/download/")
        print("• Or use package manager:")
        print("  - Windows: scoop install zig")
        print("  - macOS: brew install zig")
        print("  - Linux: snap install zig --classic")
        return 1
    
    # Build the backend
    if not build_zig_backend():
        return 1
    
    # Test the backend
    if not test_zig_backend():
        print("⚠️  Build succeeded but tests failed")
        return 1
    
    print("\n🎉 Zig backend build completed successfully!")
    print("\n💡 Usage:")
    print("from pyfunc import pipe, set_zig_threshold")
    print("set_zig_threshold(1000)  # Use Zig for datasets >= 1000")
    print("result = pipe([1, 2, 3, 4, 5]).sum().get()  # Auto-selects backend")
    print("result = pipe([1, 2, 3, 4, 5]).sum_zig().get()  # Force Zig")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())