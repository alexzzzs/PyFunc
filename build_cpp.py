#!/usr/bin/env python3
"""
Build script for PyFunc C++ backend.
"""

import subprocess
import sys
import os
import shutil

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

def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    # Check for C++ compiler
    if not run_command("g++ --version", "Checking C++ compiler"):
        print("❌ C++ compiler not found. Please install g++ or clang++")
        return False
    
    # Check for Python development headers
    try:
        import pybind11
        print("✅ pybind11 found")
    except ImportError:
        print("❌ pybind11 not found. Install with: pip install pybind11")
        return False
    
    return True

def build_with_setup():
    """Build using setup.py."""
    print("\n🏗️  Building with setup.py...")
    
    # Set environment variable to enable C++ build
    env = os.environ.copy()
    env['PYFUNC_BUILD_CPP'] = '1'
    
    # Use UTF-8 encoding to avoid Unicode issues on Windows
    if os.name == 'nt':
        env['PYTHONIOENCODING'] = 'utf-8'
    
    # Build in development mode
    cmd = f"{sys.executable} setup.py build_ext --inplace"
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, env=env, capture_output=True, text=True)
        print("✅ C++ extension built successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Build failed:")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def build_with_cmake():
    """Build using CMake (alternative method)."""
    print("\n🏗️  Building with CMake...")
    
    # Create build directory
    build_dir = "build"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
    
    # Configure
    if not run_command(f"cd {build_dir} && cmake ..", "Configuring with CMake"):
        return False
    
    # Build
    if not run_command(f"cd {build_dir} && make -j4", "Building with CMake"):
        return False
    
    # Copy the built module to the source directory
    built_module = None
    for file in os.listdir(build_dir):
        if file.startswith("pyfunc_native") and (file.endswith(".so") or file.endswith(".pyd")):
            built_module = file
            break
    
    if built_module:
        shutil.copy(os.path.join(build_dir, built_module), ".")
        print(f"✅ Copied {built_module} to source directory")
        return True
    else:
        print("❌ Built module not found")
        return False

def test_build():
    """Test if the built module works."""
    print("\n🧪 Testing built module...")
    
    try:
        import pyfunc_native
        print("✅ Module imports successfully")
        
        # Test a simple operation
        test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = pyfunc_native.sum_operation(test_data)
        expected = 15.0
        
        if abs(result - expected) < 1e-10:
            print(f"✅ Basic operation test passed (sum = {result})")
            return True
        else:
            print(f"❌ Basic operation test failed (expected {expected}, got {result})")
            return False
            
    except ImportError as e:
        print(f"❌ Module import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    print("🚀 PyFunc C++ Backend Build Script")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Try building with setup.py first
    if build_with_setup():
        if test_build():
            print("\n🎉 Build completed successfully!")
            print("\nTo test the C++ backend:")
            print("  python examples/cpp_backend_example.py")
            print("  python -m pytest tests/test_cpp_backend.py")
        else:
            print("\n❌ Build completed but tests failed")
            sys.exit(1)
    else:
        print("\n⚠️  setup.py build failed, trying CMake...")
        if build_with_cmake():
            if test_build():
                print("\n🎉 CMake build completed successfully!")
            else:
                print("\n❌ CMake build completed but tests failed")
                sys.exit(1)
        else:
            print("\n❌ Both build methods failed")
            print("\nTroubleshooting:")
            print("1. Make sure you have a C++ compiler installed")
            print("2. Install pybind11: pip install pybind11")
            print("3. Check that Python development headers are installed")
            sys.exit(1)

if __name__ == "__main__":
    main()